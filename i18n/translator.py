"""
i18n/translator.py

Beschrijving: Translation helper voor Project Generator
Applicatie: Project Generator
Versie: 1.0.5
Auteur: Barremans
"""

import json
from pathlib import Path
from typing import Dict, Optional


class Translator:
    """Translation helper voor meertaligheid."""
    
    def __init__(self, locale: str = "nl_NL"):
        self.locale = locale
        self.translations: Dict[str, str] = {}
        self.fallback_locale = "en_US"
        self.fallback_translations: Dict[str, str] = {}
        self._load_translations()
    
    def _load_translations(self):
        """Laad translation bestanden."""
        locales_dir = Path(__file__).parent / "locales"
        
        # Laad gekozen locale
        locale_file = locales_dir / f"{self.locale}.json"
        if locale_file.exists():
            with open(locale_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        
        # Laad fallback
        if self.locale != self.fallback_locale:
            fallback_file = locales_dir / f"{self.fallback_locale}.json"
            if fallback_file.exists():
                with open(fallback_file, "r", encoding="utf-8") as f:
                    self.fallback_translations = json.load(f)
    
    def get(self, key: str, **kwargs) -> str:
        """Haal vertaling op."""
        text = self.translations.get(key)
        
        if text is None:
            text = self.fallback_translations.get(key)
        
        if text is None:
            return key
        
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text
    
    def set_locale(self, locale: str):
        """Verander actieve locale."""
        self.locale = locale
        self._load_translations()
    
    def get_available_locales(self) -> list:
        """Haal beschikbare locales op."""
        locales_dir = Path(__file__).parent / "locales"
        if not locales_dir.exists():
            return []
        
        locales = []
        for file in locales_dir.glob("*.json"):
            locales.append(file.stem)
        
        return sorted(locales)


# Singleton
_translator: Optional[Translator] = None


def get_translator(locale: str = "nl_NL") -> Translator:
    """Haal translator instance op."""
    global _translator
    if _translator is None:
        _translator = Translator(locale)
    return _translator


def t(key: str, **kwargs) -> str:
    """Shortcut voor vertaling."""
    return get_translator().get(key, **kwargs)