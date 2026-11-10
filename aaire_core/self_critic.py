# File: aaire_core/self_critic.py

from typing import Dict, Any, List

class AAIRESelfCriticEngine:
    """
    AAIRE के लिए 100% ओरिजिनल सेल्फ-रिफ्लेक्शन और क्रिटिक इंजन।
    यह एआई आउटपुट या कोड की समीक्षा करता है और सुधार के सुझाव देता है।
    """
    def __init__(self):
        self.review_logs: List[Dict[str, Any]] = []

    def evaluate_output(self, task_description: str, ai_output: str) -> Dict[str, Any]:
        """
        एआई के आउटपुट का क्रिटिकल विश्लेषण करता है।
        """
        critique_result = {
            "task": task_description,
            "passed_quality_check": True,
            "critique_notes": [],
            "suggestions": []
        }

        # बुनियादी सुरक्षा और गुणवत्ता मानदंड जांचना
        if not ai_output or len(ai_output.strip()) < 5:
            critique_result["passed_quality_check"] = False
            critique_result["critique_notes"].append("Output is too short or empty.")
            critique_result["suggestions"].append("Generate a detailed and complete response.")

        if "error" in ai_output.lower() or "exception" in ai_output.lower():
            critique_result["passed_quality_check"] = False
            critique_result["critique_notes"].append("Potential error signature found in output.")
            critique_result["suggestions"].append("Refactor the code to handle edge cases.")

        if critique_result["passed_quality_check"]:
            critique_result["critique_notes"].append("Output meets standard quality parameters.")

        self.review_logs.append(critique_result)
        return critique_result
      
