#!/usr/bin/env python3
"""UCB1 Monte-Carlo Tree Search & Bayesian Decision Engine."""
from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MCTSNode:
    action: str
    parent: Optional[MCTSNode] = None
    children: List[MCTSNode] = field(default_factory=list)
    visits: int = 0
    value: float = 0.0

    def ucb1_score(self, exploration_c: float = 1.414) -> float:
        if self.visits == 0:
            return float("inf")
        parent_visits = self.parent.visits if self.parent else 1
        exploitation = self.value / self.visits
        exploration = exploration_c * math.sqrt(math.log(max(parent_visits, 1)) / self.visits)
        return exploitation + exploration


class MCTSReasoner:
    def __init__(self, prior_beliefs: Optional[Dict[str, float]] = None) -> None:
        self.beliefs: Dict[str, float] = prior_beliefs or {}

    def update_bayesian_belief(self, hypothesis: str, likelihood_given_true: float, false_alarm_rate: float = 0.1) -> float:
        prior = self.beliefs.get(hypothesis, 0.5)
        numerator = likelihood_given_true * prior
        denominator = numerator + false_alarm_rate * (1.0 - prior)
        posterior = (numerator / denominator) if denominator > 0 else prior
        self.beliefs[hypothesis] = round(min(max(posterior, 0.001), 0.999), 4)
        return self.beliefs[hypothesis]

    def search_optimal_strategy(self, candidate_actions: Dict[str, float], simulations: int = 200) -> Dict[str, object]:
        root = MCTSNode(action="ROOT")
        for act in candidate_actions:
            root.children.append(MCTSNode(action=act, parent=root))

        rng = random.Random(42)
        for _ in range(simulations):
            leaf = max(root.children, key=lambda n: n.ucb1_score())
            base_prob = candidate_actions[leaf.action]
            reward = 1.0 if rng.random() < base_prob else 0.0
            leaf.visits += 1
            leaf.value += reward
            root.visits += 1

        best = max(root.children, key=lambda n: n.visits)
        return {
            "selected_action": best.action,
            "confidence": round(best.value / max(best.visits, 1), 4),
            "simulations_run": simulations,
            "action_visits": {c.action: c.visits for c in root.children}
        }
      
