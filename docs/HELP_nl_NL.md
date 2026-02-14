# Project Generator - Uitgebreide Help

**Versie:** 1.0.4  
**Auteur:** Barremans

---

## 📚 Inhoudsopgave

1. [Overzicht](#overzicht)
2. [Basis Gebruik](#basis-gebruik)
3. [Instellingen](#instellingen)
4. [Modern Python Packaging](#modern-python-packaging)
5. [Scripts Systeem](#scripts-systeem)
6. [Keyboard Shortcuts](#keyboard-shortcuts)
7. [Projectstructuur](#projectstructuur)
8. [Development Workflow](#development-workflow)
9. [Veelgestelde Vragen](#veelgestelde-vragen)

---

## Overzicht

De Python Project Generator maakt automatisch een complete, professionele Python projectstructuur aan volgens moderne best practices (PEP 517/518/621).

### Wat krijg je?

- ✅ Moderne `pyproject.toml` configuratie
- ✅ Backwards compatible `setup.py`
- ✅ Development tools (Black, Flake8, MyPy, pytest)
- ✅ QSS stylesheets voor Qt applicaties
- ✅ Standaard icons
- ✅ Utility scripts
- ✅ VS Code integratie
- ✅ Git configuratie
- ✅ Documentatie templates

---

## Basis Gebruik

### Stap 1: Projectlocatie
- Klik **Bladeren** om een map te selecteren (start bij C:\ of ingestelde root)
- Vul de **applicatienaam** in
- Deze naam wordt gebruikt voor de hoofdmap en in alle bestanden

### Stap 2: Project Informatie
- **Auteur**: Jouw naam (wordt in alle headers en pyproject.toml gebruikt)
- **Versie**: Standaard 1.0.0 (SemVer formaat)
- **Beschrijving**: Optioneel, komt in README.md en pyproject.toml

### Stap 3: Opties
- **Virtuele omgeving**: Maakt automatisch een venv aan met pip

### Stap 4: Samenvatting
- Controleer alle instellingen
- Klik **Genereer Project** of druk op **Enter**

### Stap 5: Resultaat
Na generatie krijg je 4 opties:
- **📁 Open Projectmap**: Windows Verkenner
- **💻 Open in Editor**: VS Code of geconfigureerde editor
- **🆕 Nieuw Project**: Start wizard opnieuw
- **❌ Sluiten**: Sluit applicatie

---

## Instellingen

Via **Menu → Bestand → Instellingen** (of **Ctrl+,**):

### Standaard Auteur
- Wordt automatisch ingevuld bij nieuwe projecten
- Gebruikt in pyproject.toml, LICENSE, alle headers

### Standaard Projectmap
- Start locatie bij bladeren
- Bijvoorbeeld: `C:\Projects` of `D:\Development`

### Editor Pad
Commando of pad naar je favoriete editor:
- **VS Code**: `code` (standaard)
- **Notepad++**: `notepad++`
- **Sublime**: `subl`
- **PyCharm**: `C:\Program Files\JetBrains\PyCharm\bin\pycharm64.exe`
- **Volledig pad**: Voor elke andere editor

---

## Modern Python Packaging

### pyproject.toml - De moderne standaard

Het `pyproject.toml` bestand is het hart van moderne Python projecten (PEP 621).

#### Structuur
```toml
[build-system]
# Hoe het project gebouwd wordt
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
# Project metadata
name = "mijn-project"
version = "1.0.0"
description = "Beschrijving"
authors = [{name = "Jouw Naam"}]

# Dependencies
dependencies = [
    "PyQt6>=6.6.1",
    "requests>=2.31.0"
]

# Development dependencies (optioneel)
[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "black>=23.0.0"
]

# Tool configuratie
[tool.black]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
```

#### Waarom pyproject.toml?

**Voordelen:**
1. ✅ **Centraal configuratie punt** - Alles op één plek
2. ✅ **Moderne standaard** - PEP 621 compliant
3. ✅ **Tool integratie** - Black, pytest, mypy configuratie
4. ✅ **Geen setup.py nodig** - Optioneel voor backwards compatibility
5. ✅ **Type checking** - TOML is gestructureerd en valideerbaar

**Nadelen:**
- ⚠️ Python < 3.11 heeft oudere pip nodig
- ⚠️ Sommige oude tools kennen het niet

#### Dependencies toevoegen

**Handmatig:**
```toml
[project]
dependencies = [
    "PyQt6>=6.6.1",
    "requests>=2.31.0",
    "Pillow>=10.1.0"
]
```

**Via script (zie Scripts Systeem):**
```bash
cd scripts
python update_toml.py --add-dep "pandas>=2.0.0"
```

#### Dev dependencies

Voor development tools:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "black>=23.0.0",
    "flake8>=6.1.0"
]
```

Installeren:
```bash
pip install -e ".[dev]"
```

---

## Scripts Systeem

Elk gegenereerd project krijgt een `scripts/` folder met utility scripts.

### 📁 scripts/update_toml.py

**Functie**: Update pyproject.toml automatisch

**Gebruik:**
```bash
cd scripts

# Voeg dependency toe
python update_toml.py --add-dep "requests>=2.31.0"

# Voeg dev dependency toe
python update_toml.py --add-dev "pytest-cov>=4.1.0"

# Update versie
python update_toml.py --set-version "1.0.1"

# Update auteur
python update_toml.py --set-author "Nieuwe Naam"

# Update beschrijving
python update_toml.py --set-description "Nieuwe beschrijving"
```

**Werking:**
1. Leest `pyproject.toml`
2. Parsed met `tomli` (lezen) en `tomli_w` (schrijven)
3. Maakt backup (`pyproject.toml.bak`)
4. Update gevraagde velden
5. Schrijft terug met formatting

**Voorbeeld:**
```bash
# Voor project versie verhogen:
python update_toml.py --set-version "1.1.0"

# Voor nieuwe dependency:
python update_toml.py --add-dep "pandas>=2.0.0"
```

### 📁 scripts/bump_version.py

**Functie**: Verhoog versienummer overal in het project

**Gebruik:**
```bash
cd scripts

# Verhoog patch (1.0.0 → 1.0.1)
python bump_version.py patch

# Verhoog minor (1.0.1 → 1.1.0)
python bump_version.py minor

# Verhoog major (1.1.0 → 2.0.0)
python bump_version.py major

# Specifieke versie
python bump_version.py --version 2.5.3
```

**Update deze bestanden:**
- `app/version.py` → `__version__ = "x.x.x"`
- `pyproject.toml` → `[project] version = "x.x.x"`
- `docs/changelog.md` → Voegt nieuwe sectie toe

**Werking:**
1. Leest huidige versie uit `app/version.py`
2. Berekent nieuwe versie (SemVer)
3. Update alle bestanden
4. Voegt changelog entry toe
5. Print samenvatting

### 📁 scripts/generate_requirements.py

**Functie**: Genereer requirements.txt uit pyproject.toml

**Gebruik:**
```bash
cd scripts

# Genereer alleen runtime dependencies
python generate_requirements.py

# Inclusief dev dependencies
python generate_requirements.py --dev

# Output naar ander bestand
python generate_requirements.py --output requirements-dev.txt --dev
```

**Werking:**
1. Leest dependencies uit `pyproject.toml`
2. Schrijft naar `requirements.txt`
3. Optioneel: inclusief `[project.optional-dependencies]`

**Waarom?**
- Sommige tools werken alleen met `requirements.txt`
- Deployment platforms (Heroku, etc.) verwachten dit
- Backwards compatibility

### 📁 scripts/validate_project.py

**Functie**: Valideer project structuur en configuratie

**Gebruik:**
```bash
cd scripts
python validate_project.py
```

**Controleert:**
- ✅ Alle verwachte folders en bestanden aanwezig
- ✅ pyproject.toml is valide TOML
- ✅ Dependencies zijn installeerbaar
- ✅ Tests zijn uitvoerbaar
- ✅ Code style (Black, Flake8)

---

## Keyboard Shortcuts

### Navigatie
- **Enter**: Volgende stap
- **Shift+Tab**: Vorige stap

### Menu
- **Ctrl+N**: Nieuw project
- **Ctrl+,**: Instellingen
- **F1**: Help
- **Ctrl+Q**: Afsluiten

---

## Projectstructuur

### Volledige layout
```
MijnProject/
├── pyproject.toml          # Modern Python configuratie (PEP 621)
├── setup.py                # Backwards compatibility
├── MANIFEST.in             # Package distributie
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # Development guide
├── Makefile                # Development shortcuts
├── README.md
├── requirements.txt
├── .gitignore
│
├── .vscode/                # VS Code configuratie
│   ├── launch.json         # Debug configuratie
│   └── settings.json       # Python settings
│
├── app/                    # Hoofdapplicatie (Python package)
│   ├── __init__.py
│   ├── main.py            # Entry point
│   └── version.py         # Versie definitie
│
├── assets/                 # Media bestanden
│   └── icons/             # Standaard icons (PNG, ICO)
│
├── config/                 # Configuratie
│   └── settings.json
│
├── css/                    # Qt StyleSheets
│   ├── main.qss           # Hoofd styling
│   └── detail.qss         # Detail windows
│
├── data/                   # Data opslag
│   └── .gitkeep
│
├── docs/                   # Documentatie
│   └── changelog.md
│
├── helpers/                # Helper functies (package)
│   └── __init__.py
│
├── md/                     # Markdown files
│   └── help.md
│
├── scripts/                # Utility scripts
│   ├── update_toml.py     # Update pyproject.toml
│   ├── bump_version.py    # Verhoog versie
│   ├── generate_requirements.py
│   └── validate_project.py
│
├── tests/                  # Unit tests (package)
│   └── __init__.py
│
├── utils/                  # Utilities (package)
│   └── __init__.py
│
├── venv/                   # Virtuele omgeving (optioneel)
│
├── export_to_usb.bat       # Export script
└── MijnProject.spec        # PyInstaller config
```

---

## Development Workflow

### Eerste keer setup
```bash
# 1. Activeer venv
venv\Scripts\activate

# 2. Installeer dev dependencies
pip install -e ".[dev]"

# 3. Verifieer installatie
make test
```

### Dagelijkse workflow
```bash
# Code schrijven...

# Format code
make format

# Run linters
make lint

# Run tests
make test

# Of met coverage
make coverage
```

### Nieuwe feature toevoegen
```bash
# 1. Maak feature branch
git checkout -b feature/nieuwe-functie

# 2. Schrijf code + tests

# 3. Format en lint
make format
make lint

# 4. Run tests
make test

# 5. Commit
git commit -m "feat: voeg nieuwe functie toe"

# 6. Push en open PR
git push origin feature/nieuwe-functie
```

### Versie verhogen
```bash
# Voor patch release (bugfix)
cd scripts
python bump_version.py patch

# Voor minor release (nieuwe feature)
python bump_version.py minor

# Voor major release (breaking change)
python bump_version.py major

# Update changelog handmatig in docs/changelog.md
```

### Distributie maken
```bash
# Build wheel en source distributie
make build

# Resultaat in dist/:
# - mijn-project-1.0.0.tar.gz
# - mijn_project-1.0.0-py3-none-any.whl

# Upload naar PyPI (optioneel)
twine upload dist/*
```

---

## Veelgestelde Vragen

### Wat is TOML?

**TOML** = Tom's Obvious, Minimal Language

Een configuratie formaat dat:
- ✅ Makkelijk te lezen voor mensen
- ✅ Makkelijk te parsen voor machines
- ✅ Sterk getypeerd
- ✅ Ondersteunt comments

**Voorbeeld:**
```toml
# Dit is een comment
[section]
key = "waarde"
number = 42
array = ["item1", "item2"]
```

### Moet ik pyproject.toml handmatig bewerken?

**Nee!** Gebruik de scripts:
- `update_toml.py` voor dependencies
- `bump_version.py` voor versies

**Ja!** Voor:
- Complexe configuratie
- Tool-specifieke settings
- Metadata updates

### Wat als ik geen TOML wil?

Je kan ook alleen `requirements.txt` gebruiken:
```bash
# Genereer uit pyproject.toml
cd scripts
python generate_requirements.py

# Nu heb je requirements.txt
pip install -r requirements.txt
```

### Hoe voeg ik een nieuwe dependency toe?

**Methode 1 - Script (aanbevolen):**
```bash
cd scripts
python update_toml.py --add-dep "requests>=2.31.0"
pip install requests
```

**Methode 2 - Handmatig:**
1. Open `pyproject.toml`
2. Voeg toe aan `[project] dependencies`
3. Run `pip install -e .`

**Methode 3 - Traditioneel:**
1. `pip install requests`
2. `pip freeze > requirements.txt`

### Werkt dit met oudere Python versies?

**pyproject.toml** werkt met:
- ✅ Python 3.11+ (volledig)
- ✅ Python 3.8-3.10 (met pip >= 21.3)
- ⚠️ Python 3.7 (pip upgrade nodig)

**Backwards compatibility:**
- `setup.py` werkt met alle Python 3.x
- Gebruik dat als fallback

### Hoe laad ik QSS stylesheets?
```python
from pathlib import Path
from PyQt6.QtWidgets import QApplication

def load_stylesheet(name: str) -> str:
    """Laad QSS stylesheet."""
    qss_file = Path("css") / name
    if qss_file.exists():
        return qss_file.read_text(encoding="utf-8")
    return ""

# In je applicatie:
app = QApplication([])
app.setStyleSheet(load_stylesheet("main.qss"))
```

### Hoe gebruik ik de icons?
```python
from pathlib import Path
from PyQt6.QtGui import QIcon

def get_icon(name: str) -> QIcon:
    """Haal icon op."""
    icon_path = Path("assets/icons") / name
    if icon_path.exists():
        return QIcon(str(icon_path))
    return QIcon()

# Gebruik:
window.setWindowIcon(get_icon("app_icon.png"))
button.setIcon(get_icon("folder.png"))
```

### Wat doet de Makefile?

**Shortcuts voor development:**
- `make install` - Installeer dependencies
- `make dev` - Installeer dev dependencies
- `make test` - Run tests
- `make coverage` - Tests met coverage
- `make lint` - Run linters
- `make format` - Format code
- `make clean` - Verwijder cache
- `make run` - Run applicatie
- `make build` - Build distributie

**Werkt op:**
- ✅ Linux / Mac (native)
- ✅ Windows (via Git Bash, WSL, of MinGW)

**Zonder Make:**
Gebruik de onderliggende commando's:
```bash
pytest tests/
black .
flake8 .
```

---

## Ondersteuning

### Help nodig?

1. **Check de documentatie**: `docs/`, `md/help.md`
2. **Check de scripts**: `scripts/` met `--help`
3. **Open een issue**: Op het project repository
4. **Neem contact op**: Met de ontwikkelaar

### Nuttige links

- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 621](https://peps.python.org/pep-0621/) - pyproject.toml
- [TOML Specificatie](https://toml.io/)
- [Black Documentation](https://black.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)

---

**Versie:** 1.0.4  
**Laatste update:** 2024-02-12  
**Auteur:** Barremans