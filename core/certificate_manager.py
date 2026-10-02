"""
core/certificate_manager.py

Windows code-signing certificate helper for Project Generator.
Uses PowerShell for the Windows certificate store and Authenticode.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

DEFAULT_SUBJECT = "CN=CGK Local Signing"
DEFENDER_CERTIFICATE_URL = (
    "https://security.microsoft.com/securitysettings/endpoints/"
    "custom_ti_indicators?tid=526b32fa-8cb1-4d6a-9e2b-fd48e2a0e296"
    "&childviewid=certificate"
)


class CertificateManagerError(RuntimeError):
    pass


@dataclass
class SigningCertificate:
    subject: str
    issuer: str
    thumbprint: str
    serial_number: str
    not_before: str
    not_after: str
    has_private_key: bool
    store: str

    @property
    def expires(self) -> datetime | None:
        try:
            return datetime.fromisoformat(self.not_after)
        except (TypeError, ValueError):
            return None

    @property
    def days_remaining(self) -> int | None:
        expires = self.expires
        if not expires:
            return None
        return (expires - datetime.now(expires.tzinfo)).days if expires.tzinfo else (expires - datetime.now()).days

    @property
    def is_expired(self) -> bool:
        days = self.days_remaining
        return days is not None and days < 0


@dataclass
class SignedFile:
    path: str
    status: str
    status_message: str
    subject: str = ""
    thumbprint: str = ""
    not_after: str = ""


def _powershell(script: str, timeout: int = 120) -> str:
    """Run a non-interactive PowerShell command and return stdout."""
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    security_module = r"$env:WINDIR\System32\WindowsPowerShell\v1.0\Modules\Microsoft.PowerShell.Security\Microsoft.PowerShell.Security.psd1"
    script = (
        "$ErrorActionPreference='Stop'; "
        f"Import-Module \"{security_module}\" -Force -ErrorAction Stop; "
        + script
    )
    proc = subprocess.run(
        [
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            script,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        creationflags=creationflags,
    )
    if proc.returncode != 0:
        message = (proc.stderr or proc.stdout or "PowerShell command failed").strip()
        raise CertificateManagerError(message)
    return proc.stdout.strip()


def _json_result(script: str):
    output = _powershell(script)
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise CertificateManagerError(f"Invalid PowerShell JSON output: {exc}\n{output}") from exc


ACTIVE_CERT_FILE = Path.home() / ".project_generator" / "signing_certificate.json"

def current_windows_user() -> str:
    import os
    return (os.environ.get("USERDOMAIN", "") + "\\" + os.environ.get("USERNAME", "")).strip("\\")

def is_elevated() -> bool:
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def get_active_thumbprint() -> str:
    try:
        return json.loads(ACTIVE_CERT_FILE.read_text(encoding="utf-8")).get("thumbprint", "")
    except Exception:
        return ""

def set_active_certificate(cert: SigningCertificate) -> Path:
    ACTIVE_CERT_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_CERT_FILE.write_text(json.dumps({
        "subject": cert.subject, "thumbprint": cert.thumbprint,
        "store": cert.store, "not_after": cert.not_after,
        "windows_user": current_windows_user()
    }, indent=2), encoding="utf-8")
    return ACTIVE_CERT_FILE


def list_code_signing_certificates(subject: str = "") -> list[SigningCertificate]:
    subject_filter = subject.replace("'", "''")
    script = rf"""
