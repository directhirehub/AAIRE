# File: aaire_core/telegram_gateway.py

import json
from typing import Dict, Any, Callable, Optional

class AAIRETelegramGateway:
    """
    AAIRE के लिए 100% ओरिजिनल टेलीग्राम बॉट और वेबहुक गेटवे।
    यह @aairebot और अन्य इवेंट वेबहुक्स से आने वाले संदेशों और कमांड्स को प्रोसेस करता है।
    """
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token
        self.registered_handlers: Dict[str, Callable[..., Any]] = {}
        self.event_log: list = []

    def register_command_handler(self, command: str, func: Callable[..., Any]):
        """
        किसी विशेष टेलीग्राम कमांड (जैसे /status, /deploy) के लिए फंक्शन रजिस्टर करता है।
        """
        self.registered_handlers[command] = func

    def handle_incoming_webhook(self, webhook_payload: dict) -> Dict[str, Any]:
        """
        टेलीग्राम या अन्य वेबहुक से मिलने वाले पेलोड को पार्स और हैंडल करता है।
        """
        self.event_log.append(webhook_payload)
        
        # टेलीग्राम मैसेज स्ट्रक्चर की सामान्य जांच
        message = webhook_payload.get("message", {})
        text = message.get("text", "").strip()
        chat_id = message.get("chat", {}).get("id")

        if not text:
            return {"status": "ignored", "reason": "No text found in payload"}

        # कमांड पहचानना (जैसे /start, /status)
        command_parts = text.split(" ")
        cmd = command_parts[0].lower()
        args = command_parts[1:]

        response = {
            "chat_id": chat_id,
            "command": cmd,
            "handled": False,
            "result": None
        }

        if cmd in self.registered_handlers:
            try:
                res = self.registered_handlers[cmd](*args)
                response["handled"] = True
                response["result"] = res
            except Exception as e:
                response["handled"] = False
                response["error"] = str(e)
        else:
            response["result"] = f"Unknown command: {cmd}. AAIRE Core is active."

        return response
      
