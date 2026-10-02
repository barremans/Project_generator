# -*- mode: python ; coding: utf-8 -*-
# File:    /Project_Generator.spec
# Rol:     PyInstaller build-specificatie voor de Project Generator-app
# Versie:  1.2.0
# Auteur:  Barremans
# Changes: 1.2.0 - Windows VersionInfo-resource toegevoegd aan de EXE()-call
#                   (version='version_info.txt') — de exe had voorheen GEEN
#                   CompanyName/ProductName/FileDescription/FileVersion in
#                   zijn Windows-eigenschappen (Verkenner > Rechtsklik >
#                   Eigenschappen > Details toonde niets). Ontbrekende
#                   VersionInfo is één van de signalen die SmartScreen/
#                   Defender-reputatiescoring gebruikt om een binary als
#                   verdacht te beoordelen — samen met het signing-
#                   certificaat (zie build_installer.bat v1.1.0) onderdeel
#                   van de "Kan geen toegang krijgen..."-analyse op andere
#                   machines. version_info.txt wordt NIET statisch
#                   meegeleverd, maar dynamisch gegenereerd door
#                   build_installer.bat v1.2.0 vóór elke PyInstaller-build
#                   (zodat FileVersion/ProductVersion altijd de effectieve
#                   build-versie weerspiegelen, i.p.v. een hardcoded getal
#                   dat na een versiebump stil achterloopt).
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
import os

# Fallback: als build_installer.bat dit niet vooraf gegenereerd heeft (bv.
# direct 'pyinstaller Project_Generator.spec' zonder het bat-script), schrijf
# een minimale placeholder-versie weg zodat de build niet hard crasht.
# build_installer.bat v1.2.0 overschrijft dit normaal altijd met de echte
# build-versie vóór deze .spec aangeroepen wordt.
if not os.path.exists('version_info.txt'):
    with open('version_info.txt', 'w', encoding='utf-8') as _vf:
        _vf.write(
            "VSVersionInfo(\n"
            "  ffi=FixedFileInfo(filevers=(0,0,0,0), prodvers=(0,0,0,0), mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0,0)),\n"
            "  kids=[StringFileInfo([StringTable(u'040904B0', [\n"
            "    StringStruct(u'CompanyName', u'CGK'),\n"
            "    StringStruct(u'FileDescription', u'Python Project Generator'),\n"
            "    StringStruct(u'FileVersion', u'0.0.0'),\n"
            "    StringStruct(u'InternalName', u'Project_Generator'),\n"
            "    StringStruct(u'OriginalFilename', u'Project_Generator.exe'),\n"
            "    StringStruct(u'ProductName', u'Python Project Generator'),\n"
            "    StringStruct(u'ProductVersion', u'0.0.0')])]),\n"
            "  VarFileInfo([VarStruct(u'Translation', [1033, 1200])])]\n"
            ")\n"
        )

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
    version='version_info.txt',
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
