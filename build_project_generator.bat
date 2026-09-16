@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

rem ============================================================
rem File:    /build_project_generator.bat
rem Rol:     Build-script voor de Project Generator-app zelf
rem Applicatie: Project Generator
rem Versie:  1.1.0
rem Auteur:  Barremans
rem Changes: 1.1.0 - DISPLAY_NAME-variabele toegevoegd naast PROJECT_NAME.
rem                   De Inno Setup-sectie gebruikte op 6 plaatsen de
rem                   hardcoded tekst "Python Project Generator" i.p.v.
rem                   een variabele, los van PROJECT_NAME ("Project_
rem                   Generator", met underscore, gebruikt voor bestands-
rem                   /mapnamen). Beide namen kloppen elk op zich, maar
rem                   stonden inconsistent naast elkaar. Nu op één plek
rem                   gedefinieerd (%DISPLAY_NAME%) en overal hergebruikt
rem                   i.p.v. 6x dezelfde tekst herhaald. Geen functionele
rem                   wijziging aan de effectief gegenereerde installer
rem                   (zelfde weergavenaam als voorheen).
rem Changes: 1.0.0 - Baseline.
rem ============================================================

cd /d "%~dp0"

echo.
echo ========================================
echo  Project Generator - Build Script
echo ========================================
echo.

set "PROJECT_NAME=Project_Generator"
set "DISPLAY_NAME=Python Project Generator"
set "SPEC_FILE=Project_Generator.spec"
set "DST_FOLDER=dist"

rem ---- Python (.venv eerst!) ----
set "PYEXE="
if exist ".venv\Scripts\python.exe" set "PYEXE=.venv\Scripts\python.exe"
if not defined PYEXE if exist "venv\Scripts\python.exe" set "PYEXE=venv\Scripts\python.exe"
if not defined PYEXE set "PYEXE=python"

echo [INFO] Python: %PYEXE%
"%PYEXE%" --version || (echo ERROR: Python niet gevonden & pause & exit /b 1)
echo [OK] Python gevonden
echo.

rem ---- Versie bump ----
echo Wil je de versie verhogen?
choice /C JN /N /M "Kies J (Ja) of N (Nee): "
if errorlevel 2 goto SKIP_BUMP

echo.
echo Welke versie?
echo   P = patch (1.0.0 -> 1.0.1)
echo   M = minor (1.0.0 -> 1.1.0)
echo   J = major (1.0.0 -> 2.0.0)
echo.
choice /C PMJ /N /M "Kies P, M of J: "
if errorlevel 3 set "PART=major"
if errorlevel 2 set "PART=minor"
if errorlevel 1 set "PART=patch"

echo.
echo [1] Versie verhogen (%PART%)...
"%PYEXE%" scripts\bump_version.py %PART%
echo [OK] Versie verhoogd
goto CONTINUE

:SKIP_BUMP
echo [1] Versie bump overgeslagen

:CONTINUE
echo.

rem ---- Versie robuust uitlezen ----
echo [2] Versie lezen uit app/version.py...

set "VERSION_TMP=__read_version_tmp.py"
set "VERSION_OUT=__version_out.txt"

del /q "%VERSION_TMP%" "%VERSION_OUT%" 2>nul

> "%VERSION_TMP%" echo import importlib.util, sys
>>"%VERSION_TMP%" echo try:
>>"%VERSION_TMP%" echo ^    spec = importlib.util.spec_from_file_location("ver","app/version.py")
>>"%VERSION_TMP%" echo ^    m = importlib.util.module_from_spec(spec)
>>"%VERSION_TMP%" echo ^    spec.loader.exec_module(m)
>>"%VERSION_TMP%" echo ^    v = str(getattr(m,"__version__","0.0.0"))
>>"%VERSION_TMP%" echo except Exception:
>>"%VERSION_TMP%" echo ^    v = "0.0.0"
>>"%VERSION_TMP%" echo open(r"%VERSION_OUT%","w",encoding="utf-8").write(v.strip())

"%PYEXE%" "%VERSION_TMP%"
if errorlevel 1 (
    echo ERROR: Versie uitlezen mislukt
    del /q "%VERSION_TMP%" 2>nul
    pause
    exit /b 1
)

del /q "%VERSION_TMP%" 2>nul

set "APP_VERSION="
set /p APP_VERSION=<"%VERSION_OUT%"
del /q "%VERSION_OUT%" 2>nul

if "%APP_VERSION%"=="" set "APP_VERSION=0.0.0"

echo [OK] Versie: %APP_VERSION%
echo.

rem ---- Paden ----
set "BUILD_FOLDER=%PROJECT_NAME%_%APP_VERSION%"
set "ABS_BUILD=%CD%\%DST_FOLDER%\%BUILD_FOLDER%"
set "ISS_FILE=%DST_FOLDER%\installer.iss"

rem ---- Clean ----
echo [3] Opruimen oude builds...
if exist build rmdir /s /q build 2>nul
if exist "%DST_FOLDER%" rmdir /s /q "%DST_FOLDER%" 2>nul
echo [OK] Opgeruimd
echo.

