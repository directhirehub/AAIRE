#!/usr/bin/env python3
"""Part 2: AAIRE v4.1 Task State Machine & Data Models."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from config import utc_now

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    goal: str = ""
    agent_type: str = "General-Agent"
    dependencies: List[str] = field(default_factory=list)
    complexity: int = 1
    status: str = "PENDING"
    attempts: int = 0
    max_retries: int = 30
    generated_code: Optional[str] = None
    ast_verified: bool = False
    ast_complexity_score: int = 0
    self_corrected: bool = False
    consensus_score: float = 0.0
    result: Optional[str] = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    created_at: str = field(default_factory=utc_now)
  
