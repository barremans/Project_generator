# Project Generator - Help

## Overzicht

De Python Project Generator maakt automatisch een complete, professionele Python projectstructuur aan.

## Gebruik

### Stap 1: Projectlocatie
- Klik **Bladeren** om een map te selecteren
- Vul de **applicatienaam** in
- Deze naam wordt gebruikt voor de hoofdmap en in alle bestanden

### Stap 2: Project Informatie
- **Auteur**: Jouw naam (wordt in alle headers gebruikt)
- **Versie**: Standaard 1.0.0 (SemVer)
- **Beschrijving**: Optioneel, komt in README.md

### Stap 3: Opties
- **Virtuele omgeving**: Maakt automatisch een venv aan met pip

### Stap 4: Samenvatting
- Controleer alle instellingen
- Klik **Genereer Project** of druk op **Enter**

## Instellingen

Via **Menu → Bestand → Instellingen** (of **Ctrl+,**) kun je instellen:
- **Standaard auteur**: Wordt automatisch ingevuld bij nieuwe projecten
- **Standaard projectmap**: Start locatie bij bladeren
- **Editor pad**: Commando of pad naar je favoriete editor

### Editor voorbeelden:
- VS Code: `code`
- Notepad++: `notepad++`
- Sublime: `subl`
- Of volledig pad: `C:\Program Files\...\editor.exe`

## Keyboard Shortcuts

### Navigatie
- **Enter**: Volgende stap
- **Shift+Tab**: Vorige stap

### Menu
- **Ctrl+N**: Nieuw project
- **Ctrl+,**: Instellingen
- **F1**: Help
- **Ctrl+Q**: Afsluiten

## Projectstructuur

Elk gegenereerd project bevat:
```
YourApp/
├── .vscode/           # VS Code configuratie
│   ├── launch.json
│   └── settings.json
├── app/               # Hoofdapplicatie
│   ├── __init__.py
│   ├── main.py
│   └── version.py
├── config/            # Configuratie
│   └── settings.json
├── css/               # Stylesheets
├── data/              # Data opslag
├── docs/              # Documentatie
│   └── changelog.md
├── helpers/           # Helper functies
├── utils/             # Utilities
├── md/                # Markdown
│   └── help.md
├── tests/             # Unit tests
├── venv/              # Virtuele omgeving (optioneel)
├── README.md
├── requirements.txt
├── .gitignore
├── export_to_usb.bat
└── YourApp.spec
```

## Features

### Automatische Headers
Elk bestand krijgt een header met:
- Relatief pad
- Beschrijving
- Applicatienaam
- Versie
- Auteur

### Commentaar stijlen
- Python: `""" docstring """`
- Batch: `REM`
- Markdown: `<!-- -->`
- JSON: geen (niet ondersteund)

### Export Script
Het `export_to_usb.bat` script:
- Exporteert project naar USB
- Maakt requirements.txt
- Optioneel venv meenemen
- Excludeert 'zzz' map
- Logt export details

### PyInstaller Support
Het `.spec` bestand bevat:
- Basis configuratie
- Assets verzameling
- Tree structuren voor data/docs/css

## Ondersteuning

Voor vragen, problemen of suggesties:
- Bekijk de **Changelog** voor recent nieuws
- Controleer de project documentatie
- Neem contact op met de ontwikkelaar

## Tips

1. **Eerste keer**: Stel je standaard auteur in via Settings
2. **Snelheid**: Gebruik Enter/Shift+Tab voor snelle navigatie
3. **Venv**: Laat aangevinkt voor automatische setup
4. **Editor**: Configureer je favoriete editor voor snelle toegang
5. **Hergebruik**: Gebruik "Nieuw Project" knop na voltooiing

---

**Versie:** 1.0.3  
**Auteur:** Barremans