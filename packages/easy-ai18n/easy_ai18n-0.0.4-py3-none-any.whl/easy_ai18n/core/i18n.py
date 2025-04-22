"""
翻译函数调用时
"""

import inspect
import sys
from types import FrameType
from typing import Type, Union

from .loader import Loader
from .parser import ASTParser, StringData
from ..config import ic
from ..log import logger
from ..utiles import gen_id


class PreLanguageSelector:
    """前置语言选择器"""

    def __init__(self, i18n: "I18n", lang: str = None):
        self.i18n = i18n
        self.lang = lang

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return ""

    def __call__(self, *args, sep: str = ic.def_sep) -> str:
        """
        调用后置语言选择器
        _[前置语言选择器]('内容')
        :param args: 要翻译的文本
        :param sep: 分隔符
        :return:
        """
        frame = inspect.currentframe().f_back
        return self.i18n.t(*args, sep=sep, frame=frame)[self.lang]


class I18nContent(str):
    """内容"""

    def __new__(
        cls,
        text: str,
        variables: dict = None,
        lang: str = None,
        post_lang_selector: Type["PostLanguageSelector"] | None = None,
    ):
        return str.__new__(cls, text)

    def __init__(
        self,
        text: str,
        variables: dict = None,
        lang: str = None,
        post_lang_selector: Type["PostLanguageSelector"] | None = None,
    ):
        self.text = text
        self.variables = variables or {}
        self.lang = lang
        self.post_lang_selector = post_lang_selector or PostLanguageSelector

    def __str__(self) -> str:
        return self.__getitem__(self.lang)

    def __repr__(self) -> str:
        return self.__getitem__(self.lang)

    def __getitem__(self, lang: Union[int, slice, any]) -> str:
        """_('内容')[后置语言选择器]"""
        if isinstance(lang, (int, slice)):
            return super().__getitem__(lang)
        return self.__call__(lang)

    def __call__(self, lang: Union[int, slice, any]):
        """_('内容')(后置语言选择器)"""
        return str(self.post_lang_selector(self.text, self.variables, lang))

    def __int__(self):
        return int(self.__str__())


class PostLanguageSelector:
    """后置语言选择器"""

    def __init__(self, text: str, variables: dict = None, lang: str = None):
        """
        语言选择器，用于选择翻译后的语言
        :param text: 要翻译的文本
        :param variables: 变量字典，用于替换f-string中的变量
        """
        self.text = text
        self.variables = variables or {}
        self.lang = lang

    def __str__(self) -> str:
        return self.__getitem__(self.lang)

    def __repr__(self) -> str:
        return self.__getitem__(self.lang)

    def __getitem__(self, key: str | None) -> str:
        """_('内容')[后置语言选择器]"""
        return self.format(key)

    def format(self, lang: str | None = None) -> str:
        """格式化字符串并应用翻译"""
        try:
            if not lang:
                return self._format(self.text)
            translated = Loader().get_by_text(self.text, lang)
            return self._format(translated)
        except Exception as e:
            logger.error(f"后置语言选择器错误: {e}")
            return self.text

    def _format(self, raw_string) -> str:
        for v in self.variables:
            raw_string = raw_string.replace(f"{{{v}}}", str(self.variables[v]))
        return raw_string


class I18n:
    def __init__(
        self,
        default_lang: str = None,
        pre_lang_selector: Type[PreLanguageSelector] | None = None,
        post_lang_selector: Type[PostLanguageSelector] | None = None,
    ):
        """
        初始化I18n
        :param default_lang: 全局默认使用的语言
        :param pre_lang_selector: 前置语言选择器类
        :param post_lang_selector: 后置语言选择器类
        """
        self.default_lang = default_lang
        self._cache: dict[str, StringData] = {}
        self._parse_failures: set[str] = set()
        self.pre_lang_selector = pre_lang_selector or PreLanguageSelector
        self.post_lang_selector = post_lang_selector or PostLanguageSelector
        self.content = I18nContent

    def t(self, *args, sep: str = ic.def_sep, frame: FrameType = None) -> I18nContent:  # type: ignore
        """
        入口函数

        Args:
            sep: 字符串分隔符，默认为空格
            frame: 调用者的栈帧，默认使用当前栈帧

        Returns:
            PostLanguageSelector 对象
        """
        text = sep.join([str(item) for item in args])
        f = frame or sys._getframe(1)  # 比 inspect.currentframe().f_back 速度快一点
        if not f:
            return self.content(text, post_lang_selector=self.post_lang_selector)
        positions = (
            f.f_lineno,
            f.f_lasti,
        )
        cache_key = gen_id(positions)

        # 解析错误的内容直接返回原文
        if cache_key in self._parse_failures:
            return self.content(text, post_lang_selector=self.post_lang_selector)

        # 命中缓存
        if r := self._cache.get(cache_key):
            return self.content(
                r.string,
                r.variables,
                lang=self.default_lang,
                post_lang_selector=self.post_lang_selector,
            )

        try:
            result = ASTParser().extract_string_data(frame=f, sep=sep)
            return self._handle_cache(text, cache_key, result)
        except Exception as e:
            logger.error(f"I18N未知错误: {str(e)}")
            return self.content(
                text, lang=self.default_lang, post_lang_selector=self.post_lang_selector
            )
        finally:
            # noinspection PyInconsistentReturns
            del f

    def _handle_cache(
        self, text: str, cache_key: str, result: StringData
    ) -> I18nContent:
        """处理缓存并返回结果"""
        if not result:
            self._parse_failures.add(cache_key)
            logger.warning(f"I18N解析错误: {text}")
            return self.content(text, post_lang_selector=self.post_lang_selector)

        self._cache[cache_key] = result
        return self.content(
            result.string,
            result.variables,
            lang=self.default_lang,
            post_lang_selector=self.post_lang_selector,
        )

    def clear_cache(self):
        """清除解析缓存"""
        self._cache.clear()
        self._parse_failures.clear()

    def __getitem__(self, lang: str) -> PreLanguageSelector:
        """调用前置语言选择器"""
        return self.pre_lang_selector(self, lang)

    def __call__(self, *args, sep: str = ic.def_sep) -> I18nContent:
        """调用入口函数"""
        frame = inspect.currentframe().f_back
        return self.t(*args, sep=sep, frame=frame)
