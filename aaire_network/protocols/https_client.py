#!/usr/bin/env python3
"""Client to securely fetch data from HTTPS and HTTP endpoints."""
from __future__ import annotations
import urllib.request
from typing import Optional, Tuple

class HTTPSClient:
    @staticmethod
    def get(url: str, timeout: int = 10) -> Tuple[bool, Optional[str]]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AAIRE-Network-Client/4.1"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                body = response.read().decode("utf-8", errors="ignore")
                return True, body
        except Exception as e:
            return False, str(e)
          
