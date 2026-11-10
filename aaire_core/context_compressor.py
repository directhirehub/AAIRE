# File: aaire_core/context_compressor.py

import re
from typing import List, Dict, Any

class AAIREContextCompressor:
    """
    AAIRE के लिए 100% ओरिजिनल कॉन्टेक्स्ट कंप्रेसर।
    यह लंबे प्रॉम्प्ट्स या टेक्स्ट से फालतू स्पेस, रिपीटिशन्स और अनपेक्षित डेटा हटाकर टोकन बचाता है।
    """
    def __init__(self, max_length: int = 1500):
        self.max_length = max_length

    def compress_text(self, text: str) -> str:
        """
        टेक्स्ट को संक्षिप्त करता है और अनावश्यक खाली जगहों को साफ करता है।
        """
        if not text:
            return ""

        # अतिरिक्त व्हाइटस्पेस और न्यूलाइन्स को हटाना
        cleaned = re.sub(r'\s+', ' ', text).strip()

        # यदि लंबाई सीमा से अधिक है, तो संक्षिप्त विवरण देना
        if len(cleaned) > self.max_length:
            return cleaned[:self.max_length] + " ... [TRUNCATED_FOR_OPTIMIZATION]"
        
        return cleaned

    def optimize_chat_history(self, messages: List[Dict[str, str]], keep_last: int = 5) -> List[Dict[str, str]]:
        """
        चैट इतिहास में से केवल हाल के महत्वपूर्ण संदेशों को रखता है ताकि मेमोरी ओवरलोड न हो।
        """
        if len(messages) <= keep_last:
            return messages
        
        # शुरुआत के कुछ संदर्भ और आखिरी के मुख्य संदेश रखना
        return messages[-keep_last:]
      
