"""
core/default_templates.py

Beschrijving: Standaard project templates
Applicatie: Project Generator
Versie: 1.0.5
Auteur: Barremans
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
    python_path = "${workspaceFolder}/venv/Scripts/python.exe"
    
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
    python_path = "${workspaceFolder}/venv/Scripts/python.exe"
    
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
    
    return f'''"""
setup.py

Beschrijving: Package setup (backwards compatibility)
Applicatie: {app_name}
Versie: {version}
Auteur: {author}

Note: Dit bestand is voor backwards compatibility.
De primaire configuratie staat in pyproject.toml
"""

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
    return '''"""
scripts/update_toml.py

Beschrijving: Update pyproject.toml automatisch
Versie: 1.0.5
"""

import argparse
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
    return r'''"""
scripts/bump_version.py

Beschrijving: Verhoog versienummer overal in het project
Versie: 1.0.5
"""

import argparse
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
    
    response = input(f"Doorgaan met update naar {new_version}? (y/n): ")
    if response.lower() != "y":
        print("❌ Geannuleerd")
        sys.exit(0)
    
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
    return '''"""
scripts/generate_requirements.py

Beschrijving: Genereer requirements.txt uit pyproject.toml
Versie: 1.0.5
"""

import argparse
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
    return '''"""
scripts/validate_project.py

Beschrijving: Valideer project structuur en configuratie
Versie: 1.0.5
"""

import sys
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
    return '''"""
i18n/translator.py

Beschrijving: Translation helper voor meertalige applicaties
Versie: 1.0.5
"""

import json
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
    return '''"""
i18n/__init__.py

Beschrijving: Internationalization (i18n) package
Versie: 1.0.5
"""

from i18n.translator import Translator, get_translator, t

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
    project.add_folder(config_folder)
    project.add_folder(assets_folder)
    project.add_folder(css_folder)
    project.add_folder(data_folder)
    project.add_folder(docs_folder)
    project.add_folder(helpers_folder)
    project.add_folder(utils_folder)
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
    
    return project