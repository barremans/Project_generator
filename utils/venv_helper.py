"""
File:    /utils/venv_helper.py
Rol:     Helper voor virtuele omgeving setup
Applicatie: Project Generator
Versie:  1.0.1
Auteur:  Barremans
Changes: 1.0.1 - BUGFIX: alle paden gebruikten "venv" i.p.v. ".venv" —
                  nu consistent met context.py en de CGK-conventie.
                  Let op: deze functies dupliceren generator.py's
                  ProjectGenerator._create_venv()/_get_export_script_template()
                  en worden momenteel nergens aangeroepen — overweeg één van
                  beide implementaties te laten vervallen.
Changes: 1.0.0 - Baseline.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, List


def create_venv(project_root: Path, python_exe: Optional[str] = None) -> bool:
    """
    Maak virtuele omgeving aan in project.
    
    Args:
        project_root: Root directory van het project
        python_exe: Optioneel specifiek Python executable pad
        
    Returns:
        True als succesvol
    """
    venv_path = project_root / ".venv"
    
    # Gebruik opgegeven Python of huidige interpreter
    python_cmd = python_exe if python_exe else sys.executable
    
    print(f"🐍 Virtuele omgeving aanmaken in: {venv_path}")
    print(f"   Python: {python_cmd}")
    
    try:
        # Maak venv
        subprocess.run(
            [python_cmd, "-m", "venv", str(venv_path)],
            check=True,
            capture_output=True,
            text=True
        )
        
        print(f"✅ Venv aangemaakt")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fout bij aanmaken venv: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return False


def upgrade_pip(project_root: Path) -> bool:
    """
    Upgrade pip in de virtuele omgeving.
    
    Args:
        project_root: Root directory van het project
        
    Returns:
        True als succesvol
    """
    pip_path = project_root / ".venv" / "Scripts" / "pip.exe"
    
    if not pip_path.exists():
        print(f"❌ Pip niet gevonden: {pip_path}")
        return False
    
    print("📦 Pip upgraden...")
    
    try:
        subprocess.run(
            [str(pip_path), "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
            text=True
        )
        
        print("✅ Pip geüpgraded")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fout bij upgraden pip: {e.stderr}")
        return False


def install_requirements(project_root: Path, packages: Optional[List[str]] = None) -> bool:
    """
    Installeer packages in virtuele omgeving.
    
    Args:
        project_root: Root directory van het project
        packages: Lijst van package namen (bijv. ["PyQt6", "requests"])
        
    Returns:
        True als succesvol
    """
    pip_path = project_root / ".venv" / "Scripts" / "pip.exe"
    
    if not pip_path.exists():
        print(f"❌ Pip niet gevonden: {pip_path}")
        return False
    
    # Check of requirements.txt bestaat
    req_file = project_root / "requirements.txt"
    
    if packages:
        # Installeer specifieke packages
        print(f"📦 Installeren: {', '.join(packages)}")
        
        try:
            subprocess.run(
                [str(pip_path), "install"] + packages,
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Packages geïnstalleerd")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Fout bij installeren: {e.stderr}")
            return False
    
    elif req_file.exists():
        # Installeer vanuit requirements.txt
        print(f"📦 Installeren vanuit requirements.txt")
        
        try:
            subprocess.run(
                [str(pip_path), "install", "-r", str(req_file)],
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Requirements geïnstalleerd")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Fout bij installeren: {e.stderr}")
            return False
    
    else:
        print("ℹ️  Geen packages opgegeven en geen requirements.txt gevonden")
        return True


def setup_complete_venv(project_root: Path, 
                       python_exe: Optional[str] = None,
                       packages: Optional[List[str]] = None) -> bool:
    """
    Volledige venv setup: aanmaken + pip upgrade + packages installeren.
    
    Args:
        project_root: Root directory van het project
        python_exe: Optioneel specifiek Python executable pad
        packages: Optionele lijst van te installeren packages
        
    Returns:
        True als alles succesvol
    """
    print("=" * 60)
    print("🔧 VIRTUELE OMGEVING SETUP")
    print("=" * 60)
    
    # Stap 1: Maak venv
    if not create_venv(project_root, python_exe):
        return False
    
    # Stap 2: Upgrade pip
    if not upgrade_pip(project_root):
        print("⚠️  Pip upgrade gefaald, maar venv bestaat")
    
    # Stap 3: Installeer packages
    if packages or (project_root / "requirements.txt").exists():
        if not install_requirements(project_root, packages):
            print("⚠️  Package installatie gefaald, maar venv bestaat")
    
    print()
    print("=" * 60)
    print("✅ VENV SETUP COMPLEET")
    print("=" * 60)
    print()
    print("📝 Activeren:")
    print(f"   {project_root / '.venv' / 'Scripts' / 'activate.bat'}")
    print()
    
    return True