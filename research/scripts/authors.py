#!/usr/bin/env python3
"""Who wrote the program code? Attributes files to authors from their `Authors:` headers.

Usage (from research/vendor/repos):
    python3 ../../scripts/authors.py            # author table (markdown)
    python3 ../../scripts/authors.py --files A  # program files whose first author matches A

A file counts as *program code* when it has at least 3 defs and theorems are at most 25% of its
defs + theorems. Attribution is to the first listed author (the header names who created the file,
not who edits it now); the copyright year is the creation year. Both come from file headers
because the clones are shallow.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leanlex import decls, lean_files, lex, nonblank

ROOTS = {
    "lean4": ["lean4/src/Init", "lean4/src/Std", "lean4/src/Lean", "lean4/src/lake/Lake"],
    "verso": ["verso/src"],
    "doc-gen4": ["doc-gen4/DocGen4"],
    "lean4-cli": ["lean4-cli/Cli"],
}

# Lean FRO team as listed on https://lean-lang.org/fro/team/ (fetched 2026-10-20).
FRO = ["Leo de Moura", "Sebastian Ullrich", "Ashley Blacquiere", "Henrik Böving", "Joachim Breitner",
       "David Thrane Christiansen", "Emilio Jesús Gallego Arias", "Sebastian Graf", "Julia Markus Himmel",
       "Marc Huisinga", "Mac Malone", "Joscha Mennicken", "Kyle Miller", "Kim Morrison",
       "Wojciech Nawrocki", "Jason Reed", "Paul Reichert", "Sofia Rodrigues", "Rob Simmons"]
ALIASES = {"Leonardo de Moura": "Leo de Moura", "Scott Morrison": "Kim Morrison",
           "Markus Himmel": "Julia Markus Himmel", "Julia M. Himmel": "Julia Markus Himmel", "Mac": "Mac Malone",
           "David Christiansen": "David Thrane Christiansen", "Henrik Boving": "Henrik Böving"}

AUTH_RE = re.compile(r"^\s*Authors?\s*:\s*(.*)$", re.M)
YEAR_RE = re.compile(r"Copyright \(c\)\s*(\d{4})")


def authors(text):
    m = AUTH_RE.search(text[:3000])
    if not m:
        return []
    names = re.split(r",|\band\b", m.group(1).rstrip(". "))
    out = []
    for n in names:
        n = re.sub(r"\s+", " ", n).strip()
        if n:
            out.append(ALIASES.get(n, n))
    return out


def scan():
    rows = []
    for repo, dirs in ROOTS.items():
        dirs = [d for d in dirs if os.path.isdir(d)]
        for p in lean_files(dirs):
            text = open(p, encoding="utf-8", errors="replace").read()
            fi = lex(p)
            kinds = collections.Counter(d.kw for d in decls({k: getattr(fi, k) for k in fi.__slots__}))
            defs = kinds["def"] + kinds["abbrev"] + kinds["instance"] + kinds["opaque"]
            thms = kinds["theorem"] + kinds["lemma"]
            au = authors(text)
            y = YEAR_RE.search(text[:600])
            rows.append(dict(path=p, repo=repo, first=au[0] if au else "(none)", all=au,
                             year=int(y.group(1)) if y else None, nb=nonblank(fi.raw), defs=defs,
                             thms=thms, prog=defs >= 3 and thms <= 0.25 * (defs + thms)))
    return rows


# Survey columns: FRO program code split by first author, so a pattern can be checked across authors.
# Published tables label authors by letter, in order of their share of program code (A is the largest),
# because the point is to compare conventions, not people. Names are needed here only to classify files.
# Author A's code is split at 2024 (grind and `Meta/Sym` vs the 2016-2022 bootstrap code).
COLUMN_AUTHORS = ["Leo de Moura", "David Thrane Christiansen", "Henrik Böving", "Sofia Rodrigues", "Mac Malone",
                  "Sebastian Ullrich", "Sebastian Graf"]
OTHER_FRO = {"Joachim Breitner", "Kim Morrison", "Kyle Miller", "Marc Huisinga", "Wojciech Nawrocki",
             "Paul Reichert", "Julia Markus Himmel", "Joscha Mennicken", "Rob Simmons"}
COLUMNS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "author-columns.json")


def letters(rows):
    """Letter for each first author, by share of program lines (A, B, ..., Z, AA, AB, ...)."""
    nb = collections.Counter()
    for r in rows:
        if r["prog"] and r["first"] != "(none)":
            nb[r["first"]] += r["nb"]
    names = [n for n, _ in nb.most_common()]
    label = lambda i: chr(65 + i) if i < 26 else chr(64 + i // 26) + chr(65 + i % 26)
    return {n: label(i) for i, n in enumerate(names)}


def column_of(r, letter):
    a = r["first"]
    if a == COLUMN_AUTHORS[0]:
        return letter[a] + ("24" if (r["year"] or 0) >= 2024 else "old")
    if a in COLUMN_AUTHORS:
        return letter[a]
    return "Others" if a in OTHER_FRO else None


def write_columns(rows):
    import json
    letter = letters(rows)
    cols = collections.defaultdict(list)
    for r in rows:
        c = column_of(r, letter) if r["prog"] else None
        if c:
            cols[c].append(r["path"])
    first = letter[COLUMN_AUTHORS[0]]
    order = [first + "24", first + "old"] + [letter[a] for a in COLUMN_AUTHORS[1:]] + ["Others"]
    with open(COLUMNS_JSON, "w") as fh:
        json.dump([[c, sorted(cols[c])] for c in order], fh, indent=0)
    for c in order:
        print(c, len(cols[c]), "files")


def main():
    rows = scan()
    if len(sys.argv) > 1 and sys.argv[1] == "--write-columns":
        write_columns(rows)
        return
    if len(sys.argv) > 2 and sys.argv[1] == "--files":  # takes an author's name
        for r in rows:
            if r["prog"] and r["first"] == sys.argv[2]:
                print(r["path"])
        return
    agg = collections.defaultdict(lambda: dict(files=0, nb=0, defs=0, thms=0, years=[], where=collections.Counter()))
    for r in rows:
        if not r["prog"]:
            continue
        a = agg[r["first"]]
        a["files"] += 1
        a["nb"] += r["nb"]
        a["defs"] += r["defs"]
        a["thms"] += r["thms"]
        if r["year"]:
            a["years"].append(r["year"])
        parts = r["path"].split("/")
        a["where"]["/".join(parts[:4] if parts[0] == "lean4" else parts[:2])] += r["nb"]
    tot = sum(a["nb"] for a in agg.values())
    letter = letters(rows)
    print(f"Program files: {sum(a['files'] for a in agg.values())}, nonblank lines: {tot}\n")
    print("| first author | FRO | files | nonblank | % | defs | thms | years (min–median–max) | main dirs (by lines) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for name, a in sorted(agg.items(), key=lambda kv: -kv[1]["nb"])[:30]:
        ys = sorted(a["years"])
        yr = f"{ys[0]}–{ys[len(ys)//2]}–{ys[-1]}" if ys else "?"
        where = ", ".join(f"`{w}` {n}" for w, n in a["where"].most_common(3))
        print(f"| {letter.get(name, name)} | {'yes' if name in FRO else ''} | {a['files']} | {a['nb']} | {100*a['nb']/tot:.1f} | "
              f"{a['defs']} | {a['thms']} | {yr} | {where} |")


if __name__ == "__main__":
    main()
