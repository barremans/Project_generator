"""
gui/settings_dialog.py

Beschrijving: Settings dialoog
Applicatie: Project Generator
Versie: 1.0.3
Auteur: Barremans
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QFileDialog, QLabel,
    QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pathlib import Path

from utils.settings import AppSettings


class SettingsDialog(QDialog):
    """
    Dialog voor applicatie instellingen.
    """
    
    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Instellingen")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        # Set icon
        icons_dir = Path(__file__).parent.parent / "assets" / "icons"
        icon_path = icons_dir / "settings.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        self._setup_ui()
        self._load_current_settings()
    
    def _setup_ui(self):
        """Bouw UI op."""
        layout = QVBoxLayout(self)
        
        # Defaults group
        defaults_group = QGroupBox("Standaard Waarden")
        defaults_layout = QFormLayout()
        
        self.txt_author = QLineEdit()
        self.txt_author.setPlaceholderText("Jouw naam")
        defaults_layout.addRow("Standaard Auteur:", self.txt_author)
        
        # Project root
        root_layout = QHBoxLayout()
        self.txt_project_root = QLineEdit()
        self.txt_project_root.setPlaceholderText("C:\\")
        btn_browse_root = QPushButton("Bladeren...")
        btn_browse_root.clicked.connect(self._browse_project_root)
        root_layout.addWidget(self.txt_project_root)
        root_layout.addWidget(btn_browse_root)
        defaults_layout.addRow("Standaard Projectmap:", root_layout)
        
        defaults_group.setLayout(defaults_layout)
        layout.addWidget(defaults_group)
        
        # Editor group
        editor_group = QGroupBox("Editor Instellingen")
        editor_layout = QFormLayout()
        
        editor_path_layout = QHBoxLayout()
        self.txt_editor_path = QLineEdit()
        self.txt_editor_path.setPlaceholderText("code (voor VS Code)")
        btn_browse_editor = QPushButton("Bladeren...")
        btn_browse_editor.clicked.connect(self._browse_editor)
        editor_path_layout.addWidget(self.txt_editor_path)
        editor_path_layout.addWidget(btn_browse_editor)
        
        editor_layout.addRow("Editor Pad:", editor_path_layout)
        
        info = QLabel("💡 Standaard editors:\n"
                     "  • VS Code: code\n"
                     "  • Notepad++: notepad++\n"
                     "  • Of volledig pad naar .exe")
        info.setStyleSheet("color: #666; font-size: 9pt;")
        editor_layout.addRow(info)
        
        editor_group.setLayout(editor_layout)
        layout.addWidget(editor_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_cancel = QPushButton("Annuleren")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Opslaan")
        btn_save.clicked.connect(self._save_settings)
        btn_save.setDefault(True)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        
        layout.addLayout(btn_layout)
    
    def _load_current_settings(self):
        """Laad huidige instellingen in velden."""
        self.txt_author.setText(self.settings.default_author)
        self.txt_project_root.setText(self.settings.default_project_root)
        self.txt_editor_path.setText(self.settings.editor_path)
    
    def _browse_project_root(self):
        """Bladeren naar project root."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecteer standaard projectmap",
            self.txt_project_root.text() or "C:\\"
        )
        if folder:
            self.txt_project_root.setText(folder)
    
    def _browse_editor(self):
        """Bladeren naar editor executable."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecteer editor",
            "C:\\Program Files",
            "Executables (*.exe);;Alle bestanden (*.*)"
        )
        if file_path:
            self.txt_editor_path.setText(file_path)
    
    def _save_settings(self):
        """Sla instellingen op."""
        self.settings.default_author = self.txt_author.text().strip()
        self.settings.default_project_root = self.txt_project_root.text().strip() or "C:\\"
        self.settings.editor_path = self.txt_editor_path.text().strip() or "code"
        
        if self.settings.save():
            QMessageBox.information(self, "Opgeslagen", "Instellingen zijn opgeslagen!")
            self.accept()
        else:
            QMessageBox.critical(self, "Fout", "Kon instellingen niet opslaan.")