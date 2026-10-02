@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

rem Altijd uitvoeren vanuit de map waar dit .bat bestand staat
cd /d "%~dp0"

rem ================================================
rem build_installer.bat - Build + Inno Setup installer generator
rem File: build_installer.bat
rem Role: Bouwt de PyInstaller-EXE en genereert/compileert het Inno
rem Setup installer-script (.iss), voor zowel interactief gebruik
rem als niet-interactieve aanroep vanuit build_and_publish.ps1
rem (via env vars AS_BUMP_PART, AS_MAKE_INSTALLER, AS_DO_SIGN).
rem Version: 1.3.0
rem Author: Barremans
rem Changes: 1.3.0 - :PREFLIGHT_CERT volledig verwijderd (zie het
rem uitgebreide commentaarblok bij die verwijderde sectie
rem hieronder): 3 opeenvolgende pogingen om de PowerShell
rem Cert:\-validatie werkend te krijgen (met/zonder
rem Import-Module, met -ErrorAction Stop/SilentlyContinue)
rem faalden alle 3 op deze machine, los van het
rem certificaat zelf. signtool + de bestaande
rem verify-stap (:SIGN_FILE) zijn de enige, betrouwbare
rem validatie -- exact het patroon van de originele,
rem al bewezen build-flow van vóór de centrale
rem signing-integratie.
rem Changes: 1.2.2 - (ingetrokken, zie 1.3.0) Import-Module met
rem -ErrorAction SilentlyContinue + Get-PSDrive-check.
rem Changes: 1.2.1 - (ingetrokken, zie 1.3.0) Import-Module-regel
rem weggelaten.
rem Changes: 1.2.0 - Nieuwe stap [3c]: genereert version_info.txt (Windows
rem VersionInfo-resource: CompanyName/ProductName/
rem FileDescription/FileVersion/ProductVersion) MET de
rem effectieve build-versie, voor de PyInstaller-build.
rem Project_Generator.spec v1.2.0 verwijst er nu naar via
rem EXE(..., version='version_info.txt'). Voorheen had de
rem exe GEEN enkele Windows-metadata (leeg Eigenschappen >
rem Details-tabblad) -- samen met v1.1.0's signing-
rem verificatie het tweede stuk van de "check Inno en
rem sign goed"-analyse voor de Defender/Intune-fout.
rem Changes: 1.1.0 - Handtekening-VERIFICATIE toegevoegd na het signen
rem (signtool verify /pa /v), n.a.v. een bevestigde fout
rem op andere Windows-machines ("Kan geen toegang krijgen
rem tot het opgegeven apparaat, pad of bestand") op
rem Intune-beheerde toestellen met Controlled Folder
rem Access aan. Signen alleen ("gesigned") betekent NIET
rem automatisch "vertrouwd door Defender/SmartScreen/CFA"
rem -- dat vereist een keten naar een PUBLIEK vertrouwde
rem CA-root. Een zelfondertekend/intern certificaat (zeer
rem waarschijnlijk wat /a hier oppikt via de lokale
rem certificaatstore) signeert prima maar wordt op andere
rem machines nog steeds als onbekend behandeld. Het
rem script waarschuwt nu expliciet + toont welk
rem certificaat effectief gebruikt werd, i.p.v. stil door
rem te gaan met een niet-vertrouwde signature. Dit is een
rem organisatorisch/beleidsprobleem (Intune/Defender-
rem configuratie), geen zuivere codefout -- zie de
rem ACTIE NODIG-melding in :SIGN_FILE voor de 3 opties.
rem Changes: 1.0.0 - Aangepast vanuit ArticleSearch (build_installer.bat
rem v1.4.0, auteur Bart Bossuyt) naar Project Generator's
rem eigen structuur:
rem (1) PROJECT_NAME=Project_Generator, DISPLAY_NAME=
rem "Python Project Generator" (los van elkaar,
rem consistent met build_project_generator.bat
rem v1.1.0) i.p.v. een hardcoded "ArticleSearch".
rem (2) SPEC_FILE=Project_Generator.spec i.p.v.
rem SearchArticle.spec.
rem (3) Versie-bump roept nu "scripts\bump_version.py"
rem aan i.p.v. root-"bump_version.py" -- dit was de
rem directe oorzaak van de crash ("can't open file
rem ...\bump_version.py") toen dit script ongewijzigd
rem overgenomen werd.
rem (4) Versie wordt gelezen uit "app/version.py" i.p.v.
rem root-"version.py" (Project Generator's version.py
rem staat in app/, zie context_ProjectGenerator.md).
rem (5) APPGUID hergebruikt de AL BESTAANDE GUID uit
rem build_project_generator.bat v1.1.0
rem ({A1B2C3D4-E5F6-7890-ABCD-EF1234567890}) i.p.v.
rem ArticleSearch's GUID -- kritiek voor correcte
rem upgrade-detectie; een nieuwe GUID zou Windows
rem elke build als een andere applicatie laten zien.
rem (6) Stap [5] Assets kopieren aangepast naar Project
rem Generator's echte structuur: assets/, i18n/locales/,
rem docs/, requirements.txt -- i.p.v. ArticleSearch's
rem assets/logs/label/docs/translations +
rem requirements.txt/help.md/settings.json.
rem BUGFIX t.o.v. build_project_generator.bat v1.1.0:
rem dat script kopieerde docs/ NIET mee, terwijl
rem gui/main_window.py::_show_help()/_show_changelog()
rem wel HELP_{locale}.md/CHANGELOG_{locale}.md uit
rem docs/ leest -- zonder deze fix zou Help/Changelog
rem in een gebouwde installer altijd falen.
rem Overige logica (signing via certificaatstore,
rem Intune-safe CloseApplications=force/
rem RestartApplications=no, env-var-aansturing vanuit
rem build_and_publish.ps1) ONGEWIJZIGD overgenomen uit
rem ArticleSearch v1.4.0.
rem ================================================

rem Basisconfig
set "PROJECT_NAME=Project_Generator"
set "DISPLAY_NAME=Python Project Generator"
set "SPEC_FILE=Project_Generator.spec"
set "DST_FOLDER=dist"
set "LOGFILE=build_log.txt"
set "TIMESTAMP_URL=http://timestamp.sectigo.com"
set "SIGN_CONFIG=%USERPROFILE%\.project_generator\signing_certificate.json"
set "WINPS=C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
rem Optioneel: exacte certificaat-subject om te forceren i.p.v. automatisch
rem beste certificaat (/a). Leeg = automatisch.
set "SIGN_SUBJECT="

rem Vaste AppId (zonder de Inno-escape "{{"), gebruikt om in het [Code]-blok
rem te detecteren of er al een eerdere installatie (zelfde app) in het
rem register staat - moet EXACT overeenkomen met de AppId hieronder bij
rem [Setup] (daar WEL met "{{" geschreven). Dit is de AL BESTAANDE GUID uit
rem build_project_generator.bat v1.1.0 - NOOIT wijzigen zonder ook alle
rem eerder uitgerolde installaties te vervangen (upgrade-detectie breekt
rem anders).
set "APPGUID={A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"

rem ---- Python uit .venv prefereren ----
set "PYEXE="
if exist ".venv\Scripts\python.exe" set "PYEXE=.venv\Scripts\python.exe"
if not defined PYEXE if exist "Scripts\python.exe" set "PYEXE=Scripts\python.exe"
if not defined PYEXE set "PYEXE=python"

rem Alleen naar absolute path omzetten als het effectief een bestaand bestandspad is
for %%I in ("%PYEXE%") do (
 if exist "%%~fI" set "PYEXE=%%~fI"
)

echo [info] Python: %PYEXE%
"%PYEXE%" -V >nul 2>&1 || (echo [FOUT] Geen werkende Python gevonden.& pause & exit /b 1)

rem ================================================
rem [S0] Signing - optioneel, default N
rem ================================================
set "DO_SIGN=N"
if defined AS_DO_SIGN set "DO_SIGN=%AS_DO_SIGN%"
if defined AS_DO_SIGN echo [sign] Modus via parameter: %AS_DO_SIGN%
if not defined AS_DO_SIGN set /p DO_SIGN=[S0] Binaries signen? [J/N] (standaard N): 
if not defined DO_SIGN set "DO_SIGN=N"

set "SIGNTOOL_EXE="
set "SIGN_THUMBPRINT="
if /I "%DO_SIGN%"=="J" (
 call :LOAD_ACTIVE_CERT
 if errorlevel 1 exit /b 1
 rem GEEN aparte PowerShell Cert:\-preflight meer hier (verwijderd in
 rem 1.3.0) -- die gaf op sommige machines een FormatXmlUpdateException
 rem (zelfs met -ErrorAction SilentlyContinue nog fataal, want dat is
 rem geen gewone non-terminating fout) of "Cannot find drive Cert"
 rem (module-autoloading uitgeschakeld), los van of het certificaat zelf
 rem in orde was. signtool zelf (hieronder, via :SIGN_FILE) valideert het
 rem certificaat al -- bestaat het niet/geen private key/verlopen, dan
 rem faalt signtool met een duidelijke eigen foutmelding, en de
 rem "signtool verify /pa /v" erna is de echte controle. Dit is exact het
 rem patroon van de originele, bewezen build-flow van vóór de centrale
 rem signing-integratie.
 call :FIND_SIGNTOOL
 if not defined SIGNTOOL_EXE (
  echo [FOUT] signtool.exe niet gevonden. Build wordt gestopt.
  exit /b 1
 )
 echo [sign] signtool: %SIGNTOOL_EXE%
 echo [sign] Actieve thumbprint: %SIGN_THUMBPRINT%
)

rem ---- Versie verhogen (scripts\bump_version.py -- NIET root) ----
if defined AS_BUMP_PART (
 set "PART_TO_BUMP=%AS_BUMP_PART%"
 echo [0] Versie-bump via parameter: %AS_BUMP_PART%
) else (
 set /p PART_TO_BUMP=Welke versie wil je verhogen? ^(patch/minor/major^) : 
 if "%PART_TO_BUMP%"=="" set "PART_TO_BUMP=patch"
)
echo [0] Versie verhogen via scripts\bump_version.py (%PART_TO_BUMP%)...
"%PYEXE%" scripts\bump_version.py %PART_TO_BUMP% || (echo [FOUT] Versieverhoging mislukt.& pause & exit /b 1)

rem ---- Versie robuust uitlezen uit app/version.py ----
set "PY_READV=%TEMP%\__read_version_tmp.py"
set "VER_TXT=%TEMP%\__version_out.txt"
del /q "%PY_READV%" "%VER_TXT%" >nul 2>&1
> "%PY_READV%" echo import importlib.util, io, os, re
>>"%PY_READV%" echo p=os.path.abspath('app/version.py'); v="0.0.0"
>>"%PY_READV%" echo try:
>>"%PY_READV%" echo ^ spec=importlib.util.spec_from_file_location("ver",p)
>>"%PY_READV%" echo ^ m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
>>"%PY_READV%" echo ^ v=str(getattr(m,"__version__","0.0.0"))
>>"%PY_READV%" echo except Exception:
>>"%PY_READV%" echo ^ t=io.open(p,'r',encoding='utf-8').read()
>>"%PY_READV%" echo ^ m=re.search(r"__version__\s*=\s*['\^\"\s]*([0-9]+(?:\.[0-9]+){1,2})",t)
>>"%PY_READV%" echo ^ v=m.group(1) if m else "0.0.0"
>>"%PY_READV%" echo io.open(r'%VER_TXT%','w',encoding='utf-8').write(v.strip())
"%PYEXE%" "%PY_READV%" || (echo [FOUT] Versie uitlezen faalde.& del /q "%PY_READV%" >nul & pause & exit /b 1)
del /q "%PY_READV%" >nul 2>&1
set "NEW_VERSION=" & set /p NEW_VERSION=<"%VER_TXT%"
del /q "%VER_TXT%" >nul 2>&1
if not defined NEW_VERSION (echo [FOUT] Kon versie niet lezen.& pause & exit /b 1)
echo [1] Versie: %NEW_VERSION%

rem ---- Afgeleide paden ----
set "BUILD_FOLDER=%PROJECT_NAME%_%NEW_VERSION%"
set "ABS_BUILD_FOLDER=%CD%\%DST_FOLDER%\%BUILD_FOLDER%"
set "INITIAL_EXE=%DST_FOLDER%\%PROJECT_NAME%\%PROJECT_NAME%.exe"
set "ISS_FILE=%DST_FOLDER%\installer.iss"

rem  Opschonen
echo [2]  Opruimen...
rmdir /s /q build 2>nul
rmdir /s /q "%DST_FOLDER%" 2>nul
del /q "%LOGFILE%" 2>nul

rem Vereisten
echo [3] Pip ^& vereisten...
"%PYEXE%" -m pip install --upgrade pip >nul
if exist requirements.txt "%PYEXE%" -m pip install -r requirements.txt || (echo [FOUT] pip install -r faalde.& pause & exit /b 1)

rem  PyInstaller aanwezig?
"%PYEXE%" -c "import PyInstaller" >nul 2>&1 || (
 echo [3b] PyInstaller installeren...
 "%PYEXE%" -m pip install "pyinstaller==6.11.1" "pyinstaller-hooks-contrib==2025.0" || (echo [FOUT] Installatie PyInstaller faalde.& pause & exit /b 1)
)

rem Windows VersionInfo-resource genereren (CompanyName/ProductName/
rem FileDescription/FileVersion/ProductVersion in de exe's Eigenschappen >
rem Details) -- ontbrak volledig voorheen, wat mee bijdraagt aan een lagere
rem SmartScreen/Defender-reputatiescore. Parse NEW_VERSION (X.Y.Z) naar een
rem 4-delige tuple; ontbrekende/niet-numerieke delen vallen terug op 0.
echo [3c] Version-info resource genereren...
for /f "tokens=1-3 delims=." %%a in ("%NEW_VERSION%") do (
 set "VMAJOR=%%a"
 set "VMINOR=%%b"
 set "VPATCH=%%c"
)
if not defined VMAJOR set "VMAJOR=0"
if not defined VMINOR set "VMINOR=0"
if not defined VPATCH set "VPATCH=0"

del /q version_info.txt >nul 2>&1
> version_info.txt echo VSVersionInfo(
>>version_info.txt echo ffi=FixedFileInfo(
>>version_info.txt echo filevers=(%VMAJOR%, %VMINOR%, %VPATCH%, 0^),
>>version_info.txt echo prodvers=(%VMAJOR%, %VMINOR%, %VPATCH%, 0^),
>>version_info.txt echo mask=0x3f,
>>version_info.txt echo flags=0x0,
>>version_info.txt echo OS=0x40004,
>>version_info.txt echo fileType=0x1,
>>version_info.txt echo subtype=0x0,
>>version_info.txt echo date=(0, 0^)
>>version_info.txt echo ^),
>>version_info.txt echo kids=[
>>version_info.txt echo StringFileInfo(
>>version_info.txt echo [StringTable(
>>version_info.txt echo u'040904B0',
>>version_info.txt echo [StringStruct(u'CompanyName', u'CGK'^),
>>version_info.txt echo StringStruct(u'FileDescription', u'%DISPLAY_NAME%'^),
>>version_info.txt echo StringStruct(u'FileVersion', u'%NEW_VERSION%'^),
>>version_info.txt echo StringStruct(u'InternalName', u'%PROJECT_NAME%'^),
>>version_info.txt echo StringStruct(u'LegalCopyright', u'\xa9 2026 Barremans - CGK'^),
>>version_info.txt echo StringStruct(u'OriginalFilename', u'%PROJECT_NAME%.exe'^),
>>version_info.txt echo StringStruct(u'ProductName', u'%DISPLAY_NAME%'^),
>>version_info.txt echo StringStruct(u'ProductVersion', u'%NEW_VERSION%'^)])
>>version_info.txt echo ]^),
>>version_info.txt echo VarFileInfo([VarStruct(u'Translation', [1033, 1200]^)])
>>version_info.txt echo ]
>>version_info.txt echo ^)
echo [OK] version_info.txt aangemaakt (FileVersion/ProductVersion = %NEW_VERSION%)

echo --- Build gestart op %DATE% %TIME% --- >> "%LOGFILE%"

rem Build (via SPEC)
echo [4] PyInstaller...
"%PYEXE%" -m PyInstaller --clean --noconfirm "%SPEC_FILE%" || (echo [FOUT] PyInstaller build faalde.& pause & exit /b 1)
if not exist "%INITIAL_EXE%" (echo [FOUT] EXE niet gevonden op "%INITIAL_EXE%".& pause & exit /b 1)

rem Hernoemen naar map met versie
if exist "%DST_FOLDER%\%BUILD_FOLDER%" rmdir /S /Q "%DST_FOLDER%\%BUILD_FOLDER%"
rename "%DST_FOLDER%\%PROJECT_NAME%" "%BUILD_FOLDER%" >nul 2>&1
if errorlevel 1 (
 echo [rename] Fallback via robocopy...
 robocopy "%DST_FOLDER%\%PROJECT_NAME%" "%DST_FOLDER%\%BUILD_FOLDER%" /E /MOVE >nul
 if errorlevel 8 (echo [FOUT] Fallback kopie mislukt.& pause & exit /b 1)
 if exist "%DST_FOLDER%\%PROJECT_NAME%" rmdir /S /Q "%DST_FOLDER%\%PROJECT_NAME%"
)
if not exist "%DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe" (
 echo [FOUT] %PROJECT_NAME%.exe ontbreekt in %DST_FOLDER%\%BUILD_FOLDER%.
 pause & exit /b 1
)

rem Assets kopieren (Project Generator's eigen structuur -- zie
rem changelog hierboven, punt 6: docs/ toegevoegd t.o.v. build_project_
rem generator.bat, dat dit vergat)
echo [5] Assets kopieren...
for %%D in (assets i18n docs) do (
 if exist "%%D" xcopy /E /I /Y "%%D" "%DST_FOLDER%\%BUILD_FOLDER%\%%D" >nul
)
for %%F in (requirements.txt) do (
 if exist "%%F" copy /Y "%%F" "%DST_FOLDER%\%BUILD_FOLDER%\" >nul
)
> "%DST_FOLDER%\%BUILD_FOLDER%\version.txt" echo %NEW_VERSION%

rem [5b] Signen van de BINNEN-EXE (optioneel, certificaatstore)
if /I "%DO_SIGN%"=="J" (
 echo [5b] Signen van %DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe ...
 call :SIGN_FILE "%DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe"
 if errorlevel 1 echo [WAARSCHUWING] Signen van app-EXE faalde - build gaat wel verder ^(ongesigned^).
) else (
 echo [INFO] Signing overgeslagen ^(DO_SIGN=%DO_SIGN%^).
)

rem  Inno Setup?
if defined AS_MAKE_INSTALLER (
 set "MAKE_INSTALLER=%AS_MAKE_INSTALLER%"
 echo [6] Installer via parameter: %AS_MAKE_INSTALLER%
) else (
 set "MAKE_INSTALLER=J"
 set /p MAKE_INSTALLER=Ook Inno Setup installer bouwen? [J/N] : 
)
set "DO_ISCC=1"
if /I "%MAKE_INSTALLER%"=="N" set "DO_ISCC=0"
if "%DO_ISCC%"=="0" goto SHOW_OUTPUT

rem  Inno script genereren
if not exist "%DST_FOLDER%" mkdir "%DST_FOLDER%" >nul 2>&1
del /q "%ISS_FILE%" >nul 2>&1
echo [6b]  Installer-script genereren...

>>"%ISS_FILE%" echo ; --- Inno Setup script, automatisch gegenereerd ---
>>"%ISS_FILE%" echo [Setup]
>>"%ISS_FILE%" echo AppId={{%APPGUID:~1,-1%}
>>"%ISS_FILE%" echo AppName=%DISPLAY_NAME%
>>"%ISS_FILE%" echo AppVersion=%NEW_VERSION%
>>"%ISS_FILE%" echo AppVerName=%DISPLAY_NAME% %NEW_VERSION%
>>"%ISS_FILE%" echo DefaultDirName=C:\%PROJECT_NAME%
>>"%ISS_FILE%" echo DisableDirPage=yes
>>"%ISS_FILE%" echo UsePreviousAppDir=no
>>"%ISS_FILE%" echo DefaultGroupName=%DISPLAY_NAME%
>>"%ISS_FILE%" echo DisableProgramGroupPage=yes
>>"%ISS_FILE%" echo OutputDir=.
>>"%ISS_FILE%" echo OutputBaseFilename=%PROJECT_NAME%Setup_%NEW_VERSION%
>>"%ISS_FILE%" echo Compression=lzma
>>"%ISS_FILE%" echo SolidCompression=yes
>>"%ISS_FILE%" echo Uninstallable=yes
>>"%ISS_FILE%" echo CreateAppDir=yes
>>"%ISS_FILE%" echo PrivilegesRequired=admin
>>"%ISS_FILE%" echo ArchitecturesInstallIn64BitMode=x64
>>"%ISS_FILE%" echo DirExistsWarning=no
>>"%ISS_FILE%" echo WizardStyle=modern
>>"%ISS_FILE%" echo SetupIconFile="%ABS_BUILD_FOLDER%\assets\icons\logo.ico"
rem SignTool: laat Inno zelf setup.exe EN de ingebouwde uninstaller
rem (unins000.exe, die mee in {app} terechtkomt) signen tijdens het
rem compileren -- dat laatste bestand werd hiervoor NOOIT gesigned (de
rem oude aanpak signde enkel de buitenste, reeds gecompileerde setup.exe
rem achteraf). "mysigntool" verwijst naar de /Smysigntool=-definitie die
rem hieronder aan ISCC meegegeven wordt (enkel als DO_SIGN=J).
if /I "%DO_SIGN%"=="J" if defined SIGNTOOL_EXE (
 >>"%ISS_FILE%" echo SignTool=mysigntool
)
rem Sluit een draaiende Project_Generator.exe automatisch af voor het
rem kopieren van bestanden (lost gelockte-exe-fouten bij updates op).
rem "force" = geen prompt, ook niet interactief - vereist voor een
rem probleemloze /VERYSILENT-run via Intune. RestartApplications=no: de
rem app bewust NIET automatisch herstarten na install (Intune draait de
rem installer als SYSTEM, niet als de ingelogde gebruiker).
>>"%ISS_FILE%" echo CloseApplicationsFilter=%PROJECT_NAME%.exe
>>"%ISS_FILE%" echo CloseApplications=force
>>"%ISS_FILE%" echo RestartApplications=no
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [InstallDelete]
>>"%ISS_FILE%" echo Type: filesandordirs; Name: "{app}\_internal"
>>"%ISS_FILE%" echo Type: filesandordirs; Name: "{app}\__pycache__"
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Files]
>>"%ISS_FILE%" echo Source: "%ABS_BUILD_FOLDER%\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Icons]
>>"%ISS_FILE%" echo Name: "{group}\%DISPLAY_NAME%"; Filename: "{app}\%PROJECT_NAME%.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icons\logo.ico"
>>"%ISS_FILE%" echo Name: "{commondesktop}\%DISPLAY_NAME%"; Filename: "{app}\%PROJECT_NAME%.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icons\logo.ico"; Tasks: desktopicon
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Tasks]
>>"%ISS_FILE%" echo Name: "desktopicon"; Description: "Maak een snelkoppeling op het bureaublad"; GroupDescription: "Extra opties:"
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo [Run]
>>"%ISS_FILE%" echo Filename: "{app}\%PROJECT_NAME%.exe"; WorkingDir: "{app}"; Description: "Start %DISPLAY_NAME%"; Flags: nowait postinstall skipifsilent
>>"%ISS_FILE%" echo.
rem Puur cosmetisch - toont "bijwerken naar versie X" i.p.v. de standaard
rem welkomsttekst wanneer een vorige installatie (zelfde AppId) al in het
rem register staat. Werkt ook onder een silent/Intune-run.
>>"%ISS_FILE%" echo [Code]
>>"%ISS_FILE%" echo function IsUpgrade: Boolean;
>>"%ISS_FILE%" echo var sPrevPath: String;
>>"%ISS_FILE%" echo begin
>>"%ISS_FILE%" echo Result := RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\%APPGUID%_is1', 'InstallLocation', sPrevPath);
>>"%ISS_FILE%" echo end;
>>"%ISS_FILE%" echo.
>>"%ISS_FILE%" echo procedure InitializeWizard();
>>"%ISS_FILE%" echo begin
>>"%ISS_FILE%" echo if IsUpgrade then WizardForm.WelcomeLabel2.Caption := 'Dit zal %DISPLAY_NAME% bijwerken naar versie %NEW_VERSION%.' + #13#10#13#10 + 'Klik op Volgende om verder te gaan.';
>>"%ISS_FILE%" echo end;

rem Inno Setup compileren
echo [7] Inno Setup compileren...
set "ISCC_EXE="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC_EXE=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not defined ISCC_EXE if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set "ISCC_EXE=C:\Program Files\Inno Setup 6\ISCC.exe"
if not defined ISCC_EXE (
 echo [WAARSCHUWING] ISCC.exe niet gevonden. Installeer Inno Setup 6.
 goto SHOW_OUTPUT
)

rem [6c] Sign-wrapper voor Inno's SignTool-mechanisme. Een apart .bat-
rem bestand i.p.v. rechtstreeks een /Smysigntool="..."-string opbouwen --
rem dat laatste is bijzonder foutgevoelig in cmd.exe door geneste
rem aanhalingstekens (SIGNTOOL_EXE-pad bevat spaties, bv. "Program Files").
set "ISCC_SIGN_ARG="
if /I "%DO_SIGN%"=="J" if defined SIGNTOOL_EXE (
 echo [6c] Inno sign-wrapper aanmaken...
 > "%DST_FOLDER%\innosign.bat" echo @echo off
 if defined SIGN_SUBJECT (
 >>"%DST_FOLDER%\innosign.bat" echo "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" %%1
 ) else (
 >>"%DST_FOLDER%\innosign.bat" echo "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" %%1
 )
 rem GEEN "set "VAR=...""-vorm hier -- die paart aanhalingstekens en
 rem breekt zodra de waarde zelf al eigen quotes bevat. Platte "set
 rem VAR=..." zonder omsluitende quotes om het hele commando neemt de
 rem rest van de regel letterlijk over, quotes inbegrepen, en levert zo
 rem exact de syntax die Inno's ISCC /S-naam="commando"-parameter
 rem verwacht. innosign.bat-pad wordt bewust NIET apart gequote: dat pad
 rem bevat per CGK-conventie C:\PY\AppNaam\... geen spaties.
 set ISCC_SIGN_ARG=/Smysigntool="%CD%\%DST_FOLDER%\innosign.bat $f"
)

if defined ISCC_SIGN_ARG (
 "%ISCC_EXE%" %ISCC_SIGN_ARG% "%ISS_FILE%"
) else (
 "%ISCC_EXE%" "%ISS_FILE%"
)
if errorlevel 1 (
 echo [FOUT] Inno Setup compile mislukt. Bekijk "%ISS_FILE%".
 goto SHOW_OUTPUT
)
echo [OK] Installer aangemaakt: %DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe
if defined ISCC_SIGN_ARG echo [OK] setup.exe + unins000.exe zijn tijdens compilatie gesigned door Inno's SignTool-mechanisme.

rem [7b] Verificatie van de installer-signature (setup.exe zelf, niet de
rem embedded uninstaller -- die zit pas in {app} na een effectieve install
rem en is dus nu niet apart te verifieren).
if /I "%DO_SIGN%"=="J" (
 if exist "%DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe" (
 echo [7b] Handtekening installer verifieren...
 call :SIGN_FILE "%DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe" --verify-only
 )
) else (
 echo [INFO] Installer-signing overgeslagen ^(DO_SIGN=%DO_SIGN%^).
)

:SHOW_OUTPUT
echo.
echo Output-map: %DST_FOLDER%\%BUILD_FOLDER%
echo Testen: "%DST_FOLDER%\%BUILD_FOLDER%\%PROJECT_NAME%.exe"
echo Installer (indien gebouwd): %DST_FOLDER%\%PROJECT_NAME%Setup_%NEW_VERSION%.exe
echo Signing: %DO_SIGN%
if not defined AS_BUMP_PART pause
endlocal
exit /b 0

rem ================================================
:LOAD_ACTIVE_CERT
if not exist "%SIGN_CONFIG%" (
 echo [FOUT] Centrale signingconfig niet gevonden: %SIGN_CONFIG%
 exit /b 1
)
set "SIGN_THUMB_FILE=%TEMP%\__cgk_active_thumbprint.txt"
del /q "%SIGN_THUMB_FILE%" >nul 2>&1
"%WINPS%" -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $d=Get-Content -LiteralPath $env:SIGN_CONFIG -Raw | ConvertFrom-Json; $t=$d.thumbprint; if(-not $t){$t=$d.Thumbprint}; if(-not $t){throw 'Geen thumbprint in signingconfig'}; ($t -replace ' ','').ToUpperInvariant() | Set-Content -LiteralPath $env:SIGN_THUMB_FILE -Encoding ASCII"
if errorlevel 1 (
 echo [FOUT] Actieve thumbprint kon niet worden gelezen.
 exit /b 1
)
set /p SIGN_THUMBPRINT=<"%SIGN_THUMB_FILE%"
del /q "%SIGN_THUMB_FILE%" >nul 2>&1
if not defined SIGN_THUMBPRINT (
 echo [FOUT] Geen actieve thumbprint gevonden.
 exit /b 1
)
exit /b 0

rem ================================================
rem :PREFLIGHT_CERT is bewust VERWIJDERD (1.3.0) -- deze PowerShell
rem Cert:\-validatie (Get-ChildItem Cert:\CurrentUser\My/Root/
rem TrustedPublisher, HasPrivateKey/NotAfter-checks) bleek op deze machine
rem op 2 verschillende manieren te falen zonder dat er iets mis was met
rem het certificaat zelf:
rem   1) "Import-Module ... -ErrorAction Stop" -> FormatXmlUpdateException
rem      (dubbele ObjectSecurity-type-data, cosmetisch).
rem   2) Geen Import-Module -> "Cannot find drive Cert" (impliciet
rem      module-autoloaden staat hier uit).
rem   3) "Import-Module ... -ErrorAction SilentlyContinue" -> zelfde
rem      FormatXmlUpdateException als (1): dit is geen gewone
rem      non-terminating fout, dus -ErrorAction onderdrukt hem niet.
rem signtool zelf heeft de PowerShell Cert:-drive niet nodig (gebruikt de
rem Windows Crypto API rechtstreeks) en valideert het certificaat al bij
rem het effectieve signen (:SIGN_FILE hieronder), gevolgd door
rem "signtool verify /pa /v" als de echte controle. Dit is exact hoe de
rem originele, bewezen build-flow van vóór de centrale signing-integratie
rem al werkte -- geen aparte preflight nodig.
rem ================================================
:FIND_SIGNTOOL
set "SIGNTOOL_EXE="
if exist "C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe" (
 set "SIGNTOOL_EXE=C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe"
 goto :eof
)
if exist "C:\Program Files (x86)\Windows Kits\10\App Certification Kit\signtool.exe" (
 set "SIGNTOOL_EXE=C:\Program Files (x86)\Windows Kits\10\App Certification Kit\signtool.exe"
 goto :eof
)
if exist "C:\Program Files\Windows Kits\10\bin\x64\signtool.exe" (
 set "SIGNTOOL_EXE=C:\Program Files\Windows Kits\10\bin\x64\signtool.exe"
 goto :eof
)
for /f "delims=" %%S in ('where signtool.exe 2^>nul') do (
 set "SIGNTOOL_EXE=%%S"
 goto :eof
)
goto :eof