$ErrorActionPreference = 'Stop'
$items = @()
foreach ($store in @('Cert:\CurrentUser\My','Cert:\LocalMachine\My')) {{
    if (Test-Path $store) {{
        Get-ChildItem $store | ForEach-Object {{
            $eku = @(
                $_.EnhancedKeyUsageList | ForEach-Object {{
                    if ($null -ne $_.ObjectId) {{
                        if ($_.ObjectId -is [string]) {{
                            [string]$_.ObjectId
                        }}
                        elseif ($null -ne $_.ObjectId.Value) {{
                            [string]$_.ObjectId.Value
                        }}
                        else {{
                            [string]$_.ObjectId
                        }}
                    }}
                    elseif ($null -ne $_.Value) {{
                        [string]$_.Value
                    }}
                }}
            )
            if ($eku -contains '1.3.6.1.5.5.7.3.3') {{
                if ('{subject_filter}' -eq '' -or $_.Subject -eq '{subject_filter}') {{
                    $items += [pscustomobject]@{{
                        Subject       = $_.Subject
                        Issuer        = $_.Issuer
                        Thumbprint    = $_.Thumbprint
                        SerialNumber  = $_.SerialNumber
                        NotBefore     = $_.NotBefore.ToString('o')
                        NotAfter      = $_.NotAfter.ToString('o')
                        HasPrivateKey = [bool]$_.HasPrivateKey
                        Store         = $store
                    }}
                }}
            }}
        }}
    }}
}}
@($items) | ConvertTo-Json -Depth 4 -Compress
"""
    data = _json_result(script)
    if isinstance(data, dict):
        data = [data]
    return [
        SigningCertificate(
            subject=x.get("Subject", ""),
            issuer=x.get("Issuer", ""),
            thumbprint=x.get("Thumbprint", ""),
            serial_number=x.get("SerialNumber", ""),
            not_before=x.get("NotBefore", ""),
            not_after=x.get("NotAfter", ""),
            has_private_key=bool(x.get("HasPrivateKey")),
            store=x.get("Store", ""),
        )
        for x in data
    ]


def create_code_signing_certificate(
    common_name: str = "CGK Local Signing",
    years: int = 2,
    store: str = r"Cert:\CurrentUser\My",
) -> SigningCertificate:
    """Create a self-signed RSA/SHA256 Code Signing certificate."""
    if not common_name.strip():
        raise ValueError("Common name is required.")
    if years < 1 or years > 10:
        raise ValueError("Validity must be between 1 and 10 years.")
    cn = common_name.strip().replace("'", "''")
    safe_store = store.replace("'", "''")
    script = rf"""
