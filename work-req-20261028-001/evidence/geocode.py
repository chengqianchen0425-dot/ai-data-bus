import json, subprocess, time, urllib.parse, hashlib, os

QUERIES = [
    ("Aker Stadion", "Molde"),
    ("Romssa Arena", "Tromsø"),
    ("Aspmyra Stadion", "Bodø"),
    ("Brann Stadion", "Bergen"),
    ("Briskeby Arena", "Hamar"),
    ("Color Line Stadion", "Ålesund"),
    ("Haugesund Sparebank Arena", "Haugesund"),
    ("Intility Arena", "Oslo"),
    ("J.J. Ugland Stadion", "Grimstad"),
    ("Kristiansund Stadion", "Kristiansund"),
    ("Lerkendal Stadion", "Trondheim"),
    ("Marienlyst Stadion", "Drammen"),
    ("Nadderud Stadion", "Bærum"),
    ("Jotun Arena", "Sandefjord"),
    ("SR-Bank Arena", "Stavanger"),
    ("Sarpsborg Stadion", "Sarpsborg"),
    ("Skagerak Arena", "Skien"),
    ("Åråsen Stadion", "Lillestrøm"),
]
OUT = os.path.expanduser("~/workspace/ai-inbox/work-req-20261028-001/evidence/nominatim")
os.makedirs(OUT, exist_ok=True)
UA = "venue-audit-research/1.0 (ai-data-bus req-20261028-001)"
summary = []
for name, city in QUERIES:
    slug = "".join(c if c.isalnum() else "_" for c in f"{name}_{city}")
    q = urllib.parse.quote(f"{name}, {city}, Norway")
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=3&addressdetails=1"
    path = os.path.join(OUT, slug + ".json")
    subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url, "-o", path], check=False)
    try:
        data = json.load(open(path))
    except Exception as e:
        data = {"_error": str(e)}
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None
    first = data[0] if isinstance(data, list) and data else None
    summary.append({
        "query_name": name, "query_city": city, "url": url, "file": f"nominatim/{slug}.json",
        "sha256": sha, "n_results": len(data) if isinstance(data, list) else 0,
        "first_display_name": first["display_name"] if first else None,
        "first_lat": first["lat"] if first else None, "first_lon": first["lon"] if first else None,
        "first_class": first.get("class") if first else None, "first_type": first.get("type") if first else None,
        "first_importance": first.get("importance") if first else None,
    })
    print(name, "|", city, "->", summary[-1]["n_results"], "results;", summary[-1]["first_display_name"], summary[-1]["first_lat"], summary[-1]["first_lon"])
    time.sleep(1.2)
json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), ensure_ascii=False, indent=1)
print("done", len(summary))
