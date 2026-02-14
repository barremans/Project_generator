"""
scripts/generate_requirements.py

Beschrijving: Genereer requirements.txt uit pyproject.toml
Applicatie: Project Generator
Versie: 1.0.4
Auteur: Barremans

Gebruik:
    python generate_requirements.py
    python generate_requirements.py --dev
    python generate_requirements.py --output requirements-dev.txt --dev
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Genereer requirements.txt uit pyproject.toml"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Inclusief dev dependencies"
    )
    parser.add_argument(
        "--output",
        default="requirements.txt",
        help="Output bestand (default: requirements.txt)"
    )
    
    args = parser.parse_args()
    
    # Zoek pyproject.toml
    project_root = Path(__file__).parent.parent
    toml_file = project_root / "pyproject.toml"
    
    if not toml_file.exists():
        print(f"❌ Fout: {toml_file} niet gevonden")
        sys.exit(1)
    
    # Probeer tomli te importeren
    try:
        import tomli
    except ImportError:
        print("❌ Fout: tomli is vereist")
        print("Installeer met: pip install tomli")
        sys.exit(1)
    
    # Lees TOML
    with open(toml_file, "rb") as f:
        data = tomli.load(f)
    
    # Verzamel dependencies
    requirements = []
    
    # Runtime dependencies
    if "project" in data and "dependencies" in data["project"]:
        requirements.extend(data["project"]["dependencies"])
    
    # Dev dependencies (optioneel)
    if args.dev:
        if "project" in data and "optional-dependencies" in data["project"]:
            if "dev" in data["project"]["optional-dependencies"]:
                requirements.extend(data["project"]["optional-dependencies"]["dev"])
    
    if not requirements:
        print("⚠️  Geen dependencies gevonden in pyproject.toml")
        sys.exit(0)
    
    # Schrijf naar output
    output_file = project_root / args.output
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Gegenereerd uit pyproject.toml\n")
        f.write("# Regenereer met: python scripts/generate_requirements.py\n")
        f.write("\n")
        for req in requirements:
            f.write(f"{req}\n")
    
    print(f"✅ {len(requirements)} dependencies geschreven naar {output_file}")
    
    if args.dev:
        print("ℹ️  Inclusief dev dependencies")
    
    print()
    print("📦 Dependencies:")
    for req in requirements:
        print(f"   - {req}")


if __name__ == "__main__":
    main()