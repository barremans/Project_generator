# File:    publish.ps1
# Rol:     Project Generator - GitHub release publiceren (asset + version.txt)
# Versie:  1.0.1
# Auteur:  Barremans
# Run vanuit de repo root (C:\PY\Project_Generator):  .\publish.ps1
# Vereist: gh (ingelogd) + git
#
# Changes: 1.0.1 - Repo bevestigd: barremans/Project_generator
#                   (https://github.com/barremans/Project_generator).
# Changes: 1.0.0 - Aangepast vanuit ArticleSearch (publish.ps1 v1.2.0,
#                   auteur Bart Bossuyt) naar Project Generator:
#                   (1) Default -Owner/-Repo aangepast naar
#                       "barremans"/"Project_generator".
#                   (2) Versie wordt gelezen uit "app/version.py" i.p.v.
#                       root-"version.py" (Project Generator's structuur).
#                   (3) Asset-naam aangepast naar
#                       "Project_GeneratorSetup_<versie>.exe", exact
#                       gelijk aan wat build_installer.bat v1.0.0
#                       genereert (OutputBaseFilename=%PROJECT_NAME%Setup_
#                       %NEW_VERSION%, met PROJECT_NAME=Project_Generator).
#                   Publiceerlogica zelf (release aanmaken/hergebruiken,
#                   asset uploaden, releases/latest/version.txt schrijven,
#                   expliciete git-push-foutcontrole) ONGEWIJZIGD
#                   overgenomen uit ArticleSearch v1.2.0.

param(
    [string]$Owner = "barremans",
    [string]$Repo = "Project_generator"
)

$ErrorActionPreference = "Stop"

# Repo root = map waar dit script staat (dynamisch, geen hardcoded pad)
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

# 1) Versie lezen uit app/version.py (Project Generator's eigen structuur)
$versionPy = Join-Path $Root "app\version.py"
if (-not (Test-Path $versionPy)) { throw "Niet gevonden: $versionPy" }

$txt = Get-Content $versionPy -Raw
$m = [regex]::Match($txt, '__version__\s*=\s*["''](?<v>\d+\.\d+\.\d+)["'']')
if (-not $m.Success) { throw "Kon __version__ niet vinden in app/version.py" }
$version = $m.Groups["v"].Value

$tag = "v$version"
$assetName = "Project_GeneratorSetup_$version.exe"
$assetPath = Join-Path $Root ("dist\" + $assetName)

Write-Host "[INFO] Repo: $Owner/$Repo"
Write-Host "[INFO] Versie: $version"
Write-Host "[INFO] Tag: $tag"
Write-Host "[INFO] Asset: $assetPath"

# 2) Installer bestaat?
if (-not (Test-Path $assetPath)) {
    throw "Installer niet gevonden: $assetPath`nRun eerst build_installer.bat en maak de installer."
}

# 3) Release bestaat? Anders maken. ("release not found" mag NIET crashen)
$releaseExists = $false
try {
    & gh release view $tag --repo "$Owner/$Repo" *> $null
    if ($LASTEXITCODE -eq 0) { $releaseExists = $true }
}
catch {
    $releaseExists = $false
}

if (-not $releaseExists) {
    Write-Host "[INFO] Release $tag bestaat nog niet. Maken..."
    & gh release create $tag --repo "$Owner/$Repo" --title "$tag" --notes "Release $tag"
    if ($LASTEXITCODE -ne 0) { throw "Aanmaken release $tag mislukt." }
}
else {
    Write-Host "[INFO] Release $tag bestaat al."
}

# 4) Upload asset (clobber = overschrijven indien al aanwezig)
Write-Host "[INFO] Uploaden asset..."
& gh release upload $tag "$assetPath" --repo "$Owner/$Repo" --clobber
if ($LASTEXITCODE -ne 0) { throw "Upload asset mislukt." }

# 5) Download-URL opbouwen (stabiel, zelfde patroon als core/updater.py's _asset_url())
$downloadUrl = "https://github.com/$Owner/$Repo/releases/download/$tag/$assetName"
Write-Host "[OK] Download URL: $downloadUrl"

# 6) version.txt (2 regels) schrijven in repo - dit is het bestand dat
#    core/updater.py (check_for_update) rechtstreeks als raw-bestand ophaalt.
$versionTxt = Join-Path $Root "releases\latest\version.txt"
$versionDir = Split-Path -Parent $versionTxt
if (-not (Test-Path $versionDir)) { New-Item -ItemType Directory -Path $versionDir -Force | Out-Null }

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($versionTxt, "$version`n$downloadUrl", $utf8NoBom)

# 7) Commit + push app/version.py EN version.txt
& git add "app/version.py" "releases/latest/version.txt"
& git commit -m "Release $version - sync app/version.py and version.txt" *> $null
# 'nothing to commit' geeft git commit exitcode 1 - dat is OK, vandaar geen
# check hierop. git push WEL expliciet controleren: dit faalde eerder STIL
# bij ArticleSearch (bv. non-fast-forward) - de Release + het asset staan
# dan wel online (die lopen via 'gh', volledig los van git push), maar
# app/version.py/version.txt blijven in dat geval enkel LOKAAL gecommit, en
# de app ziet de nieuwe versie dan nooit.
& git push
if ($LASTEXITCODE -ne 0) {
    throw "git push MISLUKT (exitcode $LASTEXITCODE). De GitHub Release en de installer-asset staan wel al online (die gaan via 'gh', los van git push), maar app/version.py/releases/latest/version.txt zijn enkel LOKAAL gecommit en NIET naar GitHub gepusht - de app detecteert de nieuwe versie hierdoor niet. Los het pushprobleem op (bv. eerst 'git pull --rebase origin main') en run dan handmatig: git push"
}
Write-Host "[OK] app/version.py/version.txt succesvol gepusht naar $Owner/$Repo."

Write-Host ""
Write-Host "============================================================"
Write-Host "[DONE] Published $tag"
Write-Host "Release: https://github.com/$Owner/$Repo/releases/tag/$tag"
Write-Host "Version file: https://raw.githubusercontent.com/$Owner/$Repo/main/releases/latest/version.txt"
Write-Host "============================================================"