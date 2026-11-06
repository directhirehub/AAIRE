import math
import re
from collections import Counter

class NativeBinaryInspectors:
    """Dedicated Binary Tools: ELF, PE, Mach-O, Go, Rust, Kernel .ko, GPU, Firmware, Strings & Entropy."""
    TOOLS = (
        "inspect_elf", "inspect_pe", "inspect_macho", "inspect_go_binary", "inspect_rust_binary",
        "inspect_kernel_module", "inspect_gpu_code", "extract_strings", "scan_entropy",
        "hexdump", "firmware_scan", "carve_region", "disassemble", "inspect_desktop_installation"
    )

    def scan_entropy(self, data: bytes) -> float:
        if not data:
            return 0.0
        counts = Counter(data)
        n = len(data)
        return round(-sum((c / n) * math.log2(c / n) for c in counts.values()), 4)

    def inspect_binary_surface(self, data: bytes) -> dict:
        text = data.decode("utf-8", errors="ignore")
        ascii_strings = re.findall(r"[ -~]{5,}", text)[:25]
        urls = [s for s in ascii_strings if "http://" in s or "https://" in s]
        go_ver = re.findall(r"go1\.\d+(?:\.\d+)?", text)
        rust_crates = re.findall(r"[a-z0-9_]+-\d+\.\d+\.\d+", text)
        ko_modinfo = re.findall(r"(?:license|author|depends|vermagic)=[^\x00]+", text)
        fw_markers = [name for sig, name in [(b"\x1f\x8b", "gzip"), (b"hsqs", "squashfs"), (b"UBI#", "ubi")] if sig in data]
        return {
            "tools_active": len(self.TOOLS),
            "entropy": self.scan_entropy(data),
            "go_build_info": go_ver[:3],
            "rust_crates": rust_crates[:8],
            "kernel_modinfo": ko_modinfo[:5],
            "firmware_containers": fw_markers,
            "notable_urls": urls[:10],
            "hexdump_head": data[:16].hex()
        }
      
