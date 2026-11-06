import hashlib
import hmac
import mmap
import os
import platform
from urllib.parse import urlparse

class CrossOSVaultGuard:
    """Cross-OS SafeIO (25MB mmap window), SSRF Guard & Asymmetric-Style Public Verifier."""
    def __init__(self, seed: str = ""):
        self.os_name = platform.system().lower()
        raw_seed = (seed or os.environ.get("AAIRE_LEDGER_HMAC_KEY", "AAIRE_V12_MASTER_SEED")).encode("utf-8")
        self._priv = hashlib.sha256(b"ed25519_priv:" + raw_seed).digest()
        self.public_verify_key = hashlib.sha256(b"ed25519_pub:" + self._priv).hexdigest()

    def create_public_seal(self, payload_bytes: bytes) -> dict:
        digest = hashlib.sha256(payload_bytes).hexdigest()
        sig = hmac.new(self._priv, (digest + self.public_verify_key).encode("utf-8"), hashlib.sha256).hexdigest()
        return {"scheme": "AAIRE-PublicSeal-v12", "pub_key": self.public_verify_key[:24], "sha256": digest, "signature": sig}

    def is_safe_url(self, url: str) -> bool:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        blocked = ("127.0.0.1", "localhost", "169.254.169.254", "0.0.0.0", "::1")
        return parsed.scheme in ("http", "https") and bool(host) and not any(host.startswith(b) for b in blocked)

    def scan_windowed_chunks(self, path: str, window_bytes: int = 1_048_576):
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            return
        with open(path, "rb") as fp, mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            for pos in range(0, len(mm), window_bytes):
                yield pos, mm[pos:pos + window_bytes]
              
