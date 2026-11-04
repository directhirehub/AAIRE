import json
import math
import os
import re
import time
from collections import Counter
from aaire_core.rea_decompiler.polyglot_binary_engine import PolyglotBinaryEngine

class QuantumSynthesizer:
    """50x Self-Learning BM25 Reasoner & Pattern Memory Synthesizer."""
    def __init__(self, root_dir: str):
        self.root = root_dir
        self.decompiler = PolyglotBinaryEngine()
        self.stops = {"the", "is", "in", "of", "and", "to", "for", "with", "on", "at"}

    def tokenize(self, text: str) -> list:
        return [w for w in re.findall(r"[a-zA-Z0-9_+#.-]{2,}", str(text).lower()) if w not in self.stops]

    def learn_and_record(self, feeds: list):
        pat_path = os.path.join(self.root, "aaire_storage", "learned_patterns.json")
        mem_path = os.path.join(self.root, "aaire_storage", "aaire_memory", "episodic_memory.json")
        os.makedirs(os.path.dirname(mem_path), exist_ok=True)

        vocab = Counter(tok for f in feeds for rf in f.get("retained_facts", []) for tok in self.tokenize(rf.get("fact_text", "")))
        patterns = {"updated_at": round(time.time(), 2), "top_learned_tokens": dict(vocab.most_common(35))}
        with open(pat_path, "w", encoding="utf-8") as fp:
            json.dump(patterns, fp, indent=2, ensure_ascii=False)

        episode = {"timestamp": round(time.time(), 2), "sources_learned": len(feeds), "dominant_concepts": list(patterns["top_learned_tokens"].keys())[:10]}
        with open(mem_path, "w", encoding="utf-8") as fp:
            json.dump({"latest_rea_episode": episode}, fp, indent=2, ensure_ascii=False)

    def synthesize(self, query_or_code: str, vault: dict, top_k: int = 6) -> dict:
        artifact = self.decompiler.decompile_artifact(query_or_code)
        if artifact.get("grammar_hits", 0) >= 2 or "type" in artifact:
            return {"mode": "REA_POLYGLOT_DECOMPILATION", "result": artifact}

        nodes = [{"fact": rf["fact_text"], "url": rf["source_url"], "trust": f.get("bayesian_trust_score", 0.9), "tok": self.tokenize(rf["fact_text"])}
                 for f in vault.get("feeds", []) for rf in f.get("retained_facts", [])]
        q_tok = self.tokenize(query_or_code)
        if not nodes or not q_tok:
            return {"mode": "VAULT_SNAPSHOT", "matches": nodes[:top_k]}

        n_docs, avg_dl = len(nodes), sum(len(d["tok"]) for d in nodes) / max(1, len(nodes))
        scored = []
        for d in nodes:
            c = Counter(d["tok"])
            s = sum(math.log(1 + (n_docs - sum(1 for x in nodes if qt in x["tok"]) + 0.5) / (sum(1 for x in nodes if qt in x["tok"]) + 0.5)) *
                    ((c[qt] * 2.5) / (c[qt] + 1.5 * (0.25 + 0.75 * len(d["tok"]) / max(1, avg_dl)))) for qt in set(q_tok) if qt in c)
            if s > 0:
                scored.append((round(s * d["trust"], 4), d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return {"mode": "REA_50X_SYNTHESIS", "query": query_or_code, "matches": [{"score": s, "fact": d["fact"], "url": d["url"]} for s, d in scored[:top_k]]}
      
