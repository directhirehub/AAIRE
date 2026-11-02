#!/usr/bin/env python3
"""AAIRE Storage Optimizer: SHA-256 Self-Healer, Auto-Rotation & Cold Compression."""
from __future__ import annotations
import hashlib
import shutil
import tarfile
from pathlib import Path
from typing import Dict, Any, List, Tuple


class SnapshotManager:
    def __init__(self, backup_dir: Path = Path("aaire_storage/aaire_backup"), keep_latest: int = 5) -> None:
        self.backup_dir = backup_dir
        self.keep_latest = keep_latest
        self.archive_path = self.backup_dir / "cold_snapshots_archive.tar.gz"
        self.latest_file = self.backup_dir / "latest_state_snapshot.json"

    @staticmethod
    def _sha256(file_path: Path) -> str:
        return hashlib.sha256(file_path.read_bytes()).hexdigest()

    def verify_integrity(self, json_file: Path) -> bool:
        sha_file = Path(f"{json_file}.sha256")
        if not json_file.exists() or not sha_file.exists():
            return False
        expected_hash = sha_file.read_text(encoding="utf-8").strip().split()[0]
        return self._sha256(json_file) == expected_hash

    def heal_and_compact(self) -> Dict[str, Any]:
        if not self.backup_dir.exists():
            return {"status": "NO_BACKUP_DIR", "kept": 0, "archived": 0}

        snapshots: List[Path] = sorted(
            self.backup_dir.glob("state_snapshot_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        valid: List[Path] = []
        corrupted = 0
        for snap in snapshots:
            if self.verify_integrity(snap):
                valid.append(snap)
            else:
                snap.unlink(missing_ok=True)
                Path(f"{snap}.sha256").unlink(missing_ok=True)
                corrupted += 1

        healed = False
        if valid:
            best = valid[0]
            if not self.latest_file.exists() or self._sha256(self.latest_file) != self._sha256(best):
                shutil.copy2(best, self.latest_file)
                healed = True

        to_keep = valid[:self.keep_latest]
        to_archive = valid[self.keep_latest:]
        archived_count = 0

        if to_archive:
            mode = "a:gz" if self.archive_path.exists() else "w:gz"
            with tarfile.open(self.archive_path, mode) as tar:
                for snap in to_archive:
                    sha_companion = Path(f"{snap}.sha256")
                    tar.add(snap, arcname=snap.name)
                    snap.unlink(missing_ok=True)
                    if sha_companion.exists():
                        tar.add(sha_companion, arcname=sha_companion.name)
                        sha_companion.unlink(missing_ok=True)
                    archived_count += 1

        return {
            "status": "HEALTHY",
            "kept": len(to_keep),
            "archived": archived_count,
            "corrupted_purged": corrupted,
            "latest_healed": healed
              }
      