$ErrorActionPreference = 'Stop'
$cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject 'CN={cn}' `
    -CertStoreLocation '{safe_store}' `
    -KeyAlgorithm RSA `
    -KeyLength 3072 `
    -HashAlgorithm SHA256 `
    -NotAfter (Get-Date).AddYears({years})
[pscustomobject]@{{
    Subject       = $cert.Subject
    Issuer        = $cert.Issuer
    Thumbprint    = $cert.Thumbprint
    SerialNumber  = $cert.SerialNumber
    NotBefore     = $cert.NotBefore.ToString('o')
    NotAfter      = $cert.NotAfter.ToString('o')
    HasPrivateKey = [bool]$cert.HasPrivateKey
    Store         = '{safe_store}'
}} | ConvertTo-Json -Compress
"""
    x = _json_result(script)
    return SigningCertificate(
        subject=x["Subject"],
        issuer=x["Issuer"],
        thumbprint=x["Thumbprint"],
        serial_number=x["SerialNumber"],
        not_before=x["NotBefore"],
        not_after=x["NotAfter"],
        has_private_key=bool(x["HasPrivateKey"]),
        store=x["Store"],
    )


def export_certificate(thumbprint: str, destination: Path) -> Path:
    destination = Path(destination).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    thumb = thumbprint.replace("'", "''")
    dest = str(destination).replace("'", "''")
    script = rf"""
$ErrorActionPreference = 'Stop'
$cert = $null
foreach ($store in @('Cert:\CurrentUser\My','Cert:\LocalMachine\My')) {{
    $candidate = Get-ChildItem $store -ErrorAction SilentlyContinue |
        Where-Object {{ $_.Thumbprint -eq '{thumb}' }} |
        Select-Object -First 1
    if ($candidate) {{ $cert = $candidate; break }}
}}
if (-not $cert) {{ throw 'Certificate not found: {thumb}' }}
Export-Certificate -Cert $cert -FilePath '{dest}' -Type CERT -Force | Out-Null
"""
    _powershell(script)
    return destination




def certificate_trust_status(thumbprint: str) -> dict[str, bool]:
    """Return whether the public certificate is trusted for CurrentUser."""
    thumb = (thumbprint or "").replace("'", "''")
    script = rf"""
$ErrorActionPreference = 'Stop'
$thumb = '{thumb}'
[pscustomobject]@{{
    Root = [bool](Get-ChildItem 'Cert:\CurrentUser\Root' -ErrorAction SilentlyContinue |
        Where-Object {{ $_.Thumbprint -eq $thumb }} | Select-Object -First 1)
    TrustedPublisher = [bool](Get-ChildItem 'Cert:\CurrentUser\TrustedPublisher' -ErrorAction SilentlyContinue |
        Where-Object {{ $_.Thumbprint -eq $thumb }} | Select-Object -First 1)
}} | ConvertTo-Json -Compress
"""
    data = _json_result(script)
    return {
        "root": bool(data.get("Root", False)),
        "trusted_publisher": bool(data.get("TrustedPublisher", False)),
    }


def trust_certificate_current_user(thumbprint: str) -> dict[str, bool]:
    """
    Add the PUBLIC part of an existing signing certificate to CurrentUser Root
    and TrustedPublisher. The private key remains only in the My store.
    """
    thumb = (thumbprint or "").replace("'", "''")
    script = rf"""
$ErrorActionPreference = 'Stop'
$thumb = '{thumb}'
$cert = Get-ChildItem 'Cert:\CurrentUser\My' -ErrorAction Stop |
    Where-Object {{ $_.Thumbprint -eq $thumb }} |
    Select-Object -First 1

if (-not $cert) {{
    throw "Certificate $thumb not found in Cert:\CurrentUser\My"
}}
if (-not $cert.HasPrivateKey) {{
    throw "Certificate $thumb has no private key in Cert:\CurrentUser\My"
}}

# Construct a public-only copy. This never copies the private key.
$publicCert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 (,$cert.RawData)

foreach ($storeName in @('Root', 'TrustedPublisher')) {{
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store(
        $storeName,
        [System.Security.Cryptography.X509Certificates.StoreLocation]::CurrentUser
    )
    try {{
        $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
        $exists = $store.Certificates | Where-Object {{ $_.Thumbprint -eq $thumb }} | Select-Object -First 1
        if (-not $exists) {{
            $store.Add($publicCert)
        }}
    }}
    finally {{
        $store.Close()
    }}
}}

[pscustomobject]@{{
    Root = [bool](Get-ChildItem 'Cert:\CurrentUser\Root' -ErrorAction SilentlyContinue |
        Where-Object {{ $_.Thumbprint -eq $thumb }} | Select-Object -First 1)
    TrustedPublisher = [bool](Get-ChildItem 'Cert:\CurrentUser\TrustedPublisher' -ErrorAction SilentlyContinue |
        Where-Object {{ $_.Thumbprint -eq $thumb }} | Select-Object -First 1)
}} | ConvertTo-Json -Compress
"""
    data = _json_result(script)
    result = {
        "root": bool(data.get("Root", False)),
        "trusted_publisher": bool(data.get("TrustedPublisher", False)),
    }
    if not all(result.values()):
        raise CertificateManagerError(
            "Certificate trust could not be confirmed in CurrentUser Root and TrustedPublisher."
        )
    return result


def find_signtool() -> str:
    """Find the newest Windows SDK signtool.exe (prefer x64)."""
    script = r"""
$roots = @(
  "${env:ProgramFiles(x86)}\Windows Kits\10\bin",
  "${env:ProgramFiles}\Windows Kits\10\bin"
)
$candidates = @()
foreach ($root in $roots) {
  if (Test-Path $root) {
    $candidates += Get-ChildItem -LiteralPath $root -Filter signtool.exe -File -Recurse -ErrorAction SilentlyContinue |
      Where-Object { $_.FullName -match '\\x64\\signtool\.exe$' }
  }
}
if (-not $candidates) { throw 'signtool.exe niet gevonden. Installeer Windows SDK Signing Tools.' }
($candidates | Sort-Object FullName -Descending | Select-Object -First 1).FullName
"""
    return _powershell(script).strip()


def get_certificate_by_thumbprint(thumbprint: str) -> SigningCertificate | None:
    th = (thumbprint or "").upper()
    for cert in list_code_signing_certificates(""):
        if cert.thumbprint.upper() == th:
            return cert
    return None


def sign_file(path: Path, thumbprint: str, timestamp_url: str = "http://timestamp.sectigo.com") -> tuple[bool, str]:
    """
    Sign one executable with the explicitly selected CurrentUser certificate.
    Verification is mandatory after signing.
    """
    path = Path(path).resolve()
    if not path.is_file():
        return False, f"Bestand bestaat niet: {path}"
    cert = get_certificate_by_thumbprint(thumbprint)
    if not cert:
        return False, f"Actief certificaat niet gevonden: {thumbprint}"
    if cert.is_expired:
        return False, "Actief certificaat is verlopen."
    if not cert.has_private_key:
        return False, "Actief certificaat heeft geen private key."

    signtool = find_signtool()
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    sign = subprocess.run(
        [signtool, "sign", "/sha1", cert.thumbprint, "/fd", "SHA256",
         "/tr", timestamp_url, "/td", "SHA256", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        creationflags=flags
    )
    if sign.returncode != 0:
        return False, (sign.stdout + "\n" + sign.stderr).strip()

    verify = subprocess.run(
        [signtool, "verify", "/pa", "/v", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        creationflags=flags
    )
    output = (verify.stdout + "\n" + verify.stderr).strip()
    if verify.returncode != 0:
        return False, "Signing uitgevoerd, maar verificatie MISLUKT:\n" + output
    return True, output or "Signed en geverifieerd."


def sign_files(paths: list[Path], thumbprint: str) -> list[tuple[str, bool, str]]:
    results = []
    for path in paths:
        ok, message = sign_file(Path(path), thumbprint)
        results.append((str(path), ok, message))
    return results


def scan_signed_files(root: Path, recursive: bool = True) -> list[SignedFile]:
    """
    Scan only distributable executables in project dist folders.

    When root is C:\\PY (or another projects root), all descendant directories
    named 'dist' are discovered. Only .exe files directly in those dist folders
    are checked. PyInstaller's dist\\App\\_internal dependencies are therefore
    deliberately ignored.

    Setup executables may contain a version suffix, e.g.
    ArticleSearchSetup_15.5.2.exe; no fixed version is required.
    """
    root = Path(root).resolve()
    if not root.exists():
        raise CertificateManagerError(f"Path does not exist: {root}")

    safe_root = str(root).replace("'", "''")
    script = rf"""
$ErrorActionPreference = 'Stop'
$root = '{safe_root}'

# If the selected folder itself is a dist folder, use it.
# Otherwise discover all project dist folders recursively.
$distDirs = @()
$rootItem = Get-Item -LiteralPath $root
if ($rootItem.PSIsContainer -and $rootItem.Name -ieq 'dist') {{
    $distDirs = @($rootItem)
}} else {{
    $distDirs = @(Get-ChildItem -LiteralPath $root -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object {{ $_.Name -ieq 'dist' }})
}}

$result = foreach ($dist in $distDirs) {{
    # Intentionally NOT recursive inside dist:
    # only final application/setup executables, no _internal DLL/EXE dependencies.
    $files = @(Get-ChildItem -LiteralPath $dist.FullName -File -Filter '*.exe' -ErrorAction SilentlyContinue)
    foreach ($file in $files) {{
        try {{
            $sig = Microsoft.PowerShell.Security\Get-AuthenticodeSignature `
                -LiteralPath $file.FullName -ErrorAction Stop

            [pscustomobject]@{{
                Path          = $file.FullName
                Status        = [string]$sig.Status
                StatusMessage = [string]$sig.StatusMessage
                Subject       = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Subject }} else {{ '' }}
                Thumbprint    = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Thumbprint }} else {{ '' }}
                NotAfter      = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.NotAfter.ToString('o') }} else {{ '' }}
            }}
        }} catch {{
            [pscustomobject]@{{
                Path          = $file.FullName
                Status        = 'ERROR'
                StatusMessage = $_.Exception.Message
                Subject       = ''
                Thumbprint    = ''
                NotAfter      = ''
            }}
        }}
    }}
}}
@($result) | ConvertTo-Json -Depth 3 -Compress
"""
    data = _json_result(script)
    if isinstance(data, dict):
        data = [data]
    return [
        SignedFile(
            path=x.get("Path", ""),
            status=x.get("Status", ""),
            status_message=x.get("StatusMessage", ""),
            subject=x.get("Subject", ""),
            thumbprint=x.get("Thumbprint", ""),
            not_after=x.get("NotAfter", ""),
        )
        for x in data
    ]

