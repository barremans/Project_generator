"""
File:    /gui/tools_dialog.py
Rol:     Dialoogvenster (QDialog) dat de geporte project-doc-tool-
         functionaliteit ontsluit binnen Project Generator: headers
         controleren/toevoegen en de projectstructuur (PROJECT_STRUCTURE.md)
         genereren, tegen een gekozen projectmap en outputmap.
Applicatie: Project Generator
Versie:  1.2.0
Auteur:  Barremans
Changes: 1.2.0 - Na "Projectstructuur genereren" wordt de outputmap nu
                  automatisch geopend in de Windows Verkenner (os.startfile),
                  zoals project-doc-tool's eigen main_window.py ook deed
                  (_open_output_folder(), gekoppeld aan
                  GenerateIndexWorker.finished). Enkel voor de structuur-
                  actie -- niet voor dry-run/headers-toevoegen.
Changes: 1.1.0 - Hersteld twee ontbrekende punten uit de eerste port
                  (gemeld door gebruiker n.a.v. screenshot-vergelijking met
                  project-doc-tool's origineel):
                  (1) Outputmap is nu apart kiesbaar via "Kies outputmap"
                      (in plaats van altijd hardcoded <projectmap>/docs) --
                      wijzigt wel automatisch mee naar <projectmap>/docs
                      zodra een NIEUWE projectmap gekozen wordt, tenzij de
                      gebruiker daarna zelf een andere outputmap kiest.
                  (2) Nieuwe "Settings"-knop opent gui/tools_settings_
                      dialog.py::ToolsSettingsDialog (include/exclude-
                      lijsten + applicatie/versie-defaults), gekoppeld aan
                      utils.settings.AppSettings -- de kern van wat de
                      gebruiker miste.
                  Project- en outputmap worden nu ook persistent onthouden
                  (AppSettings.tools_last_project_root/tools_last_output_dir)
                  en bij het openen van de dialoog automatisch herladen,
                  zoals project-doc-tool's eigen main_window.py ook deed.
                  count_headers_to_add()/add_headers()/
                  generate_project_structure() krijgen nu de geconfigureerde
                  include_exts/exclude_dirs/exclude_files/applicatie/versie/
                  auteur mee i.p.v. de hardcoded module-defaults.
Changes: 1.0.0 - Baseline (zie eerdere sessie -- geen outputmap-keuze, geen
                  Settings-knop; beide bevestigd als ontbrekend).
"""

from pathlib import Path
from typing import Optional
import os

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QPlainTextEdit,
)

from core.add_headers import count_headers_to_add, add_headers
from core.generate_index import generate_project_structure
from utils.settings import AppSettings
from gui.tools_settings_dialog import ToolsSettingsDialog


# ==================================================
# WORKERS (QThread -- zelfde patroon als project-doc-tool's workers.py)
# ==================================================

class BaseWorker(QThread):
    error = pyqtSignal(str)

    def __init__(self, project_root: Path, parent=None):
        super().__init__(parent)
        self.project_root = project_root


class HeadersDryRunWorker(BaseWorker):
    result = pyqtSignal(list)

    def __init__(self, project_root, include_exts, exclude_dirs, exclude_files, parent=None):
        super().__init__(project_root, parent)
        self.include_exts = include_exts
        self.exclude_dirs = exclude_dirs
        self.exclude_files = exclude_files

    def run(self):
        try:
            actions = count_headers_to_add(
                self.project_root, self.include_exts, self.exclude_dirs, self.exclude_files
            )
            self.result.emit(actions)
        except Exception as e:
            self.error.emit(str(e))


class HeadersApplyWorker(BaseWorker):
    result = pyqtSignal(int)

    def __init__(self, project_root, applicatie, auteur, versie,
                 include_exts, exclude_dirs, exclude_files, parent=None):
        super().__init__(project_root, parent)
        self.applicatie = applicatie
        self.auteur = auteur
        self.versie = versie
        self.include_exts = include_exts
        self.exclude_dirs = exclude_dirs
        self.exclude_files = exclude_files

    def run(self):
        try:
            count = add_headers(
                self.project_root,
                applicatie=self.applicatie,
                auteur=self.auteur,
                versie=self.versie,
                include_exts=self.include_exts,
                exclude_dirs=self.exclude_dirs,
                exclude_files=self.exclude_files,
            )
            self.result.emit(count)
        except Exception as e:
            self.error.emit(str(e))


