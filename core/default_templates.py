"""
File:    /core/default_templates.py
Rol:     Standaard project templates
Applicatie: Project Generator
Versie:  1.0.9
Auteur:  Barremans
Changes: 1.0.10 - Bugfix signing
Changes: 1.0.9 - NIEUW: core/-map (Python package) toegevoegd aan
                  create_standard_project_template(), naar analogie van
                  helpers/utils/ui/dialogs/token (python_package=True →
                  generator.py's _generate_folder() maakt automatisch de
                  __init__.py aan met header). Bedoeld voor kernlogica/
                  gedeelde functionaliteit, los van app/ — zie
                  context_ProjectGenerator.md §7 en de CGK-conventie
                  app/core/ uit 01-app-structuur-template.md. Geen wijziging
                  nodig aan generator.py of templates.py: python_package
                  wordt al generiek afgehandeld.
Changes: 1.0.8 - BUGFIX: 7 template-functies (setup.py, scripts/update_toml.py,
                  scripts/bump_version.py, scripts/generate_requirements.py,
                  scripts/validate_project.py, i18n/translator.py,
                  i18n/__init__.py) bakten zelf al een verouderd
                  "Beschrijving:/Versie:"-docstring-blok in hun
                  template_body — gecombineerd met de header die
                  HeaderRenderer er al voor plakt, kreeg elk van deze
                  bestanden een DUBBELE header. Alle 7 verouderde blokken
                  verwijderd. Bijkomend: get_i18n_init_template() bestond al
                  langer maar werd nergens aangeroepen (dode code) — i18n/
                  kreeg hierdoor enkel een lege package-__init__.py in
                  plaats van de bedoelde "from i18n.translator import
                  Translator, get_translator, t"-herexport. Nu wél
                  toegevoegd aan create_standard_project_template().
                  Verder: drie nieuwe root-bestanden toegevoegd naar het
                  bewezen ArticleSearch build/release-patroon —
                  build_installer.bat (PyInstaller + Intune-veilige Inno
                  Setup-installer, met per-app uniek gegenereerde AppGuid),
                  build_and_publish.ps1 (orchestrator) en publish.ps1
                  (GitHub-release via 'gh' + version.txt), telkens werkend
                  op app/version.py en met dynamische root-resolutie.
Changes: 1.0.7 - create_standard_project_template() breidt uit met drie
                  extra lege Python-packages: ui/ (GUI-schermen, naar
                  ArticleSearch-conventie ui_*.py), dialogs/ (modale
                  QDialog-vensters, *_dialog.py) en token/ (per-domein
                  token/auth-modules, *_token.py).
Changes: 1.0.6 - BUGFIX: get_launch_json_template() en
                  get_settings_json_template() verwezen naar
                  "venv/Scripts/python.exe" i.p.v. ".venv/Scripts/python.exe".
Changes: 1.0.5 - (voorheen ongedocumenteerd) i18n-map met locales
                  (nl_NL/en_US/fr_FR/de_DE/es_ES) toegevoegd aan
                  create_standard_project_template().
"""

from pathlib import Path
from core.templates import ProjectTemplate, FolderTemplate, FileTemplate


def get_version_py_template(version: str) -> str:
    """Template voor version.py."""
    return f'__version__ = "{version}"  # Pas dit manueel aan bij elke release\n'


def get_main_py_template() -> str:
    """Template voor main.py."""
    return '''def main():
    """Hoofdapplicatie entry point."""
    print("Hello World!")


if __name__ == "__main__":
    main()
'''


def get_launch_json_template(app_name: str) -> str:
    """Template voor .vscode/launch.json."""
    python_path = "${workspaceFolder}/.venv/Scripts/python.exe"
    
    return f'''{{
    "version": "0.2.0",
    "configurations": [
        {{
            "name": "Run {app_name}",
            "type": "debugpy",
            "request": "launch",
            "program": "${{workspaceFolder}}/app/main.py",
            "console": "integratedTerminal",
            "python": "{python_path}"
        }}
    ]
}}
'''


def get_settings_json_template() -> str:
    """Template voor .vscode/settings.json."""
    python_path = "${workspaceFolder}/.venv/Scripts/python.exe"
    
    return f'''{{
    "python.defaultInterpreterPath": "{python_path}",
    "python.pythonPath": "{python_path}",
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true
}}
'''


def get_settings_config_template() -> str:
    """Template voor config/settings.json."""
    return '''{
    "app": {
        "name": "Application",
        "debug_mode": false,
        "default_locale": "en_US"
    }
}
'''


def get_gitignore_template() -> str:
    """Template voor .gitignore."""
    return '''# Virtual Environment
venv/
.venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*.code-workspace

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# MyPy
.mypy_cache/
.dmypy.json

# OS
.DS_Store
Thumbs.db
desktop.ini

# Data
data/*
!data/.gitkeep

# Logs
*.log
logs/

# Local development
*.local
.env
.env.local

# TOML backups
*.toml.bak
'''


def get_main_qss_template() -> str:
    """Template voor main.qss - Hoofd styling."""
    return '''/* ================================================
   main.qss - Hoofd styling voor applicatie
   ================================================ */

/* ----------------------------------------------
   1. Algemene Window Settings
   ---------------------------------------------- */
QMainWindow, QDialog, QWidget {
    background-color: #ffffff;
    font-family: "Segoe UI", Verdana, Arial, sans-serif;
    font-size: 11px;
    color: #333333;
}

/* ----------------------------------------------
   2. Buttons
   ---------------------------------------------- */
QPushButton {
    padding: 6px 12px;
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    color: #333333;
    font-size: 11px;
}

QPushButton:hover {
    background-color: #e6e6e6;
}

QPushButton:pressed {
    background-color: #d4d4d4;
}

QPushButton:disabled {
    background-color: #eeeeee;
    color: #aaaaaa;
    border: 1px solid #dddddd;
}

/* Primary button */
QPushButton[primary="true"] {
    background-color: #2196F3;
    color: white;
    border: 1px solid #1976D2;
}

QPushButton[primary="true"]:hover {
    background-color: #1976D2;
}

/* ----------------------------------------------
   3. Input Fields
   ---------------------------------------------- */
QLineEdit, QTextEdit, QPlainTextEdit {
    padding: 6px;
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    color: #333333;
    font-size: 11px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #2196F3;
}

/* ----------------------------------------------
   4. Labels
   ---------------------------------------------- */
QLabel {
    font-size: 11px;
    color: #333333;
}

QLabel[heading="true"] {
    font-size: 14px;
    font-weight: bold;
    color: #333333;
}

/* ----------------------------------------------
   5. Tables
   ---------------------------------------------- */
QTableWidget {
    border: 1px solid #cccccc;
    gridline-color: #dddddd;
    selection-background-color: #e6f2ff;
    selection-color: #333333;
    font-size: 11px;
    background-color: #f9f9f9;
}

QTableWidget::item {
    padding: 4px;
}

QHeaderView::section {
    background-color: #f0f0f0;
    border: 1px solid #cccccc;
    padding: 4px;
    font-weight: bold;
    color: #333333;
}

/* ----------------------------------------------
   6. Scrollbars
   ---------------------------------------------- */
QScrollBar:vertical {
    background: #f0f0f0;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #cccccc;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar:horizontal {
    background: #f0f0f0;
    height: 12px;
}

QScrollBar::handle:horizontal {
    background: #cccccc;
    min-width: 20px;
    border-radius: 4px;
}

/* ----------------------------------------------
   7. Menu Bar
   ---------------------------------------------- */
QMenuBar {
    background-color: #f0f0f0;
    border-bottom: 1px solid #cccccc;
}

QMenuBar::item {
    padding: 4px 8px;
    background: transparent;
}

QMenuBar::item:selected {
    background: #e6e6e6;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #cccccc;
}

QMenu::item {
    padding: 4px 20px;
}

QMenu::item:selected {
    background-color: #e6f2ff;
}
'''


def get_detail_qss_template() -> str:
    """Template voor detail.qss - Detail window styling."""
    return '''/* ================================================
   detail.qss – Styling voor DetailWindow
   ================================================ */

/* ----------------------------------------------
   1. Basisinstellingen voor DetailWindow (QDialog)
   ---------------------------------------------- */
DetailWindow, DetailWindow QWidget {
    background-color: #ffffff;
    font-family: "Segoe UI", Verdana, Arial, sans-serif;
    font-size: 11px;
    color: #333333;
}

/* ----------------------------------------------
   2. Titellabel bovenaan
   ---------------------------------------------- */
DetailWindow > QLabel {
    font-size: 12px;
    font-weight: bold;
    color: #333333;
    margin: 8px 0px;
}

/* ----------------------------------------------
   3. QTabWidget-containers
   ---------------------------------------------- */
QTabWidget {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
}

/* ----------------------------------------------
   4. Tabs (QTabBar::tab)
   ---------------------------------------------- */
QTabBar::tab {
    background: #f0f0f0;
    border: 1px solid #cccccc;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 12px;
    margin-right: -1px;
    font-size: 11px;
    color: #333333;
}

QTabBar::tab:selected {
    background: #ffffff;
    border: 1px solid #cccccc;
    border-bottom: 1px solid #ffffff;
    color: #333333;
    font-weight: bold;
}

QTabBar::tab:hover {
    background: #e8e8e8;
}

/* ----------------------------------------------
   5. Tabellen binnen DetailWindow
   ---------------------------------------------- */
DetailWindow QTableWidget {
    border: 1px solid #cccccc;
    gridline-color: #dddddd;
    selection-background-color: #e6f2ff;
    selection-color: #333333;
    font-size: 11px;
    background-color: #f9f9f9;
}

DetailWindow QHeaderView::section {
    background-color: #f0f0f0;
    border: 1px solid #cccccc;
    padding: 4px;
    font-weight: bold;
    color: #333333;
}

/* ----------------------------------------------
   6. Upload-knop
   ---------------------------------------------- */
DetailWindow QPushButton {
    padding: 6px 12px;
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    color: #333333;
}

DetailWindow QPushButton:hover {
    background-color: #e6e6e6;
}

/* ----------------------------------------------
   7. ScrollArea
   ---------------------------------------------- */
DetailWindow QScrollArea {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
}

/* ----------------------------------------------
   8. Scrollbars
   ---------------------------------------------- */
DetailWindow QScrollBar:vertical {
    background: #f0f0f0;
    width: 12px;
}

DetailWindow QScrollBar::handle:vertical {
    background: #cccccc;
    min-height: 20px;
    border-radius: 4px;
}
'''


def get_pyproject_toml_template(app_name: str, version: str, author: str, description: str) -> str:
    """Template voor pyproject.toml (PEP 621)."""
    desc = description if description else "Een Python applicatie"
    package_name = app_name.lower().replace(' ', '-')
    
    return f'''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{package_name}"
version = "{version}"
description = "{desc}"
readme = "README.md"
requires-python = ">=3.11"
license = {{text = "MIT"}}
authors = [
    {{name = "{author}"}}
]
keywords = ["application", "python", "i18n"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    # Voeg hier je dependencies toe
    # Bijvoorbeeld: "PyQt6>=6.6.1"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "black>=23.0.0",
    "flake8>=6.1.0",
    "mypy>=1.7.0",
    "tomli>=2.0.1",
    "tomli-w>=1.0.0",
]

[project.urls]
Homepage = "https://github.com/{author.lower().replace(' ', '-')}/{package_name}"
Repository = "https://github.com/{author.lower().replace(' ', '-')}/{package_name}"

[tool.setuptools.packages.find]
where = ["."]
include = ["app*", "helpers*", "utils*", "i18n*"]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
'''


def get_setup_py_template(app_name: str, version: str, author: str, description: str) -> str:
    """Template voor setup.py (backwards compatibility)."""
    desc = description if description else "Een Python applicatie"
    package_name = app_name.lower().replace(' ', '-')
    
    return f'''# Note: Dit bestand is voor backwards compatibility.
# De primaire configuratie staat in pyproject.toml

from setuptools import setup, find_packages
from pathlib import Path

# Lees version uit app/version.py
version = "{version}"
try:
    with open("app/version.py", "r") as f:
        exec(f.read())
        version = __version__  # noqa: F821
except Exception:
    pass

# Lees README
long_description = ""
readme_file = Path("README.md")
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

# Lees requirements
requirements = []
req_file = Path("requirements.txt")
if req_file.exists():
    with open(req_file, "r") as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="{package_name}",
    version=version,
    author="{author}",
    description="{desc}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements,
    python_requires=">=3.11",
    entry_points={{
        "console_scripts": [
            "{package_name}=app.main:main",
        ],
    }},
    include_package_data=True,
    package_data={{
        "i18n": ["locales/*.json"],
    }},
)
'''


def get_manifest_in_template() -> str:
    """Template voor MANIFEST.in."""
    return '''# Include belangrijke bestanden in distributie
include README.md
include LICENSE
include requirements.txt
include pyproject.toml

# Include configuratie
recursive-include config *.json

# Include assets
recursive-include assets *.png *.ico *.jpg *.jpeg

# Include CSS/QSS
recursive-include css *.css *.qss

# Include documentatie
recursive-include docs *.md

# Include i18n locales
recursive-include i18n/locales *.json

# Exclude compiled en cache bestanden
global-exclude __pycache__
global-exclude *.py[cod]
global-exclude .DS_Store
global-exclude *.so
global-exclude .pytest_cache
'''


def get_license_template(author: str) -> str:
    """Template voor LICENSE (MIT)."""
    from datetime import date
    year = date.today().year
    
    return f'''MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


def get_contributing_template(app_name: str) -> str:
    """Template voor CONTRIBUTING.md."""
    return f'''# Bijdragen aan {app_name}

