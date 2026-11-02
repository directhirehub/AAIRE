#!/usr/bin/env python3
"""Multi-Worker Parallel Swarm Executor with Priority Queue & Telemetry."""
from __future__ import annotations
import time
import queue
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List


@dataclass(order=True)
class SwarmTask:
    priority: int
    task_id: str = field(compare=False)
    fn: Callable[..., Any] = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)


class SwarmExecutor:
    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers
        self.task_queue: queue.PriorityQueue[SwarmTask] = queue.PriorityQueue()
        self.telemetry: Dict[str, Dict[str, Any]] = {}
        self.dead_letter_queue: List[Dict[str, Any]] = []

    def submit_task(self, task_id: str, fn: Callable[..., Any], priority: int = 5, *args: Any, **kwargs: Any) -> None:
        self.task_queue.put(SwarmTask(priority, task_id, fn, args, kwargs))

    def _run_tracked(self, task: SwarmTask) -> Any:
        start = time.perf_counter()
        try:
            result = task.fn(*task.args, **task.kwargs)
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            self.telemetry[task.task_id] = {"status": "SUCCESS", "latency_ms": latency_ms, "result": result}
            return result
        except Exception as exc:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            err_info = {"task_id": task.task_id, "error": str(exc), "latency_ms": latency_ms}
            self.telemetry[task.task_id] = {"status": "FAILED", **err_info}
            self.dead_letter_queue.append(err_info)
            return None

    def execute_all(self) -> Dict[str, Any]:
        tasks: List[SwarmTask] = []
        while not self.task_queue.empty():
            tasks.append(self.task_queue.get())

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures: List[Future] = [pool.submit(self._run_tracked, t) for t in tasks]
            for f in futures:
                f.result()

        return {
            "total_executed": len(tasks),
            "failed_count": len(self.dead_letter_queue),
            "telemetry": self.telemetry
}
      
