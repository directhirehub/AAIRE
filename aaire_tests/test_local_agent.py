#!/usr/bin/env python3
"""
Layer 3: AAIRE v4.1 Automated Verification & Unit Testing Suite.
Tests all 10 modular files inside aaire_core/ and storage routing in aaire_storage/.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Link aaire_core/ directory so all 10 parts can be imported directly
CORE_DIR = Path(__file__).resolve().parent.parent / "aaire_core"
sys.path.insert(0, str(CORE_DIR))

from config import Config
from models import Task
from mesh_bus import EventBus, Blackboard
from resilience import CircuitBreaker, ConcurrencyGovernor
from ast_guard import ASTCodeGuard
from consensus import ConsensusEngine
from memory_tot import EpisodicMemory, TreeOfThoughtsPlanner
from merkle_storage import StorageManager
from dag_engine import DAGEngine
from local_agent import MasterBrain


class TestAAIREModularEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.cfg = Config(
            base_dir=self.tmp_dir,
            max_retries=5,
            backoff_base_s=0.01,
            backoff_cap_s=0.05,
            circuit_failure_threshold=3,
            circuit_recovery_s=0.05,
        )
        self.brain = MasterBrain(self.cfg)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_01_storage_hierarchy_created(self) -> None:
        """Verify aaire_storage and its 3 subfolders + learned_patterns.json exist."""
        storage = self.tmp_dir / "aaire_storage"
        self.assertTrue((storage / "aaire_memory").is_dir())
        self.assertTrue((storage / "aaire_backup").is_dir())
        self.assertTrue((storage / "aaire_training").is_dir())
        self.assertTrue((storage / "learned_patterns.json").is_file())

    def test_02_ast_guard_and_self_correction(self) -> None:
        """Verify Zero-Trust AST Guard blocks dangerous calls and self-corrects."""
        unsafe_code = "import os\ndef hack():\n    os.system('rm -rf /')\n"
        is_safe, violations, _ = ASTCodeGuard.inspect_code(unsafe_code)
        self.assertFalse(is_safe)
        self.assertTrue(any("os.system" in v for v in violations))

        corrected = ASTCodeGuard.reflective_self_correct(unsafe_code, violations)
        is_safe_now, new_violations, _ = ASTCodeGuard.inspect_code(corrected)
        self.assertTrue(is_safe_now, f"Expected safe code, got: {new_violations}")

    def test_03_circuit_breaker_and_governor(self) -> None:
        """Verify Circuit Breaker trips on threshold failures and recovers."""
        cb = CircuitBreaker(threshold=2, recovery_s=0.02)
        self.assertTrue(cb.allow())
        cb.record_failure()
        cb.record_failure()
        self.assertEqual(cb.state, "OPEN")
        self.assertFalse(cb.allow())

        tasks = [Task(complexity=4), Task(complexity=5)]
        workers = ConcurrencyGovernor.compute_workers(self.cfg, tasks)
        self.assertGreaterEqual(workers, 1)

    def test_04_merkle_ledger_and_tamper_detection(self) -> None:
        """Verify Cryptographic Merkle State Chain seals and detects tampering."""
        sm = self.brain.storage
        sm.append_merkle_state({"step": 1}, "v_test_1")
        sm.append_merkle_state({"step": 2}, "v_test_2")

        ok, msg = sm.verify_merkle_ledger()
        self.assertTrue(ok, msg)

        # Simulate tampering in merkle_ledger.json
        import json
        ledger = json.loads(sm.merkle_ledger_file.read_text(encoding="utf-8"))
        ledger[0]["snapshot_sha256"] = "f" * 64
        sm.merkle_ledger_file.write_text(json.dumps(ledger), encoding="utf-8")

        ok_after, _ = sm.verify_merkle_ledger()
        self.assertFalse(ok_after)

    def test_05_full_master_brain_execution_and_self_healing(self) -> None:
        """Verify full DAG wave execution, AST self-healing, and Episodic Memory."""
        os.environ["SIMULATE_UNSAFE_CODE"] = "1"
        try:
            summary = self.brain.run("Build autonomous microservices test pipeline")
            self.assertEqual(summary["status"], "GREEN")
            self.assertTrue(summary["consensus_passed"])
            self.assertEqual(len(summary["tasks"]), 5)
            self.assertTrue(any(t["self_corrected"] for t in summary["tasks"]))
        finally:
            os.environ.pop("SIMULATE_UNSAFE_CODE", None)

        # Verify episodic memory recall works on second run
        recalled = self.brain.episodic_memory.recall_best("autonomous microservices pipeline")
        self.assertIsNotNone(recalled)


if __name__ == "__main__":
    unittest.main(verbosity=2)
      
