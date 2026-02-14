"""
utils/settings.py

Beschrijving: Settings manager voor applicatie configuratie
Applicatie: Project Generator
Versie: 1.0.5
Auteur: Barremans
"""

import json
from pathlib import Path
from typing import Optional


class AppSettings:
    """Beheer applicatie settings."""
    
    def __init__(self):
        self.settings_dir = Path.home() / ".project_generator"
        self.settings_file = self.settings_dir / "settings.json"
        self._data = self._load()
    
    def _load(self) -> dict:
        """Laad settings van disk."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "default_author": "",
            "default_project_root": "C:\\",
            "editor_path": "code",
            "locale": "nl_NL"  # ← NIEUW
        }
    
    def save(self) -> bool:
        """Sla settings op naar disk."""
        try:
            self.settings_dir.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    @property
    def default_author(self) -> str:
        return self._data.get("default_author", "")
    
    @default_author.setter
    def default_author(self, value: str):
        self._data["default_author"] = value
    
    @property
    def default_project_root(self) -> str:
        return self._data.get("default_project_root", "C:\\")
    
    @default_project_root.setter
    def default_project_root(self, value: str):
        self._data["default_project_root"] = value
    
    @property
    def editor_path(self) -> str:
        return self._data.get("editor_path", "code")
    
    @editor_path.setter
    def editor_path(self, value: str):
        self._data["editor_path"] = value
    
    @property
    def locale(self) -> str:  # ← NIEUW
        return self._data.get("locale", "nl_NL")
    
    @locale.setter
    def locale(self, value: str):  # ← NIEUW
        self._data["locale"] = value