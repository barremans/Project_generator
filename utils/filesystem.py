"""
utils/filesystem.py

Beschrijving: Filesystem helper functies
Applicatie: Project Generator
Versie: 1.0.0
Auteur: Barremans
"""

from pathlib import Path
from typing import Optional
import shutil


def ensure_directory(path: Path) -> bool:
    """
    Zorg dat een directory bestaat.
    
    Args:
        path: Pad naar de directory
        
    Returns:
        True als succesvol, False bij fout
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"❌ Fout bij aanmaken directory {path}: {e}")
        return False


def write_file(path: Path, content: str, encoding: str = 'utf-8') -> bool:
    """
    Schrijf inhoud naar een bestand.
    
    Args:
        path: Pad naar het bestand
        content: Inhoud om te schrijven
        encoding: Encoding (standaard utf-8)
        
    Returns:
        True als succesvol, False bij fout
    """
    try:
        # Zorg dat parent directory bestaat
        ensure_directory(path.parent)
        
        # Schrijf bestand
        path.write_text(content, encoding=encoding)
        return True
    except Exception as e:
        print(f"❌ Fout bij schrijven bestand {path}: {e}")
        return False


def path_exists(path: Path) -> bool:
    """Check of een pad bestaat."""
    return path.exists()


def is_directory_empty(path: Path) -> bool:
    """
    Check of een directory leeg is.
    
    Args:
        path: Pad naar de directory
        
    Returns:
        True als leeg of niet bestaand, False als er items in zitten
    """
    if not path.exists():
        return True
    
    if not path.is_dir():
        return False
    
    return len(list(path.iterdir())) == 0


def remove_directory(path: Path) -> bool:
    """
    Verwijder een directory en alle inhoud.
    
    Args:
        path: Pad naar de directory
        
    Returns:
        True als succesvol, False bij fout
    """
    try:
        if path.exists():
            shutil.rmtree(path)
        return True
    except Exception as e:
        print(f"❌ Fout bij verwijderen directory {path}: {e}")
        return False