Bedankt voor je interesse om bij te dragen!

## Development Setup

1. Clone de repository
2. Maak een virtuele omgeving:
```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   source venv/bin/activate  # Linux/Mac
```

3. Installeer dependencies (inclusief dev):
```bash
   pip install -e ".[dev]"
```

## Code Style

We gebruiken:
- **Black** voor code formatting (max line length: 100)
- **Flake8** voor linting
- **MyPy** voor type checking

Run deze voor je commit:
```bash
black .
flake8 .
mypy .
```

## Tests

Run alle tests:
```bash
pytest
```

Met coverage:
```bash
pytest --cov=app --cov-report=html
```

## i18n (Vertalingen)

Bij het toevoegen van nieuwe UI teksten:
1. Gebruik `t("key.name")` in plaats van hardcoded strings
2. Voeg de key toe aan alle locale bestanden in `i18n/locales/`
3. Test in meerdere talen

## Commit Messages

Gebruik duidelijke commit messages:
- `feat: add new feature`
- `fix: resolve bug in ...`
- `docs: update README`
- `refactor: improve code structure`
- `test: add tests for ...`
- `i18n: add translations for ...`

## Pull Requests

1. Fork de repository
2. Maak een feature branch (`git checkout -b feature/amazing-feature`)
3. Commit je changes (`git commit -m 'feat: add amazing feature'`)
4. Push naar je fork (`git push origin feature/amazing-feature`)
5. Open een Pull Request

## Code Review Process

- Alle PRs moeten reviewed worden
- Tests moeten slagen
- Code style moet kloppen
- Alle talen moeten bijgewerkt zijn

## Vragen?

Open een issue voor vragen of discussies.
'''


def get_makefile_template(app_name: str) -> str:
    """Template voor Makefile (handig voor development)."""
    return f'''# Makefile voor {app_name}

.PHONY: install test lint format clean run build help

help:
\t@echo "Beschikbare commando's:"
\t@echo "  make install   - Installeer dependencies"
\t@echo "  make dev       - Installeer dev dependencies"
\t@echo "  make test      - Run tests"
\t@echo "  make coverage  - Run tests met coverage"
\t@echo "  make lint      - Run linters"
\t@echo "  make format    - Format code met black"
\t@echo "  make clean     - Verwijder cache bestanden"
\t@echo "  make run       - Run applicatie"
\t@echo "  make build     - Build distributie"

install:
\tpip install -e .

dev:
\tpip install -e ".[dev]"

test:
\tpytest tests/ -v

coverage:
\tpytest tests/ --cov=app --cov=i18n --cov-report=html --cov-report=term

lint:
\tflake8 app helpers utils i18n tests
\tmypy app helpers utils i18n

format:
\tblack app helpers utils i18n tests

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {{}} + 2>/dev/null || true
\tfind . -type f -name "*.pyc" -delete 2>/dev/null || true
\tfind . -type d -name "*.egg-info" -exec rm -rf {{}} + 2>/dev/null || true
\trm -rf build/ dist/ .pytest_cache/ .mypy_cache/ htmlcov/ 2>/dev/null || true

run:
\tpython app/main.py

build:
\tpython setup.py sdist bdist_wheel
'''


def get_readme_template(app_name: str, version: str, author: str, description: str) -> str:
    """Template voor README.md."""
    desc_text = description if description else "Beschrijving van de applicatie"
    package_name = app_name.lower().replace(' ', '-')
    
    return f'''# {app_name}

**Versie:** {version}  
**Auteur:** {author}

## 📋 Beschrijving

{desc_text}

## 🌍 Meertaligheid

Deze applicatie ondersteunt de volgende talen:
- 🇳🇱 Nederlands (nl_NL)
- 🇺🇸 English (en_US)
- 🇫🇷 Français (fr_FR)
- 🇩🇪 Deutsch (de_DE)
- 🇪🇸 Español (es_ES)

Zie `i18n/README.md` voor meer informatie.

## 🚀 Installatie

### Vereisten
- Python 3.11 of hoger
- pip package manager

### Productie installatie
```bash
pip install {package_name}
```

### Development setup
1. Clone de repository
2. Maak een virtuele omgeving aan:
```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   source venv/bin/activate  # Linux/Mac
```
3. Installeer in development mode:
```bash
   pip install -e ".[dev]"
```

## 💻 Gebruik

### Via command line
```bash
{package_name}
```

### Als module
```bash
python -m app.main
```

### Development
```bash
make run
```

## 📁 Projectstructuur
```
{app_name}/
├── pyproject.toml # Project configuratie (PEP 621)
├── setup.py       # Backwards compatibility
├── MANIFEST.in    # Package manifest
├── LICENSE        # MIT License
├── README.md
├── requirements.txt
├── .gitignore
├── app/           # Hoofd applicatie code
├── assets/        # Icons en afbeeldingen
│   └── icons/     # Standaard icons
├── config/        # Configuratie bestanden
├── css/           # QSS stylesheets
├── data/          # Data opslag
├── docs/          # Documentatie
├── helpers/       # Helper functies
├── i18n/          # Internationalization
│   ├── translator.py
│   └── locales/   # Vertaalbestanden
├── md/            # Markdown bestanden
├── scripts/       # Utility scripts
├── utils/         # Utility functies
└── tests/         # Unit tests
```

## 🎨 Styling

QSS (Qt StyleSheets) bestanden bevinden zich in `css/`:
- `main.qss` - Hoofd styling
- `detail.qss` - Detail window styling

Laad een stylesheet:
```python
from pathlib import Path

def load_stylesheet(name: str) -> str:
    qss_file = Path("css") / name
    return qss_file.read_text()

app.setStyleSheet(load_stylesheet("main.qss"))
```

## 🌍 Internationalization (i18n)

Gebruik de translator in je code:
```python
from i18n import t

# Simpele vertaling
print(t("app.welcome"))

# Met variabelen
print(t("app.greeting", name="Jan"))
```

Zie `i18n/README.md` voor gedetailleerde documentatie.

## 🔧 Scripts

De `scripts/` folder bevat utility scripts:
- `update_toml.py` - Update pyproject.toml
- `bump_version.py` - Verhoog versie
- `generate_requirements.py` - Genereer requirements.txt
- `validate_project.py` - Valideer project

Zie `scripts/README.md` voor details.

## 🧪 Tests
```bash
# Run alle tests
make test

# Met coverage
make coverage

# Alleen specifieke test
pytest tests/test_specific.py -v
```

## 🛠️ Development

### Code formatting
```bash
make format
```

### Linting
```bash
make lint
```

### Build distributie
```bash
make build
```

## 📝 Changelog

Zie [CHANGELOG.md](docs/changelog.md) voor versiegeschiedenis.

## 🤝 Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor richtlijnen.

## 📄 Licentie

Dit project is gelicenseerd onder de MIT License - zie [LICENSE](LICENSE) voor details.

## 👤 Contact

**{author}**

## 🙏 Acknowledgments

- Python Community
- PyQt6 Team
'''


def get_changelog_template(version: str) -> str:
    """Template voor changelog.md."""
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    
    return f'''# Changelog

Alle belangrijke wijzigingen aan dit project worden gedocumenteerd in dit bestand.

