"""
scripts/bump_version.py

Beschrijving: Verhoog versienummer overal in het project
Applicatie: Project Generator
Versie: 1.0.6
Auteur: Barremans

Changes: 1.0.6 - BUGFIX: interactieve "Doorgaan met update naar X? (y/n)"-
                  bevestiging verwijderd. Dit script wordt uitsluitend
                  niet-interactief aangeroepen vanuit build_installer.bat
                  (scripts\\bump_version.py %PART_TO_BUMP%, zelf weer
                  aangestuurd via AS_BUMP_PART vanuit
                  build_and_publish.ps1) -- de bump_type/--version-keuze
                  is op dat moment al expliciet gemaakt, dus een extra
                  bevestiging hier voegt niets toe en blokkeert enkel de
                  bedoeld volledig geautomatiseerde build_and_publish-flow
                  (moest telkens manueel met "y" bevestigd worden).
Changes: 1.0.5 - BUGFIX: verwachtte een generiek "docs/changelog.md", dat
                  bij Project Generator nooit bestaan heeft (dit project
                  gebruikt bilingual "docs/CHANGELOG_nl_NL.md" +
                  "docs/CHANGELOG_en_US.md", zie 03-i18n-conventions.md).
                  Update-target aangepast naar die 2 echte bestanden
                  (elk met hun eigen sectiekoppen: Toegevoegd/Gewijzigd/
                  Opgelost voor NL, Added/Changed/Fixed voor EN). Verder
                  BUGFIX: een ontbrekende of mislukte changelog-update telt
                  niet langer mee in de globale success-flag -- dit blokkeerde
                  eerder de volledige versiebump (en dus de hele
                  build_and_publish.ps1-flow), terwijl app/version.py en
                  pyproject.toml intussen al wel degelijk correct
                  bijgewerkt waren. De changelog-stap is nu puur
                  informatief/advies (voegt een lege sectie toe om zelf
                  aan te vullen); geen enkele reden om de versiebump zelf
                  daarom te laten falen.

Gebruik:
    python bump_version.py patch   # 1.0.0 -> 1.0.1
    python bump_version.py minor   # 1.0.0 -> 1.1.0
    python bump_version.py major   # 1.0.0 -> 2.0.0
    python bump_version.py --version 2.5.3
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import date


def parse_version(version_str: str) -> tuple:
    """Parse version string to (major, minor, patch)."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if not match:
        raise ValueError(f"Ongeldige versie: {version_str}")
    return tuple(map(int, match.groups()))


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple to string."""
    return f"{major}.{minor}.{patch}"


def bump_version(current: str, bump_type: str) -> str:
    """Bump version based on type."""
    major, minor, patch = parse_version(current)

    if bump_type == "major":
        return format_version(major + 1, 0, 0)
    elif bump_type == "minor":
        return format_version(major, minor + 1, 0)
    elif bump_type == "patch":
        return format_version(major, minor, patch + 1)
    else:
        raise ValueError(f"Onbekend bump type: {bump_type}")


def update_version_py(file_path: Path, new_version: str) -> bool:
    """Update app/version.py."""
    if not file_path.exists():
        print(f"⚠️  {file_path} niet gevonden")
        return False

    content = file_path.read_text(encoding="utf-8")
    new_content = re.sub(
        r'__version__\s*=\s*["\'][\d.]+["\']',
        f'__version__ = "{new_version}"',
        content
    )

    file_path.write_text(new_content, encoding="utf-8")
    print(f"✅ {file_path} bijgewerkt")
    return True


def update_pyproject_toml(file_path: Path, new_version: str) -> bool:
    """Update pyproject.toml."""
    if not file_path.exists():
        print(f"⚠️  {file_path} niet gevonden")
        return False

    try:
        import tomli
        import tomli_w
    except ImportError:
        print("⚠️  tomli/tomli_w niet beschikbaar, gebruik regex fallback")
        content = file_path.read_text(encoding="utf-8")
        new_content = re.sub(
            r'version\s*=\s*["\'][\d.]+["\']',
            f'version = "{new_version}"',
            content
        )
        file_path.write_text(new_content, encoding="utf-8")
        print(f"✅ {file_path} bijgewerkt (regex)")
        return True

    with open(file_path, "rb") as f:
        data = tomli.load(f)

    if "project" in data:
        data["project"]["version"] = new_version

    with open(file_path, "wb") as f:
        tomli_w.dump(data, f)

    print(f"✅ {file_path} bijgewerkt")
    return True


def update_changelog(file_path: Path, new_version: str, lang: str = "nl") -> bool:
    """
    Voeg nieuwe (lege) sectie toe aan een changelog-bestand.

    lang: "nl" -> Toegevoegd/Gewijzigd/Opgelost, "en" -> Added/Changed/Fixed.
    Puur informatief -- de aanroeper laat dit NIET meetellen voor de
    globale success-flag (zie module-changelog v1.0.5 hierboven).
    """
    if not file_path.exists():
        print(f"⚠️  {file_path} niet gevonden (changelog-stap overgeslagen)")
        return False

    today = date.today().strftime("%Y-%m-%d")
    content = file_path.read_text(encoding="utf-8")

    if lang == "en":
        new_section = f"""## [{new_version}] - {today}

