# File: aaire_core/error_classifier.py

import sys
import traceback
from typing import Dict, Any, Optional

class AAIREErrorClassifier:
    """
    AAIRE के लिए 100% ओरिजिनल एरर क्लासिफायर और रिकवरी एडवाइजर।
    यह एक्सेक्यूशंस के दौरान आने वाली त्रुटियों का वर्गीकरण करता है और समाधान सुझाता है।
    """
    def __init__(self):
        self.error_logs: list = []

    def classify_and_prescribe(self, exception: Exception) -> Dict[str, Any]:
        """
        एरर को एनालाइज करके उसका प्रकार और रिकवरी एक्शन बताता है।
        """
        err_type = type(exception).__name__
        err_msg = str(exception)
        tb_details = traceback.format_exc()

        diagnosis = {
            "error_type": err_type,
            "message": err_msg,
            "category": "UNKNOWN",
            "suggested_action": "manual_review",
            "auto_retry_safe": False
        }

        # एरर की श्रेणी तय करना
        if "SyntaxError" in err_type or "IndentationError" in err_type:
            diagnosis["category"] = "SYNTAX_ERROR"
            diagnosis["suggested_action"] = "fix_code_structure"
            diagnosis["auto_retry_safe"] = False
        elif "Timeout" in err_type or "Connection" in err_type:
            diagnosis["category"] = "NETWORK_ERROR"
            diagnosis["suggested_action"] = "exponential_backoff_retry"
            diagnosis["auto_retry_safe"] = True
        elif "Memory" in err_type or "Alloc" in err_msg:
            diagnosis["category"] = "RESOURCE_OVERFLOW"
            diagnosis["suggested_action"] = "trigger_context_compression"
            diagnosis["auto_retry_safe"] = True
        else:
            diagnosis["category"] = "RUNTIME_EXCEPTION"
            diagnosis["suggested_action"] = "inspect_stack_trace"
            diagnosis["auto_retry_safe"] = False

        self.error_logs.append(diagnosis)
        return diagnosis
      
