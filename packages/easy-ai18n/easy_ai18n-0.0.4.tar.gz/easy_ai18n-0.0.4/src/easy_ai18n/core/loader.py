from pathlib import Path

import yaml

from ..config import ic
from ..utiles import singleton, gen_id


@singleton
class Loader:
    def __init__(self):
        self.i18n_dict = self.load_i18n_file()

    def load_i18n_file(self) -> dict:
        """
        加载i18n目录下的yaml文件
        :return: i18n字典
        """
        i18n_dict = {}
        i18n_files = ic.i18n_dir.glob("**/*.yaml")
        if not i18n_files:
            return {}
        for file in i18n_files:
            yaml.safe_load(Path(file).read_text(encoding="utf-8"))
            i18n_dict[file.name.split(".")[0]] = yaml.safe_load(
                file.read_text(encoding="utf-8")
            )
        self.i18n_dict = i18n_dict
        return i18n_dict

    def get_by_text(self, text: str, lang: str = None):
        key = gen_id(text)
        return self.i18n_dict.get(lang, {}).get(key, text)

loader = Loader()