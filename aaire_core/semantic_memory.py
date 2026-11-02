#!/usr/bin/env python3
"""Local TF-IDF Vector Search & SQLite Episodic Memory Engine."""
from __future__ import annotations
import json
import math
import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


class SemanticMemoryEngine:
    def __init__(self, db_path: Path = Path("aaire_storage/aaire_memory/semantic_vault.db")) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tokens_json TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    @staticmethod
    def _tokenize(text: str) -> Counter:
        words = re.findall(r"[a-zA-Z0-9_]{2,}", text.lower())
        return Counter(words)

    def store_memory(self, topic: str, content: str) -> int:
        token_counts = dict(self._tokenize(f"{topic} {content}"))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO memories (topic, content, tokens_json) VALUES (?, ?, ?)",
                (topic, content, json.dumps(token_counts))
            )
            return int(cursor.lastrowid or 0)

    @staticmethod
    def _cosine_similarity(vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        common = set(vec1.keys()) & set(vec2.keys())
        numerator = sum(vec1[k] * vec2[k] for k in common)
        sum1 = sum(v ** 2 for v in vec1.values())
        sum2 = sum(v ** 2 for v in vec2.values())
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return (numerator / denominator) if denominator else 0.0

    def recall(self, query: str, top_k: int = 3) -> List[Tuple[float, str, str]]:
        query_vec = dict(self._tokenize(query))
        results: List[Tuple[float, str, str]] = []
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT topic, content, tokens_json FROM memories").fetchall()
            for topic, content, tokens_json in rows:
                doc_vec = json.loads(tokens_json)
                score = self._cosine_similarity(query_vec, doc_vec)
                if score > 0.0:
                    results.append((round(score, 4), topic, content))
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]