class StructureWorker(BaseWorker):
    result = pyqtSignal(Path)

    def __init__(self, project_root, output_dir, exclude_dirs, exclude_files, parent=None):
        super().__init__(project_root, parent)
        self.output_dir = output_dir
        self.exclude_dirs = exclude_dirs
        self.exclude_files = exclude_files

    def run(self):
        try:
            output_file = generate_project_structure(
                self.project_root,
                self.output_dir,
                set(self.exclude_dirs) if self.exclude_dirs else None,
                set(self.exclude_files) if self.exclude_files else None,
            )
            self.result.emit(output_file)
        except Exception as e:
            self.error.emit(str(e))


# ==================================================
# DIALOOG
# ==================================================

class ToolsDialog(QDialog):
    """
    Bundelt headers-check/-fix en projectstructuur-generatie. Projectmap en
    outputmap zijn onafhankelijk kiesbaar (zoals project-doc-tool's
    origineel) en worden persistent onthouden via AppSettings.
    """

    def __init__(self, parent=None, initial_path: Optional[Path] = None,
                 settings: Optional[AppSettings] = None):
        super().__init__(parent)
        self.setWindowTitle("Project Generator - Tools")
        self.resize(620, 460)

        self.settings = settings if settings is not None else AppSettings()
        self.worker = None

        # Projectmap: expliciet meegegeven wint, anders laatst gebruikte uit settings.
        if initial_path:
            self.project_root: Optional[Path] = Path(initial_path)
        elif self.settings.tools_last_project_root:
            self.project_root = Path(self.settings.tools_last_project_root)
        else:
            self.project_root = None

        # Outputmap: laatst gebruikte uit settings, anders <projectmap>/docs.
        if self.settings.tools_last_output_dir:
            self.output_dir: Optional[Path] = Path(self.settings.tools_last_output_dir)
        elif self.project_root:
            self.output_dir = self.project_root / "docs"
        else:
            self.output_dir = None

        layout = QVBoxLayout(self)

        self.lbl_project = QLabel(self._project_label())
        layout.addWidget(self.lbl_project)

        row_project = QHBoxLayout()
        btn_choose_project = QPushButton("📂 Kies projectmap")
        btn_choose_project.clicked.connect(self.choose_project_folder)
        row_project.addWidget(btn_choose_project)
        layout.addLayout(row_project)

        self.lbl_output = QLabel(self._output_label())
        layout.addWidget(self.lbl_output)

        row_output = QHBoxLayout()
        btn_choose_output = QPushButton("📂 Kies outputmap")
        btn_choose_output.clicked.connect(self.choose_output_folder)
        row_output.addWidget(btn_choose_output)
        layout.addLayout(row_output)

        btn_settings = QPushButton("⚙ Settings")
        btn_settings.clicked.connect(self.open_settings)
        layout.addWidget(btn_settings)

        actions_row = QHBoxLayout()
        self.btn_dry_run = QPushButton("▶ Dry-run headers")
        self.btn_add_headers = QPushButton("✍ Headers toevoegen")
        self.btn_structure = QPushButton("📑 Projectstructuur genereren")
        for btn in (self.btn_dry_run, self.btn_add_headers, self.btn_structure):
            actions_row.addWidget(btn)
        layout.addLayout(actions_row)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.btn_dry_run.clicked.connect(self.on_dry_run)
        self.btn_add_headers.clicked.connect(self.on_add_headers)
        self.btn_structure.clicked.connect(self.on_generate_structure)

        self._update_buttons_enabled()

    # -------------- Helpers --------------

    def _project_label(self) -> str:
        return f"Projectmap: {self.project_root}" if self.project_root else "Projectmap: - (nog niet gekozen)"

    def _output_label(self) -> str:
        return f"Outputmap: {self.output_dir}" if self.output_dir else "Outputmap: - (nog niet gekozen)"

    def _update_buttons_enabled(self) -> None:
        enabled = self.project_root is not None and self.output_dir is not None
        for btn in (self.btn_dry_run, self.btn_add_headers, self.btn_structure):
            btn.setEnabled(enabled)

    def _log_line(self, text: str) -> None:
        self.log.appendPlainText(text)

    def _persist_paths(self) -> None:
        self.settings.tools_last_project_root = str(self.project_root) if self.project_root else ""
        self.settings.tools_last_output_dir = str(self.output_dir) if self.output_dir else ""
        self.settings.save()

    def choose_project_folder(self) -> None:
        start_dir = str(self.project_root) if self.project_root else str(Path.home())
        path = QFileDialog.getExistingDirectory(self, "Kies projectmap", start_dir)
        if path:
            self.project_root = Path(path)
            # Outputmap volgt automatisch mee naar <nieuwe map>/docs --
            # de gebruiker kan dat hierna nog altijd zelf overschrijven.
            self.output_dir = self.project_root / "docs"
            self.lbl_project.setText(self._project_label())
            self.lbl_output.setText(self._output_label())
            self.log.clear()
            self._update_buttons_enabled()
            self._persist_paths()

    def choose_output_folder(self) -> None:
        if not self.project_root:
            QMessageBox.warning(self, "Geen projectmap", "Kies eerst een projectmap.")
            return
        start_dir = str(self.output_dir) if self.output_dir else str(self.project_root)
        path = QFileDialog.getExistingDirectory(self, "Kies outputmap", start_dir)
        if path:
            self.output_dir = Path(path)
            self.lbl_output.setText(self._output_label())
            self._update_buttons_enabled()
            self._persist_paths()

    def open_settings(self) -> None:
        dialog = ToolsSettingsDialog(self.settings, self)
        dialog.exec()

    def _show_error(self, msg: str) -> None:
        QMessageBox.critical(self, "Fout", msg)

    def _clear_worker(self) -> None:
        self.worker = None

    # -------------- Acties --------------

    def on_dry_run(self) -> None:
        worker = HeadersDryRunWorker(
            self.project_root,
            set(self.settings.tools_include_exts),
            set(self.settings.tools_exclude_dirs),
            set(self.settings.tools_exclude_files),
        )
        self.worker = worker
        worker.result.connect(self._show_dry_run_result)
        worker.error.connect(self._show_error)
        worker.finished.connect(self._clear_worker)
        worker.start()

    def _show_dry_run_result(self, actions: list) -> None:
        if not actions:
            self._log_line("Alle bestanden hebben reeds een correcte header.")
            return

        counts = {"NO_HEADER": 0, "WRONG_HEADER": 0, "OK": 0}
        for item in actions:
            counts[item["status"]] += 1
            if item["status"] != "OK":
                self._log_line(f"  {item['status']:<13} {item['file']}")

        self._log_line(
            f"Samenvatting: {counts['NO_HEADER']} zonder header, "
            f"{counts['WRONG_HEADER']} foutieve header, {counts['OK']} OK. "
            "(dry-run -- geen wijzigingen)"
        )

    def on_add_headers(self) -> None:
        applicatie = self.settings.tools_default_applicatie or self.project_root.name
        worker = HeadersApplyWorker(
            self.project_root,
            applicatie,
            self.settings.default_author or None,
            self.settings.tools_default_versie,
            set(self.settings.tools_include_exts),
            set(self.settings.tools_exclude_dirs),
            set(self.settings.tools_exclude_files),
        )
        self.worker = worker
        worker.result.connect(lambda c: self._log_line(f"{c} bestand(en) aangepast."))
        worker.error.connect(self._show_error)
        worker.finished.connect(self._clear_worker)
        worker.start()

    def on_generate_structure(self) -> None:
        worker = StructureWorker(
            self.project_root,
            self.output_dir,
            self.settings.tools_exclude_dirs,
            self.settings.tools_exclude_files,
        )
        self.worker = worker
        worker.result.connect(lambda p: self._log_line(f"PROJECT_STRUCTURE.md aangemaakt: {p}"))
        worker.result.connect(lambda p: self._open_output_folder())
        worker.error.connect(self._show_error)
        worker.finished.connect(self._clear_worker)
        worker.start()

    def _open_output_folder(self) -> None:
        """Opent de outputmap in de Verkenner na een geslaagde structuur-generatie."""
        if self.output_dir and self.output_dir.exists():
            try:
                os.startfile(self.output_dir)
            except Exception as e:
                self._show_error(f"Kon outputmap niet openen: {e}")


# ==================================================
# Standalone testen (zolang gui/main_window.py de dialoog nog niet opent)
# ==================================================

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = ToolsDialog()
    dialog.show()
    sys.exit(app.exec())