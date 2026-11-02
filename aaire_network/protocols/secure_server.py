#!/usr/bin/env python3
"""Local Secure HTTPS Server using Python standard libraries."""
from __future__ import annotations
import http.server
import ssl
from pathlib import Path

class SecureHTTPServer:
    def __init__(self, host: str = "localhost", port: int = 4433, cert_dir: Path = Path(".")) -> None:
        self.host = host
        self.port = port
        self.cert_file = cert_dir / "cert.pem"
        self.key_file = cert_dir / "key.pem"

    def run_server(self) -> None:
        server_address = (self.host, self.port)
        httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=str(self.cert_file), keyfile=str(self.key_file))
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        print(f"Secure HTTPS Server running at https://{self.host}:{self.port}")
        httpd.serve_forever()
      
