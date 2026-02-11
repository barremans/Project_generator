"""
core/context.py

Beschrijving: Project context en metadata
Applicatie: Project Generator
Versie: 1.0.0
Auteur: Barremans
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ProjectContext:
    """
    Bevat alle metadata voor het te genereren project.
    """
    app_name: str
    version: str
    author: str
    root_path: Path
    description: str = ""
    create_venv: bool = False
    python_version: str = "3.11"
    
    def __post_init__(self):
        """Valideer en normaliseer de context."""
        if not self.app_name:
            raise ValueError("Applicatienaam mag niet leeg zijn")
        
        if not self.author:
            raise ValueError("Auteur mag niet leeg zijn")
        
        # Converteer string naar Path indien nodig
        if isinstance(self.root_path, str):
            self.root_path = Path(self.root_path)
        
        # Maak absoluut pad
        self.root_path = self.root_path.resolve()
    
    @property
    def project_root(self) -> Path:
        """Volledig pad naar de project root."""
        return self.root_path / self.app_name
    
    @property
    def venv_path(self) -> Path:
        """Pad naar virtuele omgeving."""
        return self.project_root / "venv"
    
    def get_relative_path(self, file_path: Path) -> str:
        """
        Geef relatief pad t.o.v. project root.
        Gebruikt voor headers.
        """
        try:
            return str(file_path.relative_to(self.project_root))
        except ValueError:
            return str(file_path)