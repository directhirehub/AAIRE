import json
import os

class VisualTelemetryStudio:
    """Generates Interactive HTML/SVG Visual Telemetry & Node Topology Demos from Scratch."""
    def __init__(self, root_dir: str):
        self.out_dir = os.path.join(root_dir, "aaire_storage", "generated_projects")
        os.makedirs(self.out_dir, exist_ok=True)

    def render_visual_dashboard(self, hw_metrics: dict, cluster_info: dict) -> dict:
        node = hw_metrics.get("node_id", "local_master")
        cores = hw_metrics.get("cpu_cores", 1)
        free_gb = hw_metrics.get("disk_free_gb", 10.0)
        nodes_n = cluster_info.get("nodes_configured", 3)

        html = (
            "<!DOCTYPE html><html><head><meta charset='utf-8'><title>AAIRE Live Telemetry</title>"
            "<script src='https://cdn.tailwindcss.com'></script></head>"
            "<body class='bg-slate-950 text-cyan-400 p-8 font-mono'>"
            f"<h1 class='text-2xl font-bold mb-6'>⚡ AAIRE Edge Supervisor & Node Topology ({node})</h1>"
            "<div class='grid grid-cols-3 gap-4 mb-6'>"
            f"<div class='p-4 bg-slate-900 border border-cyan-500/40 rounded-xl'>CPU Cores: <b class='text-white'>{cores}</b></div>"
            f"<div class='p-4 bg-slate-900 border border-emerald-500/40 rounded-xl'>Free Disk: <b class='text-white'>{free_gb} GB</b></div>"
            f"<div class='p-4 bg-slate-900 border border-purple-500/40 rounded-xl'>Active Cluster Nodes: <b class='text-white'>{nodes_n}</b></div>"
            "</div><svg viewBox='0 0 400 100' class='w-full bg-slate-900 rounded-xl border border-slate-800 p-4'>"
            "<line x1='70' y1='50' x2='200' y2='50' stroke='#22d3ee' stroke-width='2'/>"
            "<line x1='200' y1='50' x2='330' y2='50' stroke='#10b981' stroke-width='2'/>"
            "<circle cx='70' cy='50' r='18' fill='#0891b2'/><circle cx='200' cy='50' r='22' fill='#059669'/><circle cx='330' cy='50' r='18' fill='#7c3aed'/>"
            "</svg></body></html>"
        )
        out_file = os.path.join(self.out_dir, "telemetry_visual_demo.json")
        with open(out_file, "w", encoding="utf-8") as fp:
            json.dump({"visual_engine": "AAIRE-Visual-Telemetry-v1", "metrics": hw_metrics, "html_preview": html}, fp, indent=2)
        return {"status": "VISUAL_DEMO_RENDERED", "saved_to": "aaire_storage/generated_projects/telemetry_visual_demo.json"}
      
