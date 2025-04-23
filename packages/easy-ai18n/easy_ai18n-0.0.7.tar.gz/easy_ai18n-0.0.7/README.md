<div align="center">

<img src="https://github.com/user-attachments/assets/3d189579-f3ec-43cf-8ce1-4a4d8ecd8ac7" width="100" >

**Simple and Elegant Python3 Internationalization (i18n) Tool**

[![PyPI version](https://badge.fury.io/py/easy-ai18n.svg)](https://badge.fury.io/py/easy-ai18n)

English | [中文](docs/README.zh.md) | [日本語](docs/README.ja.md)

</div>

# 🌍 Easy AI18n

Easy AI18n is a modern internationalization tool library for Python3. It supports AI translation, multi-user scenarios, and full string formatting syntax,
making globalization of your project more elegant and natural.

## ✨ Key Features:

- **🚀 Easy to Use:** Implement i18n with just a few lines of code
- **✨ Elegant Syntax:** Use `_()` to wrap translatable texts, seamlessly integrating into your code
- **🤖 AI Translation:** Supports translation using large language models (LLMs) for high-quality results
- **📝 Full Formatting Support:** Fully supports all Python string formatting syntaxes
- **🌐 Multi-language Support:** Choose languages using `[]` selector for multilingual support

## 🔍 Comparison with Other i18n Tools

|                                                                            Other i18n Tools                                                                             |                                                                                         EasyAI18n                                                                                         |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| ![](https://github.com/user-attachments/assets/688309d1-c87f-44a0-831c-e8d0aa7b7c78)<br/>**Requires manual maintenance of keys and i18n files, high development cost**  |        ![](https://github.com/user-attachments/assets/c5ec3d37-1c44-47d8-b634-d9734f356ba8)<br/>**Automatically extracts translation content, no manual file maintenance needed**         |
|                  ![](https://github.com/user-attachments/assets/9a614f4f-2473-48c0-b3e2-a240592fd579)<br/>**Supports only partial formatting syntax**                   |                             ![](https://github.com/user-attachments/assets/3ba28ada-d028-4595-bf2f-2e2437157b0e)<br/>**Fully supports all formatting syntax**                             |
| ![](https://github.com/user-attachments/assets/fcd7a7cf-ae2c-4122-8f0e-2af1f59df651)<br/>**No real-time multi-language switching, unsuitable for multi-user scenarios** | ![](https://github.com/user-attachments/assets/76fe276d-1ff6-4771-9de9-5f3bc96e9779)<br/>**Supports default language and multi-language switching, adaptable to multi-user environments** |

---

## ⚡ Quick Start

### 📦 Installation

```shell
pip install easy-ai18n
```

### 🧪 Simple Example

```python
from easy_ai18n import EasyAI18n

i18n = EasyAI18n(target_lang=["ru", "ja", 'zh-CN'])
i18n.build()

_ = i18n.t()

print(_("Hello, world!")['zh-CN'])
```

## 🗂️ Project Structure

```
easy_ai18n
├── core                 # Core functionality module
│   ├── builder.py       # Builder: extract, translate, generate YAML files
│   ├── i18n.py          # Main translation logic
│   ├── loader.py        # Loader: load translation files
│   └── parser.py        # AST parser
├── prompts              # Translation prompts
├── translator           # Translator module
└── main.py              # Project entry point
```

## 📘 Usage Tutorial

### ⚙️ Initialize `EasyAI18n` Instance

```python
from easy_ai18n import EasyAI18n, PreLanguageSelector, PostLanguageSelector
from easy_ai18n.translator import GoogleTranslator

# Initialize EasyAI18n instance
i18n = EasyAI18n(
    global_lang="zh",  # Global default language
    target_lang=["zh", "ja"],  # Target translation languages
    languages=["zh", "ja"],  # Enabled languages (default is target_lang)
    project_dir="/path/to/your/project",  # Root directory (default is current dir)
    include=[],  # Included files/directories
    exclude=[".idea"],  # Excluded files/directories
    i18n_file_dir="i18n",  # Directory to store translation files
    func_name=["_"],  # Translation function names (supports multiple)
    sep=" ",  # Separator (default is space)
    translator=GoogleTranslator(),  # Translator (default is Google)
    pre_lang_selector=PreLanguageSelector,  # Pre language selector
    post_lang_selector=PostLanguageSelector  # Post language selector
)

# Build translation files
i18n.build()

# Set translation function, here we use _, can be customized
_ = i18n.t()

# Put strings to be translated inside the function
print(_("Hello, world!"))
```

### 🛠️ Custom Translation Function Names

```python
from easy_ai18n import EasyAI18n

i18n = EasyAI18n(
    func_name=["_t", '_']  # Custom translation function names
)

_t = i18n.t()
_ = _t

print(_t("Hello, world!"))
print(_("Hello, world!"))
```

### 🤖 Use AI for Translation

```python
from easy_ai18n import EasyAI18n
from easy_ai18n.translator import OpenAIYAMLTranslator

translator = OpenAIYAMLTranslator(api_key=..., base_url=..., model='gpt-4o-mini')

i18n = EasyAI18n(target_lang=["ru", "ja", 'zh-CN'], translator=translator)
i18n.build()

_ = i18n.t()

print(_("Hello, world!")['zh-CN'])
```

### 👥 Multi-user Language Scenarios (e.g. Telegram Bot)

Use custom language selector to dynamically select languages in multi-user environments:

```python
from pyrogram import Client
from pyrogram.types import Message

from easy_ai18n import EasyAI18n, PostLanguageSelector


class MyPostLanguageSelector(PostLanguageSelector):
    def __getitem__(self, msg: Message):
        # Get user's language
        lang = msg.from_user.language_code
        return super().__getitem__(lang)


i18n = EasyAI18n(
    target_lang=['zh', 'ru'],
    post_lang_selector=MyPostLanguageSelector,
)
_ = i18n.t()

bot = Client("my_bot")


@bot.on_message()
async def start(__, msg: Message):
    await msg.reply(_[msg]("Hello, world!"))


if __name__ == "__main__":
    bot.loop.run_until_complete(i18n.build_async())
    bot.run()
```

