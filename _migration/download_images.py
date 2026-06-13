#!/usr/bin/env python3
"""Descarga las imágenes listadas en downloads.json a sus rutas locales (idempotente)."""
import json
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "_migration", "downloads.json")

UA = "Mozilla/5.0 (X11; Linux x86_64) SuperPadLandMigration/1.0"


def fetch(url, dest):
    abspath = os.path.join(ROOT, dest)
    if os.path.exists(abspath) and os.path.getsize(abspath) > 0:
        return ("skip", dest)
    os.makedirs(os.path.dirname(abspath), exist_ok=True)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            with open(abspath, "wb") as f:
                f.write(data)
            return ("ok", dest)
        except Exception as e:
            if attempt == 2:
                return ("ERROR", f"{dest}  <- {url}  ({e})")
            time.sleep(1.5 * (attempt + 1))


def main():
    jobs = json.load(open(MANIFEST))
    ok = skip = err = 0
    errors = []
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = [ex.submit(fetch, u, d) for u, d in jobs]
        done = 0
        for fut in as_completed(futs):
            status, info = fut.result()
            done += 1
            if status == "ok":
                ok += 1
            elif status == "skip":
                skip += 1
            else:
                err += 1
                errors.append(info)
            if done % 250 == 0:
                print(f"  {done}/{len(jobs)}  (ok={ok} skip={skip} err={err})")
    print(f"\nTOTAL: ok={ok} skip={skip} err={err}")
    if errors:
        print("\nFallos:")
        for e in errors[:40]:
            print("  ", e)
        with open(os.path.join(ROOT, "_migration", "download_errors.txt"), "w") as f:
            f.write("\n".join(errors))


if __name__ == "__main__":
    main()
