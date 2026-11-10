# File: aaire_core/auto_docs.py

import os
import ast
from typing import Dict, Any, List

class AAIREAutoDocumentation:
    """
    AAIRE के लिए 100% ओरिजिनल फुल-सिस्टम ऑटो-डॉक्यूमेंटेशन और चेंजलॉग जनरेटर।
    यह पूरे प्रोजेक्ट या डायरेक्टरी को स्कैन करके सभी मॉड्यूल्स का मार्डाउन डॉक्यूमेंटेशन तैयार करता है।
    """
    def __init__(self, root_dir: str = "aaire_core"):
        self.root_dir = root_dir

    def scan_and_document_all_modules(self) -> Dict[str, Any]:
        """
        पूरे फोल्डर को स्कैन करता है और सभी पाइथन मॉड्यूल्स के फंक्शन्स और डॉकस्ट्रिंग्स निकालता है।
        """
        system_docs = {}
        if not os.path.exists(self.root_dir):
            return {"status": "error", "message": f"Directory '{self.root_dir}' not found."}

        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    module_name = file[:-3]
                    
                    doc_info = self._extract_doc_from_file(file_path)
                    system_docs[module_name] = doc_info

        return {
            "status": "success",
            "scanned_directory": self.root_dir,
            "total_modules_documented": len(system_docs),
            "modules": system_docs
        }

    def _extract_doc_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        सहायक मेथड: किसी एक फाइल से उसकी जानकारी और फंक्शन्स निकालता है।
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code_content = f.read()

            tree = ast.parse(code_content)
            module_docstring = ast.get_docstring(tree) or "No module docstring provided."
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    func_doc = ast.get_docstring(node) or "No description."
                    functions.append({"name": func_name, "docstring": func_doc})

            return {
                "file_path": file_path,
                "module_docstring": module_docstring,
                "functions": functions,
                "total_functions": len(functions)
            }
        except Exception as e:
            return {
                "file_path": file_path,
                "error": str(e)
            }

    def generate_markdown_summary(self) -> str:
        """
        स्कैन किए गए सभी मॉड्यूल्स की जानकारी से एक सुंदर मार्डाउन (Markdown) रिपोर्ट तैयार करता है।
        """
        scan_results = self.scan_and_document_all_modules()
        if scan_results.get("status") == "error":
            return f"# AAIRE System Documentation\n\nError: {scan_results.get('message')}"

        md = "# AAIRE Complete System Documentation & Module Index\n\n"
        md += f"**Scanned Directory:** `{scan_results['scanned_directory']}`\n"
        md += f"**Total Modules Documented:** {scan_results['total_modules_documented']}\n\n---\n\n"

        for mod_name, details in scan_results.get("modules", {}).items():
            md += f"## Module: `{mod_name}`\n"
            md += f"- **Path:** `{details.get('file_path', 'N/A')}`\n"
            md += f"- **Description:** {details.get('module_docstring', 'N/A')}\n"
            md += f"- **Total Functions:** {details.get('total_functions', 0)}\n\n"
            
            if details.get("functions"):
                md += "### Functions:\n"
                for func in details["functions"]:
                    md += f"  - `def {func['name']}()`: {func['docstring']}\n"
                md += "\n"
            md += "---\n\n"

        return md

    def generate_changelog_entry(self, version: str, changes: List[str]) -> str:
        """
        नया चेंजलॉग प्रविष्टि मार्डाउन फॉर्मेट में तैयार करता है।
        """
        changelog = f"## Version {version}\n"
        for change in changes:
            changelog += f"- {change}\n"
        return changelog
              
