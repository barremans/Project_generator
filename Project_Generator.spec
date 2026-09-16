# -*- mode: python ; coding: utf-8 -*-
# File:    /Project_Generator.spec
# Rol:     PyInstaller build-specificatie voor de Project Generator-app
# Versie:  1.1.0
# Auteur:  Barremans
# Changes: 1.1.0 - BUGFIX: collect_all('PySide6') vervangen door
#                   collect_all('PyQt6'). De app importeert overal PyQt6
#                   (main.py, main_window.py, settings_dialog.py,
#                   requirements.txt) — de vorige versie verzamelde
#                   binaries/datas/hiddenimports voor een pakket dat
#                   nergens gebruikt wordt, en miste daardoor de
#                   PyQt6-specifieke DLL's/plugins die PyInstaller anders
#                   niet automatisch detecteert. i18n/locales- en
#                   assets-datas ongewijzigd overgenomen.
# Changes: 1.0.0 - Baseline (PySide6-collectie, foutief voor deze app).

from PyInstaller.utils.hooks import collect_all

# Collect ALL PyQt6 components
pyqt6_datas, pyqt6_binaries, pyqt6_hiddenimports = collect_all('PyQt6')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyqt6_binaries,  # ← PyQt6 DLLs
    datas=[
        ('i18n/locales', 'i18n/locales'),
        ('assets', 'assets'),
    ] + pyqt6_datas,  # ← PyQt6 data files
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ] + pyqt6_hiddenimports,  # ← PyQt6 hidden imports
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Project_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    icon='assets/icons/logo.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Project_Generator',
)
