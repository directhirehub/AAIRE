#!/usr/bin/env python3
"""Part 9: DAG Task Dependency Resolver & Sub-Agent Execution Engine."""
from __future__ import annotations
import os
import random
import re
import time
import traceback
from collections import deque
from typing import Callable, Dict, List
from config import Config
from models import Task
from mesh_bus import EventBus, Blackboard
from resilience import CircuitBreaker
from ast_guard import ASTCodeGuard
from consensus import ConsensusEngine
from merkle_storage import StorageManager

class DAGEngine:
    """Builds Topological Task Waves and runs Sub-Agents with 30 self-healing retries."""
    def __init__(
        self,
        config: Config,
        event_bus: EventBus,
        blackboard: Blackboard,
        circuit_breaker: CircuitBreaker,
        storage: StorageManager,
        log_fn: Callable[[str, str], None]
    ) -> None:
        self.config = config
        self.event_bus = event_bus
        self.blackboard = blackboard
        self.circuit_breaker = circuit_breaker
        self.storage = storage
        self.log = log_fn

    def build_dag_tasks(self, primary_goal: str) -> List[Task]:
        r_max = self.config.max_retries
        return [
            Task(
                name="security_boundary_audit",
                goal=f"Establish Zero-Trust boundary & threat model for: {primary_goal}",
                agent_type="Security-Auditor",
                dependencies=[],
                complexity=2,
                max_retries=r_max
            ),
            Task(
                name="system_architecture_blueprint",
                goal=f"Design modular DAG & state schema for: {primary_goal}",
                agent_type="Architect-Agent",
                dependencies=[],
                complexity=3,
                max_retries=r_max
            ),
            Task(
                name="autonomous_code_synthesis",
                goal=f"Synthesize AST-verified Python implementation for: {primary_goal}",
                agent_type="Code-Generator",
                dependencies=["security_boundary_audit", "system_architecture_blueprint"],
                complexity=5,
                max_retries=r_max
            ),
            Task(
                name="heuristic_performance_optimization",
                goal=f"Optimize memory footprint and concurrency for: {primary_goal}",
                agent_type="Optimizer-Agent",
                dependencies=["autonomous_code_synthesis"],
                complexity=4,
                max_retries=r_max
            ),
            Task(
                name="multi_agent_qa_consensus",
                goal=f"Verify AST safety, run consensus vote & seal Merkle state for: {primary_goal}",
                agent_type="QA-Verifier",
                dependencies=["heuristic_performance_optimization"],
                complexity=3,
                max_retries=r_max
            ),
        ]

    @staticmethod
    def resolve_dag_waves(tasks: List[Task]) -> List[List[Task]]:
        task_map = {t.name: t for t in tasks}
        in_degree = {t.name: len(t.dependencies) for t in tasks}
        dependents: Dict[str, List[str]] = {t.name: [] for t in tasks}
        for t in tasks:
            for dep in t.dependencies:
                if dep in dependents:
                    dependents[dep].append(t.name)

        ready = deque([name for name, deg in in_degree.items() if deg == 0])
        waves: List[List[Task]] = []

        while ready:
            current_names = list(ready)
            ready.clear()
            waves.append([task_map[n] for n in current_names])
            for name in current_names:
                for child in dependents[name]:
                    in_degree[child] -= 1
                    if in_degree[child] == 0:
                        ready.append(child)

        if sum(len(w) for w in waves) != len(tasks):
            raise ValueError("Cyclic dependency detected in Task DAG!")
        return waves

    @staticmethod
    def _synthesize_agent_code(task: Task) -> str:
        safe_goal = re.sub(r"[^a-zA-Z0-9_ \-:]", "", task.goal)
        if os.environ.get("SIMULATE_UNSAFE_CODE") == "1" and task.attempts == 1:
            return f"import os\ndef unsafe_task():\n    os.system('echo {safe_goal}')\n"

        return (
            f"def {task.name}_handler(blackboard_context: dict) -> dict:\n"
            f"    \"\"\"Auto-synthesized by {task.agent_type} for: {safe_goal}\"\"\"\n"
            f"    return {{\n"
            f"        'task': '{task.name}',\n"
            f"        'agent': '{task.agent_type}',\n"
            f"        'verified': True,\n"
            f"        'shared_keys': len(blackboard_context)\n"
            f"    }}\n"
        )

    def execute_task(self, task: Task) -> Task:
        start_ns = time.perf_counter()
        last_trace = ""

        while task.attempts < task.max_retries and task.status != "SUCCESS":
            if not self.circuit_breaker.allow():
                task.status = "CIRCUIT_BROKEN"
                task.error = "Circuit Breaker is OPEN due to repeated cluster failures."
                break

            task.attempts += 1
            task.status = "RUNNING"

            try:
                raw_code = self._synthesize_agent_code(task)
                is_safe, violations, complexity = ASTCodeGuard.inspect_code(
                    raw_code, max_complexity=self.config.max_ast_complexity
                )
                if not is_safe:
                    self.log("WARNING", f"AST Guard flagged [{task.name}]: {violations}. Self-Correcting...")
                    raw_code = ASTCodeGuard.reflective_self_correct(raw_code, violations)
                    task.self_corrected = True
                    is_safe, violations, complexity = ASTCodeGuard.inspect_code(
                        raw_code, max_complexity=self.config.max_ast_complexity
                    )
                    if not is_safe:
                        task.status = "QUARANTINED"
                        raise PermissionError(f"Unrecoverable AST violation: {violations}")

                task.generated_code = raw_code
                task.ast_verified = True
                task.ast_complexity_score = complexity

                if task.agent_type == "Security-Auditor":
                    self.blackboard.write("security_policy", {"zero_trust": True, "auditor_task": task.id})
                elif task.agent_type == "Architect-Agent":
                    self.blackboard.write("architecture_blueprint", {"dag_verified": True, "architect_task": task.id})
                elif task.agent_type == "Code-Generator":
                    self.blackboard.write("compiled_module", task.generated_code)

                passed, score, votes = ConsensusEngine.evaluate(
                    task, self.blackboard, quorum=self.config.consensus_quorum
                )
                task.consensus_score = score
                if not passed:
                    task.status = "CONSENSUS_REJECTED"
                    raise RuntimeError(f"Consensus {score} below quorum {self.config.consensus_quorum}: {votes}")

                task.status = "SUCCESS"
                task.error = None
                task.result = f"[{task.agent_type}] completed '{task.name}' | AST: {complexity} | Vote: {score}"
                self.circuit_breaker.record_success()
                self.event_bus.publish("TASK_SUCCESS", task)

            except Exception as exc:
                last_trace = traceback.format_exc()
                task.error = str(exc)
                self.circuit_breaker.record_failure()

                if task.attempts < task.max_retries:
                    task.status = "RETRYING"
                    self.event_bus.publish("TASK_RETRY", task)
                    backoff = min(
                        self.config.backoff_cap_s,
                        self.config.backoff_base_s * (1.5 ** min(task.attempts, 10))
                    ) + random.uniform(0.005, 0.02)
                    time.sleep(backoff)
                else:
                    task.status = "FAILED"
                    self.storage.dump_to_dlq_autopsy(task, self.blackboard.snapshot(), last_trace)
                    self.event_bus.publish("TASK_DLQ", task)

        task.duration_ms = round((time.perf_counter() - start_ns) * 1000, 2)
        self.storage.update_learned_patterns(task)
        return task
      
