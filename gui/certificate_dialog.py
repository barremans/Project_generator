"""
gui/certificate_dialog.py

GUI for inspecting/creating/exporting Windows code-signing certificates
and scanning applications for Authenticode signatures.
"""

from __future__ import annotations

import os
import webbrowser
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView, QCheckBox, QComboBox, QDialog, QFileDialog,
    QFormLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMessageBox, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
    QTabWidget, QVBoxLayout, QWidget,
)

from core.certificate_manager import (
    DEFAULT_SUBJECT,
    DEFENDER_CERTIFICATE_URL,
    CertificateManagerError,
    create_code_signing_certificate,
    export_certificate,
    list_code_signing_certificates,
    certificate_trust_status,
    trust_certificate_current_user,
    scan_signed_files, sign_files,
    current_windows_user, is_elevated, get_active_thumbprint, set_active_certificate,
)


class ScanWorker(QThread):
    done = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, root: Path, recursive: bool = True, parent=None):
        super().__init__(parent)
        self.root = root
        self.recursive = recursive

    def run(self):
        try:
            self.done.emit(scan_signed_files(self.root, self.recursive))
        except Exception as exc:
            self.failed.emit(str(exc))


class CertificateDialog(QDialog):
    def __init__(self, parent=None, initial_path: Path | None = None):
        super().__init__(parent)
        self.setWindowTitle("Certificaten & Signing")
        self.resize(1050, 680)
        self._certs = []
        self._worker = None
        self._scan_results = []
        self._build_ui(initial_path)
        self.refresh_certificates()

    def _build_ui(self, initial_path):
        layout = QVBoxLayout(self)
        user = current_windows_user()
        env = QLabel(f"<b>Windows gebruiker:</b> {user} &nbsp;&nbsp; <b>Elevated:</b> {'Ja' if is_elevated() else 'Nee'}")
        layout.addWidget(env)
        if user.lower().endswith("\\pcadmin"):
            warning = QLabel("<b>LET OP:</b> Project Generator draait als LAPS/pcadmin. Maak hier geen productiecertificaat aan. Start als de buildgebruiker BBossuyt.")
            warning.setWordWrap(True)
            layout.addWidget(warning)
        info = QLabel(
            "Beheer Windows code-signingcertificaten, exporteer de publieke .cer "
            "voor Defender en controleer Authenticode-signatures van applicaties."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Certificates tab
        cert_tab = QWidget()
        cert_layout = QVBoxLayout(cert_tab)

        top = QHBoxLayout()
        self.subject_filter = QLineEdit(DEFAULT_SUBJECT)
        self.subject_filter.setPlaceholderText("CN=CGK Local Signing")
        top.addWidget(QLabel("Subject:"))
        top.addWidget(self.subject_filter, 1)
        btn_refresh = QPushButton("Vernieuwen")
        btn_refresh.clicked.connect(self.refresh_certificates)
        top.addWidget(btn_refresh)
        cert_layout.addLayout(top)

        self.cert_table = QTableWidget(0, 10)
        self.cert_table.setHorizontalHeaderLabels(
            ["Status", "Subject", "Thumbprint", "Geldig tot", "Dagen", "Private key", "Root", "Publisher", "Actief", "Store"]
        )
        self.cert_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.cert_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.cert_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cert_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.cert_table.horizontalHeader().setStretchLastSection(True)
        cert_layout.addWidget(self.cert_table)

        actions = QHBoxLayout()
        active_btn = QPushButton("Als actief instellen")
        active_btn.clicked.connect(self.set_active_selected)
        actions.addWidget(active_btn)

        export_btn = QPushButton("Export .cer...")
        export_btn.clicked.connect(self.export_selected)
        actions.addWidget(export_btn)

        defender_btn = QPushButton("Open Microsoft Defender")
        defender_btn.clicked.connect(lambda: webbrowser.open(DEFENDER_CERTIFICATE_URL))
        actions.addWidget(defender_btn)

        actions.addStretch()
        new_btn = QPushButton("Nieuw certificaat...")
        new_btn.clicked.connect(self.create_certificate)
        actions.addWidget(new_btn)
        cert_layout.addLayout(actions)
        tabs.addTab(cert_tab, "Certificaten")

        # Scanner tab
        scan_tab = QWidget()
        scan_layout = QVBoxLayout(scan_tab)
        path_row = QHBoxLayout()
        default_root = str(initial_path) if initial_path else r"C:\PY"
        self.scan_path = QLineEdit(default_root)
        path_row.addWidget(QLabel("Map:"))
        path_row.addWidget(self.scan_path, 1)
        browse = QPushButton("Kies map...")
        browse.clicked.connect(self.choose_scan_path)
        path_row.addWidget(browse)
        scan_layout.addLayout(path_row)

        scan_options = QHBoxLayout()
        self.recursive = QCheckBox("Projecten onder deze map zoeken (alleen dist\\*.exe)")
        self.recursive.setChecked(True)
        scan_options.addWidget(self.recursive)
        scan_options.addStretch()
        self.scan_btn = QPushButton("Dist-applicaties controleren")
        self.scan_btn.clicked.connect(self.start_scan)
        scan_options.addWidget(self.scan_btn)
        scan_layout.addLayout(scan_options)

        sign_actions = QHBoxLayout()
        sign_actions.addStretch()
        self.sign_selected_btn = QPushButton("Geselecteerde signen")
        self.sign_selected_btn.clicked.connect(self.sign_selected)
        sign_actions.addWidget(self.sign_selected_btn)
        self.sign_unsigned_btn = QPushButton("Alle unsigned signen")
        self.sign_unsigned_btn.clicked.connect(self.sign_all_unsigned)
        sign_actions.addWidget(self.sign_unsigned_btn)
        scan_layout.addLayout(sign_actions)

        self.scan_table = QTableWidget(0, 5)
        self.scan_table.setHorizontalHeaderLabels(
            ["Status", "Bestand", "Signer", "Thumbprint", "Geldig tot"]
        )
        self.scan_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.scan_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.scan_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.scan_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.scan_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        scan_layout.addWidget(self.scan_table)
        tabs.addTab(scan_tab, "Applicaties controleren")

        close_row = QHBoxLayout()
        close_row.addStretch()
        close_btn = QPushButton("Sluiten")
        close_btn.clicked.connect(self.accept)
        close_row.addWidget(close_btn)
        layout.addLayout(close_row)

    def refresh_certificates(self):
        try:
            self._certs = list_code_signing_certificates(self.subject_filter.text().strip())
        except Exception as exc:
            QMessageBox.critical(self, "Certificaten", str(exc))
            return

        self.cert_table.setRowCount(len(self._certs))
        for row, cert in enumerate(self._certs):
            days = cert.days_remaining
            if cert.is_expired:
                status = "VERLOPEN"
            elif days is not None and days <= 30:
                status = "WAARSCHUWING"
            else:
                status = "GELDIG"
            try:
                trust = certificate_trust_status(cert.thumbprint)
            except Exception:
                trust = {"root": False, "trusted_publisher": False}
            active = get_active_thumbprint().upper() == cert.thumbprint.upper()
            values = [
                status, cert.subject, cert.thumbprint, cert.not_after[:10],
                "" if days is None else str(days),
                "Ja" if cert.has_private_key else "Nee",
                "Ja" if trust["root"] else "Nee",
                "Ja" if trust["trusted_publisher"] else "Nee",
                "Ja" if active else "Nee",
                cert.store,
            ]
            for col, value in enumerate(values):
                self.cert_table.setItem(row, col, QTableWidgetItem(value))

    def _selected_cert(self):
        row = self.cert_table.currentRow()
        if row < 0 or row >= len(self._certs):
            QMessageBox.information(self, "Certificaat", "Selecteer eerst een certificaat.")
            return None
        return self._certs[row]

    def set_active_selected(self):
        cert = self._selected_cert()
        if not cert:
            return
        if cert.is_expired or not cert.has_private_key:
            QMessageBox.warning(self, "Niet bruikbaar", "Het actieve signingcertificaat moet geldig zijn en een private key hebben.")
            return
        try:
            trust = certificate_trust_status(cert.thumbprint)
            if not (trust["root"] and trust["trusted_publisher"]):
                answer = QMessageBox.question(
                    self, "Windows trust ontbreekt",
                    "Dit certificaat staat nog niet in CurrentUser\\Root en/of "
                    "CurrentUser\\TrustedPublisher.\n\n"
                    "De publieke certificaatkopie nu automatisch vertrouwen?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if answer != QMessageBox.StandardButton.Yes:
                    return
                trust_certificate_current_user(cert.thumbprint)
        except Exception as exc:
            QMessageBox.critical(self, "Trust instellen mislukt", str(exc))
            return
        set_active_certificate(cert)
        self.refresh_certificates()
        QMessageBox.information(self, "Actief signingcertificaat", f"Actieve thumbprint:\n{cert.thumbprint}")

    def export_selected(self):
        cert = self._selected_cert()
        if not cert:
            return
        suggested = f"CGK_Local_Signing_{cert.thumbprint[:12]}.cer"
        filename, _ = QFileDialog.getSaveFileName(
            self, "Certificaat exporteren", str(Path.home() / "Desktop" / suggested),
            "Certificate (*.cer)"
        )
        if not filename:
            return
        try:
            path = export_certificate(cert.thumbprint, Path(filename))
            QMessageBox.information(
                self, "Export geslaagd",
                f"Publiek certificaat geëxporteerd naar:\n{path}\n\n"
                "Gebruik daarna 'Open Microsoft Defender' om deze .cer als Certificate Indicator toe te voegen."
            )
        except Exception as exc:
            QMessageBox.critical(self, "Export mislukt", str(exc))

    def create_certificate(self):
        if current_windows_user().lower().endswith("\\pcadmin"):
            QMessageBox.critical(self, "Geblokkeerd", "Je draait als LAPS/pcadmin. Start Project Generator als BBossuyt om het productiecertificaat aan te maken.")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("Nieuw code-signingcertificaat")
        form = QFormLayout(dialog)
        name = QLineEdit("CGK Local Signing")
        years = QSpinBox()
        years.setRange(1, 10)
        years.setValue(2)
        store = QComboBox()
        store.addItems([r"Cert:\CurrentUser\My"])
        store.setToolTip("Productiecertificaten worden per buildgebruiker in CurrentUser\\My bewaard.")
        form.addRow("Common name:", name)
        form.addRow("Geldigheid (jaren):", years)
        form.addRow("Certificate store:", store)

        warning = QLabel(
            "Dit maakt een NIEUW self-signed Code Signing-certificaat. "
            "Het bestaande certificaat wordt niet gewijzigd of verwijderd. "
            "Een nieuw certificaat heeft een nieuwe thumbprint."
        )
        warning.setWordWrap(True)
        form.addRow(warning)

        buttons = QHBoxLayout()
        cancel = QPushButton("Annuleren")
        create = QPushButton("Aanmaken")
        cancel.clicked.connect(dialog.reject)
        create.clicked.connect(dialog.accept)
        buttons.addStretch()
        buttons.addWidget(cancel)
        buttons.addWidget(create)
        form.addRow(buttons)

        if not dialog.exec():
            return

        try:
            cert = create_code_signing_certificate(
                common_name=name.text().strip(),
                years=years.value(),
                store=store.currentText(),
            )
        except Exception as exc:
            QMessageBox.critical(self, "Aanmaken mislukt", str(exc))
            return

        try:
            trust = trust_certificate_current_user(cert.thumbprint)
        except Exception as exc:
            self.subject_filter.setText(cert.subject)
            self.refresh_certificates()
            QMessageBox.critical(
                self, "Certificaat aangemaakt, trust mislukt",
                f"Het certificaat is aangemaakt, maar Windows trust kon niet worden ingesteld.\n\n"
                f"Thumbprint: {cert.thumbprint}\n\n{exc}\n\n"
                "Het certificaat is daarom NIET automatisch als actief ingesteld."
            )
            return

        set_active_certificate(cert)
        self.subject_filter.setText(cert.subject)
        self.refresh_certificates()
        QMessageBox.information(
            self, "Certificaat aangemaakt en vertrouwd",
            f"Subject: {cert.subject}\n"
            f"Thumbprint: {cert.thumbprint}\n"
            f"Geldig tot: {cert.not_after[:10]}\n"
            f"Private key: {'Ja' if cert.has_private_key else 'Nee'}\n"
            f"CurrentUser\\Root: {'Ja' if trust['root'] else 'Nee'}\n"
            f"CurrentUser\\TrustedPublisher: {'Ja' if trust['trusted_publisher'] else 'Nee'}\n"
            f"Actief signingcertificaat: Ja\n\n"
            "Exporteer nu de .cer en voeg het certificaat in Microsoft Defender toe als Allow / Never."
        )

    def choose_scan_path(self):
        path = QFileDialog.getExistingDirectory(self, "Kies applicatie- of projectmap", self.scan_path.text())
        if path:
            self.scan_path.setText(path)

    def start_scan(self):
        root = Path(self.scan_path.text().strip())
        if not root.exists():
            QMessageBox.warning(self, "Map", f"Map bestaat niet:\n{root}")
            return
        self.scan_btn.setEnabled(False)
        self.scan_btn.setText("Bezig met scannen...")
        self.scan_table.setRowCount(0)
        self._worker = ScanWorker(root, self.recursive.isChecked(), self)
        self._worker.done.connect(self._scan_done)
        self._worker.failed.connect(self._scan_failed)
        self._worker.start()

    def _scan_done(self, results):
        self._scan_results = list(results)
        self.scan_btn.setEnabled(True)
        self.scan_btn.setText("Dist-applicaties controleren")
        self.scan_table.setRowCount(len(results))
        for row, item in enumerate(results):
            values = [
                item.status, item.path, item.subject, item.thumbprint,
                item.not_after[:10] if item.not_after else "",
            ]
            for col, value in enumerate(values):
                self.scan_table.setItem(row, col, QTableWidgetItem(value))

    def _active_signing_cert(self):
        thumb = get_active_thumbprint()
        if not thumb:
            QMessageBox.warning(
                self, "Geen actief certificaat",
                "Ga eerst naar de tab Certificaten en kies 'Als actief instellen'."
            )
            return None
        for cert in self._certs:
            if cert.thumbprint.upper() == thumb.upper():
                if cert.is_expired or not cert.has_private_key:
                    QMessageBox.warning(self, "Certificaat niet bruikbaar",
                                        "Het actieve certificaat is verlopen of heeft geen private key.")
                    return None
                return cert
        self.refresh_certificates()
        for cert in self._certs:
            if cert.thumbprint.upper() == thumb.upper():
                return cert
        QMessageBox.warning(self, "Certificaat niet gevonden",
                            f"De actieve thumbprint is niet beschikbaar:\n{thumb}")
        return None

    def _confirm_and_sign(self, paths):
        cert = self._active_signing_cert()
        if not cert or not paths:
            return
        preview = "\n".join(str(p) for p in paths[:10])
        if len(paths) > 10:
            preview += f"\n... en nog {len(paths)-10} bestand(en)"
        answer = QMessageBox.question(
            self, "Bestanden signen",
            f"Signen met:\n{cert.subject}\n{cert.thumbprint}\n\n"
            f"Bestanden ({len(paths)}):\n{preview}\n\n"
            "Na signing wordt elk bestand automatisch met signtool geverifieerd.\n\nDoorgaan?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        results = sign_files([Path(p) for p in paths], cert.thumbprint)
        failed = [(p,m) for p,ok,m in results if not ok]
        if failed:
            text = "\n\n".join(f"{p}\n{m}" for p,m in failed[:5])
            QMessageBox.critical(self, "Signing niet volledig geslaagd",
                                 f"{len(results)-len(failed)} geslaagd, {len(failed)} mislukt.\n\n{text}")
        else:
            QMessageBox.information(self, "Signing geslaagd",
                                    f"{len(results)} bestand(en) gesigned en geverifieerd.")
        self.start_scan()

    def sign_selected(self):
        rows = sorted({idx.row() for idx in self.scan_table.selectionModel().selectedRows()})
        if not rows:
            QMessageBox.information(self, "Selectie", "Selecteer eerst één of meer unsigned bestanden.")
            return
        paths = []
        for row in rows:
            if row < len(self._scan_results):
                item = self._scan_results[row]
                if item.status == "NotSigned":
                    paths.append(item.path)
        if not paths:
            QMessageBox.information(self, "Selectie",
                                    "De geselecteerde rijen bevatten geen bestanden met status NotSigned.")
            return
        self._confirm_and_sign(paths)

    def sign_all_unsigned(self):
        paths = [x.path for x in self._scan_results if x.status == "NotSigned"]
        if not paths:
            QMessageBox.information(self, "Unsigned", "Geen unsigned distributiebestanden gevonden.")
            return
        self._confirm_and_sign(paths)

    def _scan_failed(self, message):
        self.scan_btn.setEnabled(True)
        self.scan_btn.setText("Dist-applicaties controleren")
        QMessageBox.critical(self, "Scan mislukt", message)
