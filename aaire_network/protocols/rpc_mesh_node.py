#!/usr/bin/env python3
"""Authenticated JSON-RPC 2.0 Protocol with Anti-Replay Nonce Window."""
from __future__ import annotations
import hashlib
import hmac
import json
import time
import uuid
from typing import Any, Callable, Dict, Set, Tuple


class RPCMeshNode:
    def __init__(self, shared_secret: str = "AAIRE_V7_QUANTUM_KEY") -> None:
        self.shared_secret = shared_secret.encode("utf-8")
        self.methods: Dict[str, Callable[..., Any]] = {}
        self.seen_nonces: Set[str] = set()

    def register_method(self, name: str, fn: Callable[..., Any]) -> None:
        self.methods[name] = fn

    def create_signed_request(self, method: str, params: Dict[str, Any]) -> str:
        envelope = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params,
            "timestamp": time.time(),
            "nonce": uuid.uuid4().hex
        }
        canonical = json.dumps(envelope, sort_keys=True)
        signature = hmac.new(self.shared_secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
        return json.dumps({"envelope": envelope, "signature": signature})

    def handle_request(self, raw_packet: str, max_skew_sec: float = 30.0) -> Tuple[bool, Dict[str, Any]]:
        try:
            packet = json.loads(raw_packet)
            envelope = packet["envelope"]
            signature = packet["signature"]

            canonical = json.dumps(envelope, sort_keys=True)
            expected_sig = hmac.new(self.shared_secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected_sig):
                return False, {"error": "INVALID_RPC_SIGNATURE"}

            if abs(time.time() - float(envelope["timestamp"])) > max_skew_sec:
                return False, {"error": "EXPIRED_TIMESTAMP_REPLAY_BLOCKED"}

            nonce = envelope["nonce"]
            if nonce in self.seen_nonces:
                return False, {"error": "DUPLICATE_NONCE_REPLAY_BLOCKED"}
            self.seen_nonces.add(nonce)

            fn = self.methods.get(envelope["method"])
            if not fn:
                return False, {"error": f"METHOD_NOT_FOUND: {envelope['method']}"}

            result = fn(**envelope.get("params", {}))
            return True, {"jsonrpc": "2.0", "id": envelope["id"], "result": result}
        except Exception as exc:
            return False, {"error": str(exc)}
          
