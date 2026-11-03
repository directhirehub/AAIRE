#!/usr/bin/env python3
"""AAIRE Commercial B2B API Gateway for RapidAPI / Cloudflare / Vercel Monetization."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, Tuple

from aaire_network.security_auth.zero_trust_guard import ZeroTrustGuard


class CommercialOracleGateway:
    FEED_FILE = Path("aaire_storage/verified_oracle_feed.json")

    @classmethod
    def serve_authenticated_feed(
        cls,
        client_id: str,
        provided_api_key: str,
        expected_master_key: str = "AAIRE_LIVE_PRO_KEY_2026",
        category_filter: str = "all"
    ) -> Tuple[int, Dict[str, Any]]:
        # 1. Token-Bucket Rate Limiting via ZeroTrustGuard
        if not ZeroTrustGuard.allow_request(client_id, rate_per_sec=2.0, capacity=5.0):
            return 429, {"error": "TOO_MANY_REQUESTS", "message": "Upgrade your RapidAPI tier for higher rate limits."}

        # 2. API Key Verification
        if provided_api_key != expected_master_key:
            return 401, {"error": "UNAUTHORIZED", "message": "Invalid or missing X-AAIRE-API-Key."}

        # 3. Load Live Cryptographically Verified Oracle Feed
        if not cls.FEED_FILE.exists():
            return 404, {"error": "FEED_NOT_GENERATED_YET"}

        data = json.loads(cls.FEED_FILE.read_text(encoding="utf-8"))

        if category_filter != "all":
            filtered = [f for f in data.get("feeds", []) if f.get("feed_category") == category_filter]
            data["feeds"] = filtered
            data["total_sources"] = len(filtered)

        return 200, data


if __name__ == "__main__":
    code, resp = CommercialOracleGateway.serve_authenticated_feed(
        client_id="enterprise_client_01",
        provided_api_key="AAIRE_LIVE_PRO_KEY_2026"
    )
    print(f"[Gateway Status: HTTP {code}]")
    print(f"Oracle Version: {resp.get('oracle_version')}")
    print(f"Total Verified Feeds Ready for Sale: {resp.get('total_sources')}")
  
