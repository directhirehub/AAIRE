import ast
import json
import os
import re

class TrueDynamicAGISynthesizer:
    """Generates AST-Verified Python Backend & Responsive UI/UX Code Dynamically from Prompts."""
    def __init__(self, root_dir: str):
        self.out_dir = os.path.join(root_dir, "aaire_storage", "generated_projects")
        os.makedirs(self.out_dir, exist_ok=True)

    def generate_fullstack_app(self, prompt: str) -> dict:
        words = [w for w in re.findall(r"[a-zA-Z]{3,}", prompt.lower()) if w not in {"build", "create", "for", "and", "the"}]
        cls_name = "".join(w.title() for w in (words[:2] or ["Aaire", "Portal"]))
        fields = words[1:4] or ["title", "category", "trust_score"]

        py_src = (
            "from dataclasses import dataclass, asdict\n\n"
            f"@dataclass\nclass {cls_name}Entity:\n" +
            "".join(f"    {f}: str = 'active'\n" for f in fields) +
            f"\ndef serve_{cls_name.lower()}(req: dict) -> dict:\n"
            f"    return {{'service': '{cls_name}', 'schema': asdict({cls_name}Entity()), 'req': req}}\n"
        )
        ast.parse(py_src)

        ui_cards = "".join(f"<div class='p-4 rounded-xl bg-slate-900 border border-emerald-500/30'>{f.title()}</div>" for f in fields)
        html_src = f"<!DOCTYPE html><html><head><script src='https://cdn.tailwindcss.com'></script></head><body class='bg-slate-950 text-white p-8'><h1 class='text-3xl font-bold text-emerald-400'>{cls_name}</h1><div class='grid grid-cols-3 gap-4 mt-6'>{ui_cards}</div></body></html>"

        out_file = os.path.join(self.out_dir, f"{cls_name.lower()}.json")
        with open(out_file, "w", encoding="utf-8") as fp:
            json.dump({"app": cls_name, "python_code": py_src, "html_ui": html_src}, fp, indent=2)
        return {"status": "AST_VERIFIED_APP_GENERATED", "app": cls_name, "fields": fields}
      
