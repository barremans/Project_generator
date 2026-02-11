"""
main.py

Beschrijving: Hoofdapplicatie - start de Project Generator GUI
Applicatie: Project Generator
Versie: 1.0.0
Auteur: Barremans
"""

import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import ProjectGeneratorWindow


def main():
    """Start de applicatie."""
    app = QApplication(sys.argv)
    
    # Pas stijl aan (optioneel - mooiere UI)
    app.setStyle('Fusion')
    
    # Maak en toon hoofdvenster
    window = ProjectGeneratorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()