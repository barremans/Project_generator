"""
i18n/__init__.py

Beschrijving: Internationalization package
Applicatie: Project Generator
Versie: 1.0.5
Auteur: Barremans
"""

from i18n.translator import Translator, get_translator, t

__all__ = ["Translator", "get_translator", "t"]