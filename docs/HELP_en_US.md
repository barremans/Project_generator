# Python Project Generator - Help

**Version:** 1.2.0  
**Author:** Barremans

## 📚 Table of Contents

1. [Overview](#overview)
2. [Basic Usage](#basic-usage)
3. [Settings](#settings)
4. [Tools: Headers \& Structure](#tools-headers--structure)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Project Structure](#project-structure)
7. [Development Workflow](#development-workflow)
8. [Modern Python Packaging](#modern-python-packaging)
9. [Scripts System](#scripts-system)
10. [Internationalization (i18n)](#internationalization-i18n)
11. [FAQ](#faq)

---

## 🎯 Overview

The **Python Project Generator** is a tool that automatically creates a complete, professional Python project structure following modern best practices.

### What you get

✅ **Complete folder structure** (10+ folders)  
✅ **Standard files** with proper headers  
✅ **Modern Python packaging** (PEP 621 - pyproject.toml)  
✅ **VS Code configuration** (.vscode/)  
✅ **Virtual environment** (optional)  
✅ **PyInstaller template** (.spec file)  
✅ **Export scripts** (export_to_usb.bat)  
✅ **i18n support** (5 languages)  
✅ **Development tools** (Black, Flake8, MyPy, pytest)  
✅ **QSS stylesheets** for Qt applications

---

## 🚀 Basic Usage

### Step 1: Project Location
1. Click **"Browse..."**
2. Select a folder where the project should be created
3. Enter an **application name** (e.g., "MyAwesomeApp")

### Step 2: Project Information
- **Author:** Your name (saved for future projects)
- **Version:** Default 1.0.0 (SemVer)
- **Description:** Optional description

### Step 3: Options
- **Virtual environment:** Automatically creates a venv and installs pip

### Step 4: Summary
- Review all settings
- Click **"🚀 Generate Project"**

### Step 5: Done!
- **📁 Open Project Folder** - Open in Windows Explorer
- **💻 Open in Editor** - Open in VS Code (or other editor)
- **🆕 New Project** - Restart wizard

---

## ⚙️ Settings

Via **Menu → File → Settings** you can configure:

### Default Values
- **Default Author:** Automatically filled in for new projects
- **Default Project Folder:** Start location for browser dialog

### Editor Settings
- **Editor Path:** Command or path to editor
  - VS Code: `code`
  - Notepad++: `notepad++`
  - Full path: `C:\Program Files\Editor\editor.exe`

### Language
- **Nederlands** (nl_NL)
- **English** (en_US)

Settings are saved in: `C:\Users\[USERNAME]\.project_generator\settings.json`

---

## ⌨️ Keyboard Shortcuts

### Wizard Navigation
- **Enter** - Next step
- **Shift+Tab** - Previous step

### Menu Shortcuts
- **Ctrl+N** - New Project
- **Ctrl+,** - Settings
- **Ctrl+Q** - Exit
- **F1** - Help

---

## 🛠️ Tools: Headers & Structure

Via **Menu → Tools → Headers & Structure...** you open a separate window
with two tools, ported from the former standalone project-doc-tool
project (which has thereby been fully absorbed into Project Generator):

### How it works
1. Click **📂 Choose project folder** — the folder you want to
   analyse/document (doesn't have to be a freshly generated project — any
   existing Python project folder works).
2. Click **📂 Choose output folder** — where `PROJECT_STRUCTURE.md` will be
   written. Automatically follows `<project folder>/docs` whenever you pick
   a new project folder, but stays on your own choice afterwards.
3. Three actions:
   - **▶ Dry-run headers**: shows per file whether it has a correct
     header, no header, or an incorrect header — changes nothing.
   - **✍ Add headers**: actually adds/fixes headers, in Project
     Generator's own header format.
   - **📑 Generate project structure**: writes `PROJECT_STRUCTURE.md` (a
     tree overview with per supported file the header metadata as a
     fenced code block) and then automatically opens the output folder.

Every **newly generated** project already gets this file automatically in
`docs/` upon creation (see [Project Structure](#project-structure)) — the
Tools dialog is mainly for existing/external projects, or to regenerate it
after later changes.

### Settings (Tools)
Via the **"⚙ Settings"** button in the Tools dialog (separate from the main
Settings above):
- **Include extensions**: which file types are scanned (default `.py`,
  `.txt`, `.ini`, `.yaml`, `.yml`)
- **Exclude folders**: folders skipped entirely (default includes `.git`,
  `.venv`, `__pycache__`, `build`, `dist`, `.vscode`)
- **Exclude files**: filenames that are skipped
- **Application**: fixed value for the "Applicatie:" line, or leave empty
  to automatically use the folder name
- **Default version**: fallback version for files without a header

The author name for headers is **not** a separate field here — it's the
same "Default Author" as in the main Settings.

### Standalone (no GUI)
The same functionality can also be run separately:
```bash
cd scripts
python generate_project_structure.py --project-root "C:\PY\MyApp"
python add_headers.py --project-root "C:\PY\MyApp"            # dry-run
python add_headers.py --project-root "C:\PY\MyApp" --apply    # actual changes
```

---

## 📁 Project Structure
```
MyProject/
├── pyproject.toml          # Modern Python packaging (PEP 621)
├── setup.py                # Backwards compatibility
├── MANIFEST.in             # Package manifest
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # Development guide
├── Makefile                # Development shortcuts
├── README.md
├── requirements.txt
├── .gitignore
├── .vscode/                # VS Code configuration
│   ├── launch.json
│   └── settings.json
├── app/                    # Main application
│   ├── __init__.py
│   ├── main.py
│   └── version.py
├── core/                   # Core logic / shared functionality (Python package)
│   └── __init__.py
├── assets/                 # Icons and images
│   └── icons/
├── config/                 # Configuration files
│   └── settings.json
├── css/                    # QSS stylesheets
│   ├── main.qss
│   └── detail.qss
├── data/                   # Data storage
├── docs/                   # Documentation
│   └── changelog.md
│   (PROJECT_STRUCTURE.md is generated here automatically after generation)
├── helpers/                # Helper functions
├── i18n/                   # Internationalization
│   ├── translator.py
│   └── locales/
│       ├── nl_NL.json
│       ├── en_US.json
│       ├── fr_FR.json
│       ├── de_DE.json
│       └── es_ES.json
├── md/                     # Markdown files
│   └── help.md
├── scripts/                # Utility scripts
│   ├── update_toml.py
│   ├── bump_version.py
│   ├── generate_requirements.py
│   └── validate_project.py
├── utils/                  # Utilities
├── tests/                  # Unit tests
├── venv/                   # Virtual environment (optional)
├── export_to_usb.bat       # Export script
└── MyProject.spec          # PyInstaller template
```

---

## 🛠️ Development Workflow

### Initial setup
```bash
cd MyProject
venv\Scripts\activate
pip install -e ".[dev]"
```

### Daily use
```bash
# Format code
make format

# Check code style
make lint

# Run tests
make test
```

### Version bump
```bash
cd scripts
python bump_version.py minor  # 1.0.0 → 1.1.0
```

---

## 📦 Modern Python Packaging

### pyproject.toml
Central configuration following **PEP 621**:
- Project metadata
- Dependencies
- Build system
- Tool configuration (Black, pytest, MyPy)

### Adding dependencies
```bash
cd scripts
python update_toml.py --add-dep "requests>=2.31.0"
pip install requests
```

### Dev dependencies
```bash
pip install -e ".[dev]"
```

---

## 🔧 Scripts System

### update_toml.py
Update pyproject.toml automatically:
```bash
python update_toml.py --add-dep "package>=version"
python update_toml.py --set-version "1.0.1"
```

### bump_version.py
Bump version everywhere:
```bash
python bump_version.py patch   # 1.0.0 → 1.0.1
python bump_version.py minor   # 1.0.0 → 1.1.0
python bump_version.py major   # 1.0.0 → 2.0.0
```

### generate_requirements.py
Generate requirements.txt:
```bash
python generate_requirements.py --dev
```

### validate_project.py
Validate project:
```bash
python validate_project.py
```

---

## 🌍 Internationalization (i18n)

Each generated project has multilingual support:

### Usage
```python
from i18n import t

# Simple translation
print(t("app.welcome"))

# With variables
print(t("app.greeting", name="John"))
```

### Available languages
- 🇳🇱 Nederlands (nl_NL)
- 🇺🇸 English (en_US)
- 🇫🇷 Français (fr_FR)
- 🇩🇪 Deutsch (de_DE)
- 🇪🇸 Español (es_ES)

See `i18n/README.md` in the generated project for details.

---

## ❓ FAQ

### How do I change the default author?
Menu → File → Settings → Default Author

### Where are my projects saved?
In the folder you select in Step 1. A new subfolder is created with the application name.

### Can I customize the project structure?
Yes! Edit `core/default_templates.py` in the generator itself.

### How do I add a new language?
Create a new `.json` file in `i18n/locales/` (e.g., `it_IT.json`) and copy the structure from `en_US.json`.

### Does this work with Python 3.9?
The generator works with Python 3.9+, but generated projects require Python 3.11+ due to pyproject.toml features.

### How do I update the generator itself?
Download the latest version and overwrite the files. Your settings will be preserved.

---

## 📞 Contact & Support

**Author:** Barremans  
**Version:** 1.2.0  
**License:** MIT

For questions or issues, consult the changelog or contact the developer.