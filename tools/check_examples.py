#!/usr/bin/env python3
"""Compile every Lean code block in the guide.

Usage (from the repository root):
    python3 tools/check_examples.py [FILE.md ...]

With no arguments it checks README.md and every page in guide/.

Each ```lean block is written to its own file and compiled with the toolchain in `lean-toolchain`.
A block preceded by `<!-- nocheck -->` (for example one that imports a project module that does
not exist) is skipped. A block fails if Lean reports an error; warnings are allowed, because some
"bad" examples are bad style that Lean accepts with a warning.
"""
import concurrent.futures
import glob
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLCHAIN = open(os.path.join(ROOT, "lean-toolchain")).read().strip()
BLOCK = re.compile(r"(<!-- nocheck -->\s*\n)?```lean\n(.*?)```", re.S)


def blocks(text):
    for m in BLOCK.finditer(text):
        line = text.count("\n", 0, m.start(2)) + 1
        yield line, m.group(1) is not None, m.group(2)


def check(args):
    name, line, src, tmp = args
    path = os.path.join(tmp, f"{re.sub(r'[^A-Za-z0-9]', '_', name)}_{line}.lean")
    with open(path, "w") as fh:
        fh.write(src)
    r = subprocess.run(["lean", f"+{TOOLCHAIN}", path], capture_output=True, text=True, cwd=tmp)
    out = r.stdout + r.stderr
    return name, line, r.returncode == 0 and ": error" not in out, out


def main():
    files = sys.argv[1:] or [os.path.join(ROOT, "README.md")] + sorted(glob.glob(os.path.join(ROOT, "guide", "*.md")))
    todo, skipped = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for guide in files:
            name = os.path.relpath(guide, ROOT)
            for line, nocheck, src in blocks(open(guide).read()):
                if nocheck:
                    skipped += 1
                else:
                    todo.append((name, line, src, tmp))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = sorted(pool.map(check, todo))
    failed = [(name, line, out) for name, line, ok, out in results if not ok]
    for name, line, out in failed:
        print(f"--- {name}:{line}\n{out.strip()}\n")
    print(f"{len(results) - len(failed)} of {len(results)} blocks compile; {skipped} skipped (nocheck)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
