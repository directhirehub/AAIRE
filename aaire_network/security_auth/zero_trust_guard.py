#!/usr/bin/env python3
"""Zero-Trust HMAC Auth, Token-Bucket Rate Limiter & Shannon Entropy Guard."""
from __future__ import annotations
import hashlib
import hmac
import math
import time
from collections import Counter
from typing import Dict, Tuple

from aaire_network.security_auth.traffic_guard import TrafficGuard


class ZeroTrustGuard:
    _buckets: Dict[str, Dict[str, float]] = {}

    @staticmethod
    def calculate_entropy(data: str) -> float:
        if not data:
            return 0.0
        counts = Counter(data)
        length = len(data)
        return -sum((c / length) * math.log2(c / length) for c in counts.values())

    @classmethod
    def allow_request(cls, client_id: str, rate_per_sec: float = 5.0, capacity: float = 10.0) -> bool:
        now = time.monotonic()
        bucket = cls._buckets.get(client_id, {"tokens": capacity, "last": now})
        elapsed = now - bucket["last"]
        bucket["tokens"] = min(capacity, bucket["tokens"] + elapsed * rate_per_sec)
        bucket["last"] = now

        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            cls._buckets[client_id] = bucket
            return True
        cls._buckets[client_id] = bucket
        return False

    @staticmethod
    def sign_payload(payload: str, secret_key: str) -> str:
        return hmac.new(secret_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

    @classmethod
    def verify_packet(cls, client_id: str, payload: str, signature: str, secret_key: str) -> Tuple[bool, str]:
        if not cls.allow_request(client_id):
            return False, "RATE_LIMIT_EXCEEDED"
        if not TrafficGuard.inspect_payload(payload):
            return False, "FORBIDDEN_PATTERN_DETECTED"
        if cls.calculate_entropy(payload) > 6.2:
            return False, "HIGH_ENTROPY_OBFUSCATED_PAYLOAD"
        expected_sig = cls.sign_payload(payload, secret_key)
        if not hmac.compare_digest(expected_sig, signature):
            return False, "INVALID_HMAC_SIGNATURE"
        return True, "VERIFIED_SAFE"
          
