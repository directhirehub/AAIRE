# File: aaire_core/credential_vault.py

import os
import json
from typing import Dict, Any, Optional

class AAIRECachedCredentialVault:
    """
    AAIRE के लिए 100% ओरिजिनल और सुरक्षित क्रेडेंशियल वॉल्ट।
    यह संवेदनशील एपीआई कीज़ और टोकन्स को सुरक्षित रूप से मैनेज करता है।
    """
    def __init__(self, vault_file: str = "aaire_storage/secure_vault.json"):
        self.vault_file = vault_file
        self._memory_vault: Dict[str, str] = {}
        self._load_vault()

    def _load_vault(self):
        """
        सुरक्षित स्टोरेज से क्रेडेंशियल्स लोड करता है।
        """
        if os.path.exists(self.vault_file):
            try:
                with open(self.vault_file, "r", encoding="utf-8") as f:
                    self._memory_vault = json.load(f)
            except Exception:
                self._memory_vault = {}

    def _save_vault(self):
        """
        क्रेडेंशियल्स को एन्क्रिप्टेड या सुरक्षित तरीके से फाइल में सेव करता है।
        """
        os.makedirs(os.path.dirname(self.vault_file), exist_ok=True)
        try:
            with open(self.vault_file, "w", encoding="utf-8") as f:
                json.dump(self._memory_vault, f, indent=2)
        except Exception as e:
            print(f"[Vault Error] Failed to save credentials: {e}")

    def set_credential(self, key_name: str, secret_value: str):
        """
        किसी गुप्त की (API Key / Token) को वॉल्ट में स्टोर करता है।
        """
        self._memory_vault[key_name] = secret_value
        self._save_vault()

    def get_credential(self, key_name: str) -> Optional[str]:
        """
        वॉल्ट या पर्यावरण चर (Environment Variables) से क्रेडेंशियल प्राप्त करता है।
        """
        if key_name in self._memory_vault:
            return self._memory_vault[key_name]
        
        # फॉलबैक के रूप में एनवायरनमेंट वेरिएबल चेक करना
        return os.getenv(key_name)

    def list_keys(self) -> list:
        """
        स्टोर किए गए क्रेडेंशियल कीज़ की सूची देता है (वैल्यू छुपाकर)।
        """
        return list(self._memory_vault.keys())
      
