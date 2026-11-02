#!/usr/bin/env python3
"""Part 3: Distributed Event-Driven Pub/Sub Bus & Thread-Safe Blackboard."""
from __future__ import annotations
import threading
from typing import Any, Callable, Dict, List

class EventBus:
    """Thread-safe Pub/Sub mesh for decoupled inter-agent notifications."""
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[[Any], None]]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        with self._lock:
            self._listeners.setdefault(event_type, []).append(callback)

    def publish(self, event_type: str, payload: Any) -> None:
        with self._lock:
            callbacks = list(self._listeners.get(event_type, []))
        for cb in callbacks:
            try:
                cb(payload)
            except Exception:
                pass

class Blackboard:
    """Thread-safe shared working memory for Sub-Agents to exchange artifacts."""
    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def write(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = value

    def read(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._store.get(key, default)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._store)
      
