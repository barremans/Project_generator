"""
utils/settings.py

Beschrijving: Settings manager voor applicatie configuratie
Applicatie: Project Generator
Versie: 1.1.0
Auteur: Barremans
Changes: 1.1.0 - Uitgebreid t.b.v. de project-doc-tool-samenvoeging (zie
                  context_ProjectDocTool.md §7.4): nieuwe properties
                  tools_include_exts / tools_exclude_dirs /
                  tools_exclude_files (persistente configuratie voor
                  core/add_headers.py + core/generate_index.py, i.p.v. de
                  hardcoded DEFAULT_*-constanten in die modules — die
                  blijven wel de fallback wanneer er nog niets opgeslagen
                  is), tools_default_applicatie / tools_default_versie
                  (headerdefaults; auteur hergebruikt bewust het bestaande
                  default_author i.p.v. een apart veld), en
                  tools_last_project_root / tools_last_output_dir (zodat
                  ToolsDialog de laatst gebruikte mappen onthoudt, zoals
                  project-doc-tool's eigen main_window.py ook deed).
"""

import json
from pathlib import Path
from typing import Optional, List


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
            "locale": "nl_NL",
            # ← NIEUW (v1.1.0, tools/project-doc-tool-samenvoeging)
            "tools_include_exts": [".py", ".txt", ".ini", ".yaml", ".yml"],
            "tools_exclude_dirs": [
                ".git", ".venv", "venv", "__pycache__", "build", "dist", ".vscode",
            ],
            "tools_exclude_files": [],
            "tools_default_applicatie": "",
            "tools_default_versie": "1.0.0",
            "tools_last_project_root": "",
            "tools_last_output_dir": "",
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

    # ------------------------------------------------------------
    # Tools (add_headers / generate_index) — NIEUW in v1.1.0
    # ------------------------------------------------------------

    @property
    def tools_include_exts(self) -> List[str]:
        return list(self._data.get("tools_include_exts", [".py", ".txt", ".ini", ".yaml", ".yml"]))

    @tools_include_exts.setter
    def tools_include_exts(self, value: List[str]):
        self._data["tools_include_exts"] = list(value)

    @property
    def tools_exclude_dirs(self) -> List[str]:
        return list(self._data.get(
            "tools_exclude_dirs",
            [".git", ".venv", "venv", "__pycache__", "build", "dist", ".vscode"],
        ))

    @tools_exclude_dirs.setter
    def tools_exclude_dirs(self, value: List[str]):
        self._data["tools_exclude_dirs"] = list(value)

    @property
    def tools_exclude_files(self) -> List[str]:
        return list(self._data.get("tools_exclude_files", []))

    @tools_exclude_files.setter
    def tools_exclude_files(self, value: List[str]):
        self._data["tools_exclude_files"] = list(value)

    @property
    def tools_default_applicatie(self) -> str:
        """Leeg = automatisch afleiden uit de mapnaam (ToolsDialog-gedrag)."""
        return self._data.get("tools_default_applicatie", "")

    @tools_default_applicatie.setter
    def tools_default_applicatie(self, value: str):
        self._data["tools_default_applicatie"] = value

    @property
    def tools_default_versie(self) -> str:
        return self._data.get("tools_default_versie", "1.0.0")

    @tools_default_versie.setter
    def tools_default_versie(self, value: str):
        self._data["tools_default_versie"] = value

    @property
    def tools_last_project_root(self) -> str:
        return self._data.get("tools_last_project_root", "")

    @tools_last_project_root.setter
    def tools_last_project_root(self, value: str):
        self._data["tools_last_project_root"] = value

    @property
    def tools_last_output_dir(self) -> str:
        return self._data.get("tools_last_output_dir", "")

    @tools_last_output_dir.setter
    def tools_last_output_dir(self, value: str):
        self._data["tools_last_output_dir"] = value