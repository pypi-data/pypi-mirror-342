from src.easy_ai18n import EasyAI18n
import os

os.putenv("I18N_LOG_LEVEL", "DEBUG")
i18n = EasyAI18n(target_lang=["en", "ja"])
_ = i18n.t()


def test_build():
    i18n.build()
    assert i18n.i18n_file_dir.joinpath("en.yaml").exists()


def test_i18n():
    # 普通测试
    assert _("你好, 世界") == "你好, 世界"
    assert _("你好", ", ", "世界")["ja"] == "こんにちは世界"
    assert int(_(1 + 1)) == 2

    # 使用方式
    # 前置语言选择器只能使用中括号, 后置语言选择器可以使用括号或中括号
    assert _["en"]("你好, 世界") == "Hello World"
    assert _("你好, 世界")["en"] == "Hello World"
    assert _("你好, 世界")("en") == "Hello World"

    # f-string 测试
    a, b = "你好", "世界"
    assert _["en"]("你好, 世界", f"{a}, {b}") == f"Hello, world {a}, {b}"

    # 连接符测试
    assert _["en"]("你好", b, sep="-") == f"Hello-{b}"

    # 字典&列表测试
    one = 1
    dict_test = {"a": _("hello"), "b": _("world"), "c": _(f"数字: {one}")}
    assert dict_test["a"] == "hello"
    assert dict_test["b"]["ja"] == "世界"
    assert dict_test["c"]["en"] == f"Number: {one}"

    list_test = [_("列表测试"), _(1 + 1)]
    assert list_test[0]["en"] == "List Test"
    assert int(list_test[1]) == 2

    dc_dict = {
        1: _("美国佛罗里达州迈阿密 🇺🇸\n🌏`149.154.175.53`"),
        2: _("荷兰阿姆斯特丹 🇳🇱\n🌏`149.154.167.51`"),
        3: _("美国佛罗里达州迈阿密 🇺🇸\n🌏`149.154.175.100`"),
        4: _("荷兰阿姆斯特丹 🇳🇱\n🌏`149.154.167.91`"),
        5: _("新加坡 🇸🇬\n🌏`91.108.56.130`"),
    }
    assert (
        dc_dict[3]["ja"]
        == """米国フロリダ州マイアミ🇺🇸
🌏`149.154.175.100`"""
    )

    # 多行测试
    vscode = "vscode"
    idea = "idea"
    vscode_en = f"""{vscode} is a young and ignorant girl. You have to teach her to learn, train her, and make her the most suitable for you.
{idea} is an intellectual and sensible sister who can help you do all the work"""
    vscode_ja = """VScodeは若くて無知な女の子です。あなたは彼女に学び、訓練し、彼女をあなたに最も適したものにするように教える必要があります。
アイデアは、あなたがすべての仕事をするのを助けることができる知的で賢明な姉妹です"""

    assert (
        _["en"](
            f"{vscode}是青春懵懂的少女，你要去教她学习，调教她，让她最适合你\n"
            f"{idea}是知性懂事的姐姐，她能帮你做完所有工作"
        )
        == vscode_en
    )

    assert (
        _(
            """vscode是青春懵懂的少女，你要去教她学习，调教她，让她最适合你
idea是知性懂事的姐姐，她能帮你做完所有工作"""
        )["ja"]
        == vscode_ja
    )

    assert (
        _(
            "vscode是青春懵懂的少女，你要去教她学习，调教她，让她最适合你",
            "idea是知性懂事的姐姐，她能帮你做完所有工作",
            sep=", ",
        )
        == "vscode是青春懵懂的少女，你要去教她学习，调教她，让她最适合你, idea是知性懂事的姐姐，她能帮你做完所有工作"
    )

