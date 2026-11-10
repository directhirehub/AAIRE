# File: aaire_core/skill_manager.py

from typing import Callable, Dict, Any, Optional

class AAIREAutoSkillManager:
    """
    AAIRE के लिए 100% ओरिजिनल डायनामिक स्किल बंडल और प्लगइन मैनेजर।
    यह एजेंट्स के लिए नई क्षमताओं और स्किल्स को रजिस्टर और एक्सेक्यूट करता है।
    """
    def __init__(self):
        self.skills: Dict[str, Callable[..., Any]] = {}

    def register_skill(self, skill_name: str, func: Callable[..., Any]):
        """
        किसी नए स्किल या प्लगइन को सिस्टम में रजिस्टर करता है।
        """
        self.skills[skill_name] = func

    def execute_skill(self, skill_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        रजिस्टर किए गए स्किल को उसके नाम से कॉल करता है।
        """
        if skill_name in self.skills:
            try:
                return self.skills[skill_name](*args, **kwargs)
            except Exception as e:
                return {"status": "FAILED", "error": str(e)}
        return {"status": "NOT_FOUND", "error": f"Skill '{skill_name}' is not registered."}

    def list_skills(self) -> list:
        """
        उपलब्ध सभी स्किल्स की सूची देता है।
        """
        return list(self.skills.keys())
      
