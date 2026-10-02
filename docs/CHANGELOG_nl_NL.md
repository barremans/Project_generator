# Changelog

Alle wijzigingen aan de Project Generator worden hier gedocumenteerd.

## [2.1.0] - 2026-10-02

### Toegevoegd
- Nieuw, optioneel `Datum:`-headerveld — wordt getoond in gegenereerde
  `PROJECT_STRUCTURE.md`-bestanden wanneer het aanwezig is (geen
  geforceerde placeholder voor bestanden zonder dit veld) — ging voorheen
  stilzwijgend verloren bij het uitlezen.

### Gewijzigd
- **Headerformaat gelijkgetrokken met de officiële CGK-conventie**
  (`00-conventions.md` §4) — sluit het eerder geïdentificeerde open punt af:
  - `.py`-headers worden niet langer als python-docstring geschreven, maar
    als een `#`-commentaarblok met `====`-scheidingslijnen, met de Engelse
    labels `File:`/`Role:`/`Version:`/`Author:`/`Changes:` (voorheen
    `Rol:`/`Versie:`/`Auteur:`). `.bat`/`.ps1`/`.spec`-headers volgen
    dezelfde Engelse labelfamilie, in `REM`/`#`-commentaarsyntax.
  - `.txt`/`.ini`/`.yaml`/`.yml`-headers volgen nu het eigen
    config-bestand-format uit de conventie (Nederlandse labels
    `Beschrijving:`/`Versie:`/`Auteur:`/`Applicatie:`, geen aparte
    bestandsnaam-regel meer).
  - Bewuste, bevestigde afwijking t.o.v. de letterlijke conventie: een
    expliciet `Applicatie:`-label blijft behouden (ook bij `.py`, waar de
    conventie de appnaam ongelabeld plaatst) zodat `generate_index.py` dit
    per bestand blijft kunnen uitlezen.
  - Een nieuwe "Headers toevoegen"-run op een bestaand project converteert
    oude docstring-stijl `.py`-headers automatisch naar de nieuwe
    commentaarblok-stijl.
- Het **uitlezen** van headers (gebruikt door "Projectstructuur
  genereren" op bestaande/legacy projecten) blijft bewust breed en niet
  beperkt tot het nieuwe formaat: de herkende label-aliassen zijn
  uitgebreid met een vocabularium dat op een echt bestaand project
  aangetroffen werd (`Module:`/`Project:`/`Doel:`, naast de reeds herkende
  labels), zodat oudere/anders-geformuleerde headers correct uitgelezen
  blijven i.p.v. als "geen beschrijving"/"geen applicatie" te verschijnen.

### Opgelost
- `.json`-bestanden krijgen niet langer een placeholder-metadatablok
  (`GEEN BESCHRIJVING`/`GEEN AUTEUR`/`GEEN APPLICATIE`/`V1.0.0`) in
  `PROJECT_STRUCTURE.md` — JSON kan structureel nooit een header krijgen
  (geen commentaarsyntax), dus dit was pure ruis. Het bestand zelf blijft
  gewoon zichtbaar in de boomstructuur, enkel het metadatablok vervalt.


## [2.0.5] - 2026-09-18

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 


## [2.0.4] - 2026-09-18

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 


## [2.0.3] - 2026-09-17

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 


## [2.0.2] - 2026-09-17

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 


## [2.0.1] - 2026-09-16

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 


## [2.0.0] - 2026-09-16

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 


## [1.1.1] - 2026-09-16

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 


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