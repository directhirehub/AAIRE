# File: aaire_core/latency_tracer.py

import time
from typing import Dict, Any, List

class AAIRELatencyTracer:
    """
    AAIRE के लिए 100% ओरिजिनल लेटेसी और परफॉरमेंस ट्रेसर।
    यह एजेंट्स और टूल्स के एक्सेक्यूशन टाइम को ट्रैक और रिकॉर्ड करता है।
    """
    def __init__(self):
        self.traces: List[Dict[str, Any]] = []

    def measure_execution(self, task_name: str, func, *args, **kwargs) -> Any:
        """
        किसी भी फंक्शन या टास्क को रन करके उसकी लेटेसी (मिलीसेकंड में) मापता है।
        """
        start_time = time.perf_counter()
        success = True
        result = None
        error_msg = None

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            success = False
            error_msg = str(e)
            raise
        finally:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            trace_record = {
                "task_name": task_name,
                "latency_ms": elapsed_ms,
                "success": success,
                "error": error_msg,
                "timestamp": time.time()
            }
            self.traces.append(trace_record)

        return result

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        सभी रिकॉर्ड किए गए ट्रेसेस का परफॉरमेंस समरी देता है।
        """
        if not self.traces:
            return {"total_tasks": 0, "avg_latency_ms": 0.0}

        total_tasks = len(self.traces)
        total_latency = sum(t["latency_ms"] for t in self.traces)
        avg_latency = round(total_latency / total_tasks, 2)

        return {
            "total_tasks": total_tasks,
            "avg_latency_ms": avg_latency,
            "all_traces": self.traces
        }
      
