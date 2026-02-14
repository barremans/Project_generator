# Changelog

Alle wijzigingen aan de Project Generator worden hier gedocumenteerd.

## [1.0.4] - 2024-02-12

### Toegevoegd
- **Modern Python Packaging**: pyproject.toml (PEP 517/518/621)
- **Build systeem**: setup.py voor backwards compatibility
- **Package manifest**: MANIFEST.in voor distributie
- **Licentie**: MIT License template
- **Development guide**: CONTRIBUTING.md met code style richtlijnen
- **Makefile**: Development shortcuts (make test, make lint, etc.)
- **Scripts folder**: Standaard utility scripts
  - `update_toml.py` - Update pyproject.toml automatisch
  - `bump_version.py` - Verhoog versienummer overal
  - `generate_requirements.py` - Genereer requirements uit pyproject.toml
- **QSS templates**: main.qss en detail.qss voor Qt styling
- **Icon systeem**: Automatisch kopiëren van standaard icons
- **Enhanced README**: Volledige installatie en usage instructies

### Gewijzigd
- Projectstructuur nu volledig PEP compliant
- Generator versie: 1.0.3 → 1.0.4
- Verbeterde gitignore met moderne Python patterns
- VS Code settings met Black/Flake8/MyPy integratie

### Toegevoegd aan gegenereerde projecten
- pyproject.toml met volledige configuratie
- Development tools setup (Black, Flake8, MyPy, pytest)
- Scripts folder met utility scripts
- Uitgebreide documentatie

## [1.0.3] - 2024-02-11

### Toegevoegd
- Settings dialoog voor standaard waarden
- Menu systeem met Bestand en Help
- Keyboard shortcuts (Enter voor volgende, Shift+Tab voor vorige)
- Configureerbare editor pad
- Help en Changelog dialogen
- About scherm met versie info
- Icons op alle vensters en menu items

### Verbeterd
- Standaard auteur wordt automatisch ingevuld
- Editor knop gebruikt nu configureerbaar pad
- Betere gebruikerservaring met shortcuts

## [1.0.2] - 2024-02-11

### Toegevoegd
- Result pagina na project creatie
- Knoppen: Open Projectmap, Open in Editor, Nieuw Project, Sluiten
- Bladeren start standaard bij C:\ of ingestelde root

### Verbeterd
- Applicatie sluit niet meer automatisch
- Gebruiker heeft volledige controle na generatie

## [1.0.1] - 2024-02-11

### Toegevoegd
- Wizard interface voor project creatie
- Automatische mappenstructuur generatie
- Header rendering per bestandstype
- Virtuele omgeving support
- Export naar USB script
- PyInstaller .spec template
- VS Code configuratie

### Kenmerken
- Qt6 GUI
- Template-based systeem
- Uitbreidbaar en onderhoudbaar
- Cross-platform compatible

## [1.0.0] - 2024-02-11

### Toegevoegd
- Initiële release
- Basis project generator functionaliteit