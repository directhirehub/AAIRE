#!/usr/bin/env python3
"""AAIRE v4.1 - Network Integration Test Script"""
from pathlib import Path

# Network modules import
from aaire_network.protocols.ssl_tls_handler import SSLHandler
from aaire_network.protocols.https_client import HTTPSClient
from aaire_network.security_auth.traffic_guard import TrafficGuard


def test_network_integration():
    print("=== AAIRE Network Integration Test Shuru Ho Raha Hai ===")

    # 1. SSL Certificate Test
    cert_path = Path("cert.pem")
    key_path = Path("key.pem")
    assert SSLHandler.generate_self_signed_cert(cert_path, key_path), "SSL Generation Failed"
    print("[✔] SSL/TLS Self-Signed Certificates successfully generated!")

    # 2. Traffic Guard Test
    test_payload = "Hello AAIRE, secure system active."
    assert TrafficGuard.inspect_payload(test_payload), "Traffic Guard blocked safe payload"
    print("[✔] Traffic Guard: Payload is safe and clean.")

    # 3. HTTPS Client Test
    target_url = "https://httpbin.org/get"
    success, response = HTTPSClient.get(target_url)
    assert success, f"HTTPS Connection Error: {response}"
    print(f"[✔] HTTPS Client Connected Successfully! Response length: {len(response)} characters")

    print("=== Integration Test Safal Raha ===")


if __name__ == "__main__":
    test_network_integration()
  