rem ================================================
:SIGN_FILE
if not exist "%~1" echo [FOUT] Bestand niet gevonden: %~1
if not exist "%~1" exit /b 1
if not defined SIGNTOOL_EXE (
 echo [FOUT] signtool niet geconfigureerd.
 exit /b 1
)
if /I "%~2"=="--verify-only" goto SIGN_FILE_VERIFY
echo [sign] Bestand: %~1
if defined SIGN_SUBJECT (
 "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" "%~1"
) else (
 "%SIGNTOOL_EXE%" sign /fd SHA256 /td SHA256 /tr "%TIMESTAMP_URL%" /sha1 "%SIGN_THUMBPRINT%" "%~1"
)
if errorlevel 1 echo [FOUT] signtool mislukt voor: %~1
if errorlevel 1 exit /b 1
echo [OK] Gesigned: %~1

:SIGN_FILE_VERIFY
rem [verify] BELANGRIJK: "gesigned" wil NIET zeggen "vertrouwd door Windows
rem Defender/SmartScreen/Controlled Folder Access". Die vereisen een keten
rem naar een PUBLIEK vertrouwde CA-root (DigiCert/Sectigo/GlobalSign/...).
rem Een zelfondertekend of intern CGK-certificaat signeert prima (integriteit
rem OK) maar wordt door Defender op ANDERE machines nog steeds als onbekend/
rem onvertrouwd behandeld -- dat is vermoedelijk de kern van de "Kan geen
rem toegang krijgen tot het opgegeven apparaat, pad of bestand"-fout op
rem Intune-beheerde toestellen met Controlled Folder Access aan.
rem
rem /pa = gebruik de "Default Authenticode"-verificatiepolicy (dezelfde
rem policy die Windows zelf hanteert) i.p.v. Microsoft's eigen, striktere
rem WHQL-policy -- /pa is de juiste keuze voor gewone code-signing-checks.
echo [verify] Handtekening controleren...
"%SIGNTOOL_EXE%" verify /pa /v "%~1" > "%TEMP%\__signverify.txt" 2>&1
set "VERIFY_RC=%ERRORLEVEL%"
type "%TEMP%\__signverify.txt"
findstr /C:"Issued to" "%TEMP%\__signverify.txt"
del /q "%TEMP%\__signverify.txt" >nul 2>&1

if not "%VERIFY_RC%"=="0" (
 echo.
 echo [WAARSCHUWING] Handtekening-verificatie MISLUKT ^(exitcode %VERIFY_RC%^) voor: %~1
 echo [WAARSCHUWING] Dit bestand wordt zeer waarschijnlijk geblokkeerd door
 echo Windows Defender SmartScreen / Controlled Folder Access /
 echo Attack Surface Reduction op Intune-beheerde toestellen,
 echo ook al is het technisch wel "gesigned".
 echo [ACTIE NODIG] Vraag IT/Security om ofwel:
 echo 1^) een certificaat van een publiek vertrouwde CA te
 echo gebruiken ^(niet zelfondertekend/intern^), OF
 echo 2^) dit bestand ^(of het certificaat-thumbprint^)
 echo expliciet toe te voegen aan de "Controlled Folder
 echo Access allowed apps"-lijst via Intune Endpoint
 echo Security / Attack Surface Reduction-beleid, OF
 echo 3^) de app te verpakken als Intune Win32-app
 echo ^(.intunewin^) i.p.v. de installer los te draaien.
 echo.
 exit /b 1
)
echo [OK] Handtekening geverifieerd ^(vertrouwd volgens Windows' eigen policy^).
exit /b 0