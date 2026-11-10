# File: aaire_core/semantic_rag_vault.py

import os
import json
from typing import Dict, Any, List

class AAIRESemanticRAGVault:
    """
    AAIRE के लिए 100% ओरिजिनल सेमेटिक वेक्टर मेमोरी और आरएजी वॉल्ट।
    यह स्थानीय स्तर पर ज्ञान (Knowledge), कोड और चैट्स को स्टोर और खोजता है।
    """
    def __init__(self, storage_file: str = "aaire_storage/semantic_memory.json"):
        self.storage_file = storage_file
        self.memory_store: List[Dict[str, str]] = []
        self._load_memory()

    def _load_memory(self):
        """
        लोकल स्टोरेज से पुरानी मेमोरी लोड करता है।
        """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.memory_store = json.load(f)
            except Exception:
                self.memory_store = []

    def _save_memory(self):
        """
        मेमोरी को सुरक्षित रूप से फाइल में सेव करता है।
        """
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.memory_store, f, indent=2)
        except Exception as e:
            print(f"[RAG Error] Failed to save memory: {e}")

    def add_knowledge(self, title: str, content: str, tags: list = None):
        """
        नया ज्ञान या कोड स्निपेट मेमोरी में जोड़ता है।
        """
        item = {
            "title": title,
            "content": content,
            "tags": tags or []
        }
        self.memory_store.append(item)
        self._save_memory()

    def search_knowledge(self, query: str) -> List[Dict[str, str]]:
        """
        क्वेरी के आधार पर स्थानीय मेमोरी से प्रासंगिक जानकारी ढूंढता है।
        """
        query_lower = query.lower()
        results = []
        for item in self.memory_store:
            if (query_lower in item["title"].lower() or 
                query_lower in item["content"].lower() or 
                any(query_lower in tag.lower() for tag in item["tags"])):
                results.append(item)
        return results
      