rem ---- Dependencies ----
echo [4] Dependencies controleren...
"%PYEXE%" -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [4a] PyInstaller installeren...
    "%PYEXE%" -m pip install pyinstaller --quiet
)
echo [OK] Dependencies OK
echo.

rem ---- Build ----
echo [5] PyInstaller build...
echo Dit kan enkele minuten duren...
echo.

"%PYEXE%" -m PyInstaller --clean --noconfirm "%SPEC_FILE%"
if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller build faalde!
    pause
    exit /b 1
)

echo.
echo [OK] PyInstaller build succesvol
echo.

rem ---- Hernoemen ----
echo [6] Hernoemen naar versie folder...

rename "%DST_FOLDER%\%PROJECT_NAME%" "%BUILD_FOLDER%" 2>nul
if errorlevel 1 (
    echo [INFO] Fallback via robocopy...
    robocopy "%DST_FOLDER%\%PROJECT_NAME%" "%DST_FOLDER%\%BUILD_FOLDER%" /E /MOVE /NFL /NDL /NJH /NJS >nul
    if errorlevel 8 (
        echo ERROR: Hernoemen faalde
        pause
        exit /b 1
    )
    if exist "%DST_FOLDER%\%PROJECT_NAME%" rmdir /s /q "%DST_FOLDER%\%PROJECT_NAME%" 2>nul
)

echo [OK] Folder hernoemd naar: %BUILD_FOLDER%
echo.

rem ---- Extra bestanden ----
echo [7] Extra bestanden kopieren...

if exist assets (
    xcopy /E /I /Y assets "%DST_FOLDER%\%BUILD_FOLDER%\assets" >nul
)

if exist i18n\locales (
    xcopy /E /I /Y i18n\locales "%DST_FOLDER%\%BUILD_FOLDER%\i18n\locales" >nul
)

if exist requirements.txt (
    copy /Y requirements.txt "%DST_FOLDER%\%BUILD_FOLDER%\" >nul
)

> "%DST_FOLDER%\%BUILD_FOLDER%\version.txt" echo %APP_VERSION%

echo [OK] Bestanden gekopieerd
echo.

rem ---- Inno Setup ----
echo [8] Inno Setup Installer...
echo.
echo Wil je een installer bouwen met Inno Setup?
choice /C JN /N /M "Kies J (Ja) of N (Nee): "
if errorlevel 2 goto SKIP_INSTALLER

echo.
echo [8a] Installer script genereren...

> "%ISS_FILE%" echo ; Auto gegenereerd installer script
>>"%ISS_FILE%" echo [Setup]
>>"%ISS_FILE%" echo AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}
>>"%ISS_FILE%" echo AppName=%DISPLAY_NAME%
>>"%ISS_FILE%" echo AppVersion=%APP_VERSION%
>>"%ISS_FILE%" echo AppVerName=%DISPLAY_NAME% %APP_VERSION%
>>"%ISS_FILE%" echo DefaultDirName={autopf}\%DISPLAY_NAME%
>>"%ISS_FILE%" echo DefaultGroupName=%DISPLAY_NAME%
>>"%ISS_FILE%" echo OutputDir=%DST_FOLDER%
>>"%ISS_FILE%" echo OutputBaseFilename=%PROJECT_NAME%_Setup_v%APP_VERSION%
>>"%ISS_FILE%" echo Compression=lzma2
>>"%ISS_FILE%" echo SolidCompression=yes
>>"%ISS_FILE%" echo WizardStyle=modern
>>"%ISS_FILE%" echo PrivilegesRequired=admin
>>"%ISS_FILE%" echo SetupIconFile="%CD%\assets\icons\logo.ico"
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Files]
>>"%ISS_FILE%" echo Source: "%ABS_BUILD%\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Tasks]
>>"%ISS_FILE%" echo Name: "desktopicon"; Description: "Maak snelkoppeling op bureaublad"; GroupDescription: "Extra opties:"
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Icons]
>>"%ISS_FILE%" echo Name: "{group}\%DISPLAY_NAME%"; Filename: "{app}\%PROJECT_NAME%.exe"; IconFilename: "{app}\assets\logo.ico"
>>"%ISS_FILE%" echo Name: "{commondesktop}\%DISPLAY_NAME%"; Filename: "{app}\%PROJECT_NAME%.exe"; IconFilename: "{app}\assets\logo.ico"; Tasks: desktopicon

set "ISCC="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"

if defined ISCC (
    "%ISCC%" "%ISS_FILE%"
)

:SKIP_INSTALLER

echo.
echo ========================================
echo  BUILD SUCCESVOL!
echo ========================================
echo.
echo Versie: %APP_VERSION%
echo Folder: %DST_FOLDER%\%BUILD_FOLDER%
echo EXE: %DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe
echo.

echo Wil je de output folder openen?
choice /C JN /N /M "Kies J (Ja) of N (Nee): "
if errorlevel 1 if not errorlevel 2 explorer "%DST_FOLDER%\%BUILD_FOLDER%"

pause
endlocal