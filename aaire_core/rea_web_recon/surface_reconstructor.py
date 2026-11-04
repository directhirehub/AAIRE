import json
import re
import time
import urllib.request
from urllib.parse import urljoin

class SurfaceReconstructor:
    """50x Scratch-Built Web, Hydrated State, JS Route & Fact Reconstructor."""
    def __init__(self, byte_budget: int = 750_000):
        self.budget = byte_budget
        self.ua = "Mozilla/5.0 (compatible; AAIRE-REA-50X/10.0; +https://directhirehub.in)"

    def _clean(self, val: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(val))).strip()

    def reconstruct_target(self, url: str, category: str) -> dict:
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": self.ua, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=12) as res:
                raw = res.read(self.budget).decode("utf-8", errors="ignore")
        except Exception as e:
            return {"feed_category": category, "source_url": url, "status": f"ERR:{e}", "retained_facts": [], "verified_payload": []}

        routes = re.findall(r'["\']((?:https?://[^"\'\s]+|/[a-zA-Z0-9_\-/]+(?:/api/|/v\d+/|\.json)[^"\'\s]*))["\']', raw)
        facts = []
        if raw.lstrip().startswith(("{", "[")):
            try:
                parsed = json.loads(raw)
                rows = parsed if isinstance(parsed, list) else parsed.get("data", parsed.get("items", []))
                for r in (rows if isinstance(rows, list) else [])[:25]:
                    if isinstance(r, dict) and (r.get("title") or r.get("position")):
                        t = self._clean(r.get("title") or r.get("position"))
                        u = urljoin(url, str(r.get("url") or r.get("link") or url))
                        facts.append({"fact_text": t, "source_url": u, "category": category})
            except Exception:
                pass

        for item in re.findall(r"<(?:item|entry)[^>]*>(.*?)</(?:item|entry)>", raw, re.DOTALL | re.I)[:25]:
            tm = re.search(r"<title[^>]*>(.*?)</title>", item, re.DOTALL | re.I)
            lm = re.search(r"<link[^>]*>(.*?)</link>|<link[^>]+href=[\"']([^\"']+)[\"']", item, re.DOTALL | re.I)
            if tm:
                t = self._clean(re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", tm.group(1)))
                u = urljoin(url, (lm.group(1) or lm.group(2) if lm else url).strip())
                if len(t) > 7:
                    facts.append({"fact_text": t, "source_url": u, "category": category})

        for href, text in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', raw, re.DOTALL | re.I)[:40]:
            t, u = self._clean(text), urljoin(url, href)
            if len(t) > 14 and u.startswith("http"):
                facts.append({"fact_text": t, "source_url": u, "category": category})

        facts = facts[:25]
        return {
            "feed_category": category, "source_url": url,
            "status": "HEALED_AND_EXTRACTED" if facts else "EMPTY",
            "self_healed_strategy": "rea_50x_polyglot_surface",
            "extraction_latency_ms": round((time.time() - t0) * 1000, 2),
            "discovered_routes": sorted(list(set(routes)))[:12],
            "item_count": len(facts), "retained_facts": facts,
            "verified_payload": list(dict.fromkeys([f["source_url"] for f in facts]))[:20]
          }
      
