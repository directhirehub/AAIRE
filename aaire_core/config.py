#!/usr/bin/env python3
"""Part 1: AAIRE v4.1 Configuration, Constants & Zero-Trust Forbidden Rules."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Set

VERSION = "4.1.0-OmegaGrid"

FORBIDDEN_CALLS: Set[str] = {
    "eval", "exec", "compile", "__import__", "os.system", "os.popen",
    "subprocess.Popen", "subprocess.run", "subprocess.call", "subprocess.check_output",
    "shutil.rmtree", "os.remove", "os.unlink", "os.rmdir"
}

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Config:
    base_dir: Path = field(default_factory=Path.cwd)
    storage_dirname: str = "aaire_storage"
    log_name: str = "aaire_execution.log"
    min_workers: int = 2
    max_workers: int = 8
    max_retries: int = 30
    backoff_base_s: float = 0.05
    backoff_cap_s: float = 1.5
    circuit_failure_threshold: int = 5
    circuit_recovery_s: float = 1.0
    consensus_quorum: float = 0.70
    max_ast_complexity: int = 25
  
