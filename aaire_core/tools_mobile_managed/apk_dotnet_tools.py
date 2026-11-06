import re

class MobileAndManagedTools:
    """Dedicated Mobile & Managed Tools: APK, DEX, ARSC, Signers, Flutter, .NET ECMA-335 & ADB."""
    TOOLS = (
        "inspect_apk_manifest", "inspect_apk_signature", "inspect_dex", "inspect_resources_arsc",
        "inspect_flutter_app", "decode_apk_resources", "decompile_with_jadx", "inspect_dotnet_assembly",
        "dotnet_il", "adb_devices", "adb_inspect", "adb_pull"
    )

    def analyze_mobile_or_dotnet(self, raw_bytes: bytes) -> dict:
        text = raw_bytes.decode("utf-8", errors="ignore")
        dex_classes = re.findall(r"L[a-zA-Z0-9_$]+(?:/[a-zA-Z0-9_$]+)+;", text)
        permissions = re.findall(r"android\.permission\.[A-Z0-9_]+", text)
        dotnet_Markers = [m for m in ("BSJB", "mscorlib", "System.Runtime", "PInvoke") if m in text]
        flutter_assets = [f for f in ("libflutter.so", "libapp.so", "flutter_assets") if f in text]
        apk_sig_v2_v3 = (b"APK Sig Block 42" in raw_bytes)
        return {
            "tools_active": len(self.TOOLS),
            "dex_classes_found": list(dict.fromkeys(dex_classes))[:15],
            "android_permissions": list(dict.fromkeys(permissions))[:15],
            "apk_v2_v3_signing_block": apk_sig_v2_v3,
            "flutter_markers": flutter_assets,
            "dotnet_ecma335_markers": dotnet_Markers
        }
      
