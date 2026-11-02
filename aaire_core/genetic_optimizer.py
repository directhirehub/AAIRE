#!/usr/bin/env python3
"""Genetic AST Code Profiler (CPU Nanoseconds + Memory Allocation) & Skill Evolver."""
from __future__ import annotations
import ast
import json
import time
import tracemalloc
from pathlib import Path
from typing import Any, Dict, List


class GeneticCodeOptimizer:
    BANNED = {"eval", "exec", "open", "__import__", "compile", "system", "popen"}

    def __init__(self, vault_file: Path = Path("aaire_storage/learned_patterns.json")) -> None:
        self.vault_file = vault_file
        self.vault_file.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _is_ast_safe(cls, code_str: str) -> bool:
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    return False
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in cls.BANNED:
                    return False
            return True
        except SyntaxError:
            return False

    def evolve_best_variant(
        self,
        task_name: str,
        fn_name: str,
        candidates: Dict[str, str],
        test_input: Any
    ) -> Dict[str, Any]:
        safe_builtins = {
            "sum": sum, "len": len, "range": range, "min": min, "max": max,
            "sorted": sorted, "list": list, "set": set, "dict": dict, "round": round
        }
        leaderboard: List[Dict[str, Any]] = []

        for variant_id, code in candidates.items():
            if not self._is_ast_safe(code):
                continue
            env: Dict[str, Any] = {"__builtins__": safe_builtins}
            try:
                exec(compile(code, f"<{variant_id}>", "exec"), env)
                fn = env[fn_name]

                tracemalloc.start()
                t0 = time.perf_counter_ns()
                output = fn(test_input)
                elapsed_ns = time.perf_counter_ns() - t0
                _, peak_bytes = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                fitness = round(1e9 / max(elapsed_ns + (peak_bytes * 10), 1), 4)
                leaderboard.append({
                    "variant": variant_id,
                    "elapsed_ns": elapsed_ns,
                    "peak_bytes": peak_bytes,
                    "fitness": fitness,
                    "output": output,
                    "code": code
                })
            except Exception:
                if tracemalloc.is_tracing():
                    tracemalloc.stop()

        if not leaderboard:
            return {"status": "NO_VALID_CANDIDATES"}

        leaderboard.sort(key=lambda x: x["fitness"], reverse=True)
        winner = leaderboard[0]
        self._save_winner(task_name, winner)
        return {
            "status": "OPTIMIZED",
            "winner_variant": winner["variant"],
            "elapsed_ns": winner["elapsed_ns"],
            "peak_bytes": winner["peak_bytes"],
            "fitness": winner["fitness"],
            "output": winner["output"],
            "total_tested": len(leaderboard)
        }

    def _save_winner(self, task_name: str, winner: Dict[str, Any]) -> None:
        data: Dict[str, Any] = {}
        if self.vault_file.exists():
            try:
                data = json.loads(self.vault_file.read_text(encoding="utf-8"))
            except Exception:
                data = {}
        data.setdefault("v7_genetic_champions", {})[task_name] = {
            "variant": winner["variant"],
            "elapsed_ns": winner["elapsed_ns"],
            "fitness": winner["fitness"],
            "code": winner["code"]
        }
        self.vault_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
              
