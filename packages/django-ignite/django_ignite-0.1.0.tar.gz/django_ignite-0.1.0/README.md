# Django Ignite

[![PyPI version](https://badge.fury.io/py/django-ignite.svg)](https://badge.fury.io/py/django-ignite)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`django-ignite`  is a developer-first CLI tool to scaffold Django projects in seconds — with a consistent layout, automated virtual environment setup, Django version selection, and enhanced settings structure.

## Why Django Ignite?

Creating a Django project is easy. Creating it `the right way every time` — with proper structure, dependencies, and settings — takes time.

**Django Ignite saves you that time**, with:

- Custom `core/` app structure
- Configurable Django versions
- Automatic `venv` or `uv` env setup
- Pre-configured `INSTALLED_APPS` sections
- Clean CLI experience powered by `rich` and `InquirerPy`

## Purpose

The goal of `django-ignite` is to:

- 🔁 Speed up project bootstrapping
- ✅ Ensure structure and dependency consistency
- 🧱 Lay a clean, scalable foundation for new apps
- 🧩 Include third-party app integration scaffolds from day one
- 🌱 Make Django projects easier to start, extend, and maintain

Whether you're a solo developer or part of a team, `django-ignite` gives you a consistent and clean starting point.

## Features

- ✅ Interactive CLI with `InquirerPy`
- ⚙️ Choose between `uv` or standard `venv`
- 📦 Selectable Django version (`4.2`, `5.2`, more coming)
- 📘 Auto-injects `THIRD_PARTY_APPS` and `MY_APPS` into `settings.py`
- 📄 Optional root or subfolder project directory
- 📁 Clean, readable codebase with `rich` terminal feedback

## Installation

### From PyPI

```bash
pip install django-ignite
```

Once installed, just run:

```bash
django-ignite
```

## Usage Example

```bash
django-ignite
```

You'll be prompted to choose:

- **Project name**
- **Django version** (`4.2` or `5.2`)
- **Environment type** (`uv` or `venv`)
- **Where to create the project** (in root or subfolder)

### Output structure

If you select:
- project name: `my_project`
- create in root: `No`

You'll get:

```
my_project/
├── core/
│   ├── __init__.py
│   ├── settings.py
│   └── ...
├── manage.py
├── .venv/
└── .gitignore
```


### `settings.py` Patch Example

This block is automatically added after the default `INSTALLED_APPS`:

```python
# Third-party applications
THIRD_PARTY_APPS = [

]

# Custom applications
MY_APPS = [

]

# Update installed applications
INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += MY_APPS
```

## Coming Soon

- `accounts/` app scaffolding
- Django REST API starter
- `.env` + `django-environ` integration
- Settings split: `base.py`, `dev.py`, `prod.py`
- GitHub template repo

## Contributing

Contributions are welcome! Feel free to submit a Pull Request to enhance the project or fix any issues
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Contact

## Contact

Build and Develop by [Nazmul Hassan](https://www.linkedin.com/in/nhassan96/). For questions, suggestions, or collaboration, feel free to connect!
