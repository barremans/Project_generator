"""
core/header_renderer.py

Beschrijving: Genereert headers per bestandsextensie
Applicatie: Project Generator
Versie: 1.0.0
Auteur: Barremans
"""

from typing import Dict, Callable
from core.context import ProjectContext


class HeaderRenderer:
    """
    Genereert correcte headers op basis van bestandsextensie.
    """
    
    # Mapping: extensie -> render functie
    _renderers: Dict[str, Callable] = {}
    
    def __init__(self, context: ProjectContext):
        self.context = context
        self._setup_renderers()
    
    def _setup_renderers(self):
        """Registreer alle header renderers."""
        self._renderers = {
            '.py': self._render_python,
            '.json': self._render_json,
            '.md': self._render_markdown,
            '.txt': self._render_txt,
            '.bat': self._render_bat,
            '.spec': self._render_spec,
            '.gitignore': self._render_plain,
            '.qss': self._render_qss,
        }
    
    def render(self, relative_path: str, description: str = "") -> str:
        """
        Genereer header voor een bestand.
        
        Args:
            relative_path: Relatief pad (bijv. "app/main.py")
            description: Optionele beschrijving
            
        Returns:
            Volledige header als string
        """
        # Bepaal extensie
        if '.' in relative_path:
            ext = '.' + relative_path.rsplit('.', 1)[1]
        else:
            ext = relative_path  # Voor .gitignore etc
        
        # Zoek juiste renderer
        renderer = self._renderers.get(ext, self._render_default)
        
        return renderer(relative_path, description)
    
    def _render_python(self, path: str, desc: str) -> str:
        """Python docstring header."""
        return f'''"""
{path}

Beschrijving: {desc}
Applicatie: {self.context.app_name}
Versie: {self.context.version}
Auteur: {self.context.author}
"""

'''
    
    def _render_json(self, path: str, desc: str) -> str:
        """JSON heeft geen officiële comments - lege string."""
        return ""
    
    def _render_markdown(self, path: str, desc: str) -> str:
        """Markdown HTML comment."""
        return f'''<!--
{path}

Beschrijving: {desc}
Applicatie: {self.context.app_name}
Versie: {self.context.version}
Auteur: {self.context.author}
-->

'''
    
    def _render_txt(self, path: str, desc: str) -> str:
        """Tekstbestand met # comments."""
        return f'''# {path}
#
# Beschrijving: {desc}
# Applicatie: {self.context.app_name}
# Versie: {self.context.version}
# Auteur: {self.context.author}

'''
    
    def _render_bat(self, path: str, desc: str) -> str:
        """Batch bestand met REM header."""
        return f'''REM ============================================================
REM {path}
REM 
REM Beschrijving: {desc}
REM Applicatie: {self.context.app_name}
REM Versie: {self.context.version}
REM Auteur: {self.context.author}
REM ============================================================

'''
    
    def _render_spec(self, path: str, desc: str) -> str:
        """PyInstaller spec bestand."""
        return f'''# -*- mode: python ; coding: utf-8 -*-
# {path}
#
# Beschrijving: {desc}
# Applicatie: {self.context.app_name}
# Versie: {self.context.version}
# Auteur: {self.context.author}

'''
    
    def _render_qss(self, path: str, desc: str) -> str:
        """Qt StyleSheet - CSS-style comments."""
        return f'''/*
{path}

Beschrijving: {desc}
Applicatie: {self.context.app_name}
Versie: {self.context.version}
Auteur: {self.context.author}
*/

'''
    
    def _render_plain(self, path: str, desc: str) -> str:
        """Geen header (bijv. .gitignore)."""
        return ""
    
    def _render_default(self, path: str, desc: str) -> str:
        """Fallback: hash comments."""
        return f'''# {path}
# Beschrijving: {desc}
# Applicatie: {self.context.app_name}
# Versie: {self.context.version}
# Auteur: {self.context.author}

'''