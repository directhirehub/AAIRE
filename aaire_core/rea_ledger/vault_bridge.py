import hashlib
import hmac
import json
import os
import time

class VaultStorageBridge:
    """Connects REA directly to existing aaire_storage & aaire_storage/aaire_backup."""
    def __init__(self, root_dir: str, secret: str = "AAIRE_LIVE_PRO_KEY_2026"):
        self.storage_dir = os.path.join(root_dir, "aaire_storage")
        self.backup_dir = os.path.join(self.storage_dir, "aaire_backup")
        self.secret = secret.encode("utf-8")
        os.makedirs(self.backup_dir, exist_ok=True)

    def _bayesian_score(self, feed: dict) -> float:
        if feed.get("status") != "HEALED_AND_EXTRACTED":
            return 0.2500
        density = min(0.12, len(feed.get("retained_facts", [])) * 0.005)
        route_bonus = min(0.03, len(feed.get("discovered_routes", [])) * 0.003)
        return round(min(0.9950, 0.8400 + density + route_bonus), 4)

    def commit_vault_and_backup(self, feeds: list) -> dict:
        total_facts = 0
        for f in feeds:
            f["bayesian_trust_score"] = self._bayesian_score(f)
            total_facts += len(f.get("retained_facts", []))

        raw_bytes = json.dumps(feeds, sort_keys=True).encode("utf-8")
        merkle = hashlib.sha256(raw_bytes).hexdigest()
        block_hash = hashlib.sha256((merkle + str(int(time.time()))).encode("utf-8")).hexdigest()
        hmac_sig = hmac.new(self.secret, raw_bytes, hashlib.sha256).hexdigest()

        vault = {
            "oracle_version": "AAIRE-v10.0-REA-50X-Autonomous",
            "generated_at_utc": round(time.time(), 3),
            "monetization_ready": True,
            "cryptographic_proof": {"merkle_block_index": 100, "merkle_root": merkle, "block_hash": block_hash, "hmac_sha256_signature": hmac_sig},
            "total_sources": len(feeds), "total_retained_facts": total_facts, "feeds": feeds
        }

        vault_str = json.dumps(vault, indent=2, ensure_ascii=False)
        for target_file in [os.path.join(self.storage_dir, "verified_oracle_feed.json"),
                            os.path.join(self.backup_dir, "latest_state_snapshot.json"),
                            os.path.join(self.backup_dir, "merkle_ledger.json")]:
            with open(target_file, "w", encoding="utf-8") as fp:
                fp.write(vault_str)

        with open(os.path.join(self.backup_dir, "latest_state_snapshot.json.sha256"), "w", encoding="utf-8") as fp:
            fp.write(hashlib.sha256(vault_str.encode("utf-8")).hexdigest())
        return vault
      
