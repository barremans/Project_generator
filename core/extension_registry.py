"""
File:    /core/extension_registry.py
Rol:     Centrale definitie van ondersteunde bestandsextensies voor
         PROJECT_STRUCTURE.md-generatie en add_headers, en het uitlezen/
         opbouwen van headermetadata voor die bestanden.
Applicatie: Project Generator
Versie:  2.5.0
Auteur:  Barremans
Changes: 2.5.0 - Aliaslijst uitgebreid na mismatch vastgesteld op een echt
                  bestaand project (capacitor_esr_validator,
                  instrument_profiles.py): dat project gebruikt een VIERDE
                  headervocabularium ("Module:"/"Project:"/"Doel:"/"Datum:",
                  naast Versie:/Auteur: die toevallig al herkend werden) dat
                  nog niet in _LABEL_ALIASES zat — PROJECT_STRUCTURE.md toonde
                  daardoor "GEEN BESCHRIJVING"/"GEEN APPLICATIE" voor zo goed
                  als elk bestand, terwijl die info wel degelijk aanwezig was
                  (enkel onder andere labels). Toegevoegd: "module" ->
                  bestandsnaam, "project" -> applicatie, "doel" ->
                  beschrijving. Nieuw: "datum"/"date" als apart
                  (optioneel, geen DEFAULT_*) metadataveld — stond voorheen
                  nergens gemodelleerd en ging dus stilzwijgend verloren bij
                  het uitlezen, ondanks dat het echt in het bestand staat.
Changes: 2.4.0 - EXTENSION_TEMPLATES volledig herschreven naar de officiële
                  CGK-conventie uit 00-conventions.md §4, i.p.v. Project
                  Generator's eigen Dutch-labeled docstring-stijl (open punt
                  context_ProjectGenerator.md §7.3 — hiermee afgesloten):
                  (1) .py: niet langer een python-docstring ("\"\"\"..."),
                      maar een "#"-commentaarblok met "===="-scheidingslijnen,
                      conform de conventie. Labels nu Engels: File:/Role:/
                      Version:/Author:/Changes: i.p.v. Rol:/Versie:/Auteur:.
                  (2) BEWUSTE afwijking t.o.v. de letterlijke conventie
                      (bevestigd door gebruiker): de conventie plaatst de
                      appnaam ongelabeld op de tweede regel ("# <AppNaam>"),
                      wat niet machine-leesbaar is voor generate_index.py's
                      per-bestand "Applicatie"-metadata. In plaats daarvan
                      krijgt die regel alsnog een expliciet "Applicatie:"
                      -label — enige toegevoegde regel t.o.v. de standaard,
                      de rest volgt die 1-op-1.
                  (3) .txt/.ini/.yaml/.yml volgen nu de conventie's TWEEDE
                      format ("Requirements / tekstuele configuratiefiles"):
                      Nederlandse labels Beschrijving:/Versie:/Auteur:/
                      Applicatie:, GEEN aparte bestandsnaam-regel (stond er
                      v2.2.0-2.3.0 nog wel in, niet conform de conventie).
                  (4) Leeslogica (_extract_raw_metadata/_LABEL_ALIASES)
                      BEWUST ONGEWIJZIGD: blijft breed/tolerant zodat
                      bestaande/legacy projecten (oudere project-doc-tool-
                      stijl, ArticleSearch, …) bij "Projectstructuur
                      genereren" correct blijven uitgelezen worden, ook al
                      schrijft add_headers.py voortaan nog maar één stijl.
                      Onderscheid schrijven (nieuw project / headers
                      toevoegen = altijd de nieuwe CGK-stijl) vs. lezen
                      (bestaande projecten = alle herkende stijlen) expliciet
                      bevestigd door gebruiker.
Changes: 2.3.0 - BUGFIX: extract_metadata_from_text() vulde defaults al
                  in vóór add_headers.py zijn eigen "applicatie"-fallback
                  kon toepassen, waardoor die parameter effectief nooit
                  gebruikt werd (bevestigd via smoketest). Metadata-extractie
                  opgesplitst in _extract_raw_metadata() (geen defaults,
                  intern) en extract_metadata_from_text() (met defaults,
                  publieke API — ongewijzigd gedrag voor bestaande
                  aanroepers zoals core/generate_index.py). add_headers.py
                  gebruikt voortaan de raw-variant.
Changes: 2.2.0 - EXTENSION_TEMPLATES/get_template_for_extension() opnieuw
                  toegevoegd (nodig voor het geporte core/add_headers.py),
                  maar NIET in project-doc-tool's originele formaat: de
                  templates volgen nu Project Generator's eigen
                  header_renderer.py-stijl (docstring voor .py, hash-
                  commentaar voor .txt/.ini/.yaml/.yml — labels File:/Rol:/
                  Applicatie:/Versie:/Auteur:/Changes:). Bevestigd door
                  gebruiker als de te schrijven standaard bij het toevoegen/
                  herstellen van headers (i.p.v. project-doc-tool's oude
                  Bestandsnaam:/Beschrijving:-vocabularium).
                  .json is BEWUST NIET opgenomen in EXTENSION_TEMPLATES:
                  het origineel schreef "//"-commentaar in .json-bestanden,
                  wat ongeldige JSON oplevert (JSON kent geen commentaar-
                  syntax) — header_renderer.py's eigen _render_json()
                  retourneert dan ook terecht "" (geen header). add_headers
                  slaat .json dus voortaan over i.p.v. het bestand te
                  corrumperen. Nieuwe helper has_recognized_header() voor
                  hergebruik door core/add_headers.py (ongeacht vocabulaire).
Changes: 2.1.0 - Geport vanuit project-doc-tool (extension_registry.py
                  v2.0.4, auteur Barre) in het kader van de samenvoeging
                  (zie context_ProjectDocTool.md §7.4). extract_metadata_
                  from_text() herkent nu TWEE headervocabulaires i.p.v. één:
                  (1) het originele project-doc-tool-formaat en (2) Project
                  Generator's eigen header_renderer.py-formaat.
"""

from typing import Dict, Optional

# ============================================================
# DEFAULTS (ENIGE WAARHEID)
# ============================================================

DEFAULT_BESCHRIJVING = "GEEN BESCHRIJVING"
DEFAULT_AUTEUR = "GEEN AUTEUR"
DEFAULT_APPLICATIE = "GEEN APPLICATIE"
DEFAULT_VERSIE = "V1.0.0"

# ============================================================
# EXTENSION REGISTRY — welke bestandstypes worden gescand op metadata
# ============================================================

EXTENSION_REGISTRY: Dict[str, dict] = {
    ".py": {"type": "python", "comment": "#"},
    ".txt": {"type": "text", "comment": "#"},
    ".ini": {"type": "ini", "comment": "#"},
    ".yaml": {"type": "yaml", "comment": "#"},
    ".yml": {"type": "yaml", "comment": "#"},
    ".json": {"type": "json", "comment": "//"},
}

# ============================================================
# HEADER TEMPLATES — conform 00-conventions.md §4, + Applicatie:-label
# ============================================================
# Placeholders: {file} {rol} {applicatie} {versie} {auteur}
# (interne sleutelnamen ongewijzigd t.o.v. vorige versies — enkel de
# omliggende labeltekst per extensie is aangepast aan de CGK-conventie)
#
# .py  -> conventie-format "Python (*.py)": "#"-commentaarblok met
#         "===="-scheidingslijnen, Engelse labels File:/Role:/Version:/
#         Author:/Changes:. Enige toevoeging t.o.v. de letterlijke
#         conventie: expliciet "Applicatie:"-label i.p.v. een ongelabelde
#         appnaam-regel (bevestigd, nodig voor generate_index.py).
# .txt/.ini/.yaml/.yml -> conventie-format "Requirements / tekstuele
#         configuratiefiles": Nederlandse labels Beschrijving:/Versie:/
#         Auteur:/Applicatie:, geen aparte bestandsnaam-regel.
# .json is bewust afwezig (zie Changes 2.2.0 hierboven).

EXTENSION_TEMPLATES: Dict[str, str] = {
    ".py": (
        "# =============================================================================\n"
        "# Applicatie: {applicatie}\n"
        "# File:    {file}\n"
        "# Role:    {rol}\n"
        "# Version: {versie}\n"
        "# Author:  {auteur}\n"
        "# Changes: {versie} - Baseline (header automatisch toegevoegd).\n"
        "# =============================================================================\n\n"
    ),
    ".txt": (
        "# Beschrijving: {rol}\n"
        "# Versie: {versie}\n"
        "# Auteur: {auteur}\n"
        "# Applicatie: {applicatie}\n\n"
    ),
    ".ini": (
        "# Beschrijving: {rol}\n"
        "# Versie: {versie}\n"
        "# Auteur: {auteur}\n"
        "# Applicatie: {applicatie}\n\n"
    ),
    ".yaml": (
        "# Beschrijving: {rol}\n"
        "# Versie: {versie}\n"
        "# Auteur: {auteur}\n"
        "# Applicatie: {applicatie}\n\n"
    ),
    ".yml": (
        "# Beschrijving: {rol}\n"
        "# Versie: {versie}\n"
        "# Auteur: {auteur}\n"
        "# Applicatie: {applicatie}\n\n"
    ),
}


def get_template_for_extension(extension: str) -> Optional[str]:
    """Geeft het headertemplate voor een extensie, of None indien niet ondersteund."""
    return EXTENSION_TEMPLATES.get(extension.lower())


# ============================================================
# LABEL-ALIASSEN — meerdere headervocabularia naar één interne sleutel
# ============================================================
# BEWUST breed gehouden (niet beperkt tot de nieuwe CGK-stijl): dit is de
# LEESKANT, gebruikt bij "Projectstructuur genereren" op zowel nieuwe als
# bestaande/legacy projecten. Volgorde binnen elke lijst bepaalt voorrang
# bij een eventueel dubbele match (komt in de praktijk niet voor, want
# elke header gebruikt één vocabularium consistent).
_LABEL_ALIASES: Dict[str, list] = {
    "bestandsnaam": ["bestandsnaam", "file", "module"],
    "beschrijving": ["beschrijving", "rol", "role", "doel"],
    "auteur": ["auteur", "author"],
    "applicatie": ["applicatie", "application", "project"],
    "versie": ["versie", "version"],
    "datum": ["datum", "date"],
}

_ALL_ALIAS_LABELS = {
    alias for aliases in _LABEL_ALIASES.values() for alias in aliases
}


def has_recognized_header(text: str) -> bool:
    """
    Check of tekst minstens één herkend headerlabel bevat (ongeacht welk
    vocabularium) — gebruikt door add_headers.py om te bepalen of een
    bestand al een header heeft, zonder zelf de aliaslijst te dupliceren.
    """
    for raw in text.splitlines():
        line = raw.strip()
        for token in ("#", "//", "/*", "*/", "*"):
            if line.startswith(token):
                line = line[len(token):].strip()
        if ":" not in line:
            continue
        label = line.split(":", 1)[0].strip().lower()
        if label in _ALL_ALIAS_LABELS:
            return True
    return False


def _extract_raw_metadata(text: str) -> dict:
    """
    Leest headerlabels zonder defaults in te vullen (interne helper).
    Ontbrekende velden blijven None — nodig zodat aanroepers (zoals
    add_headers.py) hun eigen fallback-waarde kunnen toepassen vóór de
    generieke DEFAULT_*-constanten.
    """
    metadata = {
        "bestandsnaam": None,
        "beschrijving": None,
        "auteur": None,
        "applicatie": None,
        "versie": None,
        "datum": None,
    }

    label_to_key = {
        alias: key
        for key, aliases in _LABEL_ALIASES.items()
        for alias in aliases
    }

    for raw in text.splitlines():
        line = raw.strip()

        for token in ("#", "//", "/*", "*/", "*"):
            if line.startswith(token):
                line = line[len(token):].strip()

        if ":" not in line:
            continue

        label, _, value = line.partition(":")
        key = label_to_key.get(label.strip().lower())

        if key and metadata[key] is None:
            metadata[key] = value.strip()

    return metadata


def extract_metadata_from_text(text: str) -> dict:
    """
    Leest headermetadata uit de eerste regels van een bestand, met
    DEFAULT_*-waarden voor ontbrekende velden ingevuld. Gebruik
    _extract_raw_metadata() rechtstreeks wanneer je zelf een andere
    fallback-waarde wil toepassen vóór de generieke defaults (zoals
    core/add_headers.py doet voor "applicatie").

    Herkent inmiddels meerdere headervocabularia: project-doc-tool's eigen
    formaat ("Bestandsnaam:"/"Beschrijving:"/...), de CGK-conforme
    schrijfstijl ("File:"/"Role:"/"Version:"/"Author:"/"Applicatie:"),
    Project Generator's vorige header_renderer.py-formaat ("File:"/"Rol:"/
    ...), en het "Module:"/"Project:"/"Doel:"/"Datum:"-vocabularium dat in
    bestaande projecten zoals capacitor_esr_validator voorkomt. Bestanden
    worden nooit gewijzigd — dit is uitsluitend lezen.

    "datum" krijgt BEWUST geen DEFAULT_*-waarde (blijft None/afwezig als
    niet gevonden) — in tegenstelling tot de andere vier velden is dit geen
    verplicht onderdeel van elk headerformaat, dus een "GEEN DATUM"-fallback
    zou ruis toevoegen aan elk bestand dat dit veld nooit had.
    """
    metadata = _extract_raw_metadata(text)

    metadata["beschrijving"] = metadata["beschrijving"] or DEFAULT_BESCHRIJVING
    metadata["auteur"] = metadata["auteur"] or DEFAULT_AUTEUR
    metadata["applicatie"] = metadata["applicatie"] or DEFAULT_APPLICATIE
    metadata["versie"] = metadata["versie"] or DEFAULT_VERSIE
    # metadata["datum"] blijft ongewijzigd: None indien niet aanwezig.

    return metadata


def is_supported_extension(extension: str) -> bool:
    """Check of een extensie ondersteund wordt voor metadata-extractie."""
    return extension.lower() in EXTENSION_REGISTRY