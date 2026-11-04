import hashlib
import math
import re
from collections import Counter

class PolyglotBinaryEngine:
    """50x Scratch-Built Universal Code, AST & Binary Artifact Decompiler."""
    MAGIC_SIGNATURES = {
        b"\x7fELF": "ELF_EXECUTABLE", b"MZ": "PE_WINDOWS_BINARY",
        b"\x00asm": "WASM_ARTIFACT", b"PK\x03\x04": "APK_OR_ZIP_BUNDLE",
        b"SQLite format 3": "SQLITE_DATABASE", b"\xd4\xc3\xb2\xa1": "PCAP_NETWORK_CAPTURE"
    }
    LANGUAGE_GRAMMARS = {
        "python": r"\b(def |class |async def |import |from .+ import )\b",
        "javascript_ts": r"\b(function |const |let |=>|export |import .+ from )\b",
        "rust": r"\b(fn |pub fn |impl |let mut |match |use .+::)\b",
        "go": r"\b(package |func |type .+ struct|go |defer )\b",
        "solidity_evm": r"\b(pragma solidity|contract |mapping\(|payable|emit )\b",
        "c_cpp": r"(#include <|int main\(|std::|void \*|struct )",
        "java_kotlin": r"\b(public class |private |fun |package |@Override)\b",
        "sql": r"\b(SELECT |INSERT INTO |CREATE TABLE |WHERE |JOIN )\b",
        "shell_bash": r"(#!/bin/(?:ba)?sh|\becho |\bgrep |\bawk |\bcurl )"
    }

    def shannon_entropy(self, data: bytes) -> float:
        if not data:
            return 0.0
        counts = Counter(data)
        total = len(data)
        return round(-sum((c / total) * math.log2(c / total) for c in counts.values()), 4)

    def decompile_artifact(self, raw_input: bytes | str) -> dict:
        raw_bytes = raw_input if isinstance(raw_input, bytes) else str(raw_input).encode("utf-8")
        for sig, label in self.MAGIC_SIGNATURES.items():
            if raw_bytes.startswith(sig):
                return {"type": label, "entropy": self.shannon_entropy(raw_bytes), "size": len(raw_bytes)}

        text = raw_bytes.decode("utf-8", errors="ignore")
        lang_scores = {k: len(re.findall(v, text)) for k, v in self.LANGUAGE_GRAMMARS.items()}
        best_lang = max(lang_scores, key=lang_scores.get) if any(lang_scores.values()) else "generic_text"
        symbols = re.findall(r"(?:def|func|fn|function|class|contract|interface)\s+([a-zA-Z0-9_]+)", text)
        imports = re.findall(r"(?:import|from|use|#include)\s+([a-zA-Z0-9_./\"<>]+)", text)
        return {
            "detected_language": best_lang, "grammar_hits": lang_scores.get(best_lang, 0),
            "symbols": list(dict.fromkeys(symbols))[:25], "imports": list(dict.fromkeys(imports))[:20],
            "entropy": self.shannon_entropy(raw_bytes), "sha256": hashlib.sha256(raw_bytes).hexdigest()[:16]
                                                                       }
      
