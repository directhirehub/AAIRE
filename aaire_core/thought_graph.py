# File: aaire_core/thought_graph.py

import json
import os
from typing import Dict, Any, List

class AAIREThoughtGraph:
    """
    AAIRE के लिए 100% ओरिजिनल एपिसोडिक मेमोरी और थॉट ग्राफ।
    यह पिछले गोल्स, डिसीजंस और रणनीतियों के संबंधों को स्टोर और ट्रैक करता है।
    """
    def __init__(self, storage_path: str = "aaire_storage/thought_graph.json"):
        self.storage_path = storage_path
        self.nodes: List[Dict[str, Any]] = []
        self._load_graph()

    def _load_graph(self):
        """
        लोकल स्टोरेज से पुराना थॉट ग्राफ लोड करता है।
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.nodes = json.load(f)
            except Exception:
                self.nodes = []

    def _save_graph(self):
        """
        थॉट ग्राफ को सुरक्षित रूप से फाइल में सेव करता है।
        """
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.nodes, f, indent=2)
        except Exception as e:
            print(f"[ThoughtGraph Error] Failed to save graph: {e}")

    def add_thought_node(self, goal: str, strategy_used: str, outcome: str, success: bool):
        """
        नए थॉट नोड या एपिसोडिक अनुभव को ग्राफ में जोड़ता है।
        """
        node = {
            "goal": goal,
            "strategy": strategy_used,
            "outcome": outcome,
            "success": success
        }
        self.nodes.append(node)
        self._save_graph()

    def get_past_insights(self, query_goal: str) -> List[Dict[str, Any]]:
        """
        समान गोल्स या पुरानी रणनीतियों के आधार पर सीखे गए अनुभवों को ढूंढता है।
        """
        query_lower = query_goal.lower()
        results = []
        for node in self.nodes:
            if query_lower in node["goal"].lower() or query_lower in node["strategy"].lower():
                results.append(node)
        return results
      
