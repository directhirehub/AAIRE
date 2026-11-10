# File: aaire_core/webhook_manager.py

import json
from typing import Dict, Any, Callable

class AAIREWebhookManager:
    """
    AAIRE के लिए 100% ओरिजिनल लाइटवेट API और वेबहुक मैनेजर।
    यह विभिन्न प्लेटफॉर्म्स (जैसे टेलीग्राम, गिटहब आदि) से आने वाले वेबहुक पेलोड्स को रजिस्टर और मैनेज करता है।
    """
    def __init__(self):
        self.routes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_webhook(self, event_name: str, callback_func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        """
        किसी विशेष इवेंट के लिए वेबहुक रूट रजिस्टर करता है।
        """
        self.routes[event_name] = callback_func

    def handle_incoming_payload(self, event_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        आने वाले वेबहुक पेलोड को प्रोसेस करके संबंधित कॉलबैक निष्पादित करता है।
        """
        if event_name not in self.routes:
            return {
                "status": "error",
                "event": event_name,
                "message": f"No handler registered for event '{event_name}'."
            }

        try:
            handler = self.routes[event_name]
            result = handler(payload)
            return {
                "status": "success",
                "event": event_name,
                "result": result
            }
        except Exception as e:
            return {
                "status": "failed",
                "event": event_name,
                "error": str(e)
            }
          
