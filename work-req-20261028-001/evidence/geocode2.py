"""Re-run Nominatim queries capturing per-query retrieved_at (Asia/Shanghai).
Overwrites evidence/nominatim/*.json; final sha256 is computed at build time from disk."""
import json, subprocess, time, urllib.parse, os
from datetime import datetime, timezone, timedelta

QUERIES = [
    ("Aker Stadion", "Molde"),
    ("Romssa Arena", "Tromsø"),
    ("Aspmyra Stadion", "Bodø"),
    ("Brann Stadion", "Bergen"),
    ("Briskeby Arena", "Hamar"),
    ("Color Line Stadion", "Ålesund"),
    ("Haugesund Sparebank Arena", "Haugesund"),
    ("Haugesund Stadion", "Haugesund"),          # retry: sponsor name returned 0
    ("Intility Arena", "Oslo"),
    ("J.J. Ugland Stadion", "Grimstad"),         # 0 results, kept as evidence of miss
    ("Levermyr Stadion", "Grimstad"),            # retry: location name for Jerv ground
    ("Kristiansund Stadion", "Kristiansund"),
    ("Lerkendal Stadion", "Trondheim"),
    ("Marienlyst Stadion", "Drammen"),
    ("Nadderud Stadion", "Bærum"),
    ("Jotun Arena", "Sandefjord"),
    ("SR-Bank Arena", "Stavanger"),              # 0 results, kept as evidence of miss
    ("Viking Stadion", "Stavanger"),             # retry: returned as Lyse Arena (2025 rename)
    ("Sarpsborg Stadion", "Sarpsborg"),
    ("Skagerak Arena", "Skien"),
    ("Åråsen Stadion", "Lillestrøm"),
]
OUT = os.path.expanduser("~/workspace/ai-inbox/work-req-20261028-001/evidence/nominatim")
os.makedirs(OUT, exist_ok=True)
UA = "venue-audit-research/1.0 (ai-data-bus req-20261028-001)"
CST = timezone(timedelta(hours=8))
log = []
for name, city in QUERIES:
    slug = "".join(c if c.isalnum() else "_" for c in f"{name}_{city}")
    q = urllib.parse.quote(f"{name}, {city}, Norway")
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=3&addressdetails=1"
    path = os.path.join(OUT, slug + ".json")
    subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url, "-o", path], check=False)
    ts = datetime.now(CST).isoformat(timespec="seconds")
    try:
        data = json.load(open(path))
        n = len(data) if isinstance(data, list) else 0
        first = data[0] if n else None
    except Exception:
        n, first = 0, None
    log.append({"query_name": name, "query_city": city, "url": url,
                "file": f"nominatim/{slug}.json", "retrieved_at": ts, "n_results": n,
                "first_display_name": first["display_name"] if first else None,
                "first_lat": first["lat"] if first else None, "first_lon": first["lon"] if first else None,
                "first_class": first.get("class") if first else None,
                "first_type": first.get("type") if first else None,
                "first_importance": first.get("importance") if first else None})
    print(name, "|", city, "->", n, "|", ts)
    time.sleep(1.2)
json.dump(log, open(os.path.join(OUT, "query_log.json"), "w"), ensure_ascii=False, indent=1)
print("done", len(log))
