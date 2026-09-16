from pathlib import Path
import importlib.util

# Voor Python 3.11+
try:
    import tomllib
except ModuleNotFoundError:
    print("Gebruik Python 3.11+ voor tomllib ondersteuning.")
    raise

import tomli_w  # pip install tomli-w

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = PROJECT_ROOT / "app" / "version.py"
PYPROJECT_FILE = PROJECT_ROOT / "pyproject.toml"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"


# ---------------------------
# Versie uitlezen uit version.py
# ---------------------------
def get_version():
    spec = importlib.util.spec_from_file_location("version", VERSION_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "__version__", "0.0.0")


# ---------------------------
# Requirements uitlezen
# ---------------------------
def get_dependencies():
    if not REQUIREMENTS_FILE.exists():
        return []

    deps = []
    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                deps.append(line)
    return deps


def main():
    version = get_version()
    dependencies = get_dependencies()

    project_data = {
        "name": PROJECT_ROOT.name.replace("_", "-"),
        "version": version,
        "description": "Python Project Generator",
        "authors": [{"name": "Barremans"}],
        "readme": "README.md",
        "requires-python": ">=3.10",
        "dependencies": dependencies,
    }

    data = {"project": project_data}

    # Bestaande pyproject laden indien aanwezig
    if PYPROJECT_FILE.exists():
        with open(PYPROJECT_FILE, "rb") as f:
            existing = tomllib.load(f)
    else:
        existing = {}

    existing["project"] = project_data

    with open(PYPROJECT_FILE, "wb") as f:
        tomli_w.dump(existing, f)

    print(f"✅ pyproject.toml aangemaakt/geüpdatet (versie {version})")


if __name__ == "__main__":
    main()
