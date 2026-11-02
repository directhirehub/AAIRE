#!/usr/bin/env python3
"""Part 8: Atomic Storage, Cryptographic Merkle State Ledger & DLQ Autopsy."""
from __future__ import annotations
import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from config import Config, utc_now
from models import Task

class StorageManager:
    """Manages aaire_storage hierarchy, atomic writes, Merkle chain, and DLQ."""
    def __init__(self, config: Config) -> None:
        self.config = config
        self.storage_root = config.base_dir / config.storage_dirname
        self.memory_dir = self.storage_root / "aaire_memory"
        self.backup_dir = self.storage_root / "aaire_backup"
        self.training_dir = self.storage_root / "aaire_training"

        for folder in (self.storage_root, self.memory_dir, self.backup_dir, self.training_dir):
            folder.mkdir(parents=True, exist_ok=True)

        self.learned_patterns_file = self.storage_root / "learned_patterns.json"
        self.merkle_ledger_file = self.backup_dir / "merkle_ledger.json"
        self.dlq_autopsy_file = self.training_dir / "dlq_autopsy.json"

        if not self.learned_patterns_file.exists():
            self.atomic_write_json(self.learned_patterns_file, {})

    @staticmethod
    def atomic_write_json(target_path: Path, data: Any) -> str:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(data, indent=2, ensure_ascii=False)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        tmp_fd, tmp_path = tempfile.mkstemp(dir=target_path.parent, text=True)
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, target_path)
            return digest
        except Exception as e:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise RuntimeError(f"Atomic write failed for {target_path}: {e}") from e

    def append_merkle_state(self, state_summary: Dict[str, Any], version_tag: str) -> str:
        snapshot_file = self.backup_dir / f"state_snapshot_{version_tag}.json"
        checksum_file = self.backup_dir / f"state_snapshot_{version_tag}.json.sha256"

        snapshot_hash = self.atomic_write_json(snapshot_file, state_summary)
        checksum_file.write_text(snapshot_hash, encoding="utf-8")
        self.atomic_write_json(self.backup_dir / "latest_state_snapshot.json", state_summary)

        ledger: List[Dict[str, Any]] = []
        if self.merkle_ledger_file.exists():
            try:
                loaded = json.loads(self.merkle_ledger_file.read_text(encoding="utf-8"))
                if isinstance(loaded, list):
                    ledger = loaded
            except Exception:
                ledger = []

        prev_root = ledger[-1]["merkle_root"] if ledger else ("0" * 64)
        combined = f"{prev_root}:{snapshot_hash}:{version_tag}"
        merkle_root = hashlib.sha256(combined.encode("utf-8")).hexdigest()

        ledger.append({
            "index": len(ledger),
            "version_tag": version_tag,
            "timestamp": utc_now(),
            "snapshot_file": snapshot_file.name,
            "snapshot_sha256": snapshot_hash,
            "prev_merkle_root": prev_root,
            "merkle_root": merkle_root
        })
        self.atomic_write_json(self.merkle_ledger_file, ledger)
        return merkle_root

    def verify_merkle_ledger(self) -> Tuple[bool, str]:
        if not self.merkle_ledger_file.exists():
            return True, "Merkle ledger clean (genesis state)."
        try:
            ledger = json.loads(self.merkle_ledger_file.read_text(encoding="utf-8"))
            if not isinstance(ledger, list):
                return False, "Merkle ledger format corrupted."
            prev_root = "0" * 64
            for block in ledger:
                expected = f"{prev_root}:{block['snapshot_sha256']}:{block['version_tag']}"
                recomputed = hashlib.sha256(expected.encode("utf-8")).hexdigest()
                if recomputed != block.get("merkle_root"):
                    return False, f"Tamper detected at Block #{block.get('index')}!"
                prev_root = recomputed
            return True, f"Merkle chain verified intact ({len(ledger)} blocks)."
        except Exception as e:
            return False, f"Merkle verification error: {e}"

    def rollback_to_last_valid_state(self) -> Optional[Dict[str, Any]]:
        latest_path = self.backup_dir / "latest_state_snapshot.json"
        if latest_path.exists():
            try:
                return json.loads(latest_path.read_text(encoding="utf-8"))
            except Exception:
                return None
        return None

    def update_learned_patterns(self, task: Task) -> None:
        try:
            patterns = json.loads(self.learned_patterns_file.read_text(encoding="utf-8"))
            if not isinstance(patterns, dict):
                patterns = {}
        except Exception:
            patterns = {}

        entry = patterns.get(task.name, {"runs": 0, "successes": 0, "avg_duration_ms": 0.0})
        runs = entry.get("runs", 0) + 1
        successes = entry.get("successes", 0) + (1 if task.status == "SUCCESS" else 0)
        prev_avg = entry.get("avg_duration_ms", 0.0)
        new_avg = round(((prev_avg * (runs - 1)) + task.duration_ms) / runs, 2)

        patterns[task.name] = {
            "agent_type": task.agent_type,
            "runs": runs,
            "successes": successes,
            "success_rate": round(successes / runs, 4),
            "avg_duration_ms": new_avg,
            "last_status": task.status,
            "last_updated": utc_now()
        }
        self.atomic_write_json(self.learned_patterns_file, patterns)

    def dump_to_dlq_autopsy(self, task: Task, blackboard_snap: Dict[str, Any], trace_str: str) -> None:
        records: List[Dict[str, Any]] = []
        if self.dlq_autopsy_file.exists():
            try:
                loaded = json.loads(self.dlq_autopsy_file.read_text(encoding="utf-8"))
                if isinstance(loaded, list):
                    records = loaded
            except Exception:
                records = []

        records.append({
            "autopsy_id": str(uuid.uuid4())[:12],
            "timestamp": utc_now(),
            "task": asdict(task),
            "blackboard_state": blackboard_snap,
            "forensic_traceback": trace_str
        })
        self.atomic_write_json(self.dlq_autopsy_file, records)
      
