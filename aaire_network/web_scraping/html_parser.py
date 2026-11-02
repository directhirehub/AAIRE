#!/usr/bin/env python3
"""Lightweight regex-based HTML content extractor."""
from __future__ import annotations
import re
from typing import List

class HTMLParserUtil:
    @staticmethod
    def extract_links(html_content: str) -> List[str]:
        return re.findall(r'href=[\"\'](https?://[^\"\']+)[\"\']', html_content)
      
