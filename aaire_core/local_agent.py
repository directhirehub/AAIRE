#!/usr/bin/env python3
"""Part 10: AAIRE v4.1 Master Brain Orchestrator & CLI Entrypoint."""
from __future__ import annotations
import argparse
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, List

# Ensure sibling modules inside aaire_core/ are always importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import Config, VERSION, utc_now
from mesh_bus import EventBus, Blackboard
from resilience import CircuitBreaker, ConcurrencyGovernor
from memory_tot import EpisodicMemory, TreeOfThoughtsPlanner
from merkle_storage import StorageManager
from dag_engine import DAGEngine

class MasterBrain:
    """Central Orchestrator integrating all 10 modular subsystems."""
    def __init__(self, config: Config) -> None:
        self.config = config
        self.event_bus = EventBus()
        self.blackboard = Blackboard()
        self.circuit_breaker = CircuitBreaker(
            threshold=config.circuit_failure_threshold,
            recovery_s=config.circuit_recovery_s
        )
        self.storage = StorageManager(config)
        self._setup_logger()
        self.episodic_memory = EpisodicMemory(self.storage.memory_dir / "episodic_memory.json")
        self.dag_engine = DAGEngine(
            config=self.config,
            event_bus=self.event_bus,
            blackboard=self.blackboard,
            circuit_breaker=self.circuit_breaker,
            storage=self.storage,
            log_fn=self.log
        )
        self._register_events()

    def _setup_logger(self) -> None:
        log_path = self.config.base_dir / self.config.log_name
        self.logger = logging.getLogger("AAIRE-OmegaGrid")
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(log_path, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def _register_events(self) -> None:
        self.event_bus.subscribe("TASK_SUCCESS", lambda t: self.log("INFO", f"[MeshBus] {t.name} ({t.id}) -> SUCCESS"))
        self.event_bus.subscribe("TASK_RETRY", lambda t: self.log("WARNING", f"[MeshBus] {t.name} retry #{t.attempts}"))
        self.event_bus.subscribe("TASK_DLQ", lambda t: self.log("ERROR", f"[MeshBus] {t.name} routed to DLQ Autopsy"))

    def log(self, level: str, message: str) -> None:
        print(f"[{level}] {message}")
        lvl = level.upper()
        if lvl == "INFO":
            self.logger.info(message)
        elif lvl == "WARNING":
            self.logger.warning(message)
        elif lvl == "ERROR":
            self.logger.error(message)
        else:
            self.logger.debug(message)

    def run_self_diagnostics(self) -> bool:
        self.log("INFO", "Running Pre-Flight Self-Diagnostic Health Check...")
        ok, msg = self.storage.verify_merkle_ledger()
        if not ok:
            self.log("ERROR", f"Ledger Integrity Failure: {msg}")
            self.storage.rollback_to_last_valid_state()
            return False
        self.log("INFO", f"Health Check PASSED: {msg}")
        return True

    def run(self, primary_goal: str) -> Dict[str, Any]:
        cycle_start = time.perf_counter()
        self.log("INFO", f"=== AAIRE v{VERSION} MODULAR ENGINE ACTIVATED ===")

        if not self.run_self_diagnostics():
            raise RuntimeError("Pre-flight diagnostics failed; aborting run to protect state ledger.")

        recalled = self.episodic_memory.recall_best(primary_goal)
        tot_plan = TreeOfThoughtsPlanner.select_optimal_strategy(primary_goal, recalled)
        self.blackboard.write("tot_strategy", tot_plan)
        self.log("INFO", f"ToT Strategy: {tot_plan['selected_strategy']} (Memory Hit: {tot_plan['memory_hit']})")

        all_tasks = self.dag_engine.build_dag_tasks(primary_goal)
        waves = self.dag_engine.resolve_dag_waves(all_tasks)
        self.log("INFO", f"Resolved {len(all_tasks)} tasks into {len(waves)} topological waves.")

        completed_tasks: List[Dict[str, Any]] = []
        pipeline_aborted = False

        for wave_idx, wave in enumerate(waves, start=1):
            workers = ConcurrencyGovernor.compute_workers(self.config, wave)
            self.log("INFO", f"--- Wave {wave_idx}/{len(waves)} ({len(wave)} tasks | Workers: {workers}) ---")

            with ThreadPoolExecutor(max_workers=workers) as pool:
                future_map = {pool.submit(self.dag_engine.execute_task, t): t for t in wave}
                for future in as_completed(future_map):
                    finished = future.result()
                    completed_tasks.append(asdict(finished))
                    if finished.status != "SUCCESS":
                        pipeline_aborted = True

            if pipeline_aborted:
                self.log("ERROR", f"Wave {wave_idx} failed. Triggering Automated State Rollback...")
                self.storage.rollback_to_last_valid_state()
                break

        total_duration_ms = round((time.perf_counter() - cycle_start) * 1000, 2)
        version_tag = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

        state_summary = {
            "version": VERSION,
            "version_tag": version_tag,
            "timestamp": utc_now(),
            "primary_goal": primary_goal,
            "tot_plan": tot_plan,
            "status": "DEGRADED_ROLLED_BACK" if pipeline_aborted else "GREEN",
            "total_duration_ms": total_duration_ms,
            "consensus_passed": not pipeline_aborted,
            "tasks": completed_tasks
        }

        merkle_root = self.storage.append_merkle_state(state_summary, version_tag)
        state_summary["merkle_root"] = merkle_root
        self.episodic_memory.store_episode(primary_goal, state_summary, self.storage.atomic_write_json)

        self.log("INFO", f"=== CYCLE FINISHED [{state_summary['status']}] in {total_duration_ms}ms ===")
        return state_summary

def main() -> int:
    parser = argparse.ArgumentParser(description="AAIRE v4.1 Modular Autonomous Engine")
    parser.add_argument("--goal", type=str, default="Build and verify autonomous local reasoning microservice")
    parser.add_argument("--max-retries", type=int, default=30)
    parser.add_argument("--verify-ledger", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()

    cfg = Config(max_retries=args.max_retries)
    brain = MasterBrain(cfg)

    if args.verify_ledger:
        ok, msg = brain.storage.verify_merkle_ledger()
        print(f"Merkle Verification: {msg}")
        return 0 if ok else 1

    if args.rollback:
        restored = brain.storage.rollback_to_last_valid_state()
        return 0 if restored is not None else 1

    brain.run(args.goal)
    return 0

if __name__ == "__main__":
    sys.exit(main())
      
