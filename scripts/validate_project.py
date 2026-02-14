"""
scripts/validate_project.py

Beschrijving: Valideer project structuur en configuratie
Applicatie: Project Generator
Versie: 1.0.4
Auteur: Barremans

Gebruik:
    python validate_project.py
"""

import sys
from pathlib import Path
import subprocess


def check_file_exists(file_path: Path, required: bool = True) -> bool:
    """Check of bestand bestaat."""
    exists = file_path.exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {file_path.name}")
    return exists or not required


def check_folder_exists(folder_path: Path, required: bool = True) -> bool:
    """Check of folder bestaat."""
    exists = folder_path.exists() and folder_path.is_dir()
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {folder_path.name}/")
    return exists or not required


def validate_toml(toml_file: Path) -> bool:
    """Valideer pyproject.toml."""
    if not toml_file.exists():
        return False
    
    try:
        import tomli
        with open(toml_file, "rb") as f:
            data = tomli.load(f)
        
        # Check vereiste velden
        if "project" not in data:
            print("   ⚠️  Geen [project] sectie")
            return False
        
        required_fields = ["name", "version"]
        for field in required_fields:
            if field not in data["project"]:
                print(f"   ⚠️  Veld '{field}' ontbreekt")
                return False
        
        print(f"   ✅ Valide TOML (v{data['project']['version']})")
        return True
        
    except Exception as e:
        print(f"   ❌ TOML parse fout: {e}")
        return False


def run_tests() -> bool:
    """Run pytest."""
    try:
        result = subprocess.run(
            ["pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("   ✅ Alle tests slagen")
            return True
        else:
            print(f"   ❌ Tests gefaald (exit code {result.returncode})")
            return False
    except FileNotFoundError:
        print("   ⚠️  pytest niet gevonden (installeer met: pip install pytest)")
        return True  # Niet kritiek
    except subprocess.TimeoutExpired:
        print("   ⚠️  Tests timeout")
        return False


def check_code_style() -> bool:
    """Check code style met black --check."""
    try:
        result = subprocess.run(
            ["black", "--check", "app", "helpers", "utils"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("   ✅ Code formatting OK")
            return True
        else:
            print("   ⚠️  Code niet geformatteerd (run: make format)")
            return True  # Niet kritiek
    except FileNotFoundError:
        print("   ⚠️  black niet gevonden")
        return True
    except subprocess.TimeoutExpired:
        print("   ⚠️  Black timeout")
        return True


def main():
    print("=" * 60)
    print("🔍 Project Validatie")
    print("=" * 60)
    print()
    
    project_root = Path(__file__).parent.parent
    all_ok = True
    
    # Check bestanden
    print("📄 Bestanden:")
    all_ok &= check_file_exists(project_root / "pyproject.toml")
    all_ok &= check_file_exists(project_root / "README.md")
    all_ok &= check_file_exists(project_root / "LICENSE")
    all_ok &= check_file_exists(project_root / "requirements.txt", required=False)
    all_ok &= check_file_exists(project_root / ".gitignore")
    print()
    
    # Check folders
    print("📁 Folders:")
    all_ok &= check_folder_exists(project_root / "app")
    all_ok &= check_folder_exists(project_root / "tests")
    all_ok &= check_folder_exists(project_root / "assets")
    all_ok &= check_folder_exists(project_root / "css")
    all_ok &= check_folder_exists(project_root / "scripts")
    all_ok &= check_folder_exists(project_root / "venv", required=False)
    print()
    
    # Valideer pyproject.toml
    print("⚙️  Configuratie:")
    all_ok &= validate_toml(project_root / "pyproject.toml")
    print()
    
    # Run tests
    print("🧪 Tests:")
    all_ok &= run_tests()
    print()
    
    # Check code style
    print("🎨 Code Style:")
    all_ok &= check_code_style()
    print()
    
    # Resultaat
    print("=" * 60)
    if all_ok:
        print("✅ Validatie geslaagd!")
    else:
        print("❌ Validatie gefaald - zie bovenstaande fouten")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()