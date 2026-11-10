# File: aaire_core/approval_gate.py

from typing import Dict, Any

class AAIREApprovalGate:
    """
    AAIRE के लिए 100% ओरिजिनल ह्यूमन-इन-द-लूप अप्रूवल गेटवे।
    यह संवेदनशील ऑपरेशंस या डिप्लॉयमेंट से पहले सुरक्षा और अनुमति (Approval) सुनिश्चित करता है।
    """
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode

    def request_approval(self, action_name: str, payload_summary: str, auto_approve: bool = False) -> Dict[str, Any]:
        """
        किसी संवेदनशील टास्क के लिए अप्रूवल मांगता है या ऑटो-अप्रूव मोड की जाँच करता है।
        """
        if auto_approve:
            return {
                "action": action_name,
                "status": "approved",
                "mode": "auto_approved",
                "message": f"Action '{action_name}' was automatically approved."
            }

        # नॉन-इंटरएक्टिव या ऑटोमैटिक एनवायरनमेंट के लिए डिफिकल्ट गेट
        if self.strict_mode:
            # ऑटोनॉमस रन के दौरान लॉगिंग और सेफ स्टेट ट्रैक करने के लिए
            return {
                "action": action_name,
                "status": "pending_or_logged",
                "summary": payload_summary,
                "message": f"Approval requested for '{action_name}'. Strict mode is active."
            }
        
        return {
            "action": action_name,
            "status": "approved",
            "message": f"Action '{action_name}' approved by default policy."
        }
      
