#!/usr/bin/env python3
"""Autonomous Web Spider & SQLite Knowledge Graph Builder."""
from __future__ import annotations
import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Tuple
from urllib.parse import urlparse

from aaire_network.protocols.https_client import HTTPSClient
from aaire_network.web_scraping.html_parser import HTMLParserUtil


class KnowledgeGraphSpider:
    def __init__(self, db_path: Path = Path("aaire_storage/aaire_memory/knowledge_graph.db")) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_graph_db()

    def _init_graph_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    url TEXT PRIMARY KEY,
                    domain TEXT,
                    title TEXT,
                    summary TEXT,
                    crawled_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    source_url TEXT,
                    target_url TEXT,
                    UNIQUE(source_url, target_url)
                )
            """)

    @staticmethod
    def _extract_title_and_text(html: str) -> Tuple[str, str]:
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Untitled"
        clean_text = re.sub(r"<[^>]+>", " ", html)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        return title[:120], clean_text[:500]

    def crawl_and_index(self, seed_url: str, max_edges: int = 15) -> Dict[str, Any]:
        ok, html = HTTPSClient.get(seed_url, timeout=10)
        if not ok or not html:
            return {"status": "ERROR", "url": seed_url, "reason": html}

        domain = urlparse(seed_url).netloc
        title, summary = self._extract_title_and_text(html)
        links: List[str] = HTMLParserUtil.extract_links(html)[:max_edges]

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO nodes (url, domain, title, summary) VALUES (?, ?, ?, ?)",
                (seed_url, domain, title, summary)
            )
            for target in links:
                conn.execute(
                    "INSERT OR IGNORE INTO edges (source_url, target_url) VALUES (?, ?)",
                    (seed_url, target)
                )

        return {"status": "INDEXED", "url": seed_url, "title": title, "edges_mapped": len(links)}
      
