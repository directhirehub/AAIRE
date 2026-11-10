# File: aaire_core/model_router.py

import os
from typing import Dict, Any, Optional

class AAIREModelRouter:
    """
    AAIRE के लिए 100% ओरिजिनल मल्टी-मॉडल राउटर। 
    यह टास्क की जरूरत के अनुसार सही AI मॉडल या बैकएंड को चुनता है।
    """
    def __init__(self, default_provider: str = "gemini"):
        self.default_provider = os.getenv("AAIRE_DEFAULT_MODEL", default_provider)
        self.registered_endpoints: Dict[str, str] = {
            "gemini": "https://generativelanguage.googleapis.com/v1beta/models/",
            "openai": "https://api.openai.com/v1/chat/completions",
            "anthropic": "https://api.anthropic.com/v1/messages"
        }

    def route_request(self, task_type: str, prompt: str) -> Dict[str, Any]:
        """
        टास्क के प्रकार के आधार पर मॉडल और पैरामीटर्स तय करता है।
        """
        provider = self.default_provider
        
        if task_type == "heavy_coding":
            provider = "anthropic"  # कोडिंग के लिए श्रेष्ठ
        elif task_type == "fast_search":
            provider = "gemini"     # तेज रिस्पांस के लिए
            
        return {
            "provider": provider,
            "endpoint": self.registered_endpoints.get(provider, "local"),
            "prompt_length": len(prompt),
            "status": "routed_successfully"
        }
      
