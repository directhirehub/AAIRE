#!/usr/bin/env python3
"""Asyncio Actor Mesh Bus with 3-State Self-Healing Circuit Breaker."""
from __future__ import annotations
import asyncio
import time
from typing import Any, Callable, Coroutine, Dict, List


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 5.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = 0.0

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        return True

    def record_success(self) -> None:
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        self.failures += 1
        self.last_failure_time = time.monotonic()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"


class QuantumMeshKernel:
    def __init__(self) -> None:
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]]] = {}
        self.breakers: Dict[str, CircuitBreaker] = {}
        self.metrics: Dict[str, int] = {"published": 0, "delivered": 0, "tripped": 0}

    def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]) -> None:
        self.subscribers.setdefault(topic, []).append(handler)
        self.breakers.setdefault(topic, CircuitBreaker())

    async def publish(self, topic: str, message: Dict[str, Any]) -> List[Any]:
        self.metrics["published"] += 1
        handlers = self.subscribers.get(topic, [])
        breaker = self.breakers.get(topic, CircuitBreaker())

        if not breaker.can_execute():
            self.metrics["tripped"] += 1
            return [{"status": "CIRCUIT_OPEN", "topic": topic}]

        results = []
        for h in handlers:
            try:
                res = await asyncio.wait_for(h(message), timeout=5.0)
                breaker.record_success()
                self.metrics["delivered"] += 1
                results.append(res)
            except Exception as exc:
                breaker.record_failure()
                results.append({"status": "HANDLER_ERROR", "error": str(exc)})
        return results
      
