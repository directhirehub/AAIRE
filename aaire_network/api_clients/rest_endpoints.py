#!/usr/bin/env python3
"""REST API Handler for sending and receiving JSON payloads."""
from __future__ import annotations
import json
import urllib.request
from typing import Any, Dict, Optional, Tuple

class RESTClient:
    @staticmethod
    def post_json(url: str, data: Dict[Any, Any]) -> Tuple[bool, Optional[str]]:
        try:
            payload = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "AAIRE-REST"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return True, response.read().decode("utf-8")
        except Exception as e:
            return False, str(e)
          
