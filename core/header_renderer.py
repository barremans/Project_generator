"""
File:    /core/header_renderer.py
Rol:     Genereert headers per bestandsextensie
Applicatie: Project Generator
Versie:  1.2.0
Auteur:  Barremans
Changes: 1.2.0 - Headers voor nieuw-gegenereerde projectbestanden volgen nu
                  dezelfde CGK-conforme stijl als core/extension_registry.py
                  v2.4.0 (zelfde beslissing, één keer doorgevoerd):
                  (1) _render_python: niet langer een docstring, maar een
                      "#"-commentaarblok met "===="-scheidingslijnen,
                      Engelse labels File:/Role:/Version:/Author:/Changes:,
                      en een expliciet "Applicatie:"-label (bevestigde
                      bewuste afwijking t.o.v. de letterlijke conventie,
                      nodig voor generate_index.py's per-bestand metadata).
                  (2) _render_txt: nu het Nederlandse config-bestand-format
                      uit 00-conventions.md §4 (Beschrijving:/Versie:/
                      Auteur:/Applicatie:), geen aparte File:-regel meer.
                  (3) _render_bat/_render_spec: "Rol:" -> "Role:" en
                      "Applicatie:"-label toegevoegd, voor consistentie met
                      _render_python (zelfde Engelse-labelfamilie volgens de
                      conventie).
                  (4) _render_markdown/_render_qss: ongewijzigd gelaten —
                      niet gedekt door een van de formats in
                      00-conventions.md §4, geen beslissing hierover
                      gevraagd/genomen.
Changes: 1.1.0 - Headerformaat aangepast naar de vaste CGK-conventie:
                  toegevoegd "File:"-label (i.p.v. het kale pad op de
                  eerste regel), "Rol:"-veld toegevoegd (i.p.v.
                  "Beschrijving:"), en een "Changes:"-regel met
                  "1.0.0 - Baseline." toegevoegd zodat elk gegenereerd
                  bestand vanaf de start een changelog-spoor heeft. Het
                  binnenkomende pad wordt nu ongewijzigd doorgegeven
                  (context.get_relative_path() levert intussen zelf al
                  het leidende "/").
Changes: 1.0.0 - Baseline.
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
            '.ini': self._render_txt,
            '.yaml': self._render_txt,
            '.yml': self._render_txt,
            '.bat': self._render_bat,
            '.ps1': self._render_bat,
            '.spec': self._render_spec,
            '.gitignore': self._render_plain,
            '.qss': self._render_qss,
        }

    def render(self, relative_path: str, description: str = "") -> str:
        """
        Genereer header voor een bestand.

        Args:
            relative_path: Relatief pad, mét leidend "/" (bijv. "/app/main.py")
            description: Optionele beschrijving (wordt gebruikt als "Role:"/
                          "Beschrijving:", afhankelijk van het bestandstype)

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
        """
        CGK-conform "#"-commentaarblok (00-conventions.md §4, "Python
        (*.py)"-format), met een expliciet "Applicatie:"-label i.p.v. de
        letterlijk-voorgeschreven ongelabelde appnaam-regel (bevestigde
        bewuste afwijking — nodig voor generate_index.py).
        """
        return f'''# =============================================================================
# Applicatie: {self.context.app_name}
# File:    {path}
# Role:    {desc}
# Version: {self.context.version}
# Author:  {self.context.author}
# Changes: {self.context.version} - Baseline.
# =============================================================================

'''

    def _render_json(self, path: str, desc: str) -> str:
        """JSON heeft geen officiële comments - lege string."""
        return ""

    def _render_markdown(self, path: str, desc: str) -> str:
        """Markdown HTML comment. (Niet gedekt door 00-conventions.md §4 — ongewijzigd.)"""
        return f'''<!--
File:    {path}
Rol:     {desc}
Applicatie: {self.context.app_name}
Versie:  {self.context.version}
Auteur:  {self.context.author}
Changes: {self.context.version} - Baseline.
-->

'''

    def _render_txt(self, path: str, desc: str) -> str:
        """
        CGK-conform config-bestand-format (00-conventions.md §4,
        "Requirements / tekstuele configuratiefiles"): Nederlandse labels,
        geen aparte File:-regel.
        """
        return f'''# Beschrijving: {desc}
# Versie: {self.context.version}
# Auteur: {self.context.author}
# Applicatie: {self.context.app_name}

'''

    def _render_bat(self, path: str, desc: str) -> str:
        """
        CGK-conform batch/PowerShell-header (00-conventions.md §4,
        "Batch/PowerShell build-scripts"): zelfde Engelse labelfamilie als
        _render_python, in REM-commentaarsyntax, + Applicatie:-label.
        """
        return f'''REM ============================================================
REM Applicatie: {self.context.app_name}
REM File:    {path}
REM Role:    {desc}
REM Version: {self.context.version}
REM Author:  {self.context.author}
REM Changes: {self.context.version} - Baseline.
REM ============================================================

'''

    def _render_spec(self, path: str, desc: str) -> str:
        """PyInstaller spec bestand — zelfde Engelse labelfamilie als _render_python."""
        return f'''# -*- mode: python ; coding: utf-8 -*-
# Applicatie: {self.context.app_name}
# File:    {path}
# Role:    {desc}
# Version: {self.context.version}
# Author:  {self.context.author}
# Changes: {self.context.version} - Baseline.

'''

    def _render_qss(self, path: str, desc: str) -> str:
        """Qt StyleSheet - CSS-style comments. (Niet gedekt door 00-conventions.md §4 — ongewijzigd.)"""
        return f'''/*
File:    {path}
Rol:     {desc}
Applicatie: {self.context.app_name}
Versie:  {self.context.version}
Auteur:  {self.context.author}
Changes: {self.context.version} - Baseline.
*/

'''

    def _render_plain(self, path: str, desc: str) -> str:
        """Geen header (bijv. .gitignore)."""
        return ""

    def _render_default(self, path: str, desc: str) -> str:
        """Fallback voor niet-expliciet-gemapte extensies: hash comments, Engelse labelfamilie."""
        return f'''# Applicatie: {self.context.app_name}
# File:    {path}
# Role:    {desc}
# Version: {self.context.version}
# Author:  {self.context.author}
# Changes: {self.context.version} - Baseline.

'''