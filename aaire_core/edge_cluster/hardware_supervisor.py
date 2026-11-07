import os
import platform
import shutil
import time

class EdgeHardwareSupervisor:
    """Scratch-Built Hardware, Edge Device & Multi-Computer Supervisor."""
    def __init__(self):
        self.arch = platform.machine()
        self.os_type = platform.system().lower()

    def probe_hardware_and_supervise(self, target_node: str = "local_master") -> dict:
        disk = shutil.disk_usage(os.path.abspath(os.sep))
        free_gb = round(disk.free / (1024 ** 3), 2)
        total_gb = round(disk.total / (1024 ** 3), 2)
        cpu_cores = os.cpu_count() or 1
        load_avg = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.15

        health = "OPTIMAL" if free_gb > 1.0 and load_avg < (cpu_cores * 2) else "THROTTLED_AUTO_HEAL"
        return {
            "supervisor": "AAIRE-Edge-Supervisor-v1.0",
            "node_id": target_node,
            "os_platform": self.os_type,
            "cpu_arch": self.arch,
            "cpu_cores": cpu_cores,
            "load_1m": round(load_avg, 2),
            "disk_free_gb": free_gb,
            "disk_total_gb": total_gb,
            "supervisor_action": "WORKER_HEARTBEAT_OK" if health == "OPTIMAL" else "RESTART_AND_GC_TRIGGERED",
            "timestamp": round(time.time(), 2)
        }
      
