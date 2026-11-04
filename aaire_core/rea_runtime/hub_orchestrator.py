import json
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from aaire_core.rea_web_recon.surface_reconstructor import SurfaceReconstructor
from aaire_core.rea_intelligence.quantum_synthesizer import QuantumSynthesizer
from aaire_core.rea_ledger.vault_bridge import VaultStorageBridge

DEFAULT_TARGETS = [
    {"url": "https://news.ycombinator.com/rss", "category": "global_tech_intelligence"},
    {"url": "https://hnrss.org/newest?points=50", "category": "global_tech_intelligence"},
    {"url": "https://remoteok.com/api", "category": "verified_job_openings"},
    {"url": "https://www.arbeitnow.com/api/job-board-api", "category": "verified_job_openings"},
    {"url": "https://arxiv.org/rss/cs.AI", "category": "autonomous_ai_research"}
]

def execute_50x_pipeline():
    recon = SurfaceReconstructor()
    feeds = [recon.reconstruct_target(t["url"], t["category"]) for t in DEFAULT_TARGETS]
    brain = QuantumSynthesizer(ROOT_DIR)
    brain.learn_and_record(feeds)
    bridge = VaultStorageBridge(ROOT_DIR)
    vault = bridge.commit_vault_and_backup(feeds)
    print(f"⚡ [AAIRE-REA 50X READY] Facts: {vault['total_retained_facts']} | Merkle: {vault['cryptographic_proof']['merkle_root'][:16]}")

def run_query(user_input: str):
    feed_path = os.path.join(ROOT_DIR, "aaire_storage", "verified_oracle_feed.json")
    vault = json.load(open(feed_path, "r", encoding="utf-8")) if os.path.exists(feed_path) else {}
    return QuantumSynthesizer(ROOT_DIR).synthesize(user_input, vault)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(run_query(" ".join(sys.argv[1:])), indent=2, ensure_ascii=False))
    else:
        execute_50x_pipeline()
      
