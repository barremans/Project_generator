"""
File:    /gui/main_window.py
Rol:     Hoofdvenster met wizard interface
Applicatie: Project Generator
Versie:  1.1.0
Auteur:  Barremans
Changes: 1.1.0 - NIEUW: "Tools"-menu toegevoegd (tussen Taal en Help, in
                  zowel _setup_menu() als _rebuild_menu() — anders verdwijnt
                  het na een taalwisseling) met actie "Headers & Structuur..."
                  die gui/tools_dialog.py::ToolsDialog opent (project-doc-
                  tool-samenvoeging, zie context_ProjectDocTool.md §7.4).
                  Indien er al een gegenereerd project is in deze sessie
                  (self.generated_project_path), wordt de dialoog daarmee
                  voorgevuld. LET OP: de i18n-keys "menu.tools" en
                  "menu.tools.headers_structuur" bestaan nog NIET in
                  i18n/locales/*.json — die heb ik niet kunnen aanpassen
                  (niet aangeleverd). Tot ze zijn toegevoegd valt t() naar
                  ongeacht welk fallback-gedrag i18n/translator.py toepast
                  bij een ontbrekende key (bv. de key zelf tonen). Zie
                  toelichting in de chat voor de voorgestelde NL/EN-teksten.
Changes: 1.0.7 - Structuur-overzicht in wizard-stap 3 (_create_options_page)
                  aangevuld met ui/, dialogs/ en token/ — nieuw toegevoegd
                  aan core/default_templates.py v1.0.7. Puur informatief,
                  geen functionele wijziging.
Changes: 1.0.6 - BUGFIX: GeneratorThread.run() emitte in zowel de
                  succes- als de faal-tak "finished.emit(True, ...)" —
                  een mislukte generatie (generator.errors gevuld) werd
                  hierdoor in de UI altijd als geslaagd getoond, en de
                  bestaande foutafhandeling in _on_finished() (het
                  QMessageBox.critical-pad) werd nooit bereikt. Faal-tak
                  emit nu correct "False" met de verzamelde
                  generator.errors als boodschap.
Changes: 1.0.5 - Baseline (voorheen ongedocumenteerd).
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QFileDialog, QCheckBox, QMessageBox, QProgressBar,
    QStackedWidget, QGroupBox, QFormLayout, QMenuBar,
    QDialog, QComboBox
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
from gui.tools_dialog import ToolsDialog
from i18n import get_translator, t


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
            
            self.progress.emit(t("wizard.step5.generating"))
            
            success = generator.generate()
            
            project_path = str(self.context.project_root)
            
            if success:
                msg = t("wizard.step6.title")
                self.finished.emit(True, msg, project_path)
            else:
                # BUGFIX (was: self.finished.emit(True, ...) in beide takken,
                # waardoor een mislukte generatie in de UI als succes
                # verscheen). generator.errors is gevuld door
                # ProjectGenerator bij elke stap die faalde.
                msg = "\n".join(generator.errors) if generator.errors else "Onbekende fout tijdens generatie."
                self.finished.emit(False, msg, project_path)
                
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}", "")


class ProjectGeneratorWindow(QMainWindow):
    """
    Hoofdvenster voor de Project Generator.
    """
    
    def __init__(self):
        super().__init__()
        
        # Settings
        self.settings = AppSettings()
        
        # Setup translator
        self.translator = get_translator(self.settings.locale)
        
        # Data
        self.project_location = None
        self.app_name = ""
        self.generated_project_path = None
        
        # Setup window
        self._setup_window()
        
        # Setup Menu
        self._setup_menu()
        
        # Setup UI
        self._setup_ui()
        
        # Setup Shortcuts
        self._setup_shortcuts()
        
        # Load defaults
        self._load_default_values()
    
    def _setup_window(self):
        """Setup window properties."""
        self.setWindowTitle(t("app.title"))
        self.setMinimumSize(700, 600)
        
        # Set window icon
        icon_path = self._get_icon_path("app_icon.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
    
    def _get_icon_path(self, icon_name: str) -> Path:
        """Haal icon pad op."""
        icons_dir = Path(__file__).parent.parent / "assets" / "icons"
        return icons_dir / icon_name
        
    def _setup_menu(self):
        """Maak menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(t("menu.file"))
        
        new_action = QAction(QIcon(str(self._get_icon_path("file.png"))), t("menu.file.new"), self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction(QIcon(str(self._get_icon_path("settings.png"))), t("menu.file.settings"), self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(t("menu.file.exit"), self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Language menu
        lang_menu = menubar.addMenu(t("menu.language"))
        
        nl_action = QAction("🇳🇱 Nederlands", self)
        nl_action.triggered.connect(lambda: self._change_language("nl_NL"))
        lang_menu.addAction(nl_action)
        
        en_action = QAction("🇬🇧 English", self)
        en_action.triggered.connect(lambda: self._change_language("en_US"))
        lang_menu.addAction(en_action)
        
        # Tools menu
        tools_menu = menubar.addMenu(t("menu.tools"))
        
        headers_structure_action = QAction(t("menu.tools.headers_structuur"), self)
        headers_structure_action.triggered.connect(self._open_tools_dialog)
        tools_menu.addAction(headers_structure_action)
        
        # Help menu
        help_menu = menubar.addMenu(t("menu.help"))
        
        help_action = QAction(QIcon(str(self._get_icon_path("help.png"))), t("menu.help.help"), self)
        help_action.setShortcut(QKeySequence("F1"))
        help_action.triggered.connect(self._show_help)
        help_menu.addAction(help_action)
        
        changelog_action = QAction(QIcon(str(self._get_icon_path("info.png"))), t("menu.help.changelog"), self)
        changelog_action.triggered.connect(self._show_changelog)
        help_menu.addAction(changelog_action)
        
        help_menu.addSeparator()
        
        about_action = QAction(QIcon(str(self._get_icon_path("info.png"))), t("menu.help.about"), self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _rebuild_menu(self):
        """Herbouw menu bar na taalwisseling."""
        # Clear existing menu
        self.menuBar().clear()
        
        # File menu
        file_menu = self.menuBar().addMenu(t("menu.file"))
        
        new_action = QAction(QIcon(str(self._get_icon_path("file.png"))), t("menu.file.new"), self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction(QIcon(str(self._get_icon_path("settings.png"))), t("menu.file.settings"), self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(t("menu.file.exit"), self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Language menu
        lang_menu = self.menuBar().addMenu(t("menu.language"))
        
        nl_action = QAction("🇳🇱 Nederlands", self)
        nl_action.triggered.connect(lambda: self._change_language("nl_NL"))
        lang_menu.addAction(nl_action)
        
        en_action = QAction("🇬🇧 English", self)
        en_action.triggered.connect(lambda: self._change_language("en_US"))
        lang_menu.addAction(en_action)
        
        # Tools menu
        tools_menu = self.menuBar().addMenu(t("menu.tools"))
        
        headers_structure_action = QAction(t("menu.tools.headers_structuur"), self)
        headers_structure_action.triggered.connect(self._open_tools_dialog)
        tools_menu.addAction(headers_structure_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu(t("menu.help"))
        
        help_action = QAction(QIcon(str(self._get_icon_path("help.png"))), t("menu.help.help"), self)
        help_action.setShortcut(QKeySequence("F1"))
        help_action.triggered.connect(self._show_help)
        help_menu.addAction(help_action)
        
        changelog_action = QAction(QIcon(str(self._get_icon_path("info.png"))), t("menu.help.changelog"), self)
        changelog_action.triggered.connect(self._show_changelog)
        help_menu.addAction(changelog_action)
        
        help_menu.addSeparator()
        
        about_action = QAction(QIcon(str(self._get_icon_path("info.png"))), t("menu.help.about"), self)
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
        self.lbl_title = QLabel(t("app.title"))
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.lbl_title.setFont(title_font)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_title)
        
        self.lbl_subtitle = QLabel(t("app.subtitle"))
        self.lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(self.lbl_subtitle)
        
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
        
        self.btn_back = QPushButton(t("button.previous"))
        self.btn_back.clicked.connect(self._go_back)
        self.btn_back.setEnabled(False)
        
        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch()
        
        self.btn_next = QPushButton(t("button.next"))
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
        
        self.group_location = QGroupBox(t("wizard.step1.title"))
        group_layout = QVBoxLayout()
        
        self.lbl_location = QLabel(t("wizard.step1.location"))
        group_layout.addWidget(self.lbl_location)
        
        # Location selector
        loc_layout = QHBoxLayout()
        
        self.txt_location = QLineEdit()
        self.txt_location.setPlaceholderText(t("wizard.step1.placeholder"))
        self.txt_location.setReadOnly(True)
        
        self.btn_browse = QPushButton(t("wizard.step1.browse"))
        self.btn_browse.clicked.connect(self._browse_location)
        
        loc_layout.addWidget(self.txt_location)
        loc_layout.addWidget(self.btn_browse)
        
        group_layout.addLayout(loc_layout)
        
        # App name
        self.lbl_appname = QLabel(f"\n{t('wizard.step1.appname')}")
        group_layout.addWidget(self.lbl_appname)
        
        self.txt_appname = QLineEdit()
        self.txt_appname.setPlaceholderText(t("wizard.step1.appname_placeholder"))
        self.txt_appname.textChanged.connect(self._validate_location_page)
        
        group_layout.addWidget(self.txt_appname)
        
        # Info
        self.lbl_location_info = QLabel(t("wizard.step1.info"))
        self.lbl_location_info.setStyleSheet("color: #666; font-style: italic; margin-top: 10px;")
        self.lbl_location_info.setWordWrap(True)
        group_layout.addWidget(self.lbl_location_info)
        
        self.group_location.setLayout(group_layout)
        layout.addWidget(self.group_location)
        layout.addStretch()
        
        return page
    
    def _create_metadata_page(self) -> QWidget:
        """Pagina 2: Metadata."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.group_metadata = QGroupBox(t("wizard.step2.title"))
        form = QFormLayout()
        
        self.txt_author = QLineEdit()
        self.txt_author.setPlaceholderText(t("wizard.step2.author_placeholder"))
        
        self.txt_version = QLineEdit()
        self.txt_version.setText("1.0.0")
        
        self.txt_description = QTextEdit()
        self.txt_description.setPlaceholderText(t("wizard.step2.description_placeholder"))
        self.txt_description.setMaximumHeight(100)
        
        form.addRow(f"{t('wizard.step2.author')}:", self.txt_author)
        form.addRow(f"{t('wizard.step2.version')}:", self.txt_version)
        form.addRow(f"{t('wizard.step2.description')}:", self.txt_description)
        
        self.group_metadata.setLayout(form)
        layout.addWidget(self.group_metadata)
        layout.addStretch()
        
        return page
    
    def _create_options_page(self) -> QWidget:
        """Pagina 3: Opties."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.group_options = QGroupBox(t("wizard.step3.title"))
        group_layout = QVBoxLayout()
        
        self.chk_venv = QCheckBox(t("wizard.step3.venv"))
        self.chk_venv.setChecked(True)
        
        self.lbl_venv_info = QLabel(t("wizard.step3.venv_info"))
        self.lbl_venv_info.setStyleSheet("color: #666; margin-left: 25px; font-size: 10pt;")
        self.lbl_venv_info.setWordWrap(True)
        
        group_layout.addWidget(self.chk_venv)
        group_layout.addWidget(self.lbl_venv_info)
        group_layout.addSpacing(10)
        
        # Info over structuur
        self.lbl_structure_title = QLabel(t("wizard.step3.structure_title"))
        self.lbl_structure_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        group_layout.addWidget(self.lbl_structure_title)
        
        structure = QLabel(
            "• .vscode/ (VS Code configuratie)\n"
            "• app/ (Hoofdapplicatie)\n"
            "• config/ (Configuratie)\n"
            "• assets/ (Icons en afbeeldingen)\n"
            "• css/ (Stylesheets)\n"
            "• data/ (Data opslag)\n"
            "• docs/ (Documentatie)\n"
            "• helpers/ (Helper functies)\n"
            "• i18n/ (Internationalization)\n"
            "• utils/ (Utilities)\n"
            "• ui/ (GUI-schermen)\n"
            "• dialogs/ (Modale vensters)\n"
            "• token/ (Token/auth-modules)\n"
            "• md/ (Markdown bestanden)\n"
            "• tests/ (Unit tests)\n"
            "• README.md, requirements.txt, .gitignore\n"
            "• export_to_usb.bat, .spec bestand"
        )
        structure.setStyleSheet("color: #333; margin-left: 20px;")
        group_layout.addWidget(structure)
        
        self.group_options.setLayout(group_layout)
        layout.addWidget(self.group_options)
        layout.addStretch()
        
        return page
    
    def _create_summary_page(self) -> QWidget:
        """Pagina 4: Samenvatting."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.group_summary = QGroupBox(t("wizard.step4.title"))
        group_layout = QVBoxLayout()
        
        self.lbl_summary_check = QLabel(t("wizard.step4.check"))
        self.lbl_summary_check.setStyleSheet("font-weight: bold;")
        group_layout.addWidget(self.lbl_summary_check)
        
        self.lbl_summary = QLabel()
        self.lbl_summary.setWordWrap(True)
        self.lbl_summary.setStyleSheet("background: #f5f5f5; padding: 15px; border-radius: 5px;")
        
        group_layout.addWidget(self.lbl_summary)
        
        self.group_summary.setLayout(group_layout)
        layout.addWidget(self.group_summary)
        layout.addStretch()
        
        return page
    
    def _create_progress_page(self) -> QWidget:
        """Pagina 5: Voortgang."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.group_progress = QGroupBox(t("wizard.step5.title"))
        group_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        
        self.lbl_progress = QLabel(t("wizard.step5.generating"))
        self.lbl_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        group_layout.addWidget(self.progress_bar)
        group_layout.addWidget(self.lbl_progress)
        
        self.group_progress.setLayout(group_layout)
        layout.addWidget(self.group_progress)
        layout.addStretch()
        
        return page
    
    def _create_result_page(self) -> QWidget:
        """Pagina 6: Resultaat."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.group_result = QGroupBox(t("wizard.step6.title"))
        group_layout = QVBoxLayout()
        
        self.lbl_result = QLabel()
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setStyleSheet("font-size: 11pt; padding: 10px;")
        
        group_layout.addWidget(self.lbl_result)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self.btn_open_folder = QPushButton(t("button.open_folder"))
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
        
        self.btn_open_editor = QPushButton(t("button.open_editor"))
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
        
        self.btn_new_project = QPushButton(t("button.new_project"))
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
        
        self.btn_close = QPushButton(t("button.close"))
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
        
        self.group_result.setLayout(group_layout)
        layout.addWidget(self.group_result)
        layout.addStretch()
        
        return page
    
    def _browse_location(self):
        """Open folder browser."""
        start_dir = self.settings.default_project_root or "C:\\"
        
        folder = QFileDialog.getExistingDirectory(
            self,
            t("wizard.step1.location"),
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
            self.btn_next.setText(t("button.generate"))
            self.btn_next.setEnabled(True)
        elif current >= 4:
            self.btn_next.setVisible(False)
            self.btn_back.setVisible(False)
        else:
            self.btn_next.setText(t("button.next"))
            self.btn_next.setEnabled(True)
            self.btn_next.setVisible(True)
            self.btn_back.setVisible(True)
    
    def _update_summary(self):
        """Update samenvatting tekst."""
        venv_text = t("wizard.step4.venv_yes") if self.chk_venv.isChecked() else t("wizard.step4.venv_no")
        desc = self.txt_description.toPlainText() or '<i>Geen</i>'
        
        summary_text = f"""
<b>{t('wizard.step4.location')}:</b><br>
{self.project_location / self.app_name}<br><br>

<b>{t('wizard.step4.appname')}:</b> {self.app_name}<br>
<b>{t('wizard.step4.author')}:</b> {self.txt_author.text()}<br>
<b>{t('wizard.step4.version')}:</b> {self.txt_version.text()}<br>
<b>{t('wizard.step4.description')}:</b> {desc}<br><br>

<b>{t('wizard.step4.options')}:</b><br>
- {t('wizard.step4.venv_option')} {venv_text}<br><br>

<b>{t('wizard.step4.will_create')}:</b><br>
- {t('wizard.step4.folders')}<br>
- {t('wizard.step4.files')}<br>
- {t('wizard.step4.export_script')}<br>
- {t('wizard.step4.spec_file')}<br>
- {t('wizard.step4.vscode_config')}<br>
"""
        
        if self.chk_venv.isChecked():
            summary_text += f"• {t('wizard.step4.venv_env')}<br>"
        
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
<p><b>{t('wizard.step6.location')}</b><br><code>{project_path}</code></p>
<p style='color: #666;'>{t('wizard.step6.info')}</p>
"""
            self.lbl_result.setText(result_text)
            self.stack.setCurrentIndex(5)
            self._update_navigation()
        else:
            QMessageBox.critical(self, "Error", message)
    
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
                    t("error.editor_not_found"),
                    t("error.editor_not_found_message", editor=editor_path)
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
    
    def _change_language(self, locale: str):
        """Verander taal en herlaad UI."""
        self.translator.set_locale(locale)
        self.settings.locale = locale
        self.settings.save()
        
        # Herlaad UI teksten
        self._refresh_ui()
    
    def _refresh_ui(self):
        """Herlaad alle UI teksten na taal wijziging."""
        # Window title
        self.setWindowTitle(t("app.title"))
        
        # Main labels
        self.lbl_title.setText(t("app.title"))
        self.lbl_subtitle.setText(t("app.subtitle"))
        
        # Page 1
        self.group_location.setTitle(t("wizard.step1.title"))
        self.lbl_location.setText(t("wizard.step1.location"))
        self.btn_browse.setText(t("wizard.step1.browse"))
        self.lbl_appname.setText(f"\n{t('wizard.step1.appname')}")
        self.txt_location.setPlaceholderText(t("wizard.step1.placeholder"))
        self.txt_appname.setPlaceholderText(t("wizard.step1.appname_placeholder"))
        self.lbl_location_info.setText(t("wizard.step1.info"))
        
        # Page 2
        self.group_metadata.setTitle(t("wizard.step2.title"))
        self.txt_author.setPlaceholderText(t("wizard.step2.author_placeholder"))
        self.txt_description.setPlaceholderText(t("wizard.step2.description_placeholder"))
        
        # Page 3
        self.group_options.setTitle(t("wizard.step3.title"))
        self.chk_venv.setText(t("wizard.step3.venv"))
        self.lbl_venv_info.setText(t("wizard.step3.venv_info"))
        self.lbl_structure_title.setText(t("wizard.step3.structure_title"))
        
        # Page 4
        self.group_summary.setTitle(t("wizard.step4.title"))
        self.lbl_summary_check.setText(t("wizard.step4.check"))
        
        # Page 5
        self.group_progress.setTitle(t("wizard.step5.title"))
        self.lbl_progress.setText(t("wizard.step5.generating"))
        
        # Page 6
        self.group_result.setTitle(t("wizard.step6.title"))
        
        # Buttons
        self.btn_back.setText(t("button.previous"))
        self.btn_open_folder.setText(t("button.open_folder"))
        self.btn_open_editor.setText(t("button.open_editor"))
        self.btn_new_project.setText(t("button.new_project"))
        self.btn_close.setText(t("button.close"))
        
        # Update navigation button text
        self._update_navigation()
        
        # Re-update summary if on summary page
        if self.stack.currentIndex() == 3:
            self._update_summary()
        
        # ← NIEUW: Rebuild menu's
        self._rebuild_menu()
    
    def _show_settings(self):
        """Toon settings dialoog."""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            # Refresh auteur veld na opslaan settings
            if self.settings.default_author:
                self.txt_author.setText(self.settings.default_author)
            
            # Check if language changed
            if self.translator.locale != self.settings.locale:
                self.translator.set_locale(self.settings.locale)
                self._refresh_ui()
    
    def _open_tools_dialog(self):
        """
        Opent de Tools-dialoog (headers controleren/toevoegen +
        PROJECT_STRUCTURE.md genereren) — geporte project-doc-tool-
        functionaliteit, zie gui/tools_dialog.py.

        Als er in deze sessie al een project gegenereerd is
        (self.generated_project_path), wordt de dialoog daarmee voorgevuld
        zodat je meteen tegen dat project kan werken.
        """
        initial_path = (
            Path(self.generated_project_path) if self.generated_project_path else None
        )
        dialog = ToolsDialog(self, initial_path=initial_path)
        dialog.exec()

    def _show_help(self):
        """Toon help."""
        # Bepaal welk bestand op basis van huidige taal
        locale = self.translator.locale
        help_file = Path(__file__).parent.parent / "docs" / f"HELP_{locale}.md"
        
        # Fallback naar Engels
        if not help_file.exists():
            help_file = Path(__file__).parent.parent / "docs" / "HELP_en_US.md"
        
        if help_file.exists():
            content = help_file.read_text(encoding='utf-8')
            self._show_markdown_dialog(t("menu.help.help"), content)
        else:
            QMessageBox.information(
                self,
                t("menu.help.help"),
                "Help documentation not found."
            )

    def _show_changelog(self):
        """Toon changelog."""
        # Bepaal welk bestand op basis van huidige taal
        locale = self.translator.locale
        changelog_file = Path(__file__).parent.parent / "docs" / f"CHANGELOG_{locale}.md"
        
        # Fallback naar Engels
        if not changelog_file.exists():
            changelog_file = Path(__file__).parent.parent / "docs" / "CHANGELOG_en_US.md"
        
        if changelog_file.exists():
            content = changelog_file.read_text(encoding='utf-8')
            self._show_markdown_dialog(t("menu.help.changelog"), content)
        else:
            QMessageBox.information(
                self,
                t("menu.help.changelog"),
                "Changelog not found."
            )
    
    def _show_about(self):
        """Toon about dialog."""
        about_text = f"""
<h2>{t("app.title")}</h2>
<p><b>{t("about.version")}</b> 1.0.5</p>
<p><b>{t("about.author")}</b> Barremans</p>
<p><b>{t("about.description")}</b><br>
{t("about.description_text")}</p>

<p><b>{t("about.features")}</b></p>
<ul>
<li>Wizard interface</li>
<li>Template-based systeem</li>
<li>Automatische venv setup</li>
<li>VS Code configuratie</li>
<li>Export scripts</li>
<li>PyInstaller templates</li>
<li>Keyboard shortcuts</li>
<li>Meertaligheid (NL/EN)</li>
</ul>

<p><b>{t("about.developed_with")}</b><br>
Python 3.11+ en PyQt6</p>

<p style='color: #666; margin-top: 20px;'>
{t("about.copyright")}
</p>
"""
        
        msg = QMessageBox(self)
        msg.setWindowTitle(t("about.title"))
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
        
        btn_close = QPushButton(t("button.close"))
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