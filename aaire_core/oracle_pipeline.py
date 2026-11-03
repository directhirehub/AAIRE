#!/usr/bin/env python3
"""AAIRE Commercial B2B Zero-Rot Verified Data Oracle Pipeline."""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Union

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

    def generate_verified_feed(
        self,
        sources: Union[Dict[str, str], List[str]],
        api_secret: str = "AAIRE_ORACLE_COMMERCIAL_KEY"
    ) -> Dict[str, Any]:
        if isinstance(sources, list):
            sources = {f"source_{i+1}": url for i, url in enumerate(sources)}

        verified_records: List[Dict[str, Any]] = []
        merkle_events: List[str] = []

        for category, url in sources.items():
            raw = self.extractor.extract_resilient_data(url)
            # Safe .get() use taaki kabhi KeyError na aaye
            item_count = raw.get("item_count", 0) if isinstance(raw, dict) else 0
            has_items = item_count > 0
            
            trust_score = self.reasoner.update_bayesian_belief(
                hypothesis=category,
                likelihood_given_true=0.96 if has_items else 0.20
            )

            record = {
                "feed_category": category,
                "source_url": url,
                "status": raw.get("status", "UNKNOWN") if isinstance(raw, dict) else "ERROR",
                "self_healed_strategy": raw.get("winning_strategy", "fallback") if isinstance(raw, dict) else "fallback",
                "extraction_latency_ns": raw.get("latency_ns", 0) if isinstance(raw, dict) else 0,
                "bayesian_trust_score": trust_score,
                "item_count": item_count,
                "verified_payload": raw.get("items", []) if isinstance(raw, dict) else []
            }
            verified_records.append(record)
            merkle_events.append(f"{category}:{url}:{item_count}:{trust_score}")

        block = self.blockchain.append_block(
            state_data={"sources_processed": len(sources), "timestamp": time.time()},
            events=merkle_events
        )

        canonical_payload = json.dumps(verified_records, sort_keys=True)
        hmac_signature = ZeroTrustGuard.sign_payload(canonical_payload, api_secret)

        oracle_package = {
            "oracle_version": "AAIRE-v7.0-ZeroRot-Enterprise",
            "generated_at_utc": round(time.time(), 3),
            "monetization_ready": True,
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
    live_commercial_sources = {
        "global_tech_intelligence": "https://news.ycombinator.com/",
        "remote_hiring_signals": "https://remoteok.com/",
        "python_ecosystem_updates": "https://pypi.org/"
    }
    pkg = oracle.generate_verified_feed(live_commercial_sources)
    print("=== AAIRE COMMERCIAL B2B ORACLE FEED GENERATED ===")
    print(f"Total Categories Indexed: {pkg['total_sources']}")
    print(f"Merkle Proof Root: {pkg['cryptographic_proof']['merkle_root']}")
    print(f"Saved to: {ZeroRotOraclePipeline.FEED_PATH}")
    