### Added
- 

### Changed
- 

### Fixed
- 

"""
    else:
        new_section = f"""## [{new_version}] - {today}

### Toegevoegd
- 

### Gewijzigd
- 

### Opgelost
- 

"""

    # Insert na eerste "## [...]"-heading
    lines = content.split("\n")
    insert_index = 0
    for i, line in enumerate(lines):
        if line.startswith("## ["):
            insert_index = i
            break

    if insert_index > 0:
        lines.insert(insert_index, new_section)
        file_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"✅ {file_path} bijgewerkt (lege sectie toegevoegd -- zelf aanvullen)")
        return True
    else:
        print(f"⚠️  Kon insert point niet vinden in {file_path}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Verhoog project versie")
    parser.add_argument(
        "bump_type",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Type versie verhoging"
    )
    parser.add_argument(
        "--version",
        help="Specifieke versie nummer (bijv. 2.5.3)"
    )

    args = parser.parse_args()

    if not args.bump_type and not args.version:
        parser.print_help()
        sys.exit(1)

    # Zoek project root
    project_root = Path(__file__).parent.parent
    version_file = project_root / "app" / "version.py"
    toml_file = project_root / "pyproject.toml"
    changelog_nl = project_root / "docs" / "CHANGELOG_nl_NL.md"
    changelog_en = project_root / "docs" / "CHANGELOG_en_US.md"

    # Lees huidige versie
    if not version_file.exists():
        print(f"❌ {version_file} niet gevonden")
        sys.exit(1)

    current_content = version_file.read_text()
    match = re.search(r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', current_content)

    if not match:
        print("❌ Kon huidige versie niet vinden in app/version.py")
        sys.exit(1)

    current_version = match.group(1)
    print(f"📌 Huidige versie: {current_version}")

    # Bereken nieuwe versie
    if args.version:
        new_version = args.version
        try:
            parse_version(new_version)
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)
    else:
        new_version = bump_version(current_version, args.bump_type)

    print(f"🚀 Nieuwe versie: {new_version}")
    print()

    # Update bestanden -- enkel version.py + pyproject.toml zijn kritiek
    success = True
    success &= update_version_py(version_file, new_version)
    success &= update_pyproject_toml(toml_file, new_version)

    # Changelogs: puur informatief, telt NIET mee voor success (zie v1.0.5)
    update_changelog(changelog_nl, new_version, lang="nl")
    update_changelog(changelog_en, new_version, lang="en")

    print()
    if success:
        print("=" * 60)
        print(f"✅ Versie verhoogd: {current_version} -> {new_version}")
        print("=" * 60)
        print()
        print("📝 Vergeet niet:")
        print("   1. Vul de nieuwe changelog-secties aan in docs/CHANGELOG_nl_NL.md / CHANGELOG_en_US.md")
        print("   2. Commit de changes: git commit -m 'chore: bump version to " + new_version + "'")
        print("   3. Tag de release: git tag v" + new_version)
    else:
        print("⚠️  Kritieke update (version.py/pyproject.toml) mislukt")
        sys.exit(1)


if __name__ == "__main__":
    main()