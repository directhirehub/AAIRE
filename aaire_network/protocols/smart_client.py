#!/usr/bin/env python3
"""Resilient HTTPS Client with Caching, Exponential Backoff & TrafficGuard."""
from __future__ import annotations
import hashlib
import json
import time
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

from aaire_network.security_auth.traffic_guard import TrafficGuard


class SmartHTTPSClient:
    CACHE_DIR = Path("aaire_storage/aaire_memory/net_cache")

    @classmethod
    def fetch_resilient(
        cls,
        url: str,
        retries: int = 3,
        timeout: int = 10,
        use_cache: bool = True
    ) -> Tuple[bool, Optional[str]]:
        if not TrafficGuard.inspect_payload(url):
            return False, "Blocked by TrafficGuard: Unsafe URL pattern"

        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
        cache_file = cls.CACHE_DIR / f"{url_hash}.json"

        if use_cache and cache_file.exists():
            try:
                cached = json.loads(cache_file.read_text(encoding="utf-8"))
                if time.time() - cached.get("ts", 0) < 3600:
                    return True, cached.get("body")
            except Exception:
                pass

        backoff = 1.0
        last_error = ""
        for attempt in range(1, retries + 1):
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": f"AAIRE-Singularity-Engine/7.0 (Attempt-{attempt})"}
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    body = resp.read().decode("utf-8", errors="ignore")
                    if not TrafficGuard.inspect_payload(body[:4096]):
                        return False, "Blocked by TrafficGuard: Malicious response payload"

                    if use_cache:
                        cache_file.write_text(
                            json.dumps({"url": url, "ts": time.time(), "body": body}),
                            encoding="utf-8"
                        )
                    return True, body
            except Exception as exc:
                last_error = str(exc)
                if attempt < retries:
                    time.sleep(backoff)
                    backoff *= 2.0

        return False, f"Failed after {retries} retries: {last_error}"
                             
