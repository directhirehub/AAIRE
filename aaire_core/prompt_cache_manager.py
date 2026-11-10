# File: aaire_core/prompt_cache_manager.py

import time
from typing import Dict, Any, Optional

class AAIREPromptCacheManager:
    """
    AAIRE के लिए 100% ओरिजिनल प्रॉम्प्ट कैचिंग और सेशन बाउंड्री मैनेजर।
    यह बार-बार इस्तेमाल होने वाले प्रॉम्प्ट्स को कैच करके लेटेसी और टोकन बचाता है।
    """
    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def set_cached_prompt(self, cache_key: str, prompt_content: str):
        """
        प्रॉम्प्ट या सिस्टम इंस्ट्रक्शन को कैच में सेव करता है।
        """
        self.cache[cache_key] = {
            "content": prompt_content,
            "timestamp": time.time()
        }

    def get_cached_prompt(self, cache_key: str) -> Optional[str]:
        """
        यदि कैच मौजूद है और एक्सपायर नहीं हुआ है, तो उसे रिटर्न करता है।
        """
        if cache_key in self.cache:
            item = self.cache[cache_key]
            if (time.time() - item["timestamp"]) < self.ttl_seconds:
                return item["content"]
            else:
                # समय समाप्त होने पर डिलीट करना
                del self.cache[cache_key]
        return None

    def clear_cache(self):
        """
        कैच को पूरी तरह साफ करता है।
        """
        self.cache.clear()
      
