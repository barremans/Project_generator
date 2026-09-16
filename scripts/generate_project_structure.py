"""
File:    /scripts/generate_project_structure.py
Rol:     Genereert PROJECT_STRUCTURE.md standalone (los van de generatie-
         wizard), tegen Project Generator's eigen projectmap of een
         opgegeven doelmap.
Applicatie: Project Generator
Versie:  1.0.0
Auteur:  Barremans
Changes: 1.0.0 - Baseline. Nieuw script t.b.v. de project-doc-tool-
                  samenvoeging (zie context_ProjectDocTool.md §7.4) — laat
                  core/generate_index.py apart uitvoeren, naar het patroon
                  van scripts/bump_version.py en scripts/validate_project.py.

Gebruik:
    python generate_project_structure.py
        (genereert docs/PROJECT_STRUCTURE.md voor Project Generator zelf)

    python generate_project_structure.py --project-root "C:\\PY\\OpenElements2Csv"
        (genereert PROJECT_STRUCTURE.md voor een andere projectmap)

    python generate_project_structure.py --project-root "C:\\PY\\MijnApp" --output-dir "C:\\PY\\MijnApp\\docs"
"""

import argparse
import sys
from pathlib import Path

# scripts/ staat als submap naast core/ — voeg de project-root toe aan
# sys.path zodat "core.generate_index" geïmporteerd kan worden.
PROJECT_ROOT_DEFAULT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT_DEFAULT))

from core.generate_index import generate_project_structure  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description="Genereer PROJECT_STRUCTURE.md voor een projectmap"
    )
    parser.add_argument(
        "--project-root",
        default=str(PROJECT_ROOT_DEFAULT),
        help="Pad naar de te documenteren projectmap (default: dit project zelf)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Pad waar PROJECT_STRUCTURE.md geschreven wordt (default: <project-root>/docs)",
    )

    args = parser.parse_args()

    project_root = Path(args.project_root)
    output_dir = Path(args.output_dir) if args.output_dir else None

    print(f"📑 Projectstructuur genereren voor: {project_root}")

    try:
        output_file = generate_project_structure(project_root, output_dir)
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    print(f"✅ PROJECT_STRUCTURE.md aangemaakt: {output_file}")


if __name__ == "__main__":
    main()