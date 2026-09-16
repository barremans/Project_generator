"""
File:    /core/add_headers.py
Rol:     Detecteert ontbrekende/foutieve headers en voegt/herstelt exact
         één correcte header per bestand, in Project Generator's eigen
         headerformaat (header_renderer.py-stijl: File:/Rol:/Applicatie:/
         Versie:/Auteur:/Changes:).
Applicatie: Project Generator
Versie:  2.2.0
Auteur:  Barremans
Changes: 2.2.0 - add_headers() accepteert nu ook "auteur" en "versie" als
                  overrides (naast het al bestaande "applicatie"),
                  aangeroepen vanuit gui/tools_dialog.py met de waarden uit
                  Instellingen (utils/settings.py v1.1.0:
                  default_author/tools_default_versie) — hersteld
                  ontbrekend punt: de originele project-doc-tool-Settings-
                  dialoog liet auteur/applicatie/versie-defaults configu-
                  reren, dat was bij het porten abusievelijk weggevallen.
Changes: 2.1.1 - Gebruikt nu _extract_raw_metadata() i.p.v.
                  extract_metadata_from_text() voor de bestaande-header-
                  check, zodat de "applicatie"-parameter van add_headers()
                  effectief als fallback werkt (zie extension_registry.py
                  v2.3.0 — bugfix gevonden via smoketest).
Changes: 2.1.0 - Geport vanuit project-doc-tool (add_headers.py v2.0.2,
                  auteur Barre) in het kader van de samenvoeging (zie
                  context_ProjectDocTool.md §7.4). Belangrijkste
                  aanpassingen t.o.v. het origineel:
                  (1) Losgekoppeld van project-doc-tool's `settings`-object
                      (project_root/include_exts/exclude_dirs/exclude_files)
                      — nu gewone functieparameters met defaults, consistent
                      met core/generate_index.py.
                  (2) Schrijft voortaan Project Generator's EIGEN
                      headerformaat (File:/Rol:/Applicatie:/Versie:/Auteur:/
                      Changes:) via de bijgewerkte
                      core/extension_registry.py (v2.2.0), i.p.v. het oude
                      Bestandsnaam:/Beschrijving:-vocabularium. Bevestigd
                      door gebruiker als de te schrijven standaard.
                  (3) .json wordt NIET meer behandeld (get_template_for_
                      extension() geeft er nu bewust geen template voor —
                      voorkomt het schrijven van ongeldige "//"-commentaar
                      in JSON-bestanden, een bug in het origineel).
                  (4) _has_header() gebruikt nu has_recognized_header() uit
                      extension_registry.py i.p.v. een harde check op
                      "beschrijving:" — zodat bestanden met een reeds
                      geldige header in ELK herkend vocabularium (inclusief
                      de oude project-doc-tool-stijl) niet onterecht als
                      "NO_HEADER" behandeld worden.
                  (5) BUGFIX: _read_file_start() gebruikte `next(f)` in een
                      generatorexpressie — sinds Python 3.7 (PEP 479) geeft
                      dat een RuntimeError zodra een bestand kórter is dan
                      max_lines, wat door de brede except-clausule stil
                      werd opgevangen als lege string (headerdetectie zou
                      dan altijd "NO_HEADER" geven voor korte bestanden).
                      Vervangen door itertools.islice(), dat correct
                      stopt bij EOF zonder te falen. Zat al zo in het
                      origineel (project-doc-tool add_headers.py v2.0.2).
                  header_engine.py is NIET geport (bevestigd dode code,
                  workers.py riep het nooit aan).
"""

from itertools import islice
from pathlib import Path
from typing import Iterable, List, Dict, Optional, Set

from core.extension_registry import (
    get_template_for_extension,
    _extract_raw_metadata,
    has_recognized_header,
)

# ==================================================
# DEFAULTS
# ==================================================

# .json bewust buiten beschouwing (zie Changes hierboven).
DEFAULT_INCLUDE_EXTS: Set[str] = {".py", ".txt", ".ini", ".yaml", ".yml"}

DEFAULT_EXCLUDE_DIRS: Set[str] = {
    ".git", ".venv", "venv", "__pycache__", "build", "dist", ".vscode",
}
DEFAULT_EXCLUDE_FILES: Set[str] = set()  # add_headers mag __init__.py wél aanvullen

PLACEHOLDER_MARKERS = (
    "{rol}",
    "{auteur}",
    "{applicatie}",
    "{versie}",
    "{file}",
)

DEFAULT_METADATA = {
    "beschrijving": "GEEN BESCHRIJVING",
    "auteur": "GEEN AUTEUR",
    "applicatie": "GEEN APPLICATIE",
    "versie": "V1.0.0",
}

# ==================================================
# DRY-RUN
# ==================================================

