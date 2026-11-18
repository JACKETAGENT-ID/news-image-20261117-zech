#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261117 (zech).

Copies the pre-rendered entry.png (drawn by generate.py) into the output
directory make.fun provides. Standard library only; no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("copied entry.png has unexpected size")


if __name__ == "__main__":
    main()
