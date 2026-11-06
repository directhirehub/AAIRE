import re

class Skills11AndMCPServer:
    """11 Investigation Skills, EN/HI/Hinglish Local Intent Parser & MCP Server inside aaire_core."""
    SKILLS_11 = (
        "reverse-engineer-anything", "native-binary-triage", "android-apk-audit",
        "electron-feature-trace", "network-to-environment", "packet-capture-triage",
        "firmware-triage", "crash-triage", "model-artifact-inspect",
        "smart-contract-triage", "web-app-recon"
    )
    INTENT_RULES = {
        "STATUS": ("status", "stats", "haal", "backup"),
        "ANALYZE": ("analyze", "jaanch", "decompile", "scan", ".apk", ".elf"),
        "BUILD": ("build", "create", "website", "ui", "ux", "banao"),
        "FEED": ("news", "khabar", "jobs", "latest", "updates")
    }

    def parse_local_intent(self, prompt: str) -> dict:
        tokens = re.findall(r"[a-zA-Z0-9_./]+", prompt.lower())
        detected = "SEARCH"
        for intent, words in self.INTENT_RULES.items():
            if any(w in prompt.lower() for w in words):
                detected = intent
                break
        return {"intent": detected, "tokens": tokens[:12], "skills_available": len(self.SKILLS_11)}

    def handle_mcp_rpc(self, method: str, params: dict) -> dict:
        if method == "tools/list":
            return {"jsonrpc": "2.0", "result": {"total_tools": 59, "skills": list(self.SKILLS_11)}}
        return {"jsonrpc": "2.0", "result": {"intent_parsed": self.parse_local_intent(params.get("prompt", "status"))}}
      
