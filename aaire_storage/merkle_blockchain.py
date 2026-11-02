#!/usr/bin/env python3
"""Immutable Merkle Blockchain Ledger & Zlib Delta State Compressor."""
from __future__ import annotations
import base64
import hashlib
import json
import time
import zlib
from pathlib import Path
from typing import Any, Dict, List


class MerkleBlockchainVault:
    def __init__(self, ledger_path: Path = Path("aaire_storage/aaire_backup/v7_merkle_chain.json")) -> None:
        self.ledger_path = ledger_path
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.chain: List[Dict[str, Any]] = self._load_chain()

    def _load_chain(self) -> List[Dict[str, Any]]:
        if self.ledger_path.exists():
            try:
                return json.loads(self.ledger_path.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    @staticmethod
    def compute_merkle_root(items: List[str]) -> str:
        if not items:
            return hashlib.sha256(b"EMPTY").hexdigest()
        layer = [hashlib.sha256(i.encode("utf-8")).hexdigest() for i in items]
        while len(layer) > 1:
            if len(layer) % 2 == 1:
                layer.append(layer[-1])
            next_layer = []
            for i in range(0, len(layer), 2):
                combined = (layer[i] + layer[i + 1]).encode("utf-8")
                next_layer.append(hashlib.sha256(combined).hexdigest())
            layer = next_layer
        return layer[0]

    @staticmethod
    def compress_state(state_obj: Dict[str, Any]) -> str:
        raw = json.dumps(state_obj, sort_keys=True).encode("utf-8")
        compressed = zlib.compress(raw, level=9)
        return base64.b85encode(compressed).decode("ascii")

    @staticmethod
    def decompress_state(payload_b85: str) -> Dict[str, Any]:
        compressed = base64.b85decode(payload_b85.encode("ascii"))
        return json.loads(zlib.decompress(compressed).decode("utf-8"))

    def append_block(self, state_data: Dict[str, Any], events: List[str]) -> Dict[str, Any]:
        prev_hash = self.chain[-1]["block_hash"] if self.chain else "0" * 64
        merkle_root = self.compute_merkle_root(events)
        compressed_payload = self.compress_state(state_data)
        index = len(self.chain)
        timestamp = round(time.time(), 3)

        block_header = f"{index}:{prev_hash}:{merkle_root}:{timestamp}:{compressed_payload}"
        block_hash = hashlib.sha256(block_header.encode("utf-8")).hexdigest()

        block = {
            "index": index,
            "timestamp": timestamp,
            "prev_hash": prev_hash,
            "merkle_root": merkle_root,
            "compressed_state": compressed_payload,
            "block_hash": block_hash
        }
        self.chain.append(block)
        self.ledger_path.write_text(json.dumps(self.chain, indent=2), encoding="utf-8")
        return block

    def verify_chain(self) -> bool:
        for i, blk in enumerate(self.chain):
            expected_prev = "0" * 64 if i == 0 else self.chain[i - 1]["block_hash"]
            if blk["prev_hash"] != expected_prev:
                return False
            header = f"{blk['index']}:{blk['prev_hash']}:{blk['merkle_root']}:{blk['timestamp']}:{blk['compressed_state']}"
            if hashlib.sha256(header.encode("utf-8")).hexdigest() != blk["block_hash"]:
                return False
        return True
      
