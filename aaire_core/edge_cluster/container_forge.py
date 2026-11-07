import json
import os
import time

class AAIREContainerForge:
    """Scratch-Built Containerization & Multi-Node Deployment Synthesizer."""
    def __init__(self, root_dir: str):
        self.out_dir = os.path.join(root_dir, "aaire_storage", "generated_projects")
        os.makedirs(self.out_dir, exist_ok=True)

    def synthesize_cluster_spec(self, cluster_name: str = "aaire-agi-grid", nodes: int = 3) -> dict:
        dockerfile = (
            "FROM python:3.11-slim\n"
            "WORKDIR /aaire\n"
            "COPY aaire_core/ ./aaire_core/\n"
            "COPY aaire_storage/ ./aaire_storage/\n"
            "ENV PYTHONUNBUFFERED=1 AAIRE_NODE_ROLE=worker\n"
            "USER 1000:1000\n"
            "CMD [\"python3\", \"aaire_core/master_orchestrator.py\", \"auto\"]\n"
        )
        services = {
            f"node_{i}": {
                "build": ".",
                "restart": "unless-stopped",
                "mem_limit": "256m",
                "environment": [f"NODE_ID=aaire_node_{i}", "CLUSTER_MODE=autonomous"]
            } for i in range(1, nodes + 1)
        }
        spec = {
            "cluster": cluster_name,
            "generated_at": round(time.time(), 2),
            "dockerfile": dockerfile,
            "compose_services": services
        }
        out_path = os.path.join(self.out_dir, "cluster_deployment_spec.json")
        with open(out_path, "w", encoding="utf-8") as fp:
            json.dump(spec, fp, indent=2)
        return {"status": "CONTAINER_SPEC_READY", "nodes_configured": nodes, "artifact": "aaire_storage/generated_projects/cluster_deployment_spec.json"}
      