Het formaat is gebaseerd op [Keep a Changelog](https://keepachangelog.com/nl/1.0.0/),
en dit project volgt [Semantic Versioning](https://semver.org/lang/nl/).

## [{version}] - {today}

### Toegevoegd
- Initiële release
- Basis projectstructuur volgens PEP 517/518/621
- Standaard configuratie
- Assets folder met standaard icons
- QSS stylesheet templates (main.qss, detail.qss)
- Moderne build configuratie (pyproject.toml)
- Development tools (Black, Flake8, MyPy, pytest)
- Makefile voor development shortcuts
- Scripts folder met utility tools
  - update_toml.py - Update pyproject.toml
  - bump_version.py - Verhoog versienummer
  - generate_requirements.py - Genereer requirements.txt
  - validate_project.py - Valideer project structuur
- **Internationalization (i18n) support**
  - Translator class voor meertaligheid
  - Locale bestanden voor 5 talen (nl_NL, en_US, fr_FR, de_DE, es_ES)
  - Uitgebreide i18n documentatie

### Gewijzigd
- n.v.t.

### Deprecated
- n.v.t.

### Verwijderd
- n.v.t.

### Opgelost
- n.v.t.

### Security
- n.v.t.
'''


def get_help_md_template(app_name: str) -> str:
    """Template voor help.md."""
    return f'''# {app_name} - Help

## 📚 Aan de slag

Welkom bij {app_name}!

## ⚙️ Configuratie

De applicatie gebruikt configuratie bestanden in de `config/` folder:
- `settings.json` - Algemene instellingen (incl. default_locale)

## 🎨 Styling

Pas de look-and-feel aan door de QSS bestanden in `css/` te bewerken:
- `main.qss` - Hoofd styling
- `detail.qss` - Detail windows

## 🌍 Talen

De applicatie ondersteunt meerdere talen via het `i18n/` systeem.

### Taal wijzigen
```python
from i18n import get_translator

translator = get_translator("nl_NL")  # Nederlands
translator.set_locale("en_US")        # Wissel naar Engels
```

### Beschikbare talen
- Nederlands (nl_NL)
- English (en_US)
- Français (fr_FR)
- Deutsch (de_DE)
- Español (es_ES)

Zie `i18n/README.md` voor volledige documentatie.

## 🔧 Functies

Beschrijf hier de hoofdfuncties van de applicatie.

### Functie 1
Beschrijving van functie 1.

### Functie 2
Beschrijving van functie 2.

## 🛠️ Development Scripts

De `scripts/` folder bevat utilities:

### update_toml.py
```bash
cd scripts
python update_toml.py --add-dep "requests>=2.31.0"
```

### bump_version.py
```bash
cd scripts
python bump_version.py patch  # 1.0.0 → 1.0.1
```

Zie `scripts/README.md` voor volledige documentatie.

## ❓ Veelgestelde vragen

### Hoe start ik de applicatie?
```bash
python app/main.py
```

### Waar staan de configuratie bestanden?
In de `config/` folder.

### Hoe pas ik de styling aan?
Bewerk de QSS bestanden in de `css/` folder.

### Hoe voeg ik een dependency toe?
```bash
cd scripts
python update_toml.py --add-dep "package-name>=version"
pip install package-name
```

### Hoe voeg ik een nieuwe taal toe?
Zie `i18n/README.md` sectie "Nieuwe taal toevoegen".

## 📞 Contact

Voor vragen of ondersteuning, neem contact op met de ontwikkelaar.
'''


def get_requirements_txt_template() -> str:
    """Template voor requirements.txt."""
    return '''# Core dependencies
# Voeg hier je packages toe
# Bijvoorbeeld:
# PyQt6>=6.6.1
# requests>=2.31.0
# Pillow>=10.1.0

# Note: Voor development dependencies, zie pyproject.toml [project.optional-dependencies]
# Genereer deze file automatisch: python scripts/generate_requirements.py
'''


def get_gitkeep_template() -> str:
    """Template voor .gitkeep bestanden."""
    return '''# Deze file zorgt ervoor dat lege mappen in git blijven bestaan
'''


def get_scripts_readme_template() -> str:
    """Template voor scripts/README.md."""
    return '''# Scripts Folder

Utility scripts voor project maintenance en automation.

## 📋 Beschikbare Scripts

### 🔧 update_toml.py
Update `pyproject.toml` automatisch.

**Gebruik:**
```bash
# Voeg dependency toe
python update_toml.py --add-dep "requests>=2.31.0"

# Voeg dev dependency toe
python update_toml.py --add-dev "pytest-cov>=4.1.0"

# Update versie
python update_toml.py --set-version "1.0.1"

# Update auteur
python update_toml.py --set-author "Nieuwe Naam"
```

**Vereisten:** `tomli`, `tomli-w`

---

### 📈 bump_version.py
Verhoog versienummer overal in het project.

**Gebruik:**
```bash
# Patch (1.0.0 → 1.0.1)
python bump_version.py patch

# Minor (1.0.0 → 1.1.0)
python bump_version.py minor

# Major (1.0.0 → 2.0.0)
python bump_version.py major

# Specifieke versie
python bump_version.py --version 2.5.3
```

**Update:**
- `app/version.py`
- `pyproject.toml`
- `docs/changelog.md` (voegt nieuwe sectie toe)

**Vereisten:** `tomli`, `tomli-w` (optioneel, gebruikt regex fallback)

---

### 📦 generate_requirements.py
Genereer `requirements.txt` uit `pyproject.toml`.

**Gebruik:**
```bash
# Alleen runtime dependencies
python generate_requirements.py

# Inclusief dev dependencies
python generate_requirements.py --dev

# Custom output
python generate_requirements.py --output requirements-dev.txt --dev
```

**Vereisten:** `tomli`

---

### ✅ validate_project.py
Valideer project structuur en configuratie.

**Gebruik:**
```bash
python validate_project.py
```

**Controleert:**
- Bestanden en folders aanwezig
- `pyproject.toml` is valide
- Tests runnen (pytest)
- Code style (black)

**Vereisten:** `tomli`, `pytest` (optioneel), `black` (optioneel)

---

## 📦 Dependencies Installeren
```bash
pip install tomli tomli-w pytest black
```

Of gebruik development mode:
```bash
pip install -e ".[dev]"
```

## 💡 Tips

- Run scripts vanuit de `scripts/` folder
- Scripts maken automatisch backups
- Check altijd de output voor errors
- Gebruik `--help` voor meer opties (waar beschikbaar)

## 🐛 Troubleshooting

### tomli/tomli-w not found
```bash
pip install tomli tomli-w
```

### Script vindt pyproject.toml niet
Zorg dat je in de `scripts/` folder staat:
```bash
cd scripts
python update_toml.py ...
```

### Permission errors
Run met admin rechten (Windows) of sudo (Linux)
'''


def get_update_toml_script() -> str:
    """Template voor scripts/update_toml.py."""
    return '''import argparse
import sys
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description="Update pyproject.toml")
    parser.add_argument("--add-dep", help="Voeg runtime dependency toe")
    parser.add_argument("--add-dev", help="Voeg dev dependency toe")
    parser.add_argument("--set-version", help="Zet versie nummer")
    parser.add_argument("--set-author", help="Zet auteur naam")
    parser.add_argument("--set-description", help="Zet beschrijving")
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    toml_file = project_root / "pyproject.toml"
    
    if not toml_file.exists():
        print(f"❌ Fout: {toml_file} niet gevonden")
        sys.exit(1)
    
    try:
        import tomli
        import tomli_w
    except ImportError:
        print("❌ Fout: tomli en tomli_w zijn vereist")
        print("Installeer met: pip install tomli tomli-w")
        sys.exit(1)
    
    with open(toml_file, "rb") as f:
        data = tomli.load(f)
    
    backup_file = toml_file.with_suffix(".toml.bak")
    shutil.copy2(toml_file, backup_file)
    print(f"📋 Backup gemaakt: {backup_file}")
    
    modified = False
    
    if args.add_dep:
        if "project" not in data:
            data["project"] = {}
        if "dependencies" not in data["project"]:
            data["project"]["dependencies"] = []
        
        if args.add_dep not in data["project"]["dependencies"]:
            data["project"]["dependencies"].append(args.add_dep)
            print(f"✅ Dependency toegevoegd: {args.add_dep}")
            modified = True
        else:
            print(f"ℹ️  Dependency bestaat al: {args.add_dep}")
    
    if args.add_dev:
        if "project" not in data:
            data["project"] = {}
        if "optional-dependencies" not in data["project"]:
            data["project"]["optional-dependencies"] = {}
        if "dev" not in data["project"]["optional-dependencies"]:
            data["project"]["optional-dependencies"]["dev"] = []
        
        if args.add_dev not in data["project"]["optional-dependencies"]["dev"]:
            data["project"]["optional-dependencies"]["dev"].append(args.add_dev)
            print(f"✅ Dev dependency toegevoegd: {args.add_dev}")
            modified = True
    
    if args.set_version:
        if "project" not in data:
            data["project"] = {}
        data["project"]["version"] = args.set_version
        print(f"✅ Versie gezet: {args.set_version}")
        modified = True
    
    if args.set_author:
        if "project" not in data:
            data["project"] = {}
        data["project"]["authors"] = [{"name": args.set_author}]
        print(f"✅ Auteur gezet: {args.set_author}")
        modified = True
    
    if args.set_description:
        if "project" not in data:
            data["project"] = {}
        data["project"]["description"] = args.set_description
        print(f"✅ Beschrijving gezet: {args.set_description}")
        modified = True
    
    if modified:
        with open(toml_file, "wb") as f:
            tomli_w.dump(data, f)
        print(f"💾 {toml_file} is bijgewerkt")
    else:
        print("ℹ️  Geen wijzigingen")
    
    print("✅ Klaar!")


if __name__ == "__main__":
    main()
'''


def get_bump_version_script() -> str:
    """Template voor scripts/bump_version.py."""
    return r'''import argparse
import re
import sys
from pathlib import Path
from datetime import date


def parse_version(version_str: str) -> tuple:
    """Parse version string to (major, minor, patch)."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if not match:
        raise ValueError(f"Ongeldige versie: {version_str}")
    return tuple(map(int, match.groups()))


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple to string."""
    return f"{major}.{minor}.{patch}"


def bump_version(current: str, bump_type: str) -> str:
    """Bump version based on type."""
    major, minor, patch = parse_version(current)
    
    if bump_type == "major":
        return format_version(major + 1, 0, 0)
    elif bump_type == "minor":
        return format_version(major, minor + 1, 0)
    elif bump_type == "patch":
        return format_version(major, minor, patch + 1)
    else:
        raise ValueError(f"Onbekend bump type: {bump_type}")


def update_version_py(file_path: Path, new_version: str) -> bool:
    """Update app/version.py."""
    if not file_path.exists():
        print(f"⚠️  {file_path} niet gevonden")
        return False
    
    content = file_path.read_text(encoding="utf-8")
    new_content = re.sub(
        r'__version__\s*=\s*["\'][\d.]+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    file_path.write_text(new_content, encoding="utf-8")
    print(f"✅ {file_path} bijgewerkt")
    return True


def update_pyproject_toml(file_path: Path, new_version: str) -> bool:
    """Update pyproject.toml."""
    if not file_path.exists():
        print(f"⚠️  {file_path} niet gevonden")
        return False
    
    try:
        import tomli
        import tomli_w
        
        with open(file_path, "rb") as f:
            data = tomli.load(f)
        
        if "project" in data:
            data["project"]["version"] = new_version
        
        with open(file_path, "wb") as f:
            tomli_w.dump(data, f)
        
        print(f"✅ {file_path} bijgewerkt")
        return True
        
    except ImportError:
        content = file_path.read_text(encoding="utf-8")
        new_content = re.sub(
            r'version\s*=\s*["\'][\d.]+["\']',
            f'version = "{new_version}"',
            content
        )
        file_path.write_text(new_content, encoding="utf-8")
        print(f"✅ {file_path} bijgewerkt (regex)")
        return True


def update_changelog(file_path: Path, new_version: str) -> bool:
    """Voeg nieuwe sectie toe aan changelog."""
    if not file_path.exists():
        print(f"⚠️  {file_path} niet gevonden")
        return False
    
    today = date.today().strftime("%Y-%m-%d")
    content = file_path.read_text(encoding="utf-8")
    
    new_section = f"""## [{new_version}] - {today}

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 

"""
    
    lines = content.split("\n")
    insert_index = 0
    for i, line in enumerate(lines):
        if line.startswith("## ["):
            insert_index = i
            break
    
    if insert_index > 0:
        lines.insert(insert_index, new_section)
        file_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"✅ {file_path} bijgewerkt")
        return True
    else:
        print(f"⚠️  Kon insert point niet vinden in {file_path}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Verhoog project versie")
    parser.add_argument(
        "bump_type",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Type versie verhoging"
    )
    parser.add_argument(
        "--version",
        help="Specifieke versie nummer (bijv. 2.5.3)"
    )
    
    args = parser.parse_args()
    
    if not args.bump_type and not args.version:
        parser.print_help()
        sys.exit(1)
    
    project_root = Path(__file__).parent.parent
    version_file = project_root / "app" / "version.py"
    toml_file = project_root / "pyproject.toml"
    changelog_file = project_root / "docs" / "changelog.md"
    
    if not version_file.exists():
        print(f"❌ {version_file} niet gevonden")
        sys.exit(1)
    
    current_content = version_file.read_text()
    match = re.search(r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', current_content)
    
    if not match:
        print("❌ Kon huidige versie niet vinden in app/version.py")
        sys.exit(1)
    
    current_version = match.group(1)
    print(f"📌 Huidige versie: {current_version}")
    
    if args.version:
        new_version = args.version
        try:
            parse_version(new_version)
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)
    else:
        new_version = bump_version(current_version, args.bump_type)
    
    print(f"🚀 Nieuwe versie: {new_version}")
    print()

    success = True
    success &= update_version_py(version_file, new_version)
    success &= update_pyproject_toml(toml_file, new_version)
    success &= update_changelog(changelog_file, new_version)
    
    print()
    if success:
        print("=" * 60)
        print(f"✅ Versie verhoogd: {current_version} → {new_version}")
        print("=" * 60)
    else:
        print("⚠️  Sommige updates zijn mislukt")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''


def get_generate_requirements_script() -> str:
    """Template voor scripts/generate_requirements.py."""
    return '''import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Genereer requirements.txt uit pyproject.toml"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Inclusief dev dependencies"
    )
    parser.add_argument(
        "--output",
        default="requirements.txt",
        help="Output bestand (default: requirements.txt)"
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    toml_file = project_root / "pyproject.toml"
    
    if not toml_file.exists():
        print(f"❌ Fout: {toml_file} niet gevonden")
        sys.exit(1)
    
    try:
        import tomli
    except ImportError:
        print("❌ Fout: tomli is vereist")
        print("Installeer met: pip install tomli")
        sys.exit(1)
    
    with open(toml_file, "rb") as f:
        data = tomli.load(f)
    
    requirements = []
    
    if "project" in data and "dependencies" in data["project"]:
        requirements.extend(data["project"]["dependencies"])
    
    if args.dev:
        if "project" in data and "optional-dependencies" in data["project"]:
            if "dev" in data["project"]["optional-dependencies"]:
                requirements.extend(data["project"]["optional-dependencies"]["dev"])
    
    if not requirements:
        print("⚠️  Geen dependencies gevonden in pyproject.toml")
        sys.exit(0)
    
    output_file = project_root / args.output
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Gegenereerd uit pyproject.toml\\n")
        f.write("# Regenereer met: python scripts/generate_requirements.py\\n")
        f.write("\\n")
        for req in requirements:
            f.write(f"{req}\\n")
    
    print(f"✅ {len(requirements)} dependencies geschreven naar {output_file}")
    
    if args.dev:
        print("ℹ️  Inclusief dev dependencies")
    
    print()
    print("📦 Dependencies:")
    for req in requirements:
        print(f"   - {req}")


if __name__ == "__main__":
    main()
'''


def get_validate_project_script() -> str:
    """Template voor scripts/validate_project.py."""
    return '''import sys
from pathlib import Path
import subprocess


def check_file_exists(file_path: Path, required: bool = True) -> bool:
    """Check of bestand bestaat."""
    exists = file_path.exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {file_path.name}")
    return exists or not required


def check_folder_exists(folder_path: Path, required: bool = True) -> bool:
    """Check of folder bestaat."""
    exists = folder_path.exists() and folder_path.is_dir()
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {folder_path.name}/")
    return exists or not required


def validate_toml(toml_file: Path) -> bool:
    """Valideer pyproject.toml."""
    if not toml_file.exists():
        return False
    
    try:
        import tomli
        with open(toml_file, "rb") as f:
            data = tomli.load(f)
        
        if "project" not in data:
            print("   ⚠️  Geen [project] sectie")
            return False
        
        required_fields = ["name", "version"]
        for field in required_fields:
            if field not in data["project"]:
                print(f"   ⚠️  Veld '{field}' ontbreekt")
                return False
        
        print(f"   ✅ Valide TOML (v{data['project']['version']})")
        return True
        
    except Exception as e:
        print(f"   ❌ TOML parse fout: {e}")
        return False


def validate_i18n(i18n_dir: Path) -> bool:
    """Valideer i18n locales."""
    if not i18n_dir.exists():
        print("   ⚠️  i18n folder niet gevonden")
        return False
    
    locales_dir = i18n_dir / "locales"
    if not locales_dir.exists():
        print("   ⚠️  locales folder niet gevonden")
        return False
    
    locale_files = list(locales_dir.glob("*.json"))
    if not locale_files:
        print("   ⚠️  Geen locale bestanden gevonden")
        return False
    
    print(f"   ✅ {len(locale_files)} locale(s) gevonden")
    return True


def run_tests() -> bool:
    """Run pytest."""
    try:
        result = subprocess.run(
            ["pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("   ✅ Alle tests slagen")
            return True
        else:
            print(f"   ❌ Tests gefaald (exit code {result.returncode})")
            return False
    except FileNotFoundError:
        print("   ⚠️  pytest niet gevonden")
        return True
    except subprocess.TimeoutExpired:
        print("   ⚠️  Tests timeout")
        return False


def check_code_style() -> bool:
    """Check code style met black --check."""
    try:
        result = subprocess.run(
            ["black", "--check", "app", "helpers", "utils", "i18n"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("   ✅ Code formatting OK")
            return True
        else:
            print("   ⚠️  Code niet geformatteerd (run: make format)")
            return True
    except FileNotFoundError:
        print("   ⚠️  black niet gevonden")
        return True
    except subprocess.TimeoutExpired:
        print("   ⚠️  Black timeout")
        return True


def main():
    print("=" * 60)
    print("🔍 Project Validatie")
    print("=" * 60)
    print()
    
    project_root = Path(__file__).parent.parent
    all_ok = True
    
    print("📄 Bestanden:")
    all_ok &= check_file_exists(project_root / "pyproject.toml")
    all_ok &= check_file_exists(project_root / "README.md")
    all_ok &= check_file_exists(project_root / "LICENSE")
    all_ok &= check_file_exists(project_root / "requirements.txt", required=False)
    all_ok &= check_file_exists(project_root / ".gitignore")
    print()
    
    print("📁 Folders:")
    all_ok &= check_folder_exists(project_root / "app")
    all_ok &= check_folder_exists(project_root / "tests")
    all_ok &= check_folder_exists(project_root / "assets")
    all_ok &= check_folder_exists(project_root / "css")
    all_ok &= check_folder_exists(project_root / "scripts")
    all_ok &= check_folder_exists(project_root / "i18n")
    all_ok &= check_folder_exists(project_root / "venv", required=False)
    print()
    
    print("⚙️  Configuratie:")
    all_ok &= validate_toml(project_root / "pyproject.toml")
    print()
    
    print("🌍 Internationalization:")
    all_ok &= validate_i18n(project_root / "i18n")
    print()
    
    print("🧪 Tests:")
    all_ok &= run_tests()
    print()
    
    print("🎨 Code Style:")
    all_ok &= check_code_style()
    print()
    
    print("=" * 60)
    if all_ok:
        print("✅ Validatie geslaagd!")
    else:
        print("❌ Validatie gefaald - zie bovenstaande fouten")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
'''


# ===== i18n TEMPLATES =====

def get_translator_py_template() -> str:
    """Template voor i18n/translator.py."""
    return '''import json
from pathlib import Path
from typing import Dict, Optional


class Translator:
    """
    Eenvoudige translator voor i18n support.
    
    Gebruik:
        translator = Translator("nl_NL")
        text = translator.get("app.welcome")
    """
    
    def __init__(self, locale: str = "en_US"):
        """
        Initialiseer translator.
        
        Args:
            locale: Taalcode (bijv. nl_NL, en_US, fr_FR)
        """
        self.locale = locale
        self.translations: Dict[str, str] = {}
        self.fallback_locale = "en_US"
        self.fallback_translations: Dict[str, str] = {}
        
        self._load_translations()
    
    def _load_translations(self):
        """Laad translation bestanden."""
        locales_dir = Path(__file__).parent / "locales"
        
        # Laad gekozen locale
        locale_file = locales_dir / f"{self.locale}.json"
        if locale_file.exists():
            with open(locale_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        
        # Laad fallback (Engels) als backup
        if self.locale != self.fallback_locale:
            fallback_file = locales_dir / f"{self.fallback_locale}.json"
            if fallback_file.exists():
                with open(fallback_file, "r", encoding="utf-8") as f:
                    self.fallback_translations = json.load(f)
    
    def get(self, key: str, **kwargs) -> str:
        """
        Haal vertaling op voor key.
        
        Args:
            key: Translation key (bijv. "app.welcome")
            **kwargs: Variabelen voor formatting (bijv. name="Jan")
        
        Returns:
            Vertaalde string, of key zelf als niet gevonden
        
        Voorbeelden:
            translator.get("app.welcome")
            translator.get("app.greeting", name="Jan")
        """
        # Probeer huidige locale
        text = self.translations.get(key)
        
        # Fallback naar Engels
        if text is None:
            text = self.fallback_translations.get(key)
        
        # Laatste fallback: return key zelf
        if text is None:
            return key
        
        # Format met kwargs indien aanwezig
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass  # Ignore missing format variables
        
        return text
    
    def set_locale(self, locale: str):
        """
        Verander actieve locale.
        
        Args:
            locale: Nieuwe taalcode
        """
        self.locale = locale
        self._load_translations()
    
    def get_available_locales(self) -> list:
        """
        Haal beschikbare locales op.
        
        Returns:
            List van locale codes
        """
        locales_dir = Path(__file__).parent / "locales"
        if not locales_dir.exists():
            return []
        
        locales = []
        for file in locales_dir.glob("*.json"):
            locales.append(file.stem)
        
        return sorted(locales)


# Singleton instance voor gemakkelijk gebruik
_translator: Optional[Translator] = None


def get_translator(locale: str = "en_US") -> Translator:
    """
    Haal translator instance op (singleton pattern).
    
    Args:
        locale: Taalcode (alleen bij eerste aanroep)
    
    Returns:
        Translator instance
    """
    global _translator
    if _translator is None:
        _translator = Translator(locale)
    return _translator


def t(key: str, **kwargs) -> str:
    """
    Shortcut voor get_translator().get().
    
    Args:
        key: Translation key
        **kwargs: Format variabelen
    
    Returns:
        Vertaalde string
    
    Voorbeeld:
        from i18n import t
        print(t("app.welcome"))
    """
    return get_translator().get(key, **kwargs)
'''


def get_i18n_init_template() -> str:
    """Template voor i18n/__init__.py."""
    return '''from i18n.translator import Translator, get_translator, t

__all__ = ["Translator", "get_translator", "t"]
'''


def get_locale_nl_nl_template() -> str:
    """Template voor i18n/locales/nl_NL.json."""
    data = {
        "app.name": "Mijn Applicatie",
        "app.welcome": "Welkom bij {app_name}!",
        "app.greeting": "Hallo, {name}!",
        "app.version": "Versie {version}",
        
        "menu.file": "Bestand",
        "menu.file.new": "Nieuw",
        "menu.file.open": "Openen",
        "menu.file.save": "Opslaan",
        "menu.file.exit": "Afsluiten",
        
        "menu.edit": "Bewerken",
        "menu.edit.cut": "Knippen",
        "menu.edit.copy": "Kopiëren",
        "menu.edit.paste": "Plakken",
        
        "menu.help": "Help",
        "menu.help.about": "Over",
        "menu.help.documentation": "Documentatie",
        
        "button.ok": "OK",
        "button.cancel": "Annuleren",
        "button.yes": "Ja",
        "button.no": "Nee",
        "button.close": "Sluiten",
        "button.save": "Opslaan",
        "button.delete": "Verwijderen",
        
        "message.confirm_delete": "Weet je zeker dat je dit wilt verwijderen?",
        "message.save_success": "Succesvol opgeslagen",
        "message.save_error": "Fout bij opslaan: {error}",
        "message.loading": "Bezig met laden...",
        
        "error.file_not_found": "Bestand niet gevonden",
        "error.permission_denied": "Toegang geweigerd",
        "error.unknown": "Onbekende fout: {error}"
    }
    
    import json
    return json.dumps(data, ensure_ascii=False, indent=4)


def get_locale_en_us_template() -> str:
    """Template voor i18n/locales/en_US.json."""
    data = {
        "app.name": "My Application",
        "app.welcome": "Welcome to {app_name}!",
        "app.greeting": "Hello, {name}!",
        "app.version": "Version {version}",
        
        "menu.file": "File",
        "menu.file.new": "New",
        "menu.file.open": "Open",
        "menu.file.save": "Save",
        "menu.file.exit": "Exit",
        
        "menu.edit": "Edit",
        "menu.edit.cut": "Cut",
        "menu.edit.copy": "Copy",
        "menu.edit.paste": "Paste",
        
        "menu.help": "Help",
        "menu.help.about": "About",
        "menu.help.documentation": "Documentation",
        
        "button.ok": "OK",
        "button.cancel": "Cancel",
        "button.yes": "Yes",
        "button.no": "No",
        "button.close": "Close",
        "button.save": "Save",
        "button.delete": "Delete",
        
        "message.confirm_delete": "Are you sure you want to delete this?",
        "message.save_success": "Saved successfully",
        "message.save_error": "Error saving: {error}",
        "message.loading": "Loading...",
        
        "error.file_not_found": "File not found",
        "error.permission_denied": "Permission denied",
        "error.unknown": "Unknown error: {error}"
    }
    
    import json
    return json.dumps(data, ensure_ascii=False, indent=4)


def get_locale_fr_fr_template() -> str:
    """Template voor i18n/locales/fr_FR.json."""
    data = {
        "app.name": "Mon Application",
        "app.welcome": "Bienvenue à {app_name}!",
        "app.greeting": "Bonjour, {name}!",
        "app.version": "Version {version}",
        
        "menu.file": "Fichier",
        "menu.file.new": "Nouveau",
        "menu.file.open": "Ouvrir",
        "menu.file.save": "Enregistrer",
        "menu.file.exit": "Quitter",
        
        "menu.edit": "Édition",
        "menu.edit.cut": "Couper",
        "menu.edit.copy": "Copier",
        "menu.edit.paste": "Coller",
        
        "menu.help": "Aide",
        "menu.help.about": "À propos",
        "menu.help.documentation": "Documentation",
        
        "button.ok": "OK",
        "button.cancel": "Annuler",
        "button.yes": "Oui",
        "button.no": "Non",
        "button.close": "Fermer",
        "button.save": "Enregistrer",
        "button.delete": "Supprimer",
        
        "message.confirm_delete": "Êtes-vous sûr de vouloir supprimer ceci?",
        "message.save_success": "Enregistré avec succès",
        "message.save_error": "Erreur lors de l'enregistrement: {error}",
        "message.loading": "Chargement...",
        
        "error.file_not_found": "Fichier introuvable",
        "error.permission_denied": "Permission refusée",
        "error.unknown": "Erreur inconnue: {error}"
    }
    
    import json
    return json.dumps(data, ensure_ascii=False, indent=4)


def get_locale_de_de_template() -> str:
    """Template voor i18n/locales/de_DE.json."""
    data = {
        "app.name": "Meine Anwendung",
        "app.welcome": "Willkommen bei {app_name}!",
        "app.greeting": "Hallo, {name}!",
        "app.version": "Version {version}",
        
        "menu.file": "Datei",
        "menu.file.new": "Neu",
        "menu.file.open": "Öffnen",
        "menu.file.save": "Speichern",
        "menu.file.exit": "Beenden",
        
        "menu.edit": "Bearbeiten",
        "menu.edit.cut": "Ausschneiden",
        "menu.edit.copy": "Kopieren",
        "menu.edit.paste": "Einfügen",
        
        "menu.help": "Hilfe",
        "menu.help.about": "Über",
        "menu.help.documentation": "Dokumentation",
        
        "button.ok": "OK",
        "button.cancel": "Abbrechen",
        "button.yes": "Ja",
        "button.no": "Nein",
        "button.close": "Schließen",
        "button.save": "Speichern",
        "button.delete": "Löschen",
        
        "message.confirm_delete": "Möchten Sie dies wirklich löschen?",
        "message.save_success": "Erfolgreich gespeichert",
        "message.save_error": "Fehler beim Speichern: {error}",
        "message.loading": "Wird geladen...",
        
        "error.file_not_found": "Datei nicht gefunden",
        "error.permission_denied": "Zugriff verweigert",
        "error.unknown": "Unbekannter Fehler: {error}"
    }
    
    import json
    return json.dumps(data, ensure_ascii=False, indent=4)


def get_locale_es_es_template() -> str:
    """Template voor i18n/locales/es_ES.json."""
    data = {
        "app.name": "Mi Aplicación",
        "app.welcome": "¡Bienvenido a {app_name}!",
        "app.greeting": "¡Hola, {name}!",
        "app.version": "Versión {version}",
        
        "menu.file": "Archivo",
        "menu.file.new": "Nuevo",
        "menu.file.open": "Abrir",
        "menu.file.save": "Guardar",
        "menu.file.exit": "Salir",
        
        "menu.edit": "Editar",
        "menu.edit.cut": "Cortar",
        "menu.edit.copy": "Copiar",
        "menu.edit.paste": "Pegar",
        
        "menu.help": "Ayuda",
        "menu.help.about": "Acerca de",
        "menu.help.documentation": "Documentación",
        
        "button.ok": "Aceptar",
        "button.cancel": "Cancelar",
        "button.yes": "Sí",
        "button.no": "No",
        "button.close": "Cerrar",
        "button.save": "Guardar",
        "button.delete": "Eliminar",
        
        "message.confirm_delete": "¿Estás seguro de que quieres eliminar esto?",
        "message.save_success": "Guardado exitosamente",
        "message.save_error": "Error al guardar: {error}",
        "message.loading": "Cargando...",
        
        "error.file_not_found": "Archivo no encontrado",
        "error.permission_denied": "Permiso denegado",
        "error.unknown": "Error desconocido: {error}"
    }
    
    import json
    return json.dumps(data, ensure_ascii=False, indent=4)


def get_i18n_readme_template() -> str:
    """Template voor i18n/README.md."""
    return '''# Internationalization (i18n)

Deze folder bevat de meertaligheid support voor de applicatie.

## 📁 Structuur
```
i18n/
├── __init__.py
├── translator.py          # Translation helper class
├── locales/              # Vertaalbestanden
│   ├── nl_NL.json       # Nederlands
│   ├── en_US.json       # Engels (fallback)
│   ├── fr_FR.json       # Frans
│   ├── de_DE.json       # Duits
│   └── es_ES.json       # Spaans
└── README.md            # Deze file
```

## 🚀 Gebruik

### Basis gebruik
```python
from i18n import t

# Simpele vertaling
print(t("app.welcome"))  # "Welkom bij Mijn Applicatie!"

# Met variabelen
print(t("app.greeting", name="Jan"))  # "Hallo, Jan!"
```

### Taal wijzigen
```python
from i18n import get_translator

# Start met Nederlands
translator = get_translator("nl_NL")
print(translator.get("button.ok"))  # "OK"

# Wissel naar Frans
translator.set_locale("fr_FR")
print(translator.get("button.ok"))  # "OK" (zelfde in Frans)
```

### In PyQt6
```python
from PyQt6.QtWidgets import QPushButton
from i18n import t

# Buttons
btn_ok = QPushButton(t("button.ok"))
btn_cancel = QPushButton(t("button.cancel"))

# Menu
file_menu = menubar.addMenu(t("menu.file"))
```

## 📝 Nieuwe taal toevoegen

1. Maak nieuw bestand in `locales/`:
```bash
   locales/it_IT.json  # Italiaans
```

2. Kopieer structuur van `en_US.json`

3. Vertaal alle strings:
```json
   {
       "app.welcome": "Benvenuto in {app_name}!",
       "button.ok": "OK",
       "button.cancel": "Annulla"
   }
```

4. Gebruik in je app:
```python
   translator = get_translator("it_IT")
```

## 🔑 Translation Keys

### Conventies:
- **Lowercase** met **dots** als separator
- **Logische groepering**: `categorie.subcategorie.item`
- **Beschrijvend**: `button.save` niet `btn1`

### Voorbeelden:
```
app.name                    # Applicatie naam
app.welcome                 # Welkomstbericht
menu.file.save             # Menu > File > Save
button.ok                  # OK knop
message.confirm_delete     # Bevestigingsbericht
error.file_not_found       # Foutmelding
```

## 🌍 Beschikbare Locales

| Code | Taal | Status |
|------|------|--------|
| `en_US` | English (US) | ✅ Complete (fallback) |
| `nl_NL` | Nederlands | ✅ Complete |
| `fr_FR` | Français | ✅ Complete |
| `de_DE` | Deutsch | ✅ Complete |
| `es_ES` | Español | ✅ Complete |

## 🔧 Advanced

### Format strings

Gebruik `{variable}` voor dynamische waarden:
```json
{
    "app.greeting": "Hallo, {name}!",
    "app.version": "Versie {version}",
    "message.save_error": "Fout: {error}"
}
```
```python
t("app.greeting", name="Jan")        # "Hallo, Jan!"
t("app.version", version="1.0.0")    # "Versie 1.0.0"
```

### Fallback systeem

1. Probeer gekozen locale (bijv. `nl_NL`)
2. Fallback naar Engels (`en_US`)
3. Return de key zelf als laatste optie

### Taal detectie
```python
import locale

# Systeem locale detecteren
system_locale = locale.getdefaultlocale()[0]  # bijv. "nl_NL"
translator = get_translator(system_locale)
```

## 📚 Best Practices

### ✅ DO:
- Gebruik beschrijvende keys
- Groepeer gerelateerde vertalingen
- Test alle talen regelmatig
- Houd vertalingen consistent

### ❌ DON'T:
- Hardcode strings in code
- Gebruik cijfers als keys (`msg1`, `msg2`)
- Vergeet variabelen in format strings
- Mix talen in één bestand

## 🐛 Troubleshooting

### Key niet gevonden
```python
# Returns de key zelf
t("non.existent.key")  # "non.existent.key"
```

### Locale bestand niet gevonden
```python
# Falls back naar en_US
translator = get_translator("xx_XX")  # Gebruikt Engels
```

### Format error
```python
# Ignoreert missing variabelen
t("app.greeting")  # "Hallo, {name}!" (variabele niet replaced)
```

## 📖 Meer info

- [Python i18n Best Practices](https://docs.python.org/3/library/i18n.html)
- [Locale Codes (ISO 639-1 + ISO 3166-1)](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
'''


# ===== BUILD & RELEASE TEMPLATES =====
# Gebaseerd op het bewezen ArticleSearch-patroon (build_installer15.bat,
# build_and_publish.ps1, publish.ps1, export_to_usb5.bat): dynamische
# root-resolutie (geen hardcoded paden), .venv/venv-detectie met voorkeur
# voor .venv, Intune-veilige Inno Setup-installer (CloseApplications=force,
# RestartApplications=no), en GitHub-release via de 'gh' CLI.

def get_build_installer_bat_template(app_name: str) -> str:
    return rf"""@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

rem Altijd uitvoeren vanuit de map waar dit .bat bestand staat
cd /d "%~dp0"

rem ================================================
rem build_installer.bat - Build + Inno Setup installer generator
rem File: build_installer.bat
rem Role: Bouwt de PyInstaller-EXE en genereert/compileert het Inno
rem Setup installer-script (.iss), voor zowel interactief gebruik
rem als niet-interactieve aanroep vanuit build_and_publish.ps1
rem (via env vars AS_BUMP_PART, AS_MAKE_INSTALLER, AS_DO_SIGN).
rem Version: 1.3.0
rem Author: Barremans
rem Changes: 1.3.0 - :PREFLIGHT_CERT volledig verwijderd (zie het
rem uitgebreide commentaarblok bij die verwijderde sectie
rem verderop in dit bestand): de PowerShell Cert:\-validatie
rem faalde op de doelmachine op 3 verschillende manieren
rem los van het certificaat zelf. signtool + de bestaande
rem verify-stap (:SIGN_FILE) zijn de enige, betrouwbare
rem validatie -- exact het patroon van de originele,
rem al bewezen build-flow van vóór de centrale
rem signing-integratie.
rem Changes: 1.2.0 - Nieuwe stap [3c]: genereert version_info.txt (Windows
rem VersionInfo-resource: CompanyName/ProductName/
rem FileDescription/FileVersion/ProductVersion) MET de
rem effectieve build-versie, voor de PyInstaller-build.
rem Project_Generator.spec v1.2.0 verwijst er nu naar via
rem EXE(..., version='version_info.txt'). Voorheen had de
rem exe GEEN enkele Windows-metadata (leeg Eigenschappen >
rem Details-tabblad) -- samen met v1.1.0's signing-
rem verificatie het tweede stuk van de "check Inno en
rem sign goed"-analyse voor de Defender/Intune-fout.
rem Changes: 1.1.0 - Handtekening-VERIFICATIE toegevoegd na het signen
rem (signtool verify /pa /v), n.a.v. een bevestigde fout
rem op andere Windows-machines ("Kan geen toegang krijgen
rem tot het opgegeven apparaat, pad of bestand") op
rem Intune-beheerde toestellen met Controlled Folder
rem Access aan. Signen alleen ("gesigned") betekent NIET
rem automatisch "vertrouwd door Defender/SmartScreen/CFA"
rem -- dat vereist een keten naar een PUBLIEK vertrouwde
rem CA-root. Een zelfondertekend/intern certificaat (zeer
rem waarschijnlijk wat /a hier oppikt via de lokale
rem certificaatstore) signeert prima maar wordt op andere
rem machines nog steeds als onbekend behandeld. Het
rem script waarschuwt nu expliciet + toont welk
rem certificaat effectief gebruikt werd, i.p.v. stil door
rem te gaan met een niet-vertrouwde signature. Dit is een
rem organisatorisch/beleidsprobleem (Intune/Defender-
rem configuratie), geen zuivere codefout -- zie de
rem ACTIE NODIG-melding in :SIGN_FILE voor de 3 opties.
rem Changes: 1.0.0 - Aangepast vanuit ArticleSearch (build_installer.bat
rem v1.4.0, auteur Bart Bossuyt) naar Project Generator's
rem eigen structuur:
rem (1) PROJECT_NAME=Project_Generator, DISPLAY_NAME=
rem "Python Project Generator" (los van elkaar,
rem consistent met build_project_generator.bat
rem v1.1.0) i.p.v. een hardcoded "ArticleSearch".
rem (2) SPEC_FILE=Project_Generator.spec i.p.v.
rem SearchArticle.spec.
rem (3) Versie-bump roept nu "scripts\bump_version.py"
rem aan i.p.v. root-"bump_version.py" -- dit was de
rem directe oorzaak van de crash ("can't open file
rem ...\bump_version.py") toen dit script ongewijzigd
rem overgenomen werd.
rem (4) Versie wordt gelezen uit "app/version.py" i.p.v.
rem root-"version.py" (Project Generator's version.py
rem staat in app/, zie context_ProjectGenerator.md).
rem (5) APPGUID hergebruikt de AL BESTAANDE GUID uit
rem build_project_generator.bat v1.1.0
rem ({{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}) i.p.v.
rem ArticleSearch's GUID -- kritiek voor correcte
rem upgrade-detectie; een nieuwe GUID zou Windows
rem elke build als een andere applicatie laten zien.
rem (6) Stap [5] Assets kopieren aangepast naar Project
rem Generator's echte structuur: assets/, i18n/locales/,
rem docs/, requirements.txt -- i.p.v. ArticleSearch's
rem assets/logs/label/docs/translations +
rem requirements.txt/help.md/settings.json.
rem BUGFIX t.o.v. build_project_generator.bat v1.1.0:
rem dat script kopieerde docs/ NIET mee, terwijl
rem gui/main_window.py::_show_help()/_show_changelog()
rem wel HELP_{{locale}}.md/CHANGELOG_{{locale}}.md uit
rem docs/ leest -- zonder deze fix zou Help/Changelog
rem in een gebouwde installer altijd falen.
rem Overige logica (signing via certificaatstore,
rem Intune-safe CloseApplications=force/
rem RestartApplications=no, env-var-aansturing vanuit
rem build_and_publish.ps1) ONGEWIJZIGD overgenomen uit
rem ArticleSearch v1.4.0.
rem ================================================

rem Basisconfig
set "PROJECT_NAME={app_name}"
set "DISPLAY_NAME={app_name.replace('_', ' ')}"
set "SPEC_FILE={app_name}.spec"
set "DST_FOLDER=dist"
set "LOGFILE=build_log.txt"
set "TIMESTAMP_URL=http://timestamp.sectigo.com"
set "SIGN_CONFIG=%USERPROFILE%\.project_generator\signing_certificate.json"
set "WINPS=C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
rem Optioneel: exacte certificaat-subject om te forceren i.p.v. automatisch
rem beste certificaat (/a). Leeg = automatisch.
set "SIGN_SUBJECT="

rem Vaste AppId (zonder de Inno-escape "{{{{"), gebruikt om in het [Code]-blok
rem te detecteren of er al een eerdere installatie (zelfde app) in het
rem register staat - moet EXACT overeenkomen met de AppId hieronder bij
rem [Setup] (daar WEL met "{{{{" geschreven). Dit is de AL BESTAANDE GUID uit
rem build_project_generator.bat v1.1.0 - NOOIT wijzigen zonder ook alle
rem eerder uitgerolde installaties te vervangen (upgrade-detectie breekt
rem anders).
set "APPGUID={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}"

rem ---- Python uit .venv prefereren ----
set "PYEXE="
if exist ".venv\Scripts\python.exe" set "PYEXE=.venv\Scripts\python.exe"
if not defined PYEXE if exist "Scripts\python.exe" set "PYEXE=Scripts\python.exe"
if not defined PYEXE set "PYEXE=python"

rem Alleen naar absolute path omzetten als het effectief een bestaand bestandspad is
for %%I in ("%PYEXE%") do (
 if exist "%%~fI" set "PYEXE=%%~fI"
)

echo [info] Python: %PYEXE%
"%PYEXE%" -V >nul 2>&1 || (echo [FOUT] Geen werkende Python gevonden.& pause & exit /b 1)

rem ================================================
rem [S0] Signing - optioneel, default N
rem ================================================
set "DO_SIGN=N"
if defined AS_DO_SIGN set "DO_SIGN=%AS_DO_SIGN%"
if defined AS_DO_SIGN echo [sign] Modus via parameter: %AS_DO_SIGN%
if not defined AS_DO_SIGN set /p DO_SIGN=[S0] Binaries signen? [J/N] (standaard N): 
if not defined DO_SIGN set "DO_SIGN=N"

set "SIGNTOOL_EXE="
set "SIGN_THUMBPRINT="
if /I "%DO_SIGN%"=="J" (
 call :LOAD_ACTIVE_CERT
 if errorlevel 1 exit /b 1
 rem GEEN aparte PowerShell Cert:\-preflight meer hier (verwijderd in
 rem 1.3.0) -- die gaf op sommige machines een FormatXmlUpdateException
 rem (zelfs met -ErrorAction SilentlyContinue nog fataal, want dat is
 rem geen gewone non-terminating fout) of "Cannot find drive Cert"
 rem (module-autoloading uitgeschakeld), los van of het certificaat zelf
 rem in orde was. signtool zelf (hieronder, via :SIGN_FILE) valideert het
 rem certificaat al -- bestaat het niet/geen private key/verlopen, dan
 rem faalt signtool met een duidelijke eigen foutmelding, en de
 rem "signtool verify /pa /v" erna is de echte controle. Dit is exact het
 rem patroon van de originele, bewezen build-flow van vóór de centrale
 rem signing-integratie.
 call :FIND_SIGNTOOL
 if not defined SIGNTOOL_EXE (
  echo [FOUT] signtool.exe niet gevonden. Build wordt gestopt.
  exit /b 1
 )
 echo [sign] signtool: %SIGNTOOL_EXE%
 echo [sign] Actieve thumbprint: %SIGN_THUMBPRINT%
)

rem ---- Versie verhogen (scripts\bump_version.py -- NIET root) ----
if defined AS_BUMP_PART (
 set "PART_TO_BUMP=%AS_BUMP_PART%"
 echo [0] Versie-bump via parameter: %AS_BUMP_PART%
) else (
 set /p PART_TO_BUMP=Welke versie wil je verhogen? ^(patch/minor/major^) : 
 if "%PART_TO_BUMP%"=="" set "PART_TO_BUMP=patch"
)
echo [0] Versie verhogen via scripts\bump_version.py (%PART_TO_BUMP%)...
"%PYEXE%" scripts\bump_version.py %PART_TO_BUMP% || (echo [FOUT] Versieverhoging mislukt.& pause & exit /b 1)

rem ---- Versie robuust uitlezen uit app/version.py ----
set "PY_READV=%TEMP%\__read_version_tmp.py"
set "VER_TXT=%TEMP%\__version_out.txt"
del /q "%PY_READV%" "%VER_TXT%" >nul 2>&1
> "%PY_READV%" echo import importlib.util, io, os, re
>>"%PY_READV%" echo p=os.path.abspath('app/version.py'); v="0.0.0"
>>"%PY_READV%" echo try:
>>"%PY_READV%" echo ^ spec=importlib.util.spec_from_file_location("ver",p)
>>"%PY_READV%" echo ^ m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
>>"%PY_READV%" echo ^ v=str(getattr(m,"__version__","0.0.0"))
>>"%PY_READV%" echo except Exception:
>>"%PY_READV%" echo ^ t=io.open(p,'r',encoding='utf-8').read()
>>"%PY_READV%" echo ^ m=re.search(r"__version__\s*=\s*['\^\"\s]*([0-9]+(?:\.[0-9]+){{1,2}})",t)
>>"%PY_READV%" echo ^ v=m.group(1) if m else "0.0.0"
>>"%PY_READV%" echo io.open(r'%VER_TXT%','w',encoding='utf-8').write(v.strip())
"%PYEXE%" "%PY_READV%" || (echo [FOUT] Versie uitlezen faalde.& del /q "%PY_READV%" >nul & pause & exit /b 1)
del /q "%PY_READV%" >nul 2>&1
set "NEW_VERSION=" & set /p NEW_VERSION=<"%VER_TXT%"
del /q "%VER_TXT%" >nul 2>&1
if not defined NEW_VERSION (echo [FOUT] Kon versie niet lezen.& pause & exit /b 1)
echo [1] Versie: %NEW_VERSION%

rem ---- Afgeleide paden ----
set "BUILD_FOLDER=%PROJECT_NAME%_%NEW_VERSION%"
set "ABS_BUILD_FOLDER=%CD%\%DST_FOLDER%\%BUILD_FOLDER%"
set "INITIAL_EXE=%DST_FOLDER%\%PROJECT_NAME%\%PROJECT_NAME%.exe"
set "ISS_FILE=%DST_FOLDER%\installer.iss"

rem  Opschonen
echo [2]  Opruimen...
rmdir /s /q build 2>nul
rmdir /s /q "%DST_FOLDER%" 2>nul
del /q "%LOGFILE%" 2>nul

rem Vereisten
echo [3] Pip ^& vereisten...
"%PYEXE%" -m pip install --upgrade pip >nul
if exist requirements.txt "%PYEXE%" -m pip install -r requirements.txt || (echo [FOUT] pip install -r faalde.& pause & exit /b 1)

rem  PyInstaller aanwezig?
"%PYEXE%" -c "import PyInstaller" >nul 2>&1 || (
 echo [3b] PyInstaller installeren...
 "%PYEXE%" -m pip install "pyinstaller==6.11.1" "pyinstaller-hooks-contrib==2025.0" || (echo [FOUT] Installatie PyInstaller faalde.& pause & exit /b 1)
)

rem Windows VersionInfo-resource genereren (CompanyName/ProductName/
rem FileDescription/FileVersion/ProductVersion in de exe's Eigenschappen >
rem Details) -- ontbrak volledig voorheen, wat mee bijdraagt aan een lagere
rem SmartScreen/Defender-reputatiescore. Parse NEW_VERSION (X.Y.Z) naar een
rem 4-delige tuple; ontbrekende/niet-numerieke delen vallen terug op 0.
echo [3c] Version-info resource genereren...
for /f "tokens=1-3 delims=." %%a in ("%NEW_VERSION%") do (
 set "VMAJOR=%%a"
 set "VMINOR=%%b"
 set "VPATCH=%%c"
)
if not defined VMAJOR set "VMAJOR=0"
if not defined VMINOR set "VMINOR=0"
if not defined VPATCH set "VPATCH=0"

del /q version_info.txt >nul 2>&1
> version_info.txt echo VSVersionInfo(
>>version_info.txt echo ffi=FixedFileInfo(
>>version_info.txt echo filevers=(%VMAJOR%, %VMINOR%, %VPATCH%, 0^),
>>version_info.txt echo prodvers=(%VMAJOR%, %VMINOR%, %VPATCH%, 0^),
>>version_info.txt echo mask=0x3f,
>>version_info.txt echo flags=0x0,
>>version_info.txt echo OS=0x40004,
>>version_info.txt echo fileType=0x1,
>>version_info.txt echo subtype=0x0,
>>version_info.txt echo date=(0, 0^)
>>version_info.txt echo ^),
>>version_info.txt echo kids=[
>>version_info.txt echo StringFileInfo(
>>version_info.txt echo [StringTable(
>>version_info.txt echo u'040904B0',
>>version_info.txt echo [StringStruct(u'CompanyName', u'CGK'^),
>>version_info.txt echo StringStruct(u'FileDescription', u'%DISPLAY_NAME%'^),
>>version_info.txt echo StringStruct(u'FileVersion', u'%NEW_VERSION%'^),
>>version_info.txt echo StringStruct(u'InternalName', u'%PROJECT_NAME%'^),
>>version_info.txt echo StringStruct(u'LegalCopyright', u'\xa9 2026 Barremans - CGK'^),
>>version_info.txt echo StringStruct(u'OriginalFilename', u'%PROJECT_NAME%.exe'^),
>>version_info.txt echo StringStruct(u'ProductName', u'%DISPLAY_NAME%'^),
>>version_info.txt echo StringStruct(u'ProductVersion', u'%NEW_VERSION%'^)])
>>version_info.txt echo ]^),
>>version_info.txt echo VarFileInfo([VarStruct(u'Translation', [1033, 1200]^)])
>>version_info.txt echo ]
>>version_info.txt echo ^)
echo [OK] version_info.txt aangemaakt (FileVersion/ProductVersion = %NEW_VERSION%)

echo --- Build gestart op %DATE% %TIME% --- >> "%LOGFILE%"

rem Build (via SPEC)
echo [4] PyInstaller...
"%PYEXE%" -m PyInstaller --clean --noconfirm "%SPEC_FILE%" || (echo [FOUT] PyInstaller build faalde.& pause & exit /b 1)
if not exist "%INITIAL_EXE%" (echo [FOUT] EXE niet gevonden op "%INITIAL_EXE%".& pause & exit /b 1)

rem Hernoemen naar map met versie
if exist "%DST_FOLDER%\%BUILD_FOLDER%" rmdir /S /Q "%DST_FOLDER%\%BUILD_FOLDER%"
rename "%DST_FOLDER%\%PROJECT_NAME%" "%BUILD_FOLDER%" >nul 2>&1
if errorlevel 1 (
 echo [rename] Fallback via robocopy...
 robocopy "%DST_FOLDER%\%PROJECT_NAME%" "%DST_FOLDER%\%BUILD_FOLDER%" /E /MOVE >nul
 if errorlevel 8 (echo [FOUT] Fallback kopie mislukt.& pause & exit /b 1)
 if exist "%DST_FOLDER%\%PROJECT_NAME%" rmdir /S /Q "%DST_FOLDER%\%PROJECT_NAME%"
)
if not exist "%DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe" (
 echo [FOUT] %PROJECT_NAME%.exe ontbreekt in %DST_FOLDER%\%BUILD_FOLDER%.
 pause & exit /b 1
)

rem Assets kopieren (Project Generator's eigen structuur -- zie
rem changelog hierboven, punt 6: docs/ toegevoegd t.o.v. build_project_
rem generator.bat, dat dit vergat)
echo [5] Assets kopieren...
for %%D in (assets i18n docs) do (
 if exist "%%D" xcopy /E /I /Y "%%D" "%DST_FOLDER%\%BUILD_FOLDER%\%%D" >nul
)
for %%F in (requirements.txt) do (
 if exist "%%F" copy /Y "%%F" "%DST_FOLDER%\%BUILD_FOLDER%\" >nul
)
> "%DST_FOLDER%\%BUILD_FOLDER%\version.txt" echo %NEW_VERSION%

rem [5b] Signen van de BINNEN-EXE (optioneel, certificaatstore)
if /I "%DO_SIGN%"=="J" (
 echo [5b] Signen van %DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe ...
 call :SIGN_FILE "%DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe"
 if errorlevel 1 echo [WAARSCHUWING] Signen van app-EXE faalde - build gaat wel verder ^(ongesigned^).
) else (
 echo [INFO] Signing overgeslagen ^(DO_SIGN=%DO_SIGN%^).
)

rem  Inno Setup?
if defined AS_MAKE_INSTALLER (
 set "MAKE_INSTALLER=%AS_MAKE_INSTALLER%"
 echo [6] Installer via parameter: %AS_MAKE_INSTALLER%
) else (
 set "MAKE_INSTALLER=J"
 set /p MAKE_INSTALLER=Ook Inno Setup installer bouwen? [J/N] : 
)
set "DO_ISCC=1"
if /I "%MAKE_INSTALLER%"=="N" set "DO_ISCC=0"
if "%DO_ISCC%"=="0" goto SHOW_OUTPUT

rem  Inno script genereren
if not exist "%DST_FOLDER%" mkdir "%DST_FOLDER%" >nul 2>&1
del /q "%ISS_FILE%" >nul 2>&1
echo [6b]  Installer-script genereren...

>>"%ISS_FILE%" echo ; --- Inno Setup script, automatisch gegenereerd ---
>>"%ISS_FILE%" echo [Setup]
>>"%ISS_FILE%" echo AppId={{{{%APPGUID:~1,-1%}}
>>"%ISS_FILE%" echo AppName=%DISPLAY_NAME%
>>"%ISS_FILE%" echo AppVersion=%NEW_VERSION%
>>"%ISS_FILE%" echo AppVerName=%DISPLAY_NAME% %NEW_VERSION%
>>"%ISS_FILE%" echo DefaultDirName=C:\%PROJECT_NAME%
>>"%ISS_FILE%" echo DisableDirPage=yes
>>"%ISS_FILE%" echo UsePreviousAppDir=no
>>"%ISS_FILE%" echo DefaultGroupName=%DISPLAY_NAME%
>>"%ISS_FILE%" echo DisableProgramGroupPage=yes
>>"%ISS_FILE%" echo OutputDir=.
>>"%ISS_FILE%" echo OutputBaseFilename=%PROJECT_NAME%Setup_%NEW_VERSION%
>>"%ISS_FILE%" echo Compression=lzma
>>"%ISS_FILE%" echo SolidCompression=yes
>>"%ISS_FILE%" echo Uninstallable=yes
>>"%ISS_FILE%" echo CreateAppDir=yes
>>"%ISS_FILE%" echo PrivilegesRequired=admin
>>"%ISS_FILE%" echo ArchitecturesInstallIn64BitMode=x64
>>"%ISS_FILE%" echo DirExistsWarning=no
>>"%ISS_FILE%" echo WizardStyle=modern
>>"%ISS_FILE%" echo SetupIconFile="%ABS_BUILD_FOLDER%\assets\icons\logo.ico"
rem SignTool: laat Inno zelf setup.exe EN de ingebouwde uninstaller
rem (unins000.exe, die mee in {{app}} terechtkomt) signen tijdens het
rem compileren -- dat laatste bestand werd hiervoor NOOIT gesigned (de
rem oude aanpak signde enkel de buitenste, reeds gecompileerde setup.exe
rem achteraf). "mysigntool" verwijst naar de /Smysigntool=-definitie die
rem hieronder aan ISCC meegegeven wordt (enkel als DO_SIGN=J).
if /I "%DO_SIGN%"=="J" if defined SIGNTOOL_EXE (
 >>"%ISS_FILE%" echo SignTool=mysigntool
)
rem Sluit een draaiende Project_Generator.exe automatisch af voor het
rem kopieren van bestanden (lost gelockte-exe-fouten bij updates op).
rem "force" = geen prompt, ook niet interactief - vereist voor een
rem probleemloze /VERYSILENT-run via Intune. RestartApplications=no: de
rem app bewust NIET automatisch herstarten na install (Intune draait de
rem installer als SYSTEM, niet als de ingelogde gebruiker).
>>"%ISS_FILE%" echo CloseApplicationsFilter=%PROJECT_NAME%.exe
>>"%ISS_FILE%" echo CloseApplications=force
>>"%ISS_FILE%" echo RestartApplications=no
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [InstallDelete]
>>"%ISS_FILE%" echo Type: filesandordirs; Name: "{{app}}\_internal"
>>"%ISS_FILE%" echo Type: filesandordirs; Name: "{{app}}\__pycache__"
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Files]
>>"%ISS_FILE%" echo Source: "%ABS_BUILD_FOLDER%\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Icons]
>>"%ISS_FILE%" echo Name: "{{group}}\%DISPLAY_NAME%"; Filename: "{{app}}\%PROJECT_NAME%.exe"; WorkingDir: "{{app}}"; IconFilename: "{{app}}\assets\icons\logo.ico"
>>"%ISS_FILE%" echo Name: "{{commondesktop}}\%DISPLAY_NAME%"; Filename: "{{app}}\%PROJECT_NAME%.exe"; WorkingDir: "{{app}}"; IconFilename: "{{app}}\assets\icons\logo.ico"; Tasks: desktopicon
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Tasks]
>>"%ISS_FILE%" echo Name: "desktopicon"; Description: "Maak een snelkoppeling op het bureaublad"; GroupDescription: "Extra opties:"
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Run]
>>"%ISS_FILE%" echo Filename: "{{app}}\%PROJECT_NAME%.exe"; WorkingDir: "{{app}}"; Description: "Start %DISPLAY_NAME%"; Flags: nowait postinstall skipifsilent
>>"%ISS_FILE%" echo.
rem Puur cosmetisch - toont "bijwerken naar versie X" i.p.v. de standaard
rem welkomsttekst wanneer een vorige installatie (zelfde AppId) al in het
rem register staat. Werkt ook onder een silent/Intune-run.
>>"%ISS_FILE%" echo [Code]
>>"%ISS_FILE%" echo function IsUpgrade: Boolean;
>>"%ISS_FILE%" echo var sPrevPath: String;
>>"%ISS_FILE%" echo begin
>>"%ISS_FILE%" echo Result := RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\%APPGUID%_is1', 'InstallLocation', sPrevPath);
>>"%ISS_FILE%" echo end;
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo procedure InitializeWizard();
>>"%ISS_FILE%" echo begin
>>"%ISS_FILE%" echo if IsUpgrade then WizardForm.WelcomeLabel2.Caption := 'Dit zal %DISPLAY_NAME% bijwerken naar versie %NEW_VERSION%.' + #13#10#13#10 + 'Klik op Volgende om verder te gaan.';
>>"%ISS_FILE%" echo end;

rem Inno Setup compileren
echo [7] Inno Setup compileren...
set "ISCC_EXE="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC_EXE=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not defined ISCC_EXE if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set "ISCC_EXE=C:\Program Files\Inno Setup 6\ISCC.exe"
if not defined ISCC_EXE (
 echo [WAARSCHUWING] ISCC.exe niet gevonden. Installeer Inno Setup 6.
 goto SHOW_OUTPUT
)

rem [6c] Sign-wrapper voor Inno's SignTool-mechanisme. Een apart .bat-
rem bestand i.p.v. rechtstreeks een /Smysigntool="..."-string opbouwen --
rem dat laatste is bijzonder foutgevoelig in cmd.exe door geneste
rem aanhalingstekens (SIGNTOOL_EXE-pad bevat spaties, bv. "Program Files").
set "ISCC_SIGN_ARG="
if /I "%DO_SIGN%"=="J" if defined SIGNTOOL_EXE (
 echo [6c] Inno sign-wrapper aanmaken...
 > "%DST_FOLDER%\innosign.bat" echo @echo off
 if defined SIGN_SUBJECT (
 >>"%DST_FOLDER%\innosign.bat" echo "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" %%1
 ) else (
 >>"%DST_FOLDER%\innosign.bat" echo "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" %%1
 )
 rem GEEN "set "VAR=...""-vorm hier -- die paart aanhalingstekens en
 rem breekt zodra de waarde zelf al eigen quotes bevat. Platte "set
 rem VAR=..." zonder omsluitende quotes om het hele commando neemt de
 rem rest van de regel letterlijk over, quotes inbegrepen, en levert zo
 rem exact de syntax die Inno's ISCC /S-naam="commando"-parameter
 rem verwacht. innosign.bat-pad wordt bewust NIET apart gequote: dat pad
 rem bevat per CGK-conventie C:\PY\AppNaam\... geen spaties.
 set ISCC_SIGN_ARG=/Smysigntool="%CD%\%DST_FOLDER%\innosign.bat $f"
)

if defined ISCC_SIGN_ARG (
 "%ISCC_EXE%" %ISCC_SIGN_ARG% "%ISS_FILE%"
) else (
 "%ISCC_EXE%" "%ISS_FILE%"
)
if errorlevel 1 (
 echo [FOUT] Inno Setup compile mislukt. Bekijk "%ISS_FILE%".
 goto SHOW_OUTPUT
)
echo [OK] Installer aangemaakt: %DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe
if defined ISCC_SIGN_ARG echo [OK] setup.exe + unins000.exe zijn tijdens compilatie gesigned door Inno's SignTool-mechanisme.

rem [7b] Verificatie van de installer-signature (setup.exe zelf, niet de
rem embedded uninstaller -- die zit pas in {{app}} na een effectieve install
rem en is dus nu niet apart te verifieren).
if /I "%DO_SIGN%"=="J" (
 if exist "%DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe" (
 echo [7b] Handtekening installer verifieren...
 call :SIGN_FILE "%DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe" --verify-only
 )
) else (
 echo [INFO] Installer-signing overgeslagen ^(DO_SIGN=%DO_SIGN%^).
)

:SHOW_OUTPUT
echo.
echo Output-map: %DST_FOLDER%\%BUILD_FOLDER%
echo Testen: "%DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe"
echo Installer (indien gebouwd): %DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe
echo Signing: %DO_SIGN%
if not defined AS_BUMP_PART pause
endlocal
exit /b 0

rem ================================================
:LOAD_ACTIVE_CERT
if not exist "%SIGN_CONFIG%" (
 echo [FOUT] Centrale signingconfig niet gevonden: %SIGN_CONFIG%
 exit /b 1
)
set "SIGN_THUMB_FILE=%TEMP%\__cgk_active_thumbprint.txt"
del /q "%SIGN_THUMB_FILE%" >nul 2>&1
"%WINPS%" -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $d=Get-Content -LiteralPath $env:SIGN_CONFIG -Raw | ConvertFrom-Json; $t=$d.thumbprint; if(-not $t){{$t=$d.Thumbprint}}; if(-not $t){{throw 'Geen thumbprint in signingconfig'}}; ($t -replace ' ','').ToUpperInvariant() | Set-Content -LiteralPath $env:SIGN_THUMB_FILE -Encoding ASCII"
if errorlevel 1 (
 echo [FOUT] Actieve thumbprint kon niet worden gelezen.
 exit /b 1
)
set /p SIGN_THUMBPRINT=<"%SIGN_THUMB_FILE%"
del /q "%SIGN_THUMB_FILE%" >nul 2>&1
if not defined SIGN_THUMBPRINT (
 echo [FOUT] Geen actieve thumbprint gevonden.
 exit /b 1
)
exit /b 0

rem ================================================
rem :PREFLIGHT_CERT is bewust VERWIJDERD (1.3.0) -- deze PowerShell
rem Cert:\-validatie (Get-ChildItem Cert:\CurrentUser\My/Root/
rem TrustedPublisher, HasPrivateKey/NotAfter-checks) bleek op de
rem doelmachine op 3 verschillende manieren te falen zonder dat er iets
rem mis was met het certificaat zelf:
rem   1) "Import-Module ... -ErrorAction Stop" -> FormatXmlUpdateException
rem      (dubbele ObjectSecurity-type-data, cosmetisch).
rem   2) Geen Import-Module -> "Cannot find drive Cert" (impliciet
rem      module-autoloaden staat hier uit).
rem   3) "Import-Module ... -ErrorAction SilentlyContinue" -> zelfde
rem      FormatXmlUpdateException als (1): dit is geen gewone
rem      non-terminating fout, dus -ErrorAction onderdrukt hem niet.
rem signtool zelf heeft de PowerShell Cert:-drive niet nodig (gebruikt de
rem Windows Crypto API rechtstreeks) en valideert het certificaat al bij
rem het effectieve signen (:SIGN_FILE hieronder), gevolgd door
rem "signtool verify /pa /v" als de echte controle. Dit is exact hoe de
rem originele, bewezen build-flow van vóór de centrale signing-integratie
rem al werkte -- geen aparte preflight nodig.
rem ================================================
:FIND_SIGNTOOL
set "SIGNTOOL_EXE="
if exist "C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe" (
 set "SIGNTOOL_EXE=C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe"
 goto :eof
)
if exist "C:\Program Files (x86)\Windows Kits\10\App Certification Kit\signtool.exe" (
 set "SIGNTOOL_EXE=C:\Program Files (x86)\Windows Kits\10\App Certification Kit\signtool.exe"
 goto :eof
)
if exist "C:\Program Files\Windows Kits\10\bin\x64\signtool.exe" (
 set "SIGNTOOL_EXE=C:\Program Files\Windows Kits\10\bin\x64\signtool.exe"
 goto :eof
)
for /f "delims=" %%S in ('where signtool.exe 2^>nul') do (
 set "SIGNTOOL_EXE=%%S"
 goto :eof
)
goto :eof

rem ================================================
:SIGN_FILE
if not exist "%~1" echo [FOUT] Bestand niet gevonden: %~1
if not exist "%~1" exit /b 1
if not defined SIGNTOOL_EXE (
 echo [FOUT] signtool niet geconfigureerd.
 exit /b 1
)
if /I "%~2"=="--verify-only" goto SIGN_FILE_VERIFY
echo [sign] Bestand: %~1
if defined SIGN_SUBJECT (
 "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" "%~1"
) else (
 "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" "%~1"
)
if errorlevel 1 echo [FOUT] signtool mislukt voor: %~1
if errorlevel 1 exit /b 1
echo [OK] Gesigned: %~1

:SIGN_FILE_VERIFY
rem [verify] BELANGRIJK: "gesigned" wil NIET zeggen "vertrouwd door Windows
rem Defender/SmartScreen/Controlled Folder Access". Die vereisen een keten
rem naar een PUBLIEK vertrouwde CA-root (DigiCert/Sectigo/GlobalSign/...).
rem Een zelfondertekend of intern CGK-certificaat signeert prima (integriteit
rem OK) maar wordt door Defender op ANDERE machines nog steeds als onbekend/
rem onvertrouwd behandeld -- dat is vermoedelijk de kern van de "Kan geen
rem toegang krijgen tot het opgegeven apparaat, pad of bestand"-fout op
rem Intune-beheerde toestellen met Controlled Folder Access aan.
rem
rem /pa = gebruik de "Default Authenticode"-verificatiepolicy (dezelfde
rem policy die Windows zelf hanteert) i.p.v. Microsoft's eigen, striktere
rem WHQL-policy -- /pa is de juiste keuze voor gewone code-signing-checks.
echo [verify] Handtekening controleren...
"%SIGNTOOL_EXE%" verify /pa /v "%~1" > "%TEMP%\__signverify.txt" 2>&1
set "VERIFY_RC=%ERRORLEVEL%"
type "%TEMP%\__signverify.txt"
findstr /C:"Issued to" "%TEMP%\__signverify.txt"
del /q "%TEMP%\__signverify.txt" >nul 2>&1

if not "%VERIFY_RC%"=="0" (
 echo.
 echo [WAARSCHUWING] Handtekening-verificatie MISLUKT ^(exitcode %VERIFY_RC%^) voor: %~1
 echo [WAARSCHUWING] Dit bestand wordt zeer waarschijnlijk geblokkeerd door
 echo Windows Defender SmartScreen / Controlled Folder Access /
 echo Attack Surface Reduction op Intune-beheerde toestellen,
 echo ook al is het technisch wel "gesigned".
 echo [ACTIE NODIG] Vraag IT/Security om ofwel:
 echo 1^) een certificaat van een publiek vertrouwde CA te
 echo gebruiken ^(niet zelfondertekend/intern^), OF
 echo 2^) dit bestand ^(of het certificaat-thumbprint^)
 echo expliciet toe te voegen aan de "Controlled Folder
 echo Access allowed apps"-lijst via Intune Endpoint
 echo Security / Attack Surface Reduction-beleid, OF
 echo 3^) de app te verpakken als Intune Win32-app
 echo ^(.intunewin^) i.p.v. de installer los te draaien.
 echo.
 exit /b 1
)
echo [OK] Handtekening geverifieerd ^(vertrouwd volgens Windows' eigen policy^).
exit /b 0"""

def get_build_and_publish_ps1_template(app_name: str) -> str:
    """Template voor build_and_publish.ps1."""
    return f'''# build_and_publish.ps1 - {app_name}
# Vraagt alle build-parameters vooraf, voert build_installer.bat niet-
# interactief uit (via AS_*-env vars -- moet EXACT overeenkomen met de
# env vars die build_installer.bat leest: AS_BUMP_PART/AS_MAKE_INSTALLER/
# AS_DO_SIGN, zelfde patroon als Project Generator/ArticleSearch), en
# publiceert daarna optioneel via publish.ps1 naar GitHub.
# Run vanuit de repo root: .\\build_and_publish.ps1

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$buildBat  = Join-Path $Root "build_installer.bat"
$publishPs = Join-Path $Root "publish.ps1"

if (-not (Test-Path $buildBat))  {{ throw "Niet gevonden: $buildBat" }}
if (-not (Test-Path $publishPs)) {{ throw "Niet gevonden: $publishPs" }}

Write-Host ""
Write-Host "============================================================"
Write-Host "  {app_name} - Build + Publish"
Write-Host "============================================================"
Write-Host ""

# Altijd een expliciete keuze afdwingen (nooit leeg) -- build_installer.bat
# valt anders terug op een interactieve "set /p"-prompt, die bij een
# niet-interactieve aanroep vanuit dit script blijft hangen.
$bumpPart = ""
while ($bumpPart -notin @("patch", "minor", "major")) {{
    $bumpPart = Read-Host "Versie verhogen? [patch/minor/major] (Enter = patch)"
    if ($bumpPart -eq "") {{ $bumpPart = "patch" }}
}}

$makeInstaller = ""
while ($makeInstaller -notin @("J", "N", "j", "n")) {{
    $makeInstaller = Read-Host "Inno Setup installer bouwen? [J/N] (Enter = J)"
    if ($makeInstaller -eq "") {{ $makeInstaller = "J" }}
}}
$makeInstaller = $makeInstaller.ToUpper()

$doSign = ""
while ($doSign -notin @("J", "N", "j", "n")) {{
    $doSign = Read-Host "Binaries signen (certificaatstore)? [J/N] (Enter = N)"
    if ($doSign -eq "") {{ $doSign = "N" }}
}}
$doSign = $doSign.ToUpper()

$doPublish = ""
while ($doPublish -notin @("J", "N", "j", "n")) {{
    $doPublish = Read-Host "Publiceren naar GitHub na build? [J/N] (Enter = N)"
    if ($doPublish -eq "") {{ $doPublish = "N" }}
}}
$doPublish = $doPublish.ToUpper()

Write-Host ""
Write-Host "------------------------------------------------------------"
Write-Host "  Samenvatting:"
Write-Host "    Versie-bump : $bumpPart"
Write-Host "    Installer   : $makeInstaller"
Write-Host "    Signing     : $doSign"
Write-Host "    Publiceren  : $doPublish"
Write-Host "------------------------------------------------------------"
$bevestig = Read-Host "Starten? [J/N]"
if ($bevestig.ToUpper() -ne "J") {{
    Write-Host "Afgebroken."
    exit 0
}}

Write-Host ""
Write-Host "[STEP 1/2] Build starten..."

$wrapperPath = Join-Path $Root "_build_wrapper.bat"
$wrapperContent = "@echo off`r`n"
$wrapperContent += "set AS_BUMP_PART=$bumpPart`r`n"
$wrapperContent += "set AS_MAKE_INSTALLER=$makeInstaller`r`n"
$wrapperContent += "set AS_DO_SIGN=$doSign`r`n"
$wrapperContent += "call `"$buildBat`"`r`n"
$wrapperContent += "exit /b %ERRORLEVEL%`r`n"
[System.IO.File]::WriteAllText($wrapperPath, $wrapperContent, [System.Text.Encoding]::ASCII)

& cmd.exe /c "`"$wrapperPath`""
$buildExitCode = $LASTEXITCODE

Remove-Item $wrapperPath -ErrorAction SilentlyContinue
Remove-Item Env:\\AS_BUMP_PART      -ErrorAction SilentlyContinue
Remove-Item Env:\\AS_MAKE_INSTALLER -ErrorAction SilentlyContinue
Remove-Item Env:\\AS_DO_SIGN        -ErrorAction SilentlyContinue

if ($buildExitCode -ne 0) {{
    throw "Build faalde (exitcode $buildExitCode). Zie output hierboven."
}}

Write-Host "[STEP 1/2] Build geslaagd."

if ($doPublish -eq "J") {{
    if ($makeInstaller -ne "J") {{
        Write-Host "[WARN] Installer niet gebouwd - publiceren overgeslagen."
    }} else {{
        Write-Host ""
        Write-Host "[STEP 2/2] Publiceren via publish.ps1..."
        & powershell -ExecutionPolicy Bypass -File $publishPs
        if ($LASTEXITCODE -ne 0) {{ throw "Publish faalde (exitcode $LASTEXITCODE)." }}
        Write-Host "[STEP 2/2] Publiceren geslaagd."
    }}
}} else {{
    Write-Host "[STEP 2/2] Publiceren overgeslagen (keuze gebruiker)."
}}

Write-Host ""
Write-Host "============================================================"
Write-Host "[DONE] Build + Publish afgerond."
Write-Host "============================================================"
'''


def get_publish_ps1_template(app_name: str) -> str:
    """Template voor publish.ps1."""
    repo_guess = app_name.lower().replace(" ", "-").replace("_", "-")

    return f'''# publish.ps1 - {app_name} (release + asset + version.txt)
# Run vanuit de repo root: .\\publish.ps1
# Vereist: gh (ingelogd) + git
#
# LET OP: -Owner/-Repo hieronder zijn PLACEHOLDERS. Pas deze aan naar je
# eigen GitHub-organisatie/gebruiker en repository-naam vóór je dit
# script effectief gebruikt, of geef ze mee als parameter:
#   .\\publish.ps1 -Owner "jouw-github-naam" -Repo "{repo_guess}"

param(
    [string]$Owner = "TODO-github-owner",
    [string]$Repo = "{repo_guess}"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if ($Owner -eq "TODO-github-owner") {{
    throw "Vul eerst -Owner in (of pas de default in publish.ps1 aan) vóór je publiceert."
}}

# 1) Versie lezen uit app/version.py
$versionPy = Join-Path $Root "app/version.py"
if (-not (Test-Path $versionPy)) {{ throw "Niet gevonden: $versionPy" }}

$txt = Get-Content $versionPy -Raw
$m = [regex]::Match($txt, '__version__\\s*=\\s*["''](?<v>\\d+\\.\\d+\\.\\d+)["'']')
if (-not $m.Success) {{ throw "Kon __version__ niet vinden in app/version.py" }}
$version = $m.Groups["v"].Value

$tag = "v$version"
$assetName = "{app_name}Setup_$version.exe"
$assetPath = Join-Path $Root ("dist\\" + $assetName)

Write-Host "[INFO] Repo: $Owner/$Repo"
Write-Host "[INFO] Versie: $version"
Write-Host "[INFO] Tag: $tag"
Write-Host "[INFO] Asset: $assetPath"

if (-not (Test-Path $assetPath)) {{
    throw "Installer niet gevonden: $assetPath`nRun eerst build_installer.bat (of build_and_publish.ps1) en maak de installer."
}}

$releaseExists = $false
try {{
    & gh release view $tag --repo "$Owner/$Repo" *> $null
    if ($LASTEXITCODE -eq 0) {{ $releaseExists = $true }}
}}
catch {{
    $releaseExists = $false
}}

if (-not $releaseExists) {{
    Write-Host "[INFO] Release $tag bestaat nog niet. Maken..."
    & gh release create $tag --repo "$Owner/$Repo" --title "$tag" --notes "Release $tag"
    if ($LASTEXITCODE -ne 0) {{ throw "Aanmaken release $tag mislukt." }}
}} else {{
    Write-Host "[INFO] Release $tag bestaat al."
}}

Write-Host "[INFO] Uploaden asset..."
& gh release upload $tag "$assetPath" --repo "$Owner/$Repo" --clobber
if ($LASTEXITCODE -ne 0) {{ throw "Upload asset mislukt." }}

$downloadUrl = "https://github.com/$Owner/$Repo/releases/download/$tag/$assetName"
Write-Host "[OK] Download URL: $downloadUrl"

# version.txt (2 regels) - dit is het bestand dat een updater.py-achtig
# mechanisme rechtstreeks als raw-bestand zou ophalen, analoog ArticleSearch.
$versionTxt = Join-Path $Root "releases\\latest\\version.txt"
$versionDir = Split-Path -Parent $versionTxt
if (-not (Test-Path $versionDir)) {{ New-Item -ItemType Directory -Path $versionDir -Force | Out-Null }}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($versionTxt, "$version`n$downloadUrl", $utf8NoBom)

& git add "app/version.py" "releases/latest/version.txt"
& git commit -m "Release $version - sync version.py and version.txt" *> $null
& git push
if ($LASTEXITCODE -ne 0) {{
    throw "git push MISLUKT (exitcode $LASTEXITCODE). De GitHub Release en de installer-asset staan wel al online (via 'gh', los van git push), maar app/version.py/releases/latest/version.txt zijn enkel LOKAAL gecommit. Los het pushprobleem op (bv. eerst 'git pull --rebase origin main') en run dan handmatig: git push"
}}
Write-Host "[OK] version.py/version.txt succesvol gepusht naar $Owner/$Repo."

Write-Host ""
Write-Host "============================================================"
Write-Host "[DONE] Published $tag"
Write-Host "Release: https://github.com/$Owner/$Repo/releases/tag/$tag"
Write-Host "============================================================"
'''


# ==== UPDATE create_standard_project_template ====

def create_standard_project_template(name: str, version: str, author: str, 
                                     description: str = "", create_venv: bool = False,
                                     root_path: Path = None) -> ProjectTemplate:
    """
    Creëer de standaard projectstructuur volgens moderne Python best practices.
    
    Args:
        name: Applicatie naam
        version: Versie nummer
        author: Auteur naam
        description: Optionele beschrijving
        create_venv: Of virtuele omgeving moet worden aangemaakt
        root_path: Root pad waar project wordt aangemaakt
    """
    project = ProjectTemplate(
        name=name,
        version=version,
        author=author,
        description=description,
        create_venv=create_venv
    )
    
    # .vscode folder
    vscode_folder = FolderTemplate(name=".vscode")
    vscode_folder.add_file(
        "launch.json",
        "VS Code debug configuratie",
        get_launch_json_template(name)
    )
    vscode_folder.add_file(
        "settings.json",
        "VS Code Python settings",
        get_settings_json_template()
    )
    
    # app folder (Python package)
    app_folder = FolderTemplate(name="app", python_package=True)
    app_folder.add_file("main.py", "Hoofdapplicatie", get_main_py_template())
    app_folder.add_file("version.py", "Versie informatie", get_version_py_template(version))
    
    # core folder (Python package) - kernlogica / gedeelde functionaliteit,
    # los van app/ (naar CGK-conventie: app/core/, zie 01-app-structuur-template.md)
    core_folder = FolderTemplate(name="core", python_package=True)
    
    # config folder
    config_folder = FolderTemplate(name="config")
    config_folder.add_file("settings.json", "Applicatie configuratie", get_settings_config_template())
    
    # assets folder met icons subfolder
    assets_folder = FolderTemplate(name="assets")
    icons_subfolder = FolderTemplate(name="icons")
    assets_folder.add_subfolder(icons_subfolder)
    
    # css folder met QSS templates
    css_folder = FolderTemplate(name="css")
    css_folder.add_file("main.qss", "Hoofd stylesheet", get_main_qss_template())
    css_folder.add_file("detail.qss", "Detail window stylesheet", get_detail_qss_template())
    
    # data folder
    data_folder = FolderTemplate(name="data")
    data_folder.add_file(".gitkeep", "Bewaar deze map in git", get_gitkeep_template())
    
    # docs folder
    docs_folder = FolderTemplate(name="docs")
    docs_folder.add_file("changelog.md", "Versiegeschiedenis", get_changelog_template(version))
    
    # helpers folder (Python package)
    helpers_folder = FolderTemplate(name="helpers", python_package=True)
    
    # utils folder (Python package)
    utils_folder = FolderTemplate(name="utils", python_package=True)
    
    # ui folder (Python package) - GUI-schermen (naar ArticleSearch-conventie:
    # ui_*.py-bestanden)
    ui_folder = FolderTemplate(name="ui", python_package=True)
    
    # dialogs folder (Python package) - modale QDialog-vensters (naar
    # ArticleSearch-conventie: *_dialog.py-bestanden)
    dialogs_folder = FolderTemplate(name="dialogs", python_package=True)
    
    # token folder (Python package) - per-domein token/auth-gerelateerde
    # modules (naar ArticleSearch-conventie: *_token.py-bestanden)
    token_folder = FolderTemplate(name="token", python_package=True)
    
    # md folder
    md_folder = FolderTemplate(name="md")
    md_folder.add_file("help.md", "Help documentatie", get_help_md_template(name))
    
    # tests folder (Python package)
    tests_folder = FolderTemplate(name="tests", python_package=True)
    
    # scripts folder met utility scripts
    scripts_folder = FolderTemplate(name="scripts")
    scripts_folder.add_file("README.md", "Scripts documentatie", get_scripts_readme_template())
    scripts_folder.add_file("update_toml.py", "Update pyproject.toml", get_update_toml_script())
    scripts_folder.add_file("bump_version.py", "Verhoog versie", get_bump_version_script())
    scripts_folder.add_file("generate_requirements.py", "Genereer requirements.txt", get_generate_requirements_script())
    scripts_folder.add_file("validate_project.py", "Valideer project", get_validate_project_script())
    
    # i18n folder (Python package) met locales
    i18n_folder = FolderTemplate(name="i18n", python_package=True)
    i18n_folder.add_file("__init__.py", "Package initialisatie voor i18n", get_i18n_init_template())
    i18n_folder.add_file("translator.py", "Translation helper", get_translator_py_template())
    i18n_folder.add_file("README.md", "i18n documentatie", get_i18n_readme_template())
    
    # locales subfolder
    locales_folder = FolderTemplate(name="locales")
    locales_folder.add_file("nl_NL.json", "Nederlandse vertalingen", get_locale_nl_nl_template())
    locales_folder.add_file("en_US.json", "English translations", get_locale_en_us_template())
    locales_folder.add_file("fr_FR.json", "Traductions françaises", get_locale_fr_fr_template())
    locales_folder.add_file("de_DE.json", "Deutsche Übersetzungen", get_locale_de_de_template())
    locales_folder.add_file("es_ES.json", "Traducciones españolas", get_locale_es_es_template())
    i18n_folder.add_subfolder(locales_folder)
    
    # Voeg alle folders toe
    project.add_folder(vscode_folder)
    project.add_folder(app_folder)
    project.add_folder(core_folder)  # ← core TOEGEVOEGD
    project.add_folder(config_folder)
    project.add_folder(assets_folder)
    project.add_folder(css_folder)
    project.add_folder(data_folder)
    project.add_folder(docs_folder)
    project.add_folder(helpers_folder)
    project.add_folder(utils_folder)
    project.add_folder(ui_folder)
    project.add_folder(dialogs_folder)
    project.add_folder(token_folder)
    project.add_folder(md_folder)
    project.add_folder(scripts_folder)
    project.add_folder(i18n_folder)  # ← i18n TOEGEVOEGD
    project.add_folder(tests_folder)
    
    # Root files - Basis bestanden
    project.add_file("README.md", "Project documentatie", 
                     get_readme_template(name, version, author, description))
    project.add_file("requirements.txt", "Python dependencies", 
                     get_requirements_txt_template())
    project.add_file(".gitignore", "Git ignore regels", 
                     get_gitignore_template())
    
    # Root files - Modern Python packaging (PEP 517/518/621)
    project.add_file("pyproject.toml", "Project configuratie (PEP 621)", 
                     get_pyproject_toml_template(name, version, author, description))
    project.add_file("setup.py", "Setup script (backwards compatibility)", 
                     get_setup_py_template(name, version, author, description))
    project.add_file("MANIFEST.in", "Package manifest", 
                     get_manifest_in_template())
    
    # Root files - Documentatie en licentie
    project.add_file("LICENSE", "MIT License", 
                     get_license_template(author))
    project.add_file("CONTRIBUTING.md", "Contributie richtlijnen", 
                     get_contributing_template(name))
    
    # Root files - Development tools
    project.add_file("Makefile", "Development shortcuts", 
                     get_makefile_template(name))
    
    # Root files - Build & release (naar ArticleSearch-patroon)
    project.add_file("build_installer.bat", "PyInstaller build + Inno Setup installer generator",
                     get_build_installer_bat_template(name))
    project.add_file("build_and_publish.ps1", "Build + publish orchestrator",
                     get_build_and_publish_ps1_template(name))
    project.add_file("publish.ps1", "GitHub release publiceren (asset + version.txt)",
                     get_publish_ps1_template(name))
    
    return project