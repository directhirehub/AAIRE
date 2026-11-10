import ast
import os
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class QualityReport:
    passed: bool
    score: float
    issues: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SwarmQualityGate:
    """
    AAIRE के अनलिमिटेड एजेंट्स द्वारा जनरेट किए गए कोड, JSON और टेक्स्ट आउटपुट 
    को मेमोरी या प्रोडक्शन में सेव करने से पहले कड़ाई से चेक करता है।
    """

    FORBIDDEN_CALLS = {"eval", "exec", "os.system", "subprocess.Popen"}

    def __init__(self, min_score: Optional[float] = None):
        self.min_score = min_score or float(os.getenv("QUALITY_MIN_SCORE", "0.85"))
        self.strict_mode = os.getenv("QUALITY_GATE_STRICT", "true").lower() == "true"

    def validate_python_code(self, code_str: str) -> QualityReport:
        issues: List[str] = []
        score = 1.0

        if not code_str or len(code_str.strip()) < 10:
            return QualityReport(
                passed=False,
                score=0.0,
                issues=["Generated Python code is empty or too short."]
            )

        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            return QualityReport(
                passed=False,
                score=0.0,
                issues=[f"SyntaxError at line {e.lineno}: {e.msg}"]
            )

        func_count = 0
        empty_funcs = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_count += 1
                if len(node.body) == 1 and isinstance(node.body[0], (ast.Pass, ast.Ellipsis)):
                    empty_funcs += 1
                    issues.append(f"Function '{node.name}' is an empty stub (pass/...).")
                    score -= 0.25

            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_CALLS:
                    issues.append(f"Unsafe call '{node.func.id}' detected by Quality Gate.")
                    score -= 0.50

        if "TODO" in code_str or "FIXME" in code_str:
            issues.append("Unresolved TODO/FIXME markers found in output.")
            score -= 0.15

        final_score = max(0.0, round(score, 2))
        passed = (final_score >= self.min_score) and (not self.strict_mode or len(issues) == 0)

        return QualityReport(
            passed=passed,
            score=final_score,
            issues=issues,
            metrics={"functions_analyzed": func_count, "empty_stubs": empty_funcs}
        )

    def validate_agent_output(self, output: Any, expected_type: str = "text") -> QualityReport:
        if output is None:
            return QualityReport(passed=False, score=0.0, issues=["Agent returned None."])

        if expected_type == "python":
            return self.validate_python_code(str(output))

        if expected_type == "json":
            try:
                parsed = json.loads(output) if isinstance(output, str) else output
                if not parsed:
                    return QualityReport(passed=False, score=0.2, issues=["Empty JSON payload."])
                return QualityReport(passed=True, score=1.0, metrics={"keys": len(parsed)})
            except Exception as e:
                return QualityReport(passed=False, score=0.0, issues=[f"Invalid JSON: {str(e)}"])

        text_str = str(output).strip()
        if len(text_str) < 5:
            return QualityReport(passed=False, score=0.1, issues=["Output too brief or meaningless."])

        return QualityReport(passed=True, score=1.0, metrics={"length": len(text_str)})
  
