#!/usr/bin/env python3
"""AAIRE Zero-Rot Self-Healing DOM & Data Extractor."""
from __future__ import annotations
import re
from typing import Dict, Any, List

from aaire_core.genetic_optimizer import GeneticCodeOptimizer
from aaire_network.protocols.smart_client import SmartHTTPSClient


class AutoHealerExtractor:
    def __init__(self) -> None:
        self.optimizer = GeneticCodeOptimizer()

    def extract_resilient_data(self, url: str) -> Dict[str, Any]:
        ok, html = SmartHTTPSClient.fetch_resilient(url, retries=2, use_cache=True)
        if not ok or not html:
            return {"status": "FETCH_FAILED", "url": url, "items": []}

        # Pre-extract raw anchor/heading/json tokens safely outside sandbox
        raw_links = re.findall(r'href=[\"\'](https?://[^\"\']+)[\"\']', html)
        raw_headings = [re.sub(r"<[^>]+>", "", m).strip() for m in re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html, re.I | re.S)]
        raw_words = re.findall(r"[A-Za-z0-9_/-]{4,}", html)

        bundle = {
            "links": raw_links[:50],
            "headings": [h for h in raw_headings if h][:30],
            "tokens": raw_words[:100]
        }

        # Candidate extraction strategies evolved via Genetic AST Profiler
        candidates = {
            "strategy_links_priority": (
                "def parse_dom(data):\n"
                "    items = data['links'] if len(data['links']) > 0 else data['headings']\n"
                "    return sorted(list(set(items)))[:25]"
            ),
            "strategy_hybrid_merge": (
                "def parse_dom(data):\n"
                "    combined = data['headings'] + data['links']\n"
                "    clean = [x for x in combined if len(x) > 3]\n"
                "    return list(dict.fromkeys(clean))[:25]"
            ),
            "strategy_deep_token_fallback": (
                "def parse_dom(data):\n"
                "    base = data['links'] + data['headings'] + data['tokens'][:20]\n"
                "    return sorted(list(set(base)))[:25]"
            )
        }

        evo_report = self.optimizer.evolve_best_variant(
            task_name="zero_rot_dom_extractor",
            fn_name="parse_dom",
            candidates=candidates,
            test_input=bundle
        )

        extracted = evo_report.get("output", []) if evo_report.get("status") == "OPTIMIZED" else bundle["links"][:15]
        return {
            "status": "HEALED_AND_EXTRACTED",
            "url": url,
            "winning_strategy": evo_report.get("winner_variant", "fallback"),
            "latency_ns": evo_report.get("elapsed_ns", 0),
            "item_count": len(extracted),
            "items": extracted
      }
      
