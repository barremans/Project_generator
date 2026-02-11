"""
gui/main_window.py

Beschrijving: Hoofdvenster met wizard interface
Applicatie: Project Generator
Versie: 1.0.4
Auteur: Barremans
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QFileDialog, QCheckBox, QMessageBox, QProgressBar,
    QStackedWidget, QGroupBox, QFormLayout, QMenuBar,
    QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QAction, QIcon
from pathlib import Path
import subprocess
import sys

from core.context import ProjectContext
from core.default_templates import create_standard_project_template
from core.generator import ProjectGenerator
from utils.settings import AppSettings
from gui.settings_dialog import SettingsDialog


class GeneratorThread(QThread):
    """
    Thread voor project generatie (voorkomt UI freeze).
    """
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str, str)
    
    def __init__(self, context: ProjectContext, template):
        super().__init__()
        self.context = context
        self.template = template
    
    def run(self):
        """Voer generatie uit in achtergrond."""
        try:
            generator = ProjectGenerator(self.context, self.template)
            
            self.progress.emit("Project wordt aangemaakt...")
            
            success = generator.generate()
            
            project_path = str(self.context.project_root)
            
            if success:
                msg = f"Project succesvol aangemaakt!"
                self.finished.emit(True, msg, project_path)
            else:
                msg = f"Project aangemaakt met waarschuwingen."
                self.finished.emit(True, msg, project_path)
                
        except Exception as e:
            self.finished.emit(False, f"Fout tijdens generatie:\n{str(e)}", "")


class ProjectGeneratorWindow(QMainWindow):
    """
    Hoofdvenster voor de Project Generator.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Project Generator v1.0.3")
        self.setMinimumSize(700, 600)
        
        # Set window icon
        icon_path = self._get_icon_path("app_icon.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Settings
        self.settings = AppSettings()
        
        # Data
        self.project_location = None
        self.app_name = ""
        self.generated_project_path = None
        
        # Setup Menu
        self._setup_menu()
        
        # Setup UI
        self._setup_ui()
        
        # Setup Shortcuts
        self._setup_shortcuts()
        
        # Load defaults
        self._load_default_values()
    
    def _get_icon_path(self, icon_name: str) -> Path:
        """Haal icon pad op."""
        icons_dir = Path(__file__).parent.parent / "assets" / "icons"
        return icons_dir / icon_name
        
    def _setup_menu(self):
        """Maak menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&Bestand")
        
        new_action = QAction(QIcon(str(self._get_icon_path("file.png"))), "&Nieuw Project", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction(QIcon(str(self._get_icon_path("settings.png"))), "&Instellingen", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Afsluiten", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        help_action = QAction(QIcon(str(self._get_icon_path("help.png"))), "&Help", self)
        help_action.setShortcut(QKeySequence("F1"))
        help_action.triggered.connect(self._show_help)
        help_menu.addAction(help_action)
        
        changelog_action = QAction(QIcon(str(self._get_icon_path("info.png"))), "&Changelog", self)
        changelog_action.triggered.connect(self._show_changelog)
        help_menu.addAction(changelog_action)
        
        help_menu.addSeparator()
        
        about_action = QAction(QIcon(str(self._get_icon_path("info.png"))), "&Over", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _setup_ui(self):
        """Bouw de UI op."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Python Project Generator")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Genereer automatisch een complete Python projectstructuur")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Stacked widget voor verschillende schermen
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # Voeg schermen toe
        self.stack.addWidget(self._create_location_page())
        self.stack.addWidget(self._create_metadata_page())
        self.stack.addWidget(self._create_options_page())
        self.stack.addWidget(self._create_summary_page())
        self.stack.addWidget(self._create_progress_page())
        self.stack.addWidget(self._create_result_page())
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.btn_back = QPushButton("← Vorige")
        self.btn_back.clicked.connect(self._go_back)
        self.btn_back.setEnabled(False)
        
        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch()
        
        self.btn_next = QPushButton("Volgende →")
        self.btn_next.clicked.connect(self._go_next)
        
        nav_layout.addWidget(self.btn_next)
        
        layout.addLayout(nav_layout)
        
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Enter = Volgende
        self.shortcut_next = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.shortcut_next.activated.connect(self._handle_enter)
        
        # Shift+Tab = Vorige
        self.shortcut_back = QShortcut(QKeySequence("Shift+Tab"), self)
        self.shortcut_back.activated.connect(self._handle_shift_tab)
    
    def _load_default_values(self):
        """Laad standaard waarden uit settings."""
        default_author = self.settings.default_author
        if default_author:
            self.txt_author.setText(default_author)
        
    def _handle_enter(self):
        """Handle Enter key."""
        current = self.stack.currentIndex()
        if current < 4 and self.btn_next.isEnabled() and self.btn_next.isVisible():
            self._go_next()
    
    def _handle_shift_tab(self):
        """Handle Shift+Tab."""
        current = self.stack.currentIndex()
        if current > 0 and current < 4 and self.btn_back.isEnabled():
            self._go_back()
        
    def _create_location_page(self) -> QWidget:
        """Pagina 1: Projectlocatie."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Stap 1: Projectlocatie")
        group_layout = QVBoxLayout()
        
        label = QLabel("Waar wil je het project aanmaken?")
        group_layout.addWidget(label)
        
        # Location selector
        loc_layout = QHBoxLayout()
        
        self.txt_location = QLineEdit()
        self.txt_location.setPlaceholderText("Selecteer een map...")
        self.txt_location.setReadOnly(True)
        
        btn_browse = QPushButton("Bladeren...")
        btn_browse.clicked.connect(self._browse_location)
        
        loc_layout.addWidget(self.txt_location)
        loc_layout.addWidget(btn_browse)
        
        group_layout.addLayout(loc_layout)
        
        # App name
        group_layout.addWidget(QLabel("\nApplicatienaam:"))
        
        self.txt_appname = QLineEdit()
        self.txt_appname.setPlaceholderText("Bijv: MyAwesomeApp")
        self.txt_appname.textChanged.connect(self._validate_location_page)
        
        group_layout.addWidget(self.txt_appname)
        
        # Info
        info = QLabel("💡 De applicatienaam wordt gebruikt als mapnaam en in alle bestanden.")
        info.setStyleSheet("color: #666; font-style: italic; margin-top: 10px;")
        info.setWordWrap(True)
        group_layout.addWidget(info)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        return page
    
    def _create_metadata_page(self) -> QWidget:
        """Pagina 2: Metadata."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Stap 2: Project Informatie")
        form = QFormLayout()
        
        self.txt_author = QLineEdit()
        self.txt_author.setPlaceholderText("Jouw naam")
        
        self.txt_version = QLineEdit()
        self.txt_version.setText("1.0.0")
        
        self.txt_description = QTextEdit()
        self.txt_description.setPlaceholderText("Optionele beschrijving van het project...")
        self.txt_description.setMaximumHeight(100)
        
        form.addRow("Auteur:", self.txt_author)
        form.addRow("Versie:", self.txt_version)
        form.addRow("Beschrijving:", self.txt_description)
        
        group.setLayout(form)
        layout.addWidget(group)
        layout.addStretch()
        
        return page
    
    def _create_options_page(self) -> QWidget:
        """Pagina 3: Opties."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Stap 3: Opties")
        group_layout = QVBoxLayout()
        
        self.chk_venv = QCheckBox("Virtuele omgeving (venv) aanmaken")
        self.chk_venv.setChecked(True)
        
        venv_info = QLabel("Maakt automatisch een venv aan en installeert pip.")
        venv_info.setStyleSheet("color: #666; margin-left: 25px; font-size: 10pt;")
        venv_info.setWordWrap(True)
        
        group_layout.addWidget(self.chk_venv)
        group_layout.addWidget(venv_info)
        group_layout.addSpacing(10)
        
        # Info over structuur
        info_label = QLabel("ℹ️  Standaard projectstructuur:")
        info_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        group_layout.addWidget(info_label)
        
        structure = QLabel(
            "• .vscode/ (VS Code configuratie)\n"
            "• app/ (Hoofdapplicatie)\n"
            "• config/ (Configuratie)\n"
            "• assets/ (Icons en afbeeldingen)\n"
            "• css/ (Stylesheets)\n"
            "• data/ (Data opslag)\n"
            "• docs/ (Documentatie)\n"
            "• helpers/ (Helper functies)\n"
            "• utils/ (Utilities)\n"
            "• md/ (Markdown bestanden)\n"
            "• tests/ (Unit tests)\n"
            "• README.md, requirements.txt, .gitignore\n"
            "• export_to_usb.bat, .spec bestand"
        )
        structure.setStyleSheet("color: #333; margin-left: 20px;")
        group_layout.addWidget(structure)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        return page
    
    def _create_summary_page(self) -> QWidget:
        """Pagina 4: Samenvatting."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Stap 4: Samenvatting")
        group_layout = QVBoxLayout()
        
        label = QLabel("Controleer de instellingen:")
        label.setStyleSheet("font-weight: bold;")
        group_layout.addWidget(label)
        
        self.lbl_summary = QLabel()
        self.lbl_summary.setWordWrap(True)
        self.lbl_summary.setStyleSheet("background: #f5f5f5; padding: 15px; border-radius: 5px;")
        
        group_layout.addWidget(self.lbl_summary)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        return page
    
    def _create_progress_page(self) -> QWidget:
        """Pagina 5: Voortgang."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Project wordt aangemaakt...")
        group_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        
        self.lbl_progress = QLabel("Bezig met genereren...")
        self.lbl_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        group_layout.addWidget(self.progress_bar)
        group_layout.addWidget(self.lbl_progress)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        return page
    
    def _create_result_page(self) -> QWidget:
        """Pagina 6: Resultaat."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("✅ Project succesvol aangemaakt!")
        group_layout = QVBoxLayout()
        
        self.lbl_result = QLabel()
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setStyleSheet("font-size: 11pt; padding: 10px;")
        
        group_layout.addWidget(self.lbl_result)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self.btn_open_folder = QPushButton("📁 Open Projectmap")
        self.btn_open_folder.clicked.connect(self._open_project_folder)
        self.btn_open_folder.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.btn_open_editor = QPushButton("💻 Open in Editor")
        self.btn_open_editor.clicked.connect(self._open_in_editor)
        self.btn_open_editor.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        
        self.btn_new_project = QPushButton("🆕 Nieuw Project")
        self.btn_new_project.clicked.connect(self._new_project)
        self.btn_new_project.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 10px;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        
        self.btn_close = QPushButton("❌ Sluiten")
        self.btn_close.clicked.connect(self.close)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        btn_layout.addWidget(self.btn_open_folder)
        btn_layout.addWidget(self.btn_open_editor)
        btn_layout.addWidget(self.btn_new_project)
        btn_layout.addWidget(self.btn_close)
        
        group_layout.addLayout(btn_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        return page
    
    def _browse_location(self):
        """Open folder browser."""
        start_dir = self.settings.default_project_root or "C:\\"
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecteer projectlocatie",
            start_dir
        )
        
        if folder:
            self.project_location = Path(folder)
            self.txt_location.setText(str(self.project_location))
            self._validate_location_page()
    
    def _validate_location_page(self):
        """Valideer locatie pagina."""
        has_location = self.project_location is not None
        has_name = len(self.txt_appname.text().strip()) > 0
        
        self.btn_next.setEnabled(has_location and has_name)
    
    def _go_back(self):
        """Ga naar vorige pagina."""
        current = self.stack.currentIndex()
        
        if current > 0 and current < 5:
            self.stack.setCurrentIndex(current - 1)
            self._update_navigation()
    
    def _go_next(self):
        """Ga naar volgende pagina."""
        current = self.stack.currentIndex()
        
        if current == 0:
            self.app_name = self.txt_appname.text().strip()
            self.stack.setCurrentIndex(1)
            
        elif current == 1:
            self.stack.setCurrentIndex(2)
            
        elif current == 2:
            self._update_summary()
            self.stack.setCurrentIndex(3)
            
        elif current == 3:
            self._start_generation()
        
        self._update_navigation()
    
    def _update_navigation(self):
        """Update navigatie knoppen."""
        current = self.stack.currentIndex()
        
        self.btn_back.setEnabled(current > 0 and current < 4)
        
        if current == 3:
            self.btn_next.setText("🚀 Genereer Project")
            self.btn_next.setEnabled(True)
        elif current >= 4:
            self.btn_next.setVisible(False)
            self.btn_back.setVisible(False)
        else:
            self.btn_next.setText("Volgende →")
            self.btn_next.setEnabled(True)
            self.btn_next.setVisible(True)
            self.btn_back.setVisible(True)
    
    def _update_summary(self):
        """Update samenvatting tekst."""
        summary_text = f"""
<b>Projectlocatie:</b><br>
{self.project_location / self.app_name}<br><br>

<b>Applicatienaam:</b> {self.app_name}<br>
<b>Auteur:</b> {self.txt_author.text()}<br>
<b>Versie:</b> {self.txt_version.text()}<br>
<b>Beschrijving:</b> {self.txt_description.toPlainText() or '<i>Geen</i>'}<br><br>

<b>Opties:</b><br>
- Virtuele omgeving: {'Ja' if self.chk_venv.isChecked() else 'Nee'}<br><br>

<b>Er worden aangemaakt:</b><br>
- 10+ mappen (inclusief submappen)<br>
- 15+ bestanden (met correcte headers)<br>
- export_to_usb.bat script<br>
- PyInstaller .spec bestand<br>
- VS Code configuratie<br>
"""
        
        if self.chk_venv.isChecked():
            summary_text += "• Virtuele Python omgeving<br>"
        
        self.lbl_summary.setText(summary_text)
    
    def _start_generation(self):
        """Start project generatie."""
        self.stack.setCurrentIndex(4)
        self._update_navigation()
        
        context = ProjectContext(
            app_name=self.app_name,
            version=self.txt_version.text(),
            author=self.txt_author.text(),
            root_path=self.project_location,
            description=self.txt_description.toPlainText(),
            create_venv=self.chk_venv.isChecked()
        )
        
        template = create_standard_project_template(
            name=context.app_name,
            version=context.version,
            author=context.author,
            description=context.description,
            create_venv=context.create_venv
        )
        
        self.generator_thread = GeneratorThread(context, template)
        self.generator_thread.progress.connect(self._on_progress)
        self.generator_thread.finished.connect(self._on_finished)
        self.generator_thread.start()
    
    def _on_progress(self, message: str):
        """Update voortgang."""
        self.lbl_progress.setText(message)
    
    def _on_finished(self, success: bool, message: str, project_path: str):
        """Generatie afgerond."""
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        
        self.generated_project_path = project_path
        
        if success:
            result_text = f"""
<p style='font-size: 12pt;'><b>{message}</b></p>
<p><b>Locatie:</b><br><code>{project_path}</code></p>
<p style='color: #666;'>Gebruik de knoppen hieronder om het project te openen of een nieuw project te starten.</p>
"""
            self.lbl_result.setText(result_text)
            self.stack.setCurrentIndex(5)
            self._update_navigation()
        else:
            QMessageBox.critical(self, "Fout", message)
    
    def _open_project_folder(self):
        """Open de projectmap in Windows Verkenner."""
        if self.generated_project_path:
            subprocess.run(['explorer', self.generated_project_path])
    
    def _open_in_editor(self):
        """Open project in geconfigureerde editor."""
        if self.generated_project_path:
            editor_path = self.settings.editor_path
            
            try:
                subprocess.run([editor_path, self.generated_project_path])
            except FileNotFoundError:
                QMessageBox.warning(
                    self,
                    "Editor niet gevonden",
                    f"Editor '{editor_path}' is niet gevonden.\n\n"
                    f"Configureer het juiste pad via Menu → Bestand → Instellingen"
                )
    
    def _new_project(self):
        """Start wizard opnieuw voor een nieuw project."""
        self.project_location = None
        self.app_name = ""
        self.generated_project_path = None
        
        self.txt_location.clear()
        self.txt_appname.clear()
        
        # Gebruik standaard auteur uit settings
        default_author = self.settings.default_author
        if default_author:
            self.txt_author.setText(default_author)
        else:
            self.txt_author.clear()
            
        self.txt_version.setText("1.0.0")
        self.txt_description.clear()
        self.chk_venv.setChecked(True)
        
        self.stack.setCurrentIndex(0)
        self.btn_next.setVisible(True)
        self.btn_back.setVisible(True)
        self._update_navigation()
    
    def _show_settings(self):
        """Toon settings dialoog."""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            # Refresh auteur veld na opslaan settings
            if self.settings.default_author:
                self.txt_author.setText(self.settings.default_author)
    
    def _show_help(self):
        """Toon help."""
        help_file = Path(__file__).parent.parent / "docs" / "HELP.md"
        
        if help_file.exists():
            content = help_file.read_text(encoding='utf-8')
            self._show_markdown_dialog("Help", content)
        else:
            QMessageBox.information(
                self,
                "Help",
                "Help documentatie is niet gevonden.\n\n"
                "Verwachte locatie: docs/HELP.md"
            )
    
    def _show_changelog(self):
        """Toon changelog."""
        changelog_file = Path(__file__).parent.parent / "docs" / "CHANGELOG.md"
        
        if changelog_file.exists():
            content = changelog_file.read_text(encoding='utf-8')
            self._show_markdown_dialog("Changelog", content)
        else:
            QMessageBox.information(
                self,
                "Changelog",
                "Changelog is niet gevonden.\n\n"
                "Verwachte locatie: docs/CHANGELOG.md"
            )
    
    def _show_about(self):
        """Toon about dialog."""
        about_text = """
<h2>Python Project Generator</h2>
<p><b>Versie:</b> 1.0.3</p>
<p><b>Auteur:</b> Barremans</p>
<p><b>Beschrijving:</b><br>
Automatische generator voor professionele Python projectstructuren.</p>

<p><b>Kenmerken:</b></p>
<ul>
<li>Wizard interface</li>
<li>Template-based systeem</li>
<li>Automatische venv setup</li>
<li>VS Code configuratie</li>
<li>Export scripts</li>
<li>PyInstaller templates</li>
<li>Keyboard shortcuts</li>
<li>Configureerbare instellingen</li>
</ul>

<p><b>Ontwikkeld met:</b><br>
Python 3.11+ en PyQt6</p>

<p style='color: #666; margin-top: 20px;'>
© 2024 Barremans - Alle rechten voorbehouden
</p>
"""
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Over Project Generator")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _show_markdown_dialog(self, title: str, content: str):
        """Toon markdown content in een dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(700, 600)
        
        # Set dialog icon
        icon_path = self._get_icon_path("help.png")
        if icon_path.exists():
            dialog.setWindowIcon(QIcon(str(icon_path)))
        
        layout = QVBoxLayout(dialog)
        
        # QTextEdit met Markdown support
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(content)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
                padding: 15px;
            }
        """)
        
        layout.addWidget(text_edit)
        
        btn_close = QPushButton("Sluiten")
        btn_close.clicked.connect(dialog.accept)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        layout.addWidget(btn_close)
        
        dialog.exec()