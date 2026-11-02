#!/usr/bin/env python3
"""Part 4: Dynamic Circuit Breaker & Adaptive Concurrency Governor."""
from __future__ import annotations
import os
import threading
import time
from typing import List
from config import Config
from models import Task

class CircuitBreaker:
    """Prevents cascading cluster failures across specialized sub-agents."""
    def __init__(self, threshold: int = 5, recovery_s: float = 1.0) -> None:
        self.threshold = threshold
        self.recovery_s = recovery_s
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_ts = 0.0
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            if self.state == "OPEN":
                if (time.monotonic() - self.last_failure_ts) >= self.recovery_s:
                    self.state = "HALF-OPEN"
                    return True
                return False
            return True

    def record_success(self) -> None:
        with self._lock:
            self.failures = 0
            self.state = "CLOSED"

    def record_failure(self) -> None:
        with self._lock:
            self.failures += 1
            self.last_failure_ts = time.monotonic()
            if self.failures >= self.threshold:
                self.state = "OPEN"

class ConcurrencyGovernor:
    """Auto-scales ThreadPool workers based on task complexity and CPU cores."""
    @staticmethod
    def compute_workers(config: Config, wave_tasks: List[Task]) -> int:
        if not wave_tasks:
            return config.min_workers
        avg_complexity = sum(t.complexity for t in wave_tasks) / len(wave_tasks)
        cpu_count = os.cpu_count() or 4
        scaled = max(
            config.min_workers,
            min(config.max_workers, int(cpu_count * (avg_complexity / 2.5)))
        )
        return max(1, min(scaled, len(wave_tasks)))
      
