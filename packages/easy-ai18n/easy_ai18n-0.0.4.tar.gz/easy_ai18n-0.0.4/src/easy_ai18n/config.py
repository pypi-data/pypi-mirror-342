import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class I18nConfig:
    i18n_function_name: list[str] = os.getenv("I18N_FUNCTION_NAME", "_").split(",")
    """翻译函数名"""

    i18n_dir = (
        (os.getcwd() / Path("i18n"))
        if (d := os.getenv("I18N_DIR")) is None
        else Path(d)
    )
    """翻译文件保存目录"""

    def_sep = " "
    """默认分隔符"""


ic = I18nConfig()
