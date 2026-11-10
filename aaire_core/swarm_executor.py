# --- Unlimited Dynamic Swarm & Quality Gate Integration ---
import asyncio
from typing import Callable, Dict, Any, Optional
from aaire_core.task_decomposer import TaskDecomposer, SubTask
from aaire_core.quality_gate import SwarmQualityGate


class UnlimitedSwarmEngine:
    """
    बिना किसी एजेंट लिमिट के हर सब-टास्क के लिए नया स्पेशलिस्ट एजेंट बनाता है,
    उन्हें एक साथ (Parallel) चलाता है और Quality Gate से चेक कराता है।
    """

    def __init__(self, max_retries: int = 3):
        self.decomposer = TaskDecomposer(allow_unlimited=True)
        self.quality_gate = SwarmQualityGate()
        self.max_retries = max_retries

    async def _run_single_agent(
        self,
        subtask: SubTask,
        agent_callback: Optional[Callable[[str, str, str], Any]] = None
    ) -> Dict[str, Any]:
        agent = subtask.agent_spec
        expected_type = "python" if subtask.assigned_role == "coder" else "text"

        for attempt in range(1, self.max_retries + 1):
            if agent_callback:
                raw_output = await asyncio.to_thread(
                    agent_callback,
                    agent.role_name,
                    agent.system_prompt,
                    subtask.description
                )
            else:
                raw_output = (
                    f"[{agent.agent_id} | {agent.role_name}] "
                    f"Successfully executed task: {subtask.description}"
                )

            report = self.quality_gate.validate_agent_output(raw_output, expected_type=expected_type)

            if report.passed:
                subtask.status = "COMPLETED"
                return {
                    "task_id": subtask.task_id,
                    "agent_id": agent.agent_id,
                    "role": agent.role_name,
                    "status": "PASSED",
                    "score": report.score,
                    "attempts": attempt,
                    "output": raw_output
                }

            subtask.retries = attempt
            subtask.status = "RETRYING"

        return {
            "task_id": subtask.task_id,
            "agent_id": agent.agent_id,
            "role": agent.role_name,
            "status": "FAILED_QUALITY_GATE",
            "score": 0.0,
            "attempts": self.max_retries,
            "issues": report.issues
        }

    async def execute_unlimited_swarm(
        self,
        objective: str,
        agent_callback: Optional[Callable[[str, str, str], Any]] = None
    ) -> Dict[str, Any]:
        subtasks = self.decomposer.decompose(objective)
        worker_tasks = [t for t in subtasks if t.assigned_role != "validator"]

        # सभी डायनामिक एजेंट्स को बिना किसी गिनती की रुकावट के एक साथ (Parallel) चलाएं
        parallel_runs = [
            self._run_single_agent(task, agent_callback) for task in worker_tasks
        ]
        results = await asyncio.gather(*parallel_runs)

        passed_count = sum(1 for r in results if r["status"] == "PASSED")
        return {
            "objective": objective,
            "total_dynamic_agents_spawned": len(worker_tasks),
            "passed_quality_gate": passed_count,
            "results": results
        }

    def run(self, objective: str, agent_callback: Optional[Callable[[str, str, str], Any]] = None) -> Dict[str, Any]:
        return asyncio.run(self.execute_unlimited_swarm(objective, agent_callback))
        
