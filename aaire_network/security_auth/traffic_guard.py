#!/usr/init/env python3
"""Traffic Guard for filtering secure requests and blocking malicious patterns."""
from __future__ import annotations
import re

class TrafficGuard:
    FORBIDDEN_PATTERNS = [r"<script>", r"DROP TABLE", r"exec\(", r"eval\("]

    @classmethod
    def inspect_payload(cls, data_str: str) -> bool:
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, data_str, re.IGNORECASE):
                return False
        return True
      
