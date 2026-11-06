import hashlib

class MagicFileDetector25:
    """Detects 25 File & Artifact Types via Magic Bytes and Structural Signatures."""
    MAGIC_MAP_25 = {
        b"\x7fELF": "elf_binary", b"MZ": "pe_windows", b"\xfe\xed\xfa\xce": "macho_32",
        b"\xfe\xed\xfa\xcf": "macho_64", b"\xca\xfe\xba\xbe": "macho_fat", b"dex\n": "android_dex",
        b"\x03\x00\x08\x00": "android_axml", b"\x02\x00\x0c\x00": "android_arsc",
        b"PK\x03\x04": "zip_apk_jar_ipa", b"\x1f\x8b\x08": "gzip_tar_archive",
        b"\x00asm": "wasm_module", b"SQLite format 3": "sqlite_database",
        b"GGUF": "gguf_ai_model", b"FOR1": "erlang_beam", b"GDPC": "godot_pck",
        b"\xaf\x1b\xb1\xfa": "unity_il2cpp", b"MEI\x0c\x0b\x0a\x0b\x0e": "pyinstaller_pkg",
        b"\xd4\xc3\xb2\xa1": "pcap_le", b"\xa1\xb2\xc3\xd4": "pcap_be",
        b"\x0a\x0d\x0d\x0a": "pcapng_capture", b"\x04\x00\x00\x00": "electron_asar",
        b"//!": "ptx_gpu_shader", b"\x7fCUBA": "cubin_gpu", b"0x60806040": "evm_bytecode",
        b"{\"log\"": "har_network_capture"
    }

    def sniff_artifact(self, raw_bytes: bytes) -> dict:
        detected = "unknown_or_source_text"
        for sig, kind in self.MAGIC_MAP_25.items():
            if raw_bytes.startswith(sig) or sig in raw_bytes[:64]:
                detected = kind
                break
        if detected == "unknown_or_source_text":
            sample = raw_bytes[:256].decode("utf-8", errors="ignore").lower()
            if "safetensors" in sample or "__metadata__" in sample:
                detected = "safetensors_model"
            elif "incident_id" in sample or "bug_type" in sample:
                detected = "apple_ips_crash"
        return {
            "detected_kind": detected,
            "supported_detectors": 25,
            "size_bytes": len(raw_bytes),
            "sha256": hashlib.sha256(raw_bytes).hexdigest()[:20]
        }
      
