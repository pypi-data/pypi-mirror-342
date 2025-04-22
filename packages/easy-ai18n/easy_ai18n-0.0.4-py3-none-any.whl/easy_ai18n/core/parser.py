"""
AST 解析器
"""

import ast
import inspect
import linecache
from dataclasses import dataclass
from types import FrameType

from ..config import ic


@dataclass
class StringData:
    string: str
    variables: dict


class ASTWalker:
    """
    遍历 AST 并提取指定函数调用的节点。
    """

    @staticmethod
    def get_target_nodes(node: ast.AST) -> list[ast.Call]:
        target_nodes = []
        for item in ast.walk(node):
            if isinstance(item, ast.Call):
                # 后置语言选择器 _()[]
                if (
                    isinstance(item.func, ast.Name)
                    and item.func.id in ic.i18n_function_name
                ):
                    target_nodes.append(item)
                # 前置语言选择器 _[]()
                if (
                    isinstance(item.func, ast.Subscript)
                    and isinstance(item.func.value, ast.Name)
                    and item.func.value.id in ic.i18n_function_name
                ):
                    sub = item.func
                    target_nodes.append(
                        ast.Call(func=sub.slice, args=item.args, keywords=item.keywords)
                    )

        return target_nodes


class StringConstructor:
    """
    根据传入的 AST 节点构造字符串，同时处理 f-string 表达式。
    """

    def __init__(self, default_sep: str = None):
        self.default_sep = default_sep or ic.def_sep

    def construct_from_node(
        self, call_node: ast.Call, evaluator: "VariableEvaluator" = None
    ) -> tuple[str, dict]:
        sep = next(
            (
                kw.value.value
                for kw in call_node.keywords
                if kw.arg == "sep" and isinstance(kw.value, ast.Constant)
            ),
            self.default_sep,
        )

        raw_parts: list[str] = []
        variables: dict = {}

        for arg in call_node.args:
            if isinstance(arg, ast.Constant):
                # 常量字符串直接添加
                raw_parts.append(arg.value)
            else:
                if isinstance(arg, ast.JoinedStr):
                    part, found = self._handle_f_string(arg, evaluator)
                else:
                    # 将其他表达式包装为 f-string
                    expr_src = ast.unparse(arg)  # type: ignore
                    wrapper = f'{ic.i18n_function_name[0]}(f"{{{expr_src}}}")'
                    wrapper_call: ast.Call = ast.parse(wrapper).body[0].value  # type: ignore
                    part, found = self._handle_f_string(wrapper_call.args[0], evaluator)  # type: ignore

                raw_parts.append(part)
                variables.update(found)
        if r := sep.join(raw_parts):
            return r, variables
        return "", {}

    @staticmethod
    def _handle_f_string(
        node: ast.JoinedStr, evaluator: "VariableEvaluator" = None
    ) -> tuple[str, dict]:
        parts = []
        variables = {}
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                expr = ast.unparse(value.value)
                parts.append(f"{{{expr}}}")
                if evaluator:
                    variables[expr] = evaluator.evaluate(expr)
        return "".join(parts), variables


class VariableEvaluator:
    """
    负责对表达式求值，通过依赖注入的 globals 和 locals 解耦具体的上下文。
    """

    def __init__(self, globals_dict: dict, locals_dict: dict):
        self.globals = globals_dict
        self.locals = locals_dict

    def evaluate(self, expr: str) -> any:
        try:
            if expr.isidentifier():
                return self.locals.get(expr, self.globals.get(expr, None))
            else:
                compiled_expr = compile(expr, "<string>", "eval")
                return eval(compiled_expr, self.globals, self.locals)
        except Exception as e:
            return f"<i18n_error: {str(e)}>"


class ASTParser:
    """
    通过组合 ASTWalker、StringConstructor 和 VariableEvaluator，对指定的 AST 节点进行解析。
    """

    @staticmethod
    def get_code_block(frame: FrameType):
        positions = inspect.getframeinfo(frame).positions
        filename = frame.f_code.co_filename
        lines = linecache.getlines(filename)

        start_line = positions.lineno - 1
        end_line = positions.end_lineno - 1
        # 如果是单行
        if start_line == end_line:
            return (
                lines[start_line]
                .encode()[positions.col_offset : positions.end_col_offset]
                .decode()
            )

        # 如果是多行

        # 处理第一行
        result = [lines[start_line].encode()[positions.col_offset :].decode()]

        # 处理中间行
        for i in range(start_line + 1, end_line):
            result.append(lines[i])

        # 处理最后一行
        result.append(lines[end_line].encode()[: positions.end_col_offset].decode())
        return "".join(result)

    def extract_all_strings(self, *, node: ast.AST) -> list[str]:
        """
        仅提取解析后的字符串，默认只解析第一个匹配的调用节点。
        """
        target_nodes = ASTWalker.get_target_nodes(node)

        if not target_nodes:
            return []
        strings, _ = self._extract(
            target_nodes=target_nodes,
            sep=ic.def_sep,
        )
        return strings

    def extract_string_data(
        self,
        *,
        sep: str = None,
        frame: FrameType = None,
    ) -> StringData | None:
        """
        解析第一个匹配的调用节点，并返回构造后的字符串及变量数据。
        """
        call_text = self.get_code_block(frame)
        node = ast.parse(call_text.strip())

        # 处理缩进
        target_nodes = ASTWalker.get_target_nodes(node)
        if not target_nodes:
            return None

        strings, variables_collected = self._extract(
            target_nodes=target_nodes[:1],
            sep=sep,
            get_variables_value=True,
            frame=frame,
        )
        return StringData(strings[0], variables_collected)

    @staticmethod
    def _extract(
        *,
        target_nodes: list[ast.Call],
        sep: str | None = None,
        get_variables_value: bool = False,
        frame: FrameType = None,
    ) -> tuple[list[str], dict]:
        variables_collected: dict = {}

        evaluator: VariableEvaluator | None = None
        if get_variables_value and frame:
            evaluator = VariableEvaluator(frame.f_globals, frame.f_locals)

        string_constructor = StringConstructor(sep or ic.i18n_function_name)
        strings_set = set()

        for call_node in target_nodes:
            constructed, vars_found = string_constructor.construct_from_node(
                call_node, evaluator
            )
            strings_set.add(constructed)
            variables_collected.update(vars_found)
        return list(strings_set), variables_collected
