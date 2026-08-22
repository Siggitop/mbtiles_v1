#!/usr/bin/env python3
"""
Entpackt alle gzip-komprimierten .pbf-Dateien im tiles/-Ordner in-place.
Ein einzelner Python-Prozess statt tausender Shell-Subprozess-Aufrufe -> deutlich schneller.
Ausführen im Verzeichnis, das den tiles/-Ordner enthält:  python3 decompress_tiles.py
"""
import gzip
import os
import sys
import time

TILES_DIR = "tiles"

def main():
    if not os.path.isdir(TILES_DIR):
        print(f"Ordner '{TILES_DIR}' nicht gefunden. Im Repo-Root ausführen.")
        sys.exit(1)

    total = 0
    decompressed = 0
    start = time.time()

    for root, _dirs, files in os.walk(TILES_DIR):
        for name in files:
            if not name.endswith(".pbf"):
                continue
            total += 1
            path = os.path.join(root, name)
            with open(path, "rb") as f:
                magic = f.read(2)
            if magic == b"\x1f\x8b":
                with open(path, "rb") as f:
                    data = gzip.decompress(f.read())
                with open(path, "wb") as f:
                    f.write(data)
                decompressed += 1
            if total % 5000 == 0:
                elapsed = time.time() - start
                print(f"... {total} geprüft, {decompressed} entpackt ({elapsed:.0f}s)")

    elapsed = time.time() - start
    print(f"Fertig in {elapsed:.0f}s. Geprüft: {total}, entpackt: {decompressed}")

if __name__ == "__main__":
    main()
