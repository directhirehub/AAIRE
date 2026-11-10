# File: aaire_core/swarm_priority_queue.py

import queue
import time
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List, Optional

@dataclass(order=True)
class PrioritizedTask:
    priority: int
    timestamp: float = field(compare=True)
    task_id: str = field(compare=False)
    func: Callable[..., Any] = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)

class AAIRESwarmPriorityQueue:
    """
    AAIRE के लिए 100% ओरिजिनल स्वम प्रायोरिटी क्यू (Priority Queue)।
    यह अनलिमिटेड डायनामिक एजेंट्स के टास्क को उनकी प्राथमिकता (Priority) 
    और समय के आधार पर मैनेज और एक्सेक्यूट करता है।
    """
    def __init__(self):
        self.task_queue: queue.PriorityQueue[PrioritizedTask] = queue.PriorityQueue()
        self.execution_history: List[Dict[str, Any]] = []

    def enqueue_task(self, task_id: str, priority: int, func: Callable[..., Any], *args: Any, **kwargs: Any):
        """
        टास्क को उसकी प्राथमिकता (छोटा नंबर = उच्च प्राथमिकता) के साथ क्यू में जोड़ता है।
        """
        task = PrioritizedTask(
            priority=priority,
            timestamp=time.time(),
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs
        )
        self.task_queue.put(task)

    def process_next_task(self) -> Optional[Dict[str, Any]]:
        """
        अगले उच्च-प्राथमिकता वाले टास्क को निकालकर निष्पादित (Execute) करता है।
        """
        if self.task_queue.empty():
            return None

        task = self.task_queue.get()
        start_time = time.perf_counter()
        success = True
        error_msg = None
        res = None

        try:
            res = task.func(*task.args, **task.kwargs)
        except Exception as e:
            success = False
            error_msg = str(e)
        
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        record = {
            "task_id": task.task_id,
            "priority": task.priority,
            "latency_ms": elapsed_ms,
            "success": success,
            "error": error_msg,
            "result": res
        }
        self.execution_history.append(record)
        return record

    def get_queue_stats(self) -> Dict[str, Any]:
        """
        क्यू की वर्तमान स्थिति और इतिहास का आँकड़ा देता है।
        """
        return {
            "pending_tasks_count": self.task_queue.qsize(),
            "completed_tasks_count": len(self.execution_history),
            "history": self.execution_history
      }
      
