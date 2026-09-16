# Changelog

Alle wijzigingen aan de Project Generator worden hier gedocumenteerd.

## [1.2.0] - 2026-09-16

### Toegevoegd
- **Nieuw "Tools"-menu** (tussen Taal en Help) met actie **"Headers & Structuur..."** —
  bundelt twee tools geport uit het losstaande project-doc-tool-project, dat
  hiermee is samengevoegd in Project Generator (er blijft dus nog 1
  applicatie over):
  - **Dry-run headers**: analyseert een gekozen projectmap en toont welke
    bestanden geen of een foutieve header hebben, zonder iets te wijzigen
  - **Headers toevoegen**: voegt/herstelt effectief headers, in Project
    Generator's eigen headerformaat (`File:`/`Rol:`/`Applicatie:`/`Versie:`/
    `Auteur:`/`Changes:`)
  - **Projectstructuur genereren**: genereert `PROJECT_STRUCTURE.md`
    (boomoverzicht + headermetadata per bestand als fenced code-block) voor
    een gekozen projectmap én outputmap; opent de outputmap automatisch na
    afloop
- **Nieuwe Tools-instellingen** (via de "⚙ Settings"-knop in de
  Tools-dialoog): include-extensies, exclude-mappen, exclude-bestanden, en
  headerdefaults voor applicatie/versie (auteur hergebruikt de bestaande
  "Standaard Auteur"-instelling — geen dubbel veld)
- Projectmap en outputmap van de Tools-dialoog worden onthouden tussen
  sessies
- Elk nieuw gegenereerd project krijgt voortaan automatisch een
  `docs/PROJECT_STRUCTURE.md` (nieuwe stap 9 in de generator), naast de
  mogelijkheid om dit ook apart/opnieuw te genereren via Tools
- Nieuwe standalone scripts: `scripts/generate_project_structure.py` en
  `scripts/add_headers.py` (dry-run-by-default, `--apply` voor effectieve
  wijzigingen bij add_headers)

### Gewijzigd
- `core/extension_registry.py` herkent headers voortaan in twee
  vocabularia (het oude project-doc-tool-formaat en Project Generator's
  eigen formaat) — nodig zodat reeds gegenereerde bestanden niet onterecht
  als "geen header" verschijnen

### Opgelost
- BUGFIX (geport uit project-doc-tool, bestond al in het origineel):
  header-detectie op korte bestanden (< 30 regels) faalde stil door een
  PEP 479-incompatibiliteit — nu gefixed met `itertools.islice`
- BUGFIX: het schrijven van `//`-commentaar in `.json`-bestanden (ongeldige
  JSON) is stopgezet — `.json` wordt voortaan overgeslagen bij het
  toevoegen van headers

## [1.1.0] - 2026-09-15

### Toegevoegd
- **`core/`-map**: nieuwe standaardmap in de gegenereerde projectstructuur,
  met een `__init__.py` — bedoeld voor kernlogica/gedeelde functionaliteit,
  los van de `app/`-package.

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