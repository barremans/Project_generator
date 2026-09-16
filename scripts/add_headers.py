"""
File:    /scripts/add_headers.py
Rol:     Voegt/herstelt headers standalone (los van de generatie-wizard),
         tegen een opgegeven projectmap. Standaard veilig: dry-run tenzij
         --apply expliciet meegegeven wordt.
Applicatie: Project Generator
Versie:  1.0.0
Auteur:  Barremans
Changes: 1.0.0 - Baseline. Nieuw script t.b.v. de project-doc-tool-
                  samenvoeging (zie context_ProjectDocTool.md §7.4), naar
                  het patroon van scripts/generate_project_structure.py.

Gebruik:
    python add_headers.py --project-root "C:\\PY\\OpenElements2Csv"
        (dry-run: toont wat er zou gebeuren, wijzigt niets)

    python add_headers.py --project-root "C:\\PY\\OpenElements2Csv" --apply
        (voegt/herstelt effectief headers)

    python add_headers.py --project-root "C:\\PY\\MijnApp" --apply --applicatie "MijnApp"
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT_DEFAULT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT_DEFAULT))

from core.add_headers import count_headers_to_add, add_headers  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description="Voeg/herstel headers in een projectmap (Project Generator-formaat)"
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Pad naar de te verwerken projectmap",
    )
    parser.add_argument(
        "--applicatie",
        default="GEEN APPLICATIE",
        help="Applicatienaam voor de 'Applicatie:'-regel bij ontbrekende metadata",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Voer de wijzigingen effectief door (zonder deze vlag: dry-run)",
    )

    args = parser.parse_args()
    project_root = Path(args.project_root)

    if not project_root.exists():
        print(f"❌ Projectmap bestaat niet: {project_root}")
        sys.exit(1)

    if not args.apply:
        print(f"🔍 Dry-run headers voor: {project_root}\n")
        actions = count_headers_to_add(project_root)

        if not actions:
            print("✅ Alle bestanden hebben reeds een correcte header.")
            return

        counts = {"NO_HEADER": 0, "WRONG_HEADER": 0, "OK": 0}
        for item in actions:
            counts[item["status"]] += 1
            if item["status"] != "OK":
                print(f"  {item['status']:<13} {item['file']}")

        print()
        print(f"Samenvatting: {counts['NO_HEADER']} zonder header, "
              f"{counts['WRONG_HEADER']} foutieve header, {counts['OK']} OK.")
        print("ℹ️  Dry-run — geen bestanden aangepast. Run met --apply om door te voeren.")
        return

    print(f"✍  Headers toevoegen/herstellen in: {project_root}\n")
    count = add_headers(project_root, applicatie=args.applicatie)
    print(f"✅ {count} bestand(en) aangepast.")


if __name__ == "__main__":
    main()