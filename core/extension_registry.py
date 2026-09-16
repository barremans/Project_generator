"""
File:    /core/extension_registry.py
Rol:     Centrale definitie van ondersteunde bestandsextensies voor
         PROJECT_STRUCTURE.md-generatie en add_headers, en het uitlezen/
         opbouwen van headermetadata voor die bestanden.
Applicatie: Project Generator
Versie:  2.3.0
Auteur:  Barremans
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
# HEADER TEMPLATES — Project Generator's EIGEN formaat (header_renderer.py)
# ============================================================
# Placeholders: {file} {rol} {applicatie} {versie} {auteur}
# .json is bewust afwezig (zie Changes 2.2.0 hierboven).

EXTENSION_TEMPLATES: Dict[str, str] = {
    ".py": (
        '"""\n'
        "File:    {file}\n"
        "Rol:     {rol}\n"
        "Applicatie: {applicatie}\n"
        "Versie:  {versie}\n"
        "Auteur:  {auteur}\n"
        "Changes: {versie} - Baseline (header automatisch toegevoegd).\n"
        '"""\n\n'
    ),
    ".txt": (
        "# File:    {file}\n"
        "# Rol:     {rol}\n"
        "# Applicatie: {applicatie}\n"
        "# Versie:  {versie}\n"
        "# Auteur:  {auteur}\n"
        "# Changes: {versie} - Baseline (header automatisch toegevoegd).\n\n"
    ),
    ".ini": (
        "# File:    {file}\n"
        "# Rol:     {rol}\n"
        "# Applicatie: {applicatie}\n"
        "# Versie:  {versie}\n"
        "# Auteur:  {auteur}\n"
        "# Changes: {versie} - Baseline (header automatisch toegevoegd).\n\n"
    ),
    ".yaml": (
        "# File:    {file}\n"
        "# Rol:     {rol}\n"
        "# Applicatie: {applicatie}\n"
        "# Versie:  {versie}\n"
        "# Auteur:  {auteur}\n"
        "# Changes: {versie} - Baseline (header automatisch toegevoegd).\n\n"
    ),
    ".yml": (
        "# File:    {file}\n"
        "# Rol:     {rol}\n"
        "# Applicatie: {applicatie}\n"
        "# Versie:  {versie}\n"
        "# Auteur:  {auteur}\n"
        "# Changes: {versie} - Baseline (header automatisch toegevoegd).\n\n"
    ),
}


def get_template_for_extension(extension: str) -> Optional[str]:
    """Geeft het headertemplate voor een extensie, of None indien niet ondersteund."""
    return EXTENSION_TEMPLATES.get(extension.lower())


# ============================================================
# LABEL-ALIASSEN — meerdere headervocabularia naar één interne sleutel
# ============================================================
# Volgorde binnen elke lijst bepaalt voorrang bij een eventueel dubbele
# match (komt in de praktijk niet voor, want elke header gebruikt één
# vocabularium consistent).
_LABEL_ALIASES: Dict[str, list] = {
    "bestandsnaam": ["bestandsnaam", "file"],
    "beschrijving": ["beschrijving", "rol", "role"],
    "auteur": ["auteur", "author"],
    "applicatie": ["applicatie", "application"],
    "versie": ["versie", "version"],
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

    Herkent zowel project-doc-tool's eigen headerformaat
    ("Bestandsnaam:"/"Beschrijving:"/...) als Project Generator's
    header_renderer.py-formaat ("File:"/"Rol:"/...). Bestanden worden
    nooit gewijzigd — dit is uitsluitend lezen.
    """
    metadata = _extract_raw_metadata(text)

    metadata["beschrijving"] = metadata["beschrijving"] or DEFAULT_BESCHRIJVING
    metadata["auteur"] = metadata["auteur"] or DEFAULT_AUTEUR
    metadata["applicatie"] = metadata["applicatie"] or DEFAULT_APPLICATIE
    metadata["versie"] = metadata["versie"] or DEFAULT_VERSIE

    return metadata


def is_supported_extension(extension: str) -> bool:
    """Check of een extensie ondersteund wordt voor metadata-extractie."""
    return extension.lower() in EXTENSION_REGISTRY