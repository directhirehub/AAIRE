# File: aaire_core/dynamic_tool_forge.py

import os
import sys
import importlib.util
from typing import Dict, Any

class AAIREDynamicToolForge:
    """
    AAIRE के लिए 100% ओरिजिनल डायनामिक टूल फोर्ज।
    यह जरूरत पड़ने पर ऑन-द-फ्लाई नए पायथन टूल्स/स्क्रिप्ट्स को जनरेट और रजिस्टर करता है।
    """
    def __init__(self, tools_dir: str = "aaire_core/forged_tools"):
        self.tools_dir = tools_dir
        os.makedirs(self.tools_dir, exist_ok=True)

    def forge_tool(self, tool_name: str, code_content: str) -> Dict[str, Any]:
        """
        एक नया पायथन टूल फाइल के रूप में लिखता है और उसे उपयोग के लिए तैयार करता है।
        """
        if not tool_name.endswith(".py"):
            tool_name += ".py"
        
        file_path = os.path.join(self.tools_dir, tool_name)
        
        try:
            # टूल कोड को फाइल में लिखना
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code_content)
            
            # डायनामिक रूप से मॉड्यूल को लोड करना (Verification)
            module_name = tool_name[:-3]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = mod
                spec.loader.exec_module(mod)
                
                return {
                    "status": "success",
                    "tool_name": module_name,
                    "file_path": file_path,
                    "message": f"Tool '{module_name}' forged and loaded successfully."
                }
            else:
                return {"status": "failed", "error": "Could not create module spec."}
        except Exception as e:
            return {"status": "error", "error": str(e)}
          
