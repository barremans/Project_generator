"""
gui/settings_dialog.py

Beschrijving: Settings dialoog voor applicatie instellingen
Applicatie: Project Generator
Versie: 1.0.5
Auteur: Barremans
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QFileDialog,
    QGroupBox, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pathlib import Path

from utils.settings import AppSettings
from i18n import t


class SettingsDialog(QDialog):
    """
    Dialog voor het configureren van applicatie instellingen.
    """
    
    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        
        self._setup_window()
        self._setup_ui()
        self._load_values()
    
    def _setup_window(self):
        """Setup window properties."""
        self.setWindowTitle(t("settings.title"))
        self.setMinimumWidth(500)
        self.setModal(True)
        
        # Set window icon
        icon_path = self._get_icon_path("settings.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
    
    def _get_icon_path(self, icon_name: str) -> Path:
        """Haal icon pad op."""
        icons_dir = Path(__file__).parent.parent / "assets" / "icons"
        return icons_dir / icon_name
    
    def _setup_ui(self):
        """Bouw de UI op."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Defaults group
        self.group_defaults = QGroupBox(t("settings.defaults"))
        defaults_layout = QFormLayout()
        
        self.txt_default_author = QLineEdit()
        self.txt_default_author.setPlaceholderText(t("settings.default_author_placeholder"))
        
        self.txt_default_root = QLineEdit()
        self.txt_default_root.setPlaceholderText(t("settings.default_root_placeholder"))
        
        browse_layout = QHBoxLayout()
        browse_layout.addWidget(self.txt_default_root)
        
        self.btn_browse = QPushButton(t("settings.browse"))
        self.btn_browse.clicked.connect(self._browse_root)
        browse_layout.addWidget(self.btn_browse)
        
        defaults_layout.addRow(f"{t('settings.default_author')}:", self.txt_default_author)
        defaults_layout.addRow(f"{t('settings.default_root')}:", browse_layout)
        
        self.group_defaults.setLayout(defaults_layout)
        layout.addWidget(self.group_defaults)
        
        # Editor group
        self.group_editor = QGroupBox(t("settings.editor"))
        editor_layout = QVBoxLayout()
        
        form = QFormLayout()
        
        self.txt_editor_path = QLineEdit()
        self.txt_editor_path.setPlaceholderText(t("settings.editor_placeholder"))
        
        form.addRow(f"{t('settings.editor_path')}:", self.txt_editor_path)
        
        editor_layout.addLayout(form)
        
        self.lbl_editor_info = QLabel(t("settings.editor_info"))
        self.lbl_editor_info.setStyleSheet("color: #666; font-size: 9pt; margin-top: 5px;")
        self.lbl_editor_info.setWordWrap(True)
        editor_layout.addWidget(self.lbl_editor_info)
        
        self.group_editor.setLayout(editor_layout)
        layout.addWidget(self.group_editor)
        
        # Language group
        self.group_language = QGroupBox(t("menu.language"))
        language_layout = QFormLayout()
        
        self.combo_language = QComboBox()
        self.combo_language.addItem("🇳🇱 Nederlands", "nl_NL")
        self.combo_language.addItem("🇬🇧 English", "en_US")
        
        language_layout.addRow(f"{t('settings.language')}:", self.combo_language)
        
        self.group_language.setLayout(language_layout)
        layout.addWidget(self.group_language)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_save = QPushButton(t("settings.save"))
        self.btn_save.clicked.connect(self._save_settings)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.btn_cancel = QPushButton(t("settings.cancel"))
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        
        layout.addLayout(btn_layout)
    
    def _load_values(self):
        """Laad huidige instellingen."""
        self.txt_default_author.setText(self.settings.default_author)
        self.txt_default_root.setText(self.settings.default_project_root)
        self.txt_editor_path.setText(self.settings.editor_path)
        
        # Selecteer huidige taal
        current_locale = self.settings.locale
        for i in range(self.combo_language.count()):
            if self.combo_language.itemData(i) == current_locale:
                self.combo_language.setCurrentIndex(i)
                break
    
    def _refresh_ui(self):
        """Herlaad alle UI teksten na taal wijziging."""
        self.setWindowTitle(t("settings.title"))
        
        # Groups
        self.group_defaults.setTitle(t("settings.defaults"))
        self.group_editor.setTitle(t("settings.editor"))
        self.group_language.setTitle(t("menu.language"))
        
        # Buttons
        self.btn_browse.setText(t("settings.browse"))
        self.btn_save.setText(t("settings.save"))
        self.btn_cancel.setText(t("settings.cancel"))
        
        # Placeholders
        self.txt_default_author.setPlaceholderText(t("settings.default_author_placeholder"))
        self.txt_default_root.setPlaceholderText(t("settings.default_root_placeholder"))
        self.txt_editor_path.setPlaceholderText(t("settings.editor_placeholder"))
        
        # Info label
        self.lbl_editor_info.setText(t("settings.editor_info"))
    
    def _browse_root(self):
        """Browse voor default project root."""
        folder = QFileDialog.getExistingDirectory(
            self,
            t("settings.default_root"),
            self.txt_default_root.text() or "C:\\"
        )
        
        if folder:
            self.txt_default_root.setText(folder)
    
    def _save_settings(self):
        """Sla instellingen op."""
        old_locale = self.settings.locale
        
        self.settings.default_author = self.txt_default_author.text().strip()
        self.settings.default_project_root = self.txt_default_root.text().strip()
        self.settings.editor_path = self.txt_editor_path.text().strip()
        
        # Get selected language
        selected_locale = self.combo_language.currentData()
        self.settings.locale = selected_locale
        
        if self.settings.save():
            QMessageBox.information(
                self,
                t("settings.saved"),
                t("settings.saved_message")
            )
            self.accept()
        else:
            QMessageBox.critical(
                self,
                t("settings.error"),
                t("settings.error_message")
            )