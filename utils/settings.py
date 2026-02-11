"""
utils/settings.py

Beschrijving: Applicatie settings beheer
Applicatie: Project Generator
Versie: 1.0.3
Auteur: Barremans
"""

import json
from pathlib import Path
from typing import Optional


class AppSettings:
    """
    Beheer applicatie instellingen.
    """
    
    def __init__(self):
        self.settings_file = Path.home() / ".project_generator" / "settings.json"
        self.settings = self._load_settings()
    
    def _load_settings(self) -> dict:
        """Laad settings uit bestand."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Fout bij laden settings: {e}")
                return self._get_default_settings()
        else:
            return self._get_default_settings()
    
    def _get_default_settings(self) -> dict:
        """Standaard instellingen."""
        return {
            "default_author": "",
            "default_project_root": "C:\\",
            "editor_path": "code",
            "version": "1.0.3"
        }
    
    def save(self):
        """Sla settings op naar bestand."""
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Fout bij opslaan settings: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Haal een setting op."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        """Zet een setting."""
        self.settings[key] = value
    
    @property
    def default_author(self) -> str:
        """Standaard auteur."""
        return self.get("default_author", "")
    
    @default_author.setter
    def default_author(self, value: str):
        self.set("default_author", value)
    
    @property
    def default_project_root(self) -> str:
        """Standaard project root."""
        return self.get("default_project_root", "C:\\")
    
    @default_project_root.setter
    def default_project_root(self, value: str):
        self.set("default_project_root", value)
    
    @property
    def editor_path(self) -> str:
        """Pad naar editor."""
        return self.get("editor_path", "code")
    
    @editor_path.setter
    def editor_path(self, value: str):
        self.set("editor_path", value)