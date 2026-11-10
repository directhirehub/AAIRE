# File: aaire_core/verify_runner.py

import ast
import subprocess
import sys
from typing import Dict, Any, List

class AAIREVerifyRunner:
    """
    AAIRE के लिए 100% ओरिजिनल ऑटोमेटेड टेस्ट और वैलिडेटर रनर।
    यह जनरेट किए गए कोड को डिप्लॉय या सेव करने से पहले उसकी पूर्णता और सुरक्षा जांचता है।
    """
    def __init__(self):
        self.verification_history: List[Dict[str, Any]] = []

    def verify_code_integrity(self, file_path: str, code_content: str) -> Dict[str, Any]:
        """
        कोड की सिंटैक्स शुद्धता और संभावित रनटाइम कमियों की जांच करता है।
        """
        report = {
            "file_path": file_path,
            "syntax_valid": False,
            "security_risk_detected": False,
            "issues": []
        }

        if not code_content or not code_content.strip():
            report["issues"].append("File content is empty.")
            return report

        # 1. सिंटैक्स चेक (AST Parse)
        try:
            tree = ast.parse(code_content, filename=file_path)
            report["syntax_valid"] = True
        except SyntaxError as e:
            report["issues"].append(f"SyntaxError: line {e.lineno} - {e.msg}")
            return report

        # 2. खतरनाक या अनधिकृत सिग्नल्स की जांच (जैसे eval, exec, असुरक्षित इम्पोर्ट्स)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ["eval", "exec"]:
                    report["security_risk_detected"] = True
                    report["issues"].append(f"Security Warning: Use of '{node.func.id}' detected.")

        self.verification_history.append(report)
        return report

    def run_safe_pytest(self, test_dir: str = "tests/") -> Dict[str, Any]:
        """
        सुरक्षित रूप से यूनिट टेस्ट्स (pytest) निष्पादित करता है।
        """
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_dir],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "exit_code": result.returncode,
                "output": result.stdout if result.returncode == 0 else result.stderr,
                "status": "passed" if result.returncode == 0 else "failed"
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "output": str(e),
                "status": "error_executing_tests"
            }
          
