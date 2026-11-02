#!/usr/bin/env python3
"""Part 6: Multi-Agent Weighted Consensus Voting Protocol."""
from __future__ import annotations
from typing import Dict, Tuple
from models import Task
from mesh_bus import Blackboard

class ConsensusEngine:
    """Requires Security, Architect, and QA agents to vote before approving tasks."""
    WEIGHTS = {
        "Security-Auditor": 0.40,
        "Architect-Agent": 0.30,
        "QA-Verifier": 0.30,
    }

    @classmethod
    def evaluate(cls, task: Task, blackboard: Blackboard, quorum: float = 0.70) -> Tuple[bool, float, Dict[str, float]]:
        votes: Dict[str, float] = {}
        votes["Security-Auditor"] = 1.0 if (task.ast_verified and not task.error) else 0.0
        blueprint_ok = blackboard.read("architecture_blueprint") is not None
        votes["Architect-Agent"] = 1.0 if (blueprint_ok and task.ast_complexity_score <= 25) else 0.5
        votes["QA-Verifier"] = 1.0 if (task.generated_code and "def " in task.generated_code) else 0.6

        weighted_score = sum(votes[role] * weight for role, weight in cls.WEIGHTS.items())
        weighted_score = round(weighted_score, 4)
        return (weighted_score >= quorum), weighted_score, votes
      
