@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: ============================================================
:: File:    export_to_usb.bat
:: Rol:     Algemene Python-projectexport naar USB
:: Versie:  2.0.0
:: ------------------------------------------------------------
:: - Bronmap kan als argument worden meegegeven of interactief gekozen
:: - Projectnaam wordt automatisch uit de bronmap gehaald
:: - zzz, .venv en venv worden NIET meegenomen in de hoofdcopy
:: - voorkeur voor .venv als beide virtuele omgevingen bestaan
:: - gekozen virtuele omgeving wordt exact 1 keer gekopieerd
:: - requirements.txt wordt aangemaakt indien een venv beschikbaar is
:: - USB-station wordt interactief gekozen
:: - timestamp, logbestand en uitvoeringstijd worden bijgehouden
::
:: Gebruik:
::   export_to_usb.bat
::   export_to_usb.bat "C:\PY\MijnProject"
:: ============================================================

:: === 0. Starttijd ===
for /f %%a in ('powershell -NoProfile -Command "[int64]([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"') do set "STARTSEC=%%a"

:: === 1. Timestamp ===
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "TIMESTAMP=%%i"

:: === 2. Bronmap bepalen ===
set "SOURCE_FOLDER=%~1"

if not defined SOURCE_FOLDER (
    echo.
    echo ============================================================
    echo Algemene Python-projectexport naar USB
    echo ============================================================
    echo.
    set /p "SOURCE_FOLDER=Geef de volledige projectmap (bv. C:\PY\MijnProject): "
)

:: Omringende quotes verwijderen indien de gebruiker die zelf invoerde.
set "SOURCE_FOLDER=%SOURCE_FOLDER:"=%"

:: Eventuele afsluitende backslash verwijderen, behalve bij een drive-root.
if "%SOURCE_FOLDER:~-1%"=="\" (
    if not "%SOURCE_FOLDER:~1,2%"==":\" set "SOURCE_FOLDER=%SOURCE_FOLDER:~0,-1%"
)

if not defined SOURCE_FOLDER (
    echo [FOUT] Geen bronmap opgegeven.
    goto EINDE_MET_FOUT
)

if not exist "%SOURCE_FOLDER%\" (
    echo.
    echo [FOUT] Bronmap bestaat niet:
    echo "%SOURCE_FOLDER%"
    goto EINDE_MET_FOUT
)

:: Volledig pad normaliseren en projectnaam uit laatste map halen.
for %%I in ("%SOURCE_FOLDER%") do (
    set "SOURCE_FOLDER=%%~fI"
    set "PROJECT_NAME=%%~nxI"
)

if not defined PROJECT_NAME set "PROJECT_NAME=project"

set "DOT_VENV_PATH=%SOURCE_FOLDER%\.venv"
set "VENV_NORMAL_PATH=%SOURCE_FOLDER%\venv"
set "VENV_PATH="
set "VENV_NAME="

:: === 3. Virtuele omgeving detecteren ===
if exist "%DOT_VENV_PATH%\Scripts\python.exe" (
    set "VENV_PATH=%DOT_VENV_PATH%"
    set "VENV_NAME=.venv"
) else if exist "%VENV_NORMAL_PATH%\Scripts\python.exe" (
    set "VENV_PATH=%VENV_NORMAL_PATH%"
    set "VENV_NAME=venv"
)

:: === 4. USB-station kiezen ===
:KIES_USB
echo.
set /p "USB_DRIVE=Geef de stationsletter van de USB-stick (bv. E): "

if not defined USB_DRIVE (
    echo [FOUT] Geen stationsletter ingevoerd. Probeer opnieuw.
    goto KIES_USB
)

set "USB_DRIVE=%USB_DRIVE:"=%"
set "USB_DRIVE=%USB_DRIVE::=%"
set "USB_DRIVE=%USB_DRIVE:\=%"
set "USB_DRIVE=%USB_DRIVE:~0,1%"

if not exist "%USB_DRIVE%:\" (
    echo [FOUT] Stationsletter %USB_DRIVE%: bestaat niet of is niet toegankelijk.
    goto KIES_USB
)

:: === 5. Doelmap ===
set "USB_FOLDER=%USB_DRIVE%:\export_%PROJECT_NAME%_%TIMESTAMP%"

echo.
echo ============================================================
echo %PROJECT_NAME% export
echo ============================================================
echo.
echo [INFO] Project : "%PROJECT_NAME%"
echo [INFO] Bronmap : "%SOURCE_FOLDER%"
echo [INFO] USB     : "%USB_DRIVE%:"
echo [INFO] Doelmap : "%USB_FOLDER%"
echo.

if defined VENV_PATH (
    echo [INFO] Virtuele omgeving gevonden: "%VENV_PATH%"
) else (
    echo [WAARSCHUWING] Geen .venv of venv gevonden.
)
echo.

:: === 6. Doelmap aanmaken ===
if not exist "%USB_FOLDER%" (
    mkdir "%USB_FOLDER%"
    if errorlevel 1 (
        echo [FOUT] Doelmap kon niet worden aangemaakt.
        goto EINDE_MET_FOUT
    )
)

:: === 7. requirements.txt aanmaken ===
echo.
echo ============================================================
echo [0] Python dependencies exporteren
echo ============================================================
echo.

if defined VENV_PATH (
    echo [INFO] requirements.txt wordt aangemaakt via:
    echo        "%VENV_PATH%\Scripts\python.exe"
    "%VENV_PATH%\Scripts\python.exe" -m pip freeze > "%SOURCE_FOLDER%\requirements.txt"

    if exist "%SOURCE_FOLDER%\requirements.txt" (
        echo [OK] requirements.txt aangemaakt.
    ) else (
        echo [WAARSCHUWING] requirements.txt kon niet worden aangemaakt.
    )
) else (
    echo [WAARSCHUWING] Geen virtuele omgeving gevonden.
    echo [WAARSCHUWING] requirements.txt wordt niet aangemaakt.
)

:: === 8. Projectmap kopieren ===
echo.
echo ============================================================
echo [1] Projectmap kopieren
echo ============================================================
echo.
echo [INFO] Uitgesloten: zzz, .venv en venv
echo.

robocopy "%SOURCE_FOLDER%" "%USB_FOLDER%" ^
    /E ^
    /XD "%SOURCE_FOLDER%\zzz" "%SOURCE_FOLDER%\.venv" "%SOURCE_FOLDER%\venv" ^
    /ETA ^
    /FP

set "ROBO_PROJECT=%ERRORLEVEL%"

if %ROBO_PROJECT% GEQ 8 (
    echo.
    echo [FOUT] Ernstige fout tijdens kopieren van de projectmap.
    echo [FOUT] Robocopy exit code: %ROBO_PROJECT%
    goto EINDE_MET_FOUT
)

echo.
echo [OK] Projectbestanden succesvol gekopieerd.

:: === 9. Virtuele omgeving exact 1 keer kopieren ===
echo.
echo ============================================================
echo [2] Virtuele omgeving kopieren
echo ============================================================
echo.

if defined VENV_PATH (
    echo [INFO] Bron: "%VENV_PATH%"
    echo [INFO] Doel: "%USB_FOLDER%\%VENV_NAME%"
    echo.

    robocopy "%VENV_PATH%" "%USB_FOLDER%\%VENV_NAME%" /E /ETA /FP
    set "ROBO_VENV=%ERRORLEVEL%"

    if !ROBO_VENV! GEQ 8 (
        echo.
        echo [WAARSCHUWING] Fout tijdens kopieren van de virtuele omgeving.
        echo [WAARSCHUWING] Robocopy exit code: !ROBO_VENV!
        echo [WAARSCHUWING] Projectbestanden zijn wel gekopieerd.
    ) else (
        echo.
        echo [OK] Virtuele omgeving succesvol gekopieerd: %VENV_NAME%
    )
) else (
    echo [INFO] Geen virtuele omgeving gekopieerd.
)

:: === 10. Eindtijd ===
for /f %%a in ('powershell -NoProfile -Command "[int64]([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"') do set "ENDSEC=%%a"

set /a DURATION=ENDSEC-STARTSEC
set /a HOURS=DURATION/3600
set /a MINUTES=(DURATION%%3600)/60
set /a SECONDS=DURATION%%60

:: === 11. Logbestand ===
echo.
echo ============================================================
echo [3] Logbestand schrijven
echo ============================================================
echo.

(
    echo Algemene Python-projectexport
    echo ============================
    echo.
    echo Project: %PROJECT_NAME%
    echo Exportdatum: %DATE%
    echo Exporttijd: %TIME%
    echo.
    echo Bronmap: %SOURCE_FOLDER%
    echo Bestemming: %USB_FOLDER%
    echo.
    echo Map zzz uitgesloten: JA
    echo Map .venv uitgesloten van hoofdcopy: JA
    echo Map venv uitgesloten van hoofdcopy: JA
    echo.
    echo Totale duur: %HOURS% uur %MINUTES% min %SECONDS% sec
    echo.
) > "%USB_FOLDER%\export_log.txt"

if exist "%SOURCE_FOLDER%\requirements.txt" (
    echo requirements.txt aanwezig: JA>> "%USB_FOLDER%\export_log.txt"
) else (
    echo requirements.txt aanwezig: NEE>> "%USB_FOLDER%\export_log.txt"
)

if defined VENV_PATH (
    echo Virtuele omgeving gevonden: JA>> "%USB_FOLDER%\export_log.txt"
    echo Virtuele omgeving bron: %VENV_PATH%>> "%USB_FOLDER%\export_log.txt"
    echo Virtuele omgeving naam: %VENV_NAME%>> "%USB_FOLDER%\export_log.txt"

    if exist "%USB_FOLDER%\%VENV_NAME%\" (
        echo Virtuele omgeving gekopieerd: JA>> "%USB_FOLDER%\export_log.txt"
    ) else (
        echo Virtuele omgeving gekopieerd: NEE>> "%USB_FOLDER%\export_log.txt"
    )
) else (
    echo Virtuele omgeving gevonden: NEE>> "%USB_FOLDER%\export_log.txt"
    echo Virtuele omgeving gekopieerd: NEE>> "%USB_FOLDER%\export_log.txt"
)

echo [OK] Logbestand aangemaakt.

:: === 12. Eindresultaat ===
echo.
echo ============================================================
echo EXPORT SUCCESVOL AFGEROND
echo ============================================================
echo.
echo Project : %PROJECT_NAME%
echo Doel    : "%USB_FOLDER%"
echo Duur    : %HOURS% uur %MINUTES% min %SECONDS% sec
echo.
echo ============================================================
echo.

pause
goto EINDE

:: === 13. Foutafhandeling ===
:EINDE_MET_FOUT
for /f %%a in ('powershell -NoProfile -Command "[int64]([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"') do set "ENDSEC=%%a"

set /a DURATION=ENDSEC-STARTSEC
set /a HOURS=DURATION/3600
set /a MINUTES=(DURATION%%3600)/60
set /a SECONDS=DURATION%%60

echo.
echo ============================================================
echo EXPORT AFGEBROKEN MET EEN FOUT
echo ============================================================
echo.
echo Totale duur tot fout:
echo %HOURS% uur %MINUTES% min %SECONDS% sec
echo.
pause

:EINDE
endlocal
