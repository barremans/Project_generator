"""
core/generator.py

Beschrijving: Projectgenerator - creëert volledige projectstructuur
Applicatie: Project Generator
Versie: 1.0.3
Auteur: Barremans
"""

from pathlib import Path
from typing import Optional, List
import subprocess
import sys
import shutil

from core.context import ProjectContext
from core.templates import ProjectTemplate, FolderTemplate, FileTemplate
from core.header_renderer import HeaderRenderer
from utils.filesystem import (
    ensure_directory, 
    write_file, 
    path_exists, 
    is_directory_empty
)


class ProjectGenerator:
    """
    Genereert een volledig project op basis van templates.
    """
    
    def __init__(self, context: ProjectContext, template: ProjectTemplate):
        self.context = context
        self.template = template
        self.header_renderer = HeaderRenderer(context)
        self.created_files: List[Path] = []
        self.created_folders: List[Path] = []
        self.errors: List[str] = []
    
    def generate(self) -> bool:
        """
        Genereer het volledige project.
        
        Returns:
            True als succesvol, False bij fouten
        """
        print("=" * 60)
        print(f"🚀 Project Generator - {self.context.app_name}")
        print("=" * 60)
        
        # Stap 1: Validatie
        if not self._validate():
            return False
        
        # Stap 2: Maak root directory
        if not self._create_root():
            return False
        
        # Stap 3: Genereer folders
        if not self._generate_folders():
            return False
        
        # Stap 4: Genereer root files
        if not self._generate_root_files():
            return False
        
        # Stap 5: Kopieer standaard icons
        if not self._copy_default_icons():
            print("⚠️  Waarschuwing: Standaard icons niet gekopieerd")
        
        # Stap 6: Virtuele omgeving (optioneel)
        if self.template.create_venv:
            if not self._create_venv():
                print("⚠️  Waarschuwing: Venv niet aangemaakt, maar project gaat door")
        
        # Stap 7: Export script toevoegen
        if not self._add_export_script():
            print("⚠️  Waarschuwing: Export script niet toegevoegd")
        
        # Stap 8: Spec file toevoegen
        if not self._add_spec_file():
            print("⚠️  Waarschuwing: Spec file niet toegevoegd")
        
        # Resultaat
        self._print_summary()
        
        return len(self.errors) == 0
    
    def _validate(self) -> bool:
        """Valideer voor we beginnen."""
        print("🔍 Validatie...")
        
        # Check of root path bestaat
        if not self.context.root_path.exists():
            self.errors.append(f"Root pad bestaat niet: {self.context.root_path}")
            print(f"❌ Root pad bestaat niet: {self.context.root_path}")
            return False
        
        # Check of project directory al bestaat
        if self.context.project_root.exists() and not is_directory_empty(self.context.project_root):
            print(f"⚠️  Waarschuwing: Directory {self.context.project_root} bestaat al en is niet leeg")
        
        print("✅ Validatie geslaagd")
        return True
    
    def _create_root(self) -> bool:
        """Maak project root directory."""
        print(f"📁 Project root aanmaken: {self.context.project_root}")
        
        if ensure_directory(self.context.project_root):
            self.created_folders.append(self.context.project_root)
            print(f"✅ Root directory aangemaakt")
            return True
        else:
            self.errors.append("Kon root directory niet aanmaken")
            return False
    
    def _generate_folders(self) -> bool:
        """Genereer alle folders en hun bestanden."""
        print("📁 Folders en bestanden genereren...")
        
        for folder_template in self.template.root_folders:
            folder_path = self.context.project_root / folder_template.name
            
            if not self._generate_folder(folder_path, folder_template):
                return False
        
        print(f"✅ {len(self.created_folders)} folders aangemaakt")
        return True
    
    def _generate_folder(self, folder_path: Path, folder_template: FolderTemplate, 
                        parent_path: Optional[Path] = None) -> bool:
        """
        Genereer een folder recursief.
        
        Args:
            folder_path: Volledig pad naar de folder
            folder_template: Template voor deze folder
            parent_path: Pad van parent folder
        """
        # Maak folder
        if not ensure_directory(folder_path):
            self.errors.append(f"Kon folder niet aanmaken: {folder_path}")
            return False
        
        self.created_folders.append(folder_path)
        
        # Als Python package: voeg __init__.py toe
        if folder_template.python_package:
            init_file = folder_path / "__init__.py"
            relative_path = self.context.get_relative_path(init_file)
            header = self.header_renderer.render(relative_path, f"Package initialisatie voor {folder_template.name}")
            
            if not write_file(init_file, header):
                self.errors.append(f"Kon __init__.py niet aanmaken in {folder_path}")
                return False
            
            self.created_files.append(init_file)
        
        # Genereer bestanden in deze folder
        for file_template in folder_template.files:
            file_path = folder_path / file_template.name
            
            if not self._generate_file(file_path, file_template):
                return False
        
        # Genereer subfolders recursief
        for subfolder_template in folder_template.subfolders:
            subfolder_path = folder_path / subfolder_template.name
            
            if not self._generate_folder(subfolder_path, subfolder_template, folder_path):
                return False
        
        return True
    
    def _generate_file(self, file_path: Path, file_template: FileTemplate) -> bool:
        """
        Genereer een enkel bestand.
        
        Args:
            file_path: Volledig pad naar het bestand
            file_template: Template voor dit bestand
        """
        relative_path = self.context.get_relative_path(file_path)
        
        # Genereer header
        header = self.header_renderer.render(relative_path, file_template.description)
        
        # Combineer header + body
        content = header + file_template.template_body
        
        # Schrijf bestand
        if not write_file(file_path, content):
            self.errors.append(f"Kon bestand niet aanmaken: {file_path}")
            return False
        
        self.created_files.append(file_path)
        return True
    
    def _generate_root_files(self) -> bool:
        """Genereer bestanden in de root."""
        print("📄 Root bestanden genereren...")
        
        for file_template in self.template.root_files:
            file_path = self.context.project_root / file_template.name
            
            if not self._generate_file(file_path, file_template):
                return False
        
        print(f"✅ {len(self.template.root_files)} root bestanden aangemaakt")
        return True
    
    def _copy_default_icons(self) -> bool:
        """Kopieer standaard icons naar het gegenereerde project."""
        print("🎨 Standaard icons kopiëren...")
        
        # Bron: icons van de generator zelf
        generator_root = Path(__file__).parent.parent
        source_icons_dir = generator_root / "assets" / "icons"
        
        # Bestemming: icons folder in het nieuwe project
        dest_icons_dir = self.context.project_root / "assets" / "icons"
        
        # Check of bron bestaat
        if not source_icons_dir.exists():
            print(f"⚠️  Bron icons folder niet gevonden: {source_icons_dir}")
            print(f"ℹ️  Tip: Run eerst 'python utils/icon_generator.py' om icons te genereren")
            return False
        
        # Zorg dat bestemming bestaat
        if not ensure_directory(dest_icons_dir):
            self.errors.append(f"Kon icons folder niet aanmaken: {dest_icons_dir}")
            return False
        
        # Kopieer alle .png en .ico bestanden
        copied_count = 0
        icon_extensions = {'.png', '.ico'}
        
        try:
            for icon_file in source_icons_dir.iterdir():
                if icon_file.suffix.lower() in icon_extensions:
                    dest_file = dest_icons_dir / icon_file.name
                    shutil.copy2(icon_file, dest_file)
                    self.created_files.append(dest_file)
                    copied_count += 1
            
            if copied_count > 0:
                print(f"✅ {copied_count} icons gekopieerd naar assets/icons/")
                return True
            else:
                print(f"⚠️  Geen icons gevonden om te kopiëren")
                return False
                
        except Exception as e:
            self.errors.append(f"Fout bij kopiëren icons: {str(e)}")
            print(f"❌ Fout bij kopiëren icons: {str(e)}")
            return False
    
    def _create_venv(self) -> bool:
        """Maak virtuele omgeving aan."""
        print("🐍 Virtuele omgeving aanmaken...")
        
        venv_path = self.context.venv_path
        
        try:
            # Roep Python venv module aan
            result = subprocess.run(
                [sys.executable, "-m", "venv", str(venv_path)],
                check=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            self.created_folders.append(venv_path)
            print(f"✅ Virtuele omgeving aangemaakt: {venv_path}")
            
            # Upgrade pip
            print("📦 Pip upgraden...")
            pip_path = venv_path / "Scripts" / "pip.exe"
            
            if pip_path.exists():
                try:
                    subprocess.run(
                        [str(pip_path), "install", "--upgrade", "pip"],
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    print("✅ Pip geüpgraded")
                except subprocess.TimeoutExpired:
                    print("⚠️  Pip upgrade timeout - maar venv is aangemaakt")
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  Pip upgrade gefaald: {e.stderr}")
            else:
                print("⚠️  Pip.exe niet gevonden, skip upgrade")
            
            # Installeer requirements als die bestaan
            req_file = self.context.project_root / "requirements.txt"
            if req_file.exists():
                print("📦 Requirements installeren...")
                try:
                    req_content = req_file.read_text().strip()
                    # Check of er daadwerkelijk packages in staan (niet alleen comments)
                    has_packages = any(
                        line.strip() and not line.strip().startswith('#') 
                        for line in req_content.split('\n')
                    )
                    
                    if has_packages:
                        subprocess.run(
                            [str(pip_path), "install", "-r", str(req_file)],
                            check=True,
                            capture_output=True,
                            text=True,
                            timeout=300
                        )
                        print("✅ Requirements geïnstalleerd")
                    else:
                        print("ℹ️  Requirements.txt bevat geen packages")
                except subprocess.TimeoutExpired:
                    print("⚠️  Requirements installatie timeout")
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  Requirements installatie gefaald: {e.stderr}")
            
            return True
            
        except subprocess.TimeoutExpired:
            self.errors.append("Timeout bij aanmaken venv")
            print(f"❌ Timeout bij aanmaken venv")
            return False
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Fout bij aanmaken venv: {e.stderr}")
            print(f"❌ Kon venv niet aanmaken: {e.stderr}")
            return False
        except Exception as e:
            self.errors.append(f"Onverwachte fout bij venv: {str(e)}")
            print(f"❌ Onverwachte fout: {str(e)}")
            return False
    
    def _add_export_script(self) -> bool:
        """Voeg export_to_usb.bat toe."""
        export_script_content = self._get_export_script_template()
        file_path = self.context.project_root / "export_to_usb.bat"
        
        if write_file(file_path, export_script_content):
            self.created_files.append(file_path)
            print("✅ Export script toegevoegd")
            return True
        
        self.errors.append("Kon export script niet aanmaken")
        return False
    
    def _add_spec_file(self) -> bool:
        """Voeg PyInstaller spec file toe."""
        spec_content = self._get_spec_template()
        file_path = self.context.project_root / f"{self.context.app_name}.spec"
        
        if write_file(file_path, spec_content):
            self.created_files.append(file_path)
            print("✅ Spec file toegevoegd")
            return True
        
        self.errors.append("Kon spec file niet aanmaken")
        return False
    
    def _get_export_script_template(self) -> str:
        """Template voor export_to_usb.bat - Volledige versie."""
        header = self.header_renderer.render("export_to_usb.bat", "Export script naar USB")
        
        body = '''@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

:: === 0) Starttijd (ISO) + timestamp voor doelfolder ===
for /f "usebackq tokens=*" %%a in (`powershell -NoProfile -Command "Get-Date -Format o"`) do set "START_ISO=%%a"
for /f "usebackq tokens=*" %%a in (`powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"`) do set "TIMESTAMP=%%a"

echo.
echo ================= Project Export =================
echo Start: %START_ISO%
echo.

:: === 1) Bron kiezen ===
:CHOOSE_SOURCE_MODE
echo Kies bron:
echo   [1] Huidige map  : "%cd%"
echo   [2] Map ingeven  (pad intypen)
set /p SRCHOICE=Maak een keuze (1/2) ^> 
if "%SRCHOICE%"=="1" (
    set "SOURCE_FOLDER=%cd%"
) else if "%SRCHOICE%"=="2" (
    set /p SOURCE_FOLDER=Geef het volledige pad van de bronmap ^> 
) else (
    echo Ongeldige keuze. Probeer opnieuw.
    echo.
    goto CHOOSE_SOURCE_MODE
)

if "%SOURCE_FOLDER%"=="" (
    echo [FOUT] Geen bronmap opgegeven.
    goto :ABORT
)
if not exist "%SOURCE_FOLDER%" (
    echo [FOUT] Bronmap bestaat niet: "%SOURCE_FOLDER%"
    goto :ABORT
)

:: Normaliseer mogelijk trailing backslash weg
if "%SOURCE_FOLDER:~-1%"=="\\" set "SOURCE_FOLDER=%SOURCE_FOLDER:~0,-1%"

echo [OK] Bronmap: "%SOURCE_FOLDER%"

:: === 2) Venv pad bepalen (standaard .\\venv onder bron) ===
set "VENV_PATH=%SOURCE_FOLDER%\\venv"

:: === 3) USB-station vragen ===
:ASK_USB
set /p USB_DRIVE=Geef de stationsletter van de USB-stick (bv. E): 
if "%USB_DRIVE%"=="" (
    echo [FOUT] Geen stationsletter ingevoerd. Probeer opnieuw.
    goto ASK_USB
)
if not exist "%USB_DRIVE%:\\" (
    echo [FOUT] Station %USB_DRIVE%: bestaat niet of is niet toegankelijk. Probeer opnieuw.
    goto ASK_USB
)

set "USB_FOLDER=%USB_DRIVE%:\\export_''' + self.context.app_name + '''_%TIMESTAMP%"

echo.
echo [INFO] Doelmap: "%USB_FOLDER%"

:: === 4) Doelmap aanmaken ===
if not exist "%USB_FOLDER%" (
    echo [INFO] Doelmap wordt aangemaakt...
    mkdir "%USB_FOLDER%"
    if errorlevel 1 (
        echo [FOUT] Kon doelmap niet aanmaken: "%USB_FOLDER%"
        goto :ABORT
    )
) else (
    echo [INFO] Doelmap bestaat al. Bestanden kunnen worden overschreven.
)

:: === Bevestiging ===
echo.
choice /M "Wil je de export starten"
if errorlevel 2 (
  echo Actie geannuleerd.
  goto :ABORT
)

:: === 5) requirements.txt genereren (indien venv aanwezig) ===
echo.
echo [0] Pip freeze uitvoeren (vereist geactiveerde venv)...
set "REQ_FILE=%SOURCE_FOLDER%\\requirements.txt"

if exist "%VENV_PATH%\\Scripts\\activate.bat" (
    call "%VENV_PATH%\\Scripts\\activate.bat"
    if errorlevel 1 (
        echo [WAARSCHUWING] Kon venv niet activeren: "%VENV_PATH%"
    )
    where pip >nul 2>&1
    if errorlevel 1 (
        echo [WAARSCHUWING] 'pip' niet gevonden na activeren venv. Sla requirements.txt over.
    ) else (
        pip freeze > "%REQ_FILE%" 2>nul
        if exist "%REQ_FILE%" (
            echo [OK] requirements.txt aangemaakt in bronmap.
        ) else (
            echo [FOUT] requirements.txt kon niet worden aangemaakt.
        )
    )
) else (
    echo [INFO] Geen virtuele omgeving gevonden in: "%VENV_PATH%"
    echo [INFO] requirements.txt wordt niet aangemaakt.
)

:: === 6) Project kopiëren (excl. map "zzz") ===
echo.
echo [1] Kopiëren van projectmap (excl. "zzz") met voortgang...
robocopy "%SOURCE_FOLDER%" "%USB_FOLDER%" /E /XD "%SOURCE_FOLDER%\\zzz" /ETA /FP
set "RC=%ERRORLEVEL%"
:: Robocopy exit-codes: 0/1/2/3/4/5/6/7 zijn OK/waarschuwingen; >=8 is fout
if %RC% GEQ 8 (
    echo [FOUT] Robocopy gaf foutcode %RC%.
    goto :ABORT
) else (
    echo [OK] Bestanden en submappen (zonder "zzz") gekopieerd. (RC=%RC%)
)

:: === 7) Virtuele omgeving meenemen (optioneel) ===
if exist "%VENV_PATH%" (
    echo.
    choice /M "Virtuele omgeving (venv) ook kopiëren"
    if errorlevel 2 (
        echo [INFO] Venv kopiëren overgeslagen.
    ) else (
        echo [2] Kopiëren van virtuele omgeving...
        robocopy "%VENV_PATH%" "%USB_FOLDER%\\venv" /E /ETA /FP
        set "RCV=%ERRORLEVEL%"
        if %RCV% GEQ 8 (
            echo [WAARSCHUWING] Fout bij kopiëren venv (RC=%RCV%).
        ) else (
            echo [OK] Virtuele omgeving gekopieerd. (RC=%RCV%)
        )
    )
) else (
    echo.
    echo [INFO] Geen virtuele omgeving gevonden op "%VENV_PATH%". Wordt niet meegenomen.
)

:: === 8) Logbestand schrijven ===
echo.
echo [3] Logbestand schrijven...
(
    echo Laatste export: %DATE% %TIME%
    echo Bronmap: %SOURCE_FOLDER%
    echo Bestemming: %USB_FOLDER%
    echo Virtuele omgeving-pad: %VENV_PATH%
    echo requirements.txt aanwezig:
    if exist "%REQ_FILE%" (echo   JA) else (echo   NEE)
    echo Map "zzz" uitgesloten
) > "%USB_FOLDER%\\export_log.txt"
echo [OK] Logbestand aangemaakt: "%USB_FOLDER%\\export_log.txt"

:: === 9) Eindtijd en totale duur berekenen ===
for /f "usebackq tokens=*" %%a in (`powershell -NoProfile -Command "Get-Date -Format o"`) do set "END_ISO=%%a"

for /f "usebackq tokens=*" %%a in (`
  powershell -NoProfile -Command ^
    "[int][math]::Round((New-TimeSpan -Start ([datetime]'%START_ISO%') -End ([datetime]'%END_ISO%')).TotalSeconds)"
`) do set "DURATION=%%a"

if not defined DURATION set "DURATION=0"
if !DURATION! LSS 0 set /a DURATION+=86400

set /a h=DURATION/3600
set /a m=(DURATION%%3600)/60
set /a s=DURATION%%60

echo.
echo ================= Resultaat =================
echo Starttijd (ISO): %START_ISO%
echo Eindtijd  (ISO): %END_ISO%
echo Totale duur    : !h! uur !m! min !s! sec
echo.
echo Export succesvol afgerond.
echo Project staat nu op: "%USB_FOLDER%"
echo ============================================================
echo.
pause
goto :EOF

:ABORT
echo.
echo ==== Afgebroken ====
pause
exit /b 1
'''
        return header + body
    
    def _get_spec_template(self) -> str:
        """Template voor .spec file."""
        header = self.header_renderer.render(
            f"{self.context.app_name}.spec",
            "PyInstaller configuratie"
        )
        
        body = f'''
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files
from PyInstaller.building.datastruct import Tree

block_cipher = None

# Analysis: verzamel alle dependencies
a = Analysis(
    ['app/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{self.context.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
)

# Verzamel extra data (assets, docs, css, etc)
collect_datas = []

if os.path.isdir("assets"):
    collect_datas.append(
        Tree("assets", prefix="assets", excludes=["**/__pycache__/*"])
    )

if os.path.isdir("css"):
    collect_datas.append(
        Tree("css", prefix="css", excludes=["**/__pycache__/*"])
    )

if os.path.isdir("docs"):
    collect_datas.append(
        Tree("docs", prefix="docs", excludes=["**/__pycache__/*"])
    )

if os.path.isdir("data"):
    collect_datas.append(
        Tree("data", prefix="data", excludes=["**/__pycache__/*"])
    )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *collect_datas,
    strip=False,
    upx=False,
    name='{self.context.app_name}',
)
'''
        return header + body
    
    def _print_summary(self) -> None:
        """Print samenvatting van wat er is aangemaakt."""
        print()
        print("=" * 60)
        print("📊 SAMENVATTING")
        print("=" * 60)
        print(f"✅ Folders aangemaakt: {len(self.created_folders)}")
        print(f"✅ Bestanden aangemaakt: {len(self.created_files)}")
        
        if self.errors:
            print(f"❌ Fouten: {len(self.errors)}")
            for error in self.errors:
                print(f"   - {error}")
        else:
            print("✅ Geen fouten")
        
        print()
        print(f"📁 Project locatie: {self.context.project_root}")
        
        if self.template.create_venv and self.context.venv_path.exists():
            print(f"🐍 Venv locatie: {self.context.venv_path}")
            print()
            print("📝 Activeer venv met:")
            print(f"   {self.context.venv_path / 'Scripts' / 'activate.bat'}")
        
        print("=" * 60)