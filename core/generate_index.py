"""
File:    /core/generate_index.py
Rol:     Genereert PROJECT_STRUCTURE.md — een markdown-boomoverzicht van een
         projectmap, met per ondersteund bestand de uitgelezen headermetadata
         als fenced code-block. Bestanden worden nooit gewijzigd (read-only).
Applicatie: Project Generator
Versie:  2.4.0
Auteur:  Barremans
Changes: 2.4.0 - Geport vanuit project-doc-tool (generate_index_v2.py
                  v2.3.0, auteur Barre) in het kader van de samenvoeging
                  (zie context_ProjectDocTool.md §7.4). De afhankelijkheid
                  van project-doc-tool's `core.settings.Settings`-klasse
                  (project_root/output_dir/is_excluded()/is_supported_file())
                  is vervangen door gewone functieparameters — Project
                  Generator heeft geen equivalente Settings-klasse (zijn
                  utils/settings.py::AppSettings bewaart enkel
                  auteur/projectmap/editor/taal-voorkeuren, geen
                  scan-instellingen) en dit maakt de functie generiek
                  herbruikbaar (automatisch na generatie, én standalone via
                  scripts/generate_project_structure.py). Walk-, filter- en
                  outputlogica ongewijzigd overgenomen. Gebruikt
                  extract_metadata_from_text() uit het bijgewerkte
                  core/extension_registry.py (v2.1.0, herkent nu ook Project
                  Generator's eigen headerformaat).
"""

from pathlib import Path
from typing import List, Optional, Set

from core.extension_registry import EXTENSION_REGISTRY, extract_metadata_from_text

# Standaard uitgesloten mappen/bestanden voor een gegenereerd CGK-project.
# Losstaand configureerbaar per aanroep — dit zijn enkel de defaults.
DEFAULT_EXCLUDE_DIRS: Set[str] = {
    ".git", ".venv", "venv", "__pycache__", "build", "dist", ".vscode",
}
DEFAULT_EXCLUDE_FILES: Set[str] = {
    "__init__.py",
}


def generate_project_structure(
    project_root: Path,
    output_dir: Optional[Path] = None,
    exclude_dirs: Optional[Set[str]] = None,
    exclude_files: Optional[Set[str]] = None,
) -> Path:
    """
    Genereert PROJECT_STRUCTURE.md voor de opgegeven projectmap.

    Args:
        project_root: Root van het te documenteren project.
        output_dir: Map waarin PROJECT_STRUCTURE.md geschreven wordt.
                     Standaard: <project_root>/docs.
        exclude_dirs: Mapnamen die volledig overgeslagen worden.
                       Standaard: DEFAULT_EXCLUDE_DIRS.
        exclude_files: Bestandsnamen die volledig overgeslagen worden.
                        Standaard: DEFAULT_EXCLUDE_FILES.

    Returns:
        Path naar het geschreven PROJECT_STRUCTURE.md-bestand.

    Raises:
        RuntimeError: Wanneer project_root niet bestaat of geen map is.
    """
    root = Path(project_root)

    if not root.exists():
        raise RuntimeError(f"Projectmap bestaat niet: {root}")
    if not root.is_dir():
        raise RuntimeError(f"Projectpad is geen map: {root}")

    out_dir = Path(output_dir) if output_dir else root / "docs"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_file = out_dir / "PROJECT_STRUCTURE.md"

    exclude_dirs = exclude_dirs if exclude_dirs is not None else DEFAULT_EXCLUDE_DIRS
    exclude_files = exclude_files if exclude_files is not None else DEFAULT_EXCLUDE_FILES

    lines: List[str] = [
        "# 📁 Projectstructuur",
        "",
        "_Automatisch gegenereerd – niet handmatig aanpassen._",
        "",
        f"- 📁 **{root.name}/**",
    ]

    def is_excluded(path: Path) -> bool:
        try:
            if path.is_dir():
                return path.name in exclude_dirs
            return path.name in exclude_files
        except OSError:
            return False

    def is_supported_file(path: Path) -> bool:
        return path.suffix.lower() in EXTENSION_REGISTRY

    def append_metadata(file_path: Path, indent: int) -> None:
        """Leest en voegt metadata toe voor ondersteunde bestanden (read-only)."""
        if not is_supported_file(file_path):
            return

        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeError):
            return

        try:
            metadata = extract_metadata_from_text(text)
        except Exception:
            return

        if not metadata or not any(metadata.values()):
            return

        prefix = "  " * indent
        lines.append(f"{prefix}```text")

        if metadata.get("bestandsnaam"):
            lines.append(f"{prefix}# Bestandsnaam: {metadata['bestandsnaam']}")
        if metadata.get("beschrijving"):
            lines.append(f"{prefix}# Beschrijving: {metadata['beschrijving']}")
        if metadata.get("auteur"):
            lines.append(f"{prefix}# Auteur: {metadata['auteur']}")
        if metadata.get("applicatie"):
            lines.append(f"{prefix}# Applicatie: {metadata['applicatie']}")
        if metadata.get("versie"):
            lines.append(f"{prefix}# Versie: {metadata['versie']}")

        lines.append(f"{prefix}```")

    def walk(current: Path, indent: int) -> None:
        try:
            entries = sorted(
                current.iterdir(),
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except (OSError, PermissionError):
            return

        for entry in entries:
            if is_excluded(entry):
                continue

            prefix = "  " * indent

            try:
                is_directory = entry.is_dir()
                is_file = entry.is_file()
            except OSError:
                continue

            if is_directory:
                lines.append(f"{prefix}- 📁 **{entry.name}/**")
                walk(current=entry, indent=indent + 1)
                continue

            if not is_file:
                continue

            try:
                relative_path = entry.relative_to(root).as_posix()
            except ValueError:
                relative_path = entry.name

            lines.append(f"{prefix}- 📄 **/{relative_path}**")
            append_metadata(file_path=entry, indent=indent + 1)

    walk(current=root, indent=1)

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_file