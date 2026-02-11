"""
core/templates.py

Beschrijving: Template definities voor projectstructuur
Applicatie: Project Generator
Versie: 1.0.0
Auteur: Barremans
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path


@dataclass
class FileTemplate:
    """
    Template voor een enkel bestand.
    """
    name: str                          # Bestandsnaam (bijv. "main.py")
    description: str = ""              # Beschrijving voor in header
    template_body: str = ""            # Standaard inhoud (na header)
    
    @property
    def extension(self) -> str:
        """Haal extensie op uit bestandsnaam."""
        if '.' in self.name:
            return '.' + self.name.rsplit('.', 1)[1]
        return self.name  # Voor .gitignore etc
    
    def __repr__(self) -> str:
        return f"FileTemplate(name='{self.name}')"


@dataclass
class FolderTemplate:
    """
    Template voor een map met submappen en bestanden.
    """
    name: str                                      # Mapnaam
    python_package: bool = False                   # Automatisch __init__.py toevoegen?
    files: List[FileTemplate] = field(default_factory=list)
    subfolders: List['FolderTemplate'] = field(default_factory=list)
    
    def add_file(self, name: str, description: str = "", body: str = "") -> 'FolderTemplate':
        """Voeg bestand toe (fluent interface)."""
        self.files.append(FileTemplate(name=name, description=description, template_body=body))
        return self
    
    def add_subfolder(self, folder: 'FolderTemplate') -> 'FolderTemplate':
        """Voeg submap toe (fluent interface)."""
        self.subfolders.append(folder)
        return self
    
    def __repr__(self) -> str:
        return f"FolderTemplate(name='{self.name}', files={len(self.files)}, subfolders={len(self.subfolders)})"


@dataclass
class ProjectTemplate:
    """
    Hoofdtemplate voor een volledig project.
    """
    name: str
    version: str
    author: str
    description: str = ""
    create_venv: bool = False
    python_version: str = "3.11"
    
    root_folders: List[FolderTemplate] = field(default_factory=list)
    root_files: List[FileTemplate] = field(default_factory=list)
    
    def add_folder(self, folder: FolderTemplate) -> 'ProjectTemplate':
        """Voeg root folder toe."""
        self.root_folders.append(folder)
        return self
    
    def add_file(self, name: str, description: str = "", body: str = "") -> 'ProjectTemplate':
        """Voeg root file toe."""
        self.root_files.append(FileTemplate(name=name, description=description, template_body=body))
        return self
    
    def __repr__(self) -> str:
        return f"ProjectTemplate(name='{self.name}', folders={len(self.root_folders)}, files={len(self.root_files)})"