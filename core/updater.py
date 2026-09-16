"""
File:    /core/updater.py
Rol:     Update-check tegen GitHub — leest version.txt (releases/latest/)
         voor de versievergelijking, en de release notes van de laatste
         GitHub Release via de Releases API voor "Wat is er nieuw?".
Applicatie: Project Generator
Versie:  1.0.1
Auteur:  Barremans
Changes: 1.0.1 - Repo bevestigd: barremans/Project_generator
                  (https://github.com/barremans/Project_generator) —
                  eerdere aanname "project-generator" was verkeerd
                  gespeld (moet "Project_generator" zijn, met hoofdletter
                  en underscore).
Changes: 1.0.0 - Geport vanuit ArticleSearch (updater.py v1.2.0, auteur
                  Bart Bossuyt) naar Project Generator:
                  (1) PySide6 -> PyQt6 (QMessageBox-import).
                  (2) OWNER/REPO aangepast naar "barremans"/
                      "Project_generator".
                  (3) Asset-naam aangepast naar
                      "Project_GeneratorSetup_<versie>.exe", consistent
                      met build_installer.bat v1.0.0 / publish.ps1 v1.0.0.
                  (4) TOKEN leeg gelaten i.p.v. een (verlopen)
                      ArticleSearch-PAT hergebruikt — de Releases API
                      heeft er sowieso geen nodig (publieke repo, puur
                      lezen, zie punt 1.2.0 hieronder). Enkel invullen als
                      de repo ooit Private wordt (Contents API-fallback
                      voor version.txt).
                  Overige logica (version.txt-check via raw + Contents-
                  API-fallback, release notes via Releases API zonder
                  auth) ONGEWIJZIGD overgenomen uit ArticleSearch v1.2.0
                  (daar destijds al gefixt: geen Authorization-header meer
                  nodig/gewenst voor een publieke repo se releases-lezen).
"""
import webbrowser
import requests
from packaging.version import parse as parse_version
from PyQt6.QtWidgets import QMessageBox

OWNER  = "barremans"
REPO   = "Project_generator"
BRANCH = "main"
REL_DIR = "releases/latest"

RAW_VERSION_URL      = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{REL_DIR}/version.txt"
CONTENTS_VERSION_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{REL_DIR}/version.txt?ref={BRANCH}"

# Officiële GitHub Releases API — geeft de laatste gepubliceerde
# (niet-draft, niet-pre-release) Release terug, incl. release notes (body).
RELEASES_API_LATEST = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"

# Enkel nodig als de repo ooit Private wordt (Contents API-fallback voor
# version.txt). Voor een Public repo werkt alles hieronder ook zonder
# token — laat dit dus gewoon leeg tenzij je de repo bewust Private zet.
# Zet via env var i.p.v. hardcoded indien je dit toch invult.
TOKEN = ""

def _headers_raw():
    # raw github ondersteunt geen auth
    return {"Accept": "text/plain"}

def _headers_api():
    h = {"Accept": "application/vnd.github.v3.raw"}
    if TOKEN:
        h["Authorization"] = f"token {TOKEN}"
    return h


# Aparte header-set voor de Releases API — hier willen we het JSON-object
# terug (tag_name/body/html_url), dus GEEN "v3.raw" Accept-header.
#
# Bewust GEEN Authorization-header. Het ophalen van een publieke release is
# een puur leesverkeer-endpoint en werkt bij GitHub altijd anoniem — een
# (kapot) token zou de hele request onnodig laten falen met 401, ook al zou
# het zonder token gewoon lukken (zelfde les als ArticleSearch v1.2.0).
# Mocht de repo ooit Private worden, moet hier weer een geldig token
# toegevoegd worden (analoog aan _headers_api()).
def _headers_releases_api():
    return {"Accept": "application/vnd.github+json"}


def fetch_release_notes(timeout=8) -> dict:
    """
    Haalt de release notes (body) van de laatste gepubliceerde GitHub
    Release op, via de officiële Releases API.

    Retourneert: {"tag_name": str, "body": str, "html_url": str}
    - "body" is de Markdown-tekst zoals ingevuld bij het publiceren van de
      Release op GitHub (kan leeg zijn als er niets werd ingevuld).
    - "html_url" wijst naar de releasepagina zelf — bruikbaar als fallback-
      link wanneer "body" leeg is of het ophalen faalt.

    Raises requests.HTTPError / requests.RequestException bij netwerk- of
    API-fouten — de aanroeper (UI) vangt dit af en toont een nette fallback.
    """
    r = requests.get(RELEASES_API_LATEST, headers=_headers_releases_api(), timeout=timeout)
    if not r.ok:
        raise requests.HTTPError(f"{r.status_code} for {RELEASES_API_LATEST}: {r.text[:200]}")
    data = r.json()
    return {
        "tag_name": data.get("tag_name", ""),
        "body": (data.get("body") or "").strip(),
        "html_url": data.get("html_url") or f"https://github.com/{OWNER}/{REPO}/releases/latest",
    }

def _fetch_version_txt(timeout=8) -> str:
    # 1) Raw (werkt voor public)
    try:
        r = requests.get(RAW_VERSION_URL, headers=_headers_raw(), timeout=timeout)
        if r.ok:
            return r.text
        print(f"[update-check] raw GET {RAW_VERSION_URL} -> {r.status_code}")
    except Exception as e:
        print(f"[update-check] raw exception: {e}")

    # 2) Contents API (werkt ook voor private, mits TOKEN)
    r = requests.get(CONTENTS_VERSION_URL, headers=_headers_api(), timeout=timeout)
    if not r.ok:
        # 404 bij private zonder juiste token is normaal
        raise requests.HTTPError(f"{r.status_code} for {CONTENTS_VERSION_URL}: {r.text[:200]}")
    return r.text  # met Accept: v3.raw = pure file-inhoud

def _parse_version_file(txt: str):
    # regel 1: versie; regel 2: optionele download-URL
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    if not lines:
        raise RuntimeError("version.txt is leeg")
    version = lines[0].lstrip("vV")
    url = lines[1] if len(lines) >= 2 and lines[1].startswith(("http://", "https://")) else None
    return version, url

def _asset_url(version: str, asset_name: str = None) -> str:
    if not asset_name:
        asset_name = f"Project_GeneratorSetup_{version}.exe"
    return f"https://github.com/{OWNER}/{REPO}/releases/download/v{version}/{asset_name}"

def check_for_update(current_version: str, parent=None, callback=None) -> bool:
    try:
        txt = _fetch_version_txt()
        remote_version, _ = _parse_version_file(txt)
        is_newer = parse_version(remote_version) > parse_version(current_version)
        print(f"[update-check] Lokale versie: {current_version}, Remote versie: {remote_version}")
        if callback:
            callback(is_newer)
        elif is_newer:
            QMessageBox.information(
                parent, "Nieuwe versie beschikbaar",
                f"Je gebruikt {current_version}, nieuwste is {remote_version}.\n"
                f"Klik op 'Update nu' om te downloaden."
            )
        return is_newer
    except Exception as e:
        print(f"[update-check] Mislukt: {e}")
        if callback:
            callback(False)
        return False

def download_latest_release(parent=None):
    try:
        txt = _fetch_version_txt()
        version, url = _parse_version_file(txt)
        if not url:
            url = _asset_url(version)
        QMessageBox.information(parent, "Update", "De nieuwste installer wordt geopend in je browser.")
        webbrowser.open(url)
    except Exception as e:
        QMessageBox.critical(parent, "Fout bij download", str(e))