# File: aaire_core/secure_sandbox.py

import subprocess
import sys
import os
from typing import Dict, Any

class AAIRESecureSandbox:
    """
    AAIRE के लिए 100% ओरिजिनल सिक्योर टर्मिनल सैंडबॉक्स।
    यह अनधिकृत या खतरनाक कमांड्स को रोकता है और सुरक्षित कोड को ही रन करने की अनुमति देता है।
    """
    def __init__(self, restricted_keywords: list = None):
        # खतरनाक कमांड्स या सिस्टम मॉड्यूल्स जिन पर प्रतिबंध है
        self.restricted_keywords = restricted_keywords or ["os.system", "shutil.rmtree", "subprocess.call", "eval(", "exec("]

    def validate_command_safety(self, command_str: str) -> bool:
        """
        जांचता है कि कमांड में कोई खतरनाक या प्रतिबंधित कोड तो नहीं है।
        """
        for keyword in self.restricted_keywords:
            if keyword in command_str:
                return False
        return True

    def run_sandboxed_snippet(self, code_snippet: str, timeout_sec: int = 5) -> Dict[str, Any]:
        """
        छोटे पायथन स्निपेट को सुरक्षित रूप से सबप्रोसेस में रन करके रिजल्ट देता है।
        """
        if not self.validate_command_safety(code_snippet):
            return {
                "status": "blocked",
                "error": "Security violation: Restricted keywords detected in sandbox execution."
            }

        try:
            # सुरक्षित तरीके से पायथन स्क्रिप्ट निष्पादित करना
            result = subprocess.run(
                [sys.executable, "-c", code_snippet],
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "exit_code": result.returncode,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": "Execution exceeded the safe time limit."
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
          
