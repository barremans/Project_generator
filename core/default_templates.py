"""
core/default_templates.py

Beschrijving: Standaard project templates
Applicatie: Project Generator
Versie: 1.0.3
Auteur: Barremans
"""

from pathlib import Path
from core.templates import ProjectTemplate, FolderTemplate, FileTemplate


def get_version_py_template(version: str) -> str:
    """Template voor version.py."""
    return f'__version__ = "{version}"  # Pas dit manueel aan bij elke release\n'


def get_main_py_template() -> str:
    """Template voor main.py."""
    return '''if __name__ == "__main__":
    print("Hello World!")
'''


def get_launch_json_template(app_name: str) -> str:
    """Template voor .vscode/launch.json."""
    # Gebruik workspace folder variabele voor portabiliteit
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
    # Gebruik workspace folder variabele voor portabiliteit
    python_path = "${workspaceFolder}/venv/Scripts/python.exe"
    
    return f'''{{
    "python.defaultInterpreterPath": "{python_path}",
    "python.pythonPath": "{python_path}"
}}
'''


def get_settings_config_template() -> str:
    """Template voor config/settings.json."""
    return '''{
    "app": {
        "name": "Application",
        "debug_mode": false
    }
}
'''


def get_gitignore_template() -> str:
    """Template voor .gitignore."""
    return '''# Virtual Environment
venv/
.venv/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Distribution / packaging
dist/
build/
*.egg-info/
*.egg

# PyInstaller
*.spec

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db

# Data
data/*
!data/.gitkeep

# Assets
assets/*
!assets/.gitkeep

# Logs
*.log
'''


def get_readme_template(app_name: str, version: str, author: str, description: str) -> str:
    """Template voor README.md."""
    desc_text = description if description else "Beschrijving van de applicatie"
    
    return f'''# {app_name}

**Versie:** {version}  
**Auteur:** {author}

## 📋 Beschrijving

{desc_text}

## 🚀 Installatie

### Vereisten
- Python 3.11 of hoger
- pip package manager

### Stappen
1. Clone of download dit project
2. Maak een virtuele omgeving aan:
```bash
   python -m venv venv
```
3. Activeer de virtuele omgeving:
   - Windows: `venv\\Scripts\\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Installeer dependencies:
```bash
   pip install -r requirements.txt
```

## 💻 Gebruik
```bash
python app/main.py
```

## 📁 Projectstructuur
```
{app_name}/
├── app/           # Hoofd applicatie code
├── assets/        # Icons en afbeeldingen
├── config/        # Configuratie bestanden
├── css/           # Stylesheets
├── data/          # Data opslag
├── docs/          # Documentatie
├── helpers/       # Helper functies
├── md/            # Markdown bestanden
├── utils/         # Utility functies
└── tests/         # Unit tests
```

## 🧪 Tests
```bash
python -m pytest tests/
```

## 📝 Changelog

Zie [CHANGELOG.md](docs/changelog.md) voor versiegeschiedenis.

## 📄 Licentie

Alle rechten voorbehouden.

## 👤 Contact

**{author}**
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
- Basis projectstructuur
- Standaard configuratie
- Assets folder voor icons en afbeeldingen

### Gewijzigd
- n.v.t.

### Verwijderd
- n.v.t.

### Opgelost
- n.v.t.
'''


def get_help_md_template(app_name: str) -> str:
    """Template voor help.md."""
    return f'''# {app_name} - Help

## Aan de slag

Welkom bij {app_name}!

## Functies

Beschrijf hier de hoofdfuncties van de applicatie.

## Veelgestelde vragen

### Vraag 1
Antwoord 1

### Vraag 2
Antwoord 2

## Contact

Voor vragen of ondersteuning, neem contact op met de ontwikkelaar.
'''


def get_requirements_txt_template() -> str:
    """Template voor requirements.txt."""
    return '''# Core dependencies
# Voeg hier je packages toe
# Bijvoorbeeld:
# PyQt6==6.6.1
# requests==2.31.0
'''


def get_gitkeep_template() -> str:
    """Template voor .gitkeep bestanden."""
    return '''# Deze file zorgt ervoor dat lege mappen in git blijven bestaan
'''


def create_standard_project_template(name: str, version: str, author: str, 
                                     description: str = "", create_venv: bool = False,
                                     root_path: Path = None) -> ProjectTemplate:
    """
    Creëer de standaard projectstructuur.
    
    Args:
        name: Applicatie naam
        version: Versie nummer
        author: Auteur naam
        description: Optionele beschrijving
        create_venv: Of virtuele omgeving moet worden aangemaakt
        root_path: Root pad waar project wordt aangemaakt (nodig voor correcte venv paden)
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
    icons_subfolder.add_file(".gitkeep", "Bewaar deze map in git", get_gitkeep_template())
    assets_folder.add_subfolder(icons_subfolder)
    
    # css folder
    css_folder = FolderTemplate(name="css")
    css_folder.add_file(".gitkeep", "Bewaar deze map in git", get_gitkeep_template())
    
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
    
    # Voeg alle folders toe
    project.add_folder(vscode_folder)
    project.add_folder(app_folder)
    project.add_folder(config_folder)
    project.add_folder(assets_folder)  # ← TOEGEVOEGD
    project.add_folder(css_folder)
    project.add_folder(data_folder)
    project.add_folder(docs_folder)
    project.add_folder(helpers_folder)
    project.add_folder(utils_folder)
    project.add_folder(md_folder)
    project.add_folder(tests_folder)
    
    # Root files
    project.add_file("README.md", "Project documentatie", 
                     get_readme_template(name, version, author, description))
    project.add_file("requirements.txt", "Python dependencies", get_requirements_txt_template())
    project.add_file(".gitignore", "Git ignore regels", get_gitignore_template())
    
    return project