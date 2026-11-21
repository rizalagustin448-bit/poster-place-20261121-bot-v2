"""AURMARA - The Harbour of Golden Stairs.

Writes one vintage travel-poster image to /output/entry.png: a golden-hour
coastal town cascading down a cliff to the sea, grand staircase, harbour
sailboats, and two people at a cafe table on the terrace.

Stdlib only: the poster is a pre-rendered asset (poster.png, drawn at build
time with Pillow - see draw_poster.py); this program just copies it to the
output directory, so it runs in the sandbox with no network and no installs.
"""

import os
import shutil
from pathlib import Path


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "poster.png"
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