def count_headers_to_add(
    project_root: Path,
    include_exts: Optional[Set[str]] = None,
    exclude_dirs: Optional[Set[str]] = None,
    exclude_files: Optional[Set[str]] = None,
) -> List[Dict]:
    """
    Analyseert alle bestanden en geeft per bestand aan: OK / NO_HEADER /
    WRONG_HEADER. Wijzigt niets — bruikbaar voor een dry-run/preview in de GUI.
    """
    actions: List[Dict] = []

    for path in _iter_files(project_root, include_exts, exclude_dirs, exclude_files):
        if not get_template_for_extension(path.suffix):
            continue

        start = _read_file_start(path)

        if not has_recognized_header(start):
            actions.append({"file": path, "status": "NO_HEADER"})
        elif _has_placeholders(start):
            actions.append({"file": path, "status": "WRONG_HEADER"})
        else:
            actions.append({"file": path, "status": "OK"})

    return actions


# ==================================================
# EFFECTIEF TOEVOEGEN
# ==================================================

def add_headers(
    project_root: Path,
    applicatie: str = "GEEN APPLICATIE",
    auteur: Optional[str] = None,
    versie: Optional[str] = None,
    include_exts: Optional[Set[str]] = None,
    exclude_dirs: Optional[Set[str]] = None,
    exclude_files: Optional[Set[str]] = None,
) -> int:
    """
    Voegt headers toe waar nodig, in Project Generator's eigen headerformaat.
    Verwijdert bestaande foutieve/oude headers eerst volledig.

    Args:
        project_root: Root van de te verwerken projectmap.
        applicatie: Applicatienaam voor de "Applicatie:"-regel wanneer een
                     bestand deze nog niet zelf vermeldt.
        auteur: Auteursnaam-fallback wanneer een bestand deze nog niet zelf
                 vermeldt (bv. uit Instellingen: default_author).
        versie: Versie-fallback wanneer een bestand deze nog niet zelf
                 vermeldt (bv. uit Instellingen: tools_default_versie).
        include_exts/exclude_dirs/exclude_files: zie DEFAULT_* hierboven.

    Returns:
        Aantal aangepaste bestanden.
    """
    modified = 0

    for path in _iter_files(project_root, include_exts, exclude_dirs, exclude_files):
        template = get_template_for_extension(path.suffix)
        if not template:
            continue

        original_text = path.read_text(encoding="utf-8", errors="ignore")
        start = _read_file_start(path)

        # Correcte header → niets doen
        if has_recognized_header(start) and not _has_placeholders(start):
            continue

        # Metadata uit bestaande (foutieve) header, indien aanwezig (raw,
        # d.w.z. GEEN defaults al ingevuld — anders zouden de fallbacks
        # hieronder nooit bereikt worden).
        extracted = _extract_raw_metadata(start)

        metadata = {
            "beschrijving": extracted.get("beschrijving") or DEFAULT_METADATA["beschrijving"],
            "auteur": extracted.get("auteur") or auteur or DEFAULT_METADATA["auteur"],
            "applicatie": extracted.get("applicatie") or applicatie or DEFAULT_METADATA["applicatie"],
            "versie": extracted.get("versie") or versie or DEFAULT_METADATA["versie"],
        }

        header = _build_header(project_root, path, template, metadata)
        body = _strip_existing_header(original_text)

        path.write_text(header + body, encoding="utf-8")
        modified += 1

    return modified


# ==================================================
# HEADER OPBOUW
# ==================================================

def _build_header(project_root: Path, path: Path, template: str, meta: dict) -> str:
    """Bouwt een correcte header (Project Generator-formaat) zonder placeholders."""
    try:
        relative_path = "/" + path.relative_to(project_root).as_posix()
    except ValueError:
        relative_path = path.name

    return template.format(
        file=relative_path,
        rol=meta["beschrijving"],
        applicatie=meta["applicatie"],
        versie=meta["versie"],
        auteur=meta["auteur"],
    )


# ==================================================
# HEADER DETECTIE
# ==================================================

def _has_placeholders(text: str) -> bool:
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def _strip_existing_header(text: str) -> str:
    """Verwijdert alle comment/header-regels aan het begin van een bestand."""
    lines = text.splitlines(keepends=True)
    index = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith(("#", "//", "/*", "*", '"""', "'''")):
            index = i + 1
            continue

        break

    return "".join(lines[index:])


# ==================================================
# FILE ITERATOR
# ==================================================

def _iter_files(
    project_root: Path,
    include_exts: Optional[Set[str]],
    exclude_dirs: Optional[Set[str]],
    exclude_files: Optional[Set[str]],
) -> Iterable[Path]:
    root = Path(project_root)
    include_exts = include_exts if include_exts is not None else DEFAULT_INCLUDE_EXTS
    exclude_dirs = exclude_dirs if exclude_dirs is not None else DEFAULT_EXCLUDE_DIRS
    exclude_files = exclude_files if exclude_files is not None else DEFAULT_EXCLUDE_FILES

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if include_exts and path.suffix not in include_exts:
            continue
        if any(part in exclude_dirs for part in path.parts):
            continue
        if path.name in exclude_files:
            continue
        yield path


def _read_file_start(path: Path, max_lines: int = 30) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return "".join(islice(f, max_lines))
    except Exception:
        return ""