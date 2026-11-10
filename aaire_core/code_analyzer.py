# File: aaire_core/code_analyzer.py

import ast
from typing import List, Dict, Any

class AAIRECodeAnalyzer:
    """
    AAIRE के लिए 100% ओरिजिनल लाइटवेट कोड और AST एनालाइज़र।
    यह पायथन कोड की संरचना, फंक्शन्स और सुरक्षा की जांच करता है।
    """
    def __init__(self):
        self.forbidden_nodes = {ast.Exec}  # पुरानी या असुरक्षित नोड्स

    def analyze_source_code(self, code_str: str) -> Dict[str, Any]:
        """
        सोर्स कोड को पार्स करके उसके फंक्शन्स, इम्पोर्ट्स और संभावित कमियों की रिपोर्ट देता है।
        """
        report: Dict[str, Any] = {
            "is_valid_syntax": True,
            "functions": [],
            "imports": [],
            "issues": []
        }

        if not code_str or not code_str.strip():
            report["is_valid_syntax"] = False
            report["issues"].append("Code string is empty.")
            return report

        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            report["is_valid_syntax"] = False
            report["issues"].append(f"SyntaxError at line {e.lineno}: {e.msg}")
            return report

        # AST ट्री को वॉक करके जानकारी निकालना
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                report["functions"].append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    report["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    report["imports"].append(node.module)
            elif isinstance(node, tuple(self.forbidden_nodes)):
                report["issues"].append(f"Forbidden construct detected: {type(node).__name__}")

        report["total_functions"] = len(report["functions"])
        report["total_imports"] = len(report["imports"])
        return report
      
