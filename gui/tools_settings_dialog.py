"""
File:    /gui/tools_settings_dialog.py
Rol:     Instellingen voor de tools (add_headers/generate_index):
         include-extensies, exclude-mappen, exclude-bestanden, en de
         headerdefaults applicatie/versie (auteur hergebruikt het
         bestaande "Standaard Auteur" uit de hoofd-instellingen).
Applicatie: Project Generator
Versie:  1.0.0
Auteur:  Barremans
Changes: 1.0.0 - Geport vanuit project-doc-tool (settings_dialog.py v2.0.1,
                  auteur Barre) in het kader van de samenvoeging (zie
                  context_ProjectDocTool.md §7.4). Dit was per abuis nog
                  niet meegenomen bij de eerste ToolsDialog-port — deze
                  dialoog was net de kern van de klacht "ik mis mijn
                  instellingen voor de doc tool". Losgekoppeld van
                  project-doc-tool's eigen `settings`-object: leest/schrijft
                  nu rechtstreeks op een utils.settings.AppSettings-
                  instantie (tools_include_exts/tools_exclude_dirs/
                  tools_exclude_files/tools_default_applicatie/
                  tools_default_versie, v1.1.0) — dus in hetzelfde
                  settings.json als de rest van Project Generator, geen
                  los tweede instellingenbestand meer. Het "Auteur"-veld
                  uit het origineel is NIET overgenomen als apart veld:
                  dat is nu hetzelfde veld als "Standaard Auteur" in de
                  hoofd-instellingen (self.settings.default_author) — één
                  bron van waarheid voor "wie ben ik" in de hele app.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QMessageBox,
    QInputDialog,
)

from utils.settings import AppSettings


class ToolsSettingsDialog(QDialog):
    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)

        self.settings = settings
        self.setWindowTitle("Tools - Instellingen")
        self.resize(500, 560)

        layout = QVBoxLayout(self)

        # =================================================
        # INCLUDE EXTENSIONS
        # =================================================

        layout.addWidget(QLabel("Include extensies"))
        self.include_list = QListWidget()
        self.include_list.addItems(self.settings.tools_include_exts)
        layout.addWidget(self.include_list)

        layout.addLayout(
            self._add_remove_buttons(self.include_list, "Nieuwe extensie (bv: .py)")
        )

        # =================================================
        # EXCLUDE DIRECTORIES
        # =================================================

        layout.addWidget(QLabel("Exclude mappen"))
        self.exclude_dirs_list = QListWidget()
        self.exclude_dirs_list.addItems(self.settings.tools_exclude_dirs)
        layout.addWidget(self.exclude_dirs_list)

        layout.addLayout(
            self._add_remove_buttons(self.exclude_dirs_list, "Nieuwe map (bv: .venv)")
        )

        # =================================================
        # EXCLUDE FILES
        # =================================================

        layout.addWidget(QLabel("Exclude bestanden"))
        self.exclude_files_list = QListWidget()
        self.exclude_files_list.addItems(self.settings.tools_exclude_files)
        layout.addWidget(self.exclude_files_list)

        layout.addLayout(
            self._add_remove_buttons(self.exclude_files_list, "Nieuwe bestandsnaam")
        )

        # =================================================
        # METADATA DEFAULTS
        # =================================================
        # "Auteur" is bewust WEGGELATEN hier — dat is settings.default_author
        # (hoofd-instellingen), niet dupliceren.

        layout.addWidget(QLabel("Applicatie (leeg = automatisch uit mapnaam)"))
        self.applicatie = QLineEdit(self.settings.tools_default_applicatie)
        layout.addWidget(self.applicatie)

        layout.addWidget(QLabel("Standaard versie (fallback bij ontbrekende header)"))
        self.versie = QLineEdit(self.settings.tools_default_versie)
        layout.addWidget(self.versie)

        # =================================================
        # ACTION BUTTONS
        # =================================================

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Opslaan")
        btn_cancel = QPushButton("Annuleren")

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _add_remove_buttons(self, list_widget, prompt):
        layout = QHBoxLayout()
        btn_add = QPushButton("➕ Toevoegen")
        btn_remove = QPushButton("➖ Verwijderen")

        layout.addWidget(btn_add)
        layout.addWidget(btn_remove)

        btn_add.clicked.connect(lambda: self._add_item(list_widget, prompt))
        btn_remove.clicked.connect(lambda: self._remove_item(list_widget))

        return layout

    def _add_item(self, list_widget, prompt):
        text, ok = QInputDialog.getText(self, "Toevoegen", prompt)
        if ok and text.strip():
            value = text.strip()
            existing = [list_widget.item(i).text() for i in range(list_widget.count())]
            if value in existing:
                QMessageBox.information(self, "Bestaat al", f"'{value}' staat al in de lijst.")
                return
            list_widget.addItem(value)

    def _remove_item(self, list_widget):
        row = list_widget.currentRow()
        if row >= 0:
            list_widget.takeItem(row)

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def save(self):
        try:
            self.settings.tools_include_exts = [
                self.include_list.item(i).text() for i in range(self.include_list.count())
            ]
            self.settings.tools_exclude_dirs = [
                self.exclude_dirs_list.item(i).text() for i in range(self.exclude_dirs_list.count())
            ]
            self.settings.tools_exclude_files = [
                self.exclude_files_list.item(i).text() for i in range(self.exclude_files_list.count())
            ]
            self.settings.tools_default_applicatie = self.applicatie.text().strip()
            self.settings.tools_default_versie = self.versie.text().strip() or "1.0.0"

            self.settings.save()
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Fout", str(e))