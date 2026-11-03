#!/usr/bin/env python3
"""AAIRE Commercial B2B Zero-Rot Verified Data Oracle Pipeline."""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, Any, List

from aaire_core.mcts_reasoner import MCTSReasoner
from aaire_network.web_scraping.auto_healer_extractor import AutoHealerExtractor
from aaire_network.security_auth.zero_trust_guard import ZeroTrustGuard
from aaire_storage.merkle_blockchain import MerkleBlockchainVault


class ZeroRotOraclePipeline:
    FEED_PATH = Path("aaire_storage/verified_oracle_feed.json")

    def __init__(self) -> None:
        self.extractor = AutoHealerExtractor()
        self.reasoner = MCTSReasoner()
        self.blockchain = MerkleBlockchainVault()

    def generate_verified_feed(self, sources: List[str], api_secret: str = "AAIRE_ORACLE_COMMERCIAL_KEY") -> Dict[str, Any]:
        verified_records: List[Dict[str, Any]] = []
        merkle_events: List[str] = []

        for url in sources:
            raw = self.extractor.extract_resilient_data(url)
            has_items = raw["item_count"] > 0
            trust_score = self.reasoner.update_bayesian_belief(
                hypothesis=url,
                likelihood_given_true=0.95 if has_items else 0.20
            )

            record = {
                "source_url": url,
                "status": raw["status"],
                "self_healed_strategy": raw["winning_strategy"],
                "extraction_latency_ns": raw["latency_ns"],
                "bayesian_trust_score": trust_score,
                "item_count": raw["item_count"],
                "verified_payload": raw["items"]
            }
            verified_records.append(record)
            merkle_events.append(f"{url}:{raw['item_count']}:{trust_score}")

        # Seal inside Zlib Merkle Blockchain for Proof-of-Freshness
        block = self.blockchain.append_block(
            state_data={"sources_processed": len(sources), "timestamp": time.time()},
            events=merkle_events
        )

        # Sign commercial payload via ZeroTrust HMAC-SHA256
        canonical_payload = json.dumps(verified_records, sort_keys=True)
        hmac_signature = ZeroTrustGuard.sign_payload(canonical_payload, api_secret)

        oracle_package = {
            "oracle_version": "AAIRE-v7.0-ZeroRot-Enterprise",
            "generated_at_utc": round(time.time(), 3),
            "cryptographic_proof": {
                "merkle_block_index": block["index"],
                "merkle_root": block["merkle_root"],
                "block_hash": block["block_hash"],
                "hmac_sha256_signature": hmac_signature
            },
            "total_sources": len(verified_records),
            "feeds": verified_records
        }

        self.FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.FEED_PATH.write_text(json.dumps(oracle_package, indent=2), encoding="utf-8")
        return oracle_package


if __name__ == "__main__":
    oracle = ZeroRotOraclePipeline()
    default_sources = [
        "https://httpbin.org/html",
        "https://httpbin.org/links/5/0"
    ]
    pkg = oracle.generate_verified_feed(default_sources)
    print("=== AAIRE ZERO-ROT ORACLE FEED GENERATED ===")
    print(f"Merkle Root: {pkg['cryptographic_proof']['merkle_root']}")
    print(f"HMAC Signature: {pkg['cryptographic_proof']['hmac_sha256_signature'][:24]}...")
    print(f"Saved to: {ZeroRotOraclePipeline.FEED_PATH}")
      
