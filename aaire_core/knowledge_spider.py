# File: aaire_core/knowledge_spider.py

import re
from typing import Dict, Any, List

class AAIREKnowledgeSpider:
    """
    AAIRE के लिए 100% ओरिजिनल और डायनामिक नॉलेज स्पाइडर।
    यह किसी भी प्रकार की वेबसाइट (जॉब पोर्टल, न्यूज, ई-कॉमर्स, क्रिप्टो ट्रेंड्स) 
    से बिना किसी हार्ड-कोडिंग के स्मार्ट तरीके से डेटा एक्सट्रेक्ट करता है।
    """
    def __init__(self):
        self.extracted_cache: List[Dict[str, Any]] = []

    def parse_dynamic_content(self, url: str, raw_html: str) -> Dict[str, Any]:
        """
        दिए गए HTML कंटेंट को डायनामिकली पार्स करता है और शीर्षक, लिंक्स, 
        कीवर्ड्स तथा प्रासंगिक डेटा को अलग करता है।
        """
        if not raw_html or not raw_html.strip():
            return {"url": url, "status": "failed", "reason": "empty_html"}

        # HTML टैग्स हटाकर साफ़ टेक्स्ट निकालना
        clean_text = re.sub(r'<[^>]+>', ' ', raw_html)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        # लिंक्स (URLs) डायनामिकली ढूंढना
        links = re.findall(r'href=[\"\'](https?://[^\"\']+)[\"\']', raw_html)

        # संभावित टाइटल्स या हेडिंग्स निकालना (h1, h2, h3 या सामान्य वाक्य)
        headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', raw_html, re.IGNORECASE)
        cleaned_headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]

        # जेनेरिक डेटा एक्सट्रैक्शन रिजल्ट
        result = {
            "source_url": url,
            "status": "success",
            "total_text_length": len(clean_text),
            "discovered_headings": cleaned_headings[:15],  # शीर्ष 15 हेडिंग्स
            "discovered_links_count": len(links),
            "sample_links": list(set(links))[:10],         # यूनीक सैम्पल लिंक्स
            "snippet": clean_text[:500] + "..." if len(clean_text) > 500 else clean_text
        }

        self.extracted_cache.append(result)
        return result

    def get_spider_stats(self) -> Dict[str, Any]:
        """
        स्पाइडर द्वारा अब तक क्रॉल किए गए डेटा का आँकड़ा देता है।
        """
        return {
            "total_pages_scanned": len(self.extracted_cache),
            "history": self.extracted_cache
      }
      
