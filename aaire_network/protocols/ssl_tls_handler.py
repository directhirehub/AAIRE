#!/usr/bin/env python3
"""Module to generate free Self-Signed SSL/TLS certificates using OpenSSL."""
from __future__ import annotations
import subprocess
from pathlib import Path

class SSLHandler:
    @staticmethod
    def generate_self_signed_cert(cert_file: Path, key_file: Path) -> bool:
        cert_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "openssl", "req", "-x509", "-newkey", "rsa:4096",
            "-keyout", str(key_file),
            "-out", str(cert_file),
            "-days", "365",
            "-nodes",
            "-subj", "/CN=localhost"
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            return False
          
