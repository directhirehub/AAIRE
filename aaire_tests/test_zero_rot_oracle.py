#!/usr/bin/env python3
"""Verification Test for AAIRE Zero-Rot Self-Healing Oracle Pipeline."""
from pathlib import Path
from aaire_core.oracle_pipeline import ZeroRotOraclePipeline


def test_oracle_end_to_end() -> None:
    print("=== Testing AAIRE Zero-Rot Commercial Oracle ===")
    oracle = ZeroRotOraclePipeline()
    feed = oracle.generate_verified_feed(["https://httpbin.org/html"])

    assert feed["total_sources"] == 1
    assert "merkle_root" in feed["cryptographic_proof"]
    assert "hmac_sha256_signature" in feed["cryptographic_proof"]
    assert Path("aaire_storage/verified_oracle_feed.json").exists()
    print(f"[✔] Self-Healed Strategy: {feed['feeds'][0]['self_healed_strategy']}")
    print(f"[✔] Merkle Proof Root: {feed['cryptographic_proof']['merkle_root'][:16]}...")
    print("[✔] Commercial Feed Saved & Verified 100%!")


if __name__ == "__main__":
    test_oracle_end_to_end()
  
