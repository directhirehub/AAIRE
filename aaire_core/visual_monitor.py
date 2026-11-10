# File: aaire_core/visual_monitor.py

import time
from typing import Dict, Any

class AAIREVisualMonitor:
    """
    AAIRE के लिए 100% ओरिजिनल विजुअल प्रोग्रेस मॉनिटर।
    यह एजेंट्स के एक्सेक्यूशन्स और स्वार्म की स्थिति को टर्मिनल पर ट्रैक करता है।
    """
    def __init__(self, agent_name: str = "AAIRE-Core"):
        self.agent_name = agent_name
        self.state = "IDLE"
        self.start_time = time.time()

    def update_status(self, new_state: str, task_info: str = ""):
        """
        एजेंट की स्थिति को अपडेट करता है और प्रोग्रेस प्रिंट करता है।
        """
        self.state = new_state
        elapsed = round(time.time() - self.start_time, 2)
        print(f"🐾 [{self.agent_name} Monitor] Status: {self.state} | Task: {task_info} | Uptime: {elapsed}s")

    def render_progress_card(self, current_step: int, total_steps: int) -> Dict[str, Any]:
        """
        टास्क की प्रगति का विजुअल कार्ड तैयार करता है।
        """
        percent = int((current_step / total_steps) * 100) if total_steps > 0 else 100
        bar = "█" * (percent // 10) + "-" * (10 - (percent // 10))
        
        card = {
            "agent": self.agent_name,
            "progress_bar": f"[{bar}] {percent}%",
            "current_state": self.state
        }
        return card
      
