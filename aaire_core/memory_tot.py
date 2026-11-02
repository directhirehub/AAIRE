#!/usr/bin/env python3
"""Part 7: Semantic Episodic Memory & Tree-of-Thoughts (ToT) Planner."""
from __future__ import annotations
import json
import math
import re
import threading
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from config import utc_now

class EpisodicMemory:
    """Pure-stdlib TF-Lite cosine similarity memory stored in aaire_memory/."""
    def __init__(self, memory_file: Path) -> None:
        self.memory_file = memory_file
        self._lock = threading.Lock()

    @staticmethod
    def _tokenize(text: str) -> Counter:
        return Counter(re.findall(r"[a-z0-9_]+", text.lower()))

    @classmethod
    def _cosine_sim(cls, a: str, b: str) -> float:
        ca, cb = cls._tokenize(a), cls._tokenize(b)
        if not ca or not cb:
            return 0.0
        common = set(ca.keys()) & set(cb.keys())
        num = sum(ca[w] * cb[w] for w in common)
        den = math.sqrt(sum(v * v for v in ca.values())) * math.sqrt(sum(v * v for v in cb.values()))
        return round(num / den, 4) if den else 0.0

    def recall_best(self, goal: str) -> Optional[Dict[str, Any]]:
        if not self.memory_file.exists():
            return None
        try:
            episodes = json.loads(self.memory_file.read_text(encoding="utf-8"))
            if not isinstance(episodes, list) or not episodes:
                return None
            scored = [(self._cosine_sim(goal, ep.get("goal", "")), ep) for ep in episodes]
            scored.sort(key=lambda x: x[0], reverse=True)
            best_score, best_ep = scored[0]
            if best_score >= 0.25:
                return {"similarity": best_score, "episode": best_ep}
        except Exception:
            return None
        return None

    def store_episode(self, goal: str, summary: Dict[str, Any], atomic_writer: Callable[[Path, Any], str]) -> None:
        with self._lock:
            episodes: List[Dict[str, Any]] = []
            if self.memory_file.exists():
                try:
                    loaded = json.loads(self.memory_file.read_text(encoding="utf-8"))
                    if isinstance(loaded, list):
                        episodes = loaded
                except Exception:
                    episodes = []
            episodes.append({
                "goal": goal,
                "timestamp": utc_now(),
                "total_duration_ms": summary.get("total_duration_ms", 0.0),
                "consensus_passed": summary.get("consensus_passed", True)
            })
            atomic_writer(self.memory_file, episodes[-100:])

class TreeOfThoughtsPlanner:
    """Evaluates candidate execution branches and selects the optimal strategy."""
    @staticmethod
    def select_optimal_strategy(goal: str, recalled_memory: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        candidates = [
            {"strategy": "Zero-Trust Defensive Synthesis", "safety_weight": 0.98, "speed_weight": 0.85},
            {"strategy": "High-Throughput Parallel Synthesis", "safety_weight": 0.88, "speed_weight": 0.96},
            {"strategy": "Heuristic Memory-Guided Synthesis", "safety_weight": 0.95, "speed_weight": 0.94},
        ]
        boost = 0.08 if recalled_memory else 0.0
        best = max(
            candidates,
            key=lambda c: round(
                (c["safety_weight"] * 0.65)
                + (c["speed_weight"] * 0.35)
                + (boost if "Memory" in c["strategy"] else 0.0),
                4
            )
        )
        return {
            "selected_strategy": best["strategy"],
            "memory_hit": recalled_memory is not None,
            "goal": goal
          }
      
