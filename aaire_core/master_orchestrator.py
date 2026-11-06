import json
import os
import sys
import time
import urllib.request

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from aaire_core.security_crypto.cross_os_vault import CrossOSVaultGuard
from aaire_core.detector_25.magic_sniffer import MagicFileDetector25
from aaire_core.tools_binaries.native_inspectors import NativeBinaryInspectors
from aaire_core.tools_mobile_managed.apk_dotnet_tools import MobileAndManagedTools
from aaire_core.tools_web_js_data.app_data_tools import WebJSAndDataModelTools
from aaire_core.tools_missing_4.completed_four import CompletedMissingFourTools
from aaire_core.tools_partial_13.completed_thirteen import CompletedPartialThirteenTools
from aaire_core.skills_11_mcp.mcp_skills_hub import Skills11AndMCPServer
from aaire_core.agi_synthesizer.true_generator import TrueDynamicAGISynthesizer

class AAIREMasterBrain:
    def __init__(self):
        self.guard = CrossOSVaultGuard()
        self.partial13 = CompletedPartialThirteenTools()
        self.missing4 = CompletedMissingFourTools()
        self.mcp = Skills11AndMCPServer()
        self.synth = TrueDynamicAGISynthesizer(ROOT_DIR)

    def run_unified_kernel(self, mode: str = "auto", prompt: str = "") -> dict:
        t0 = time.time()
        sample = (prompt or "\x7fELF_AAIRE_V12").encode("utf-8")
        matrix = {
            "detector_25": MagicFileDetector25().sniff_artifact(sample)["detected_kind"],
            "binary_tools": NativeBinaryInspectors().inspect_binary_surface(sample)["tools_active"],
            "mobile_dotnet_tools": MobileAndManagedTools().analyze_mobile_or_dotnet(sample)["tools_active"],
            "web_js_data_tools": WebJSAndDataModelTools().inspect_js_and_models(sample)["tools_active"],
            "missing_4_completed": self.missing4.decompile_native_pseudocode(sample)["status"],
            "partial_13_completed": self.partial13.decompile_pyinstaller_bytecode("x = 42")["status"],
            "mcp_and_11_skills": self.mcp.parse_local_intent(prompt or "status")["intent"],
            "dynamic_synthesizer": self.synth.generate_fullstack_app(prompt or "career job portal")["status"]
        }
        seal = self.guard.create_public_seal(json.dumps(matrix, sort_keys=True).encode("utf-8"))
        report = {"version": "AAIRE-v12.0-Unified-59Tools", "os": self.guard.os_name, "latency_ms": round((time.time() - t0) * 1000, 2), "seal": seal, "modules": matrix}
        os.makedirs(os.path.join(ROOT_DIR, "aaire_storage", "aaire_backup"), exist_ok=True)
        with open(os.path.join(ROOT_DIR, "aaire_storage", "aaire_backup", "latest_state_snapshot.json"), "w", encoding="utf-8") as fp:
            json.dump(report, fp, indent=2)
        return report

if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "auto"
    p = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    print(json.dumps(AAIREMasterBrain().run_unified_kernel(m, p), indent=2, ensure_ascii=False))
    
