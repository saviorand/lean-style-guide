#!/usr/bin/env python3
"""Stdlib style survey: counts per subtree for research/stdlib-survey.md.

Usage (from research/vendor/repos):
    python3 ../../scripts/survey.py                 # all sections
    python3 ../../scripts/survey.py naming lambda   # selected sections
    python3 ../../scripts/survey.py --cols Init,Std naming

Each section function prints markdown tables. `ex_*` helpers print sample locations (path:line)
so counts can be spot-checked by eye.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leanlex import (COLS, case_class, decls, last_component, load, nonblank, pct, per_k, quantile,
                     split_top, table)

_DATA = {}
_DECLS = {}


def files(col):
    if col not in _DATA:
        _DATA[col] = load(col)
    return _DATA[col]


_FDECLS = {}


def fdecls(f):
    if f["path"] not in _FDECLS:
        _FDECLS[f["path"]] = decls(f)
    return _FDECLS[f["path"]]


def all_decls(col):
    if col not in _DECLS:
        _DECLS[col] = [d for f in files(col) for d in fdecls(f)]
    return _DECLS[col]


def nb(col):
    return sum(nonblank(f["raw"]) for f in files(col))


_CONT = re.compile(r"^(?:where|termination_by|decreasing_by|deriving|partial_fixpoint|\||:|\)|\]|\}|⟩|with\b|else\b|"
                   r"then\b|·|-)")
PROG_KINDS = {"def", "abbrev", "instance", "opaque", "structure", "class", "class inductive", "inductive"}
THM_KINDS = {"theorem", "example"}
_MODE = {}


def mode_lines(f, mode):
    """Code lines restricted to declarations of one family: 'prog' (defs, instances, types) or 'thm'
    (theorems, examples). A declaration extends from its first line to the next unindented line that
    starts a new command."""
    key = (f["path"], mode)
    if key in _MODE:
        return _MODE[key]
    code = f["code"]
    tops = [i for i, l in enumerate(code) if l and not l[0].isspace() and not _CONT.match(l)]
    kind = [None] * len(code)
    import bisect
    for d in fdecls(f):
        j = bisect.bisect_right(tops, d.line)
        end = tops[j] if j < len(tops) else len(code)
        for k in range(d.start, end):
            kind[k] = d.kw
    want = PROG_KINDS if mode == "prog" else THM_KINDS
    out = [l if kind[i] in want else "" for i, l in enumerate(code)]
    _MODE[key] = out
    return out


_JOINED = {}


def joined(col, where):
    if (col, where) not in _JOINED:
        if where in ("prog", "thm"):
            _JOINED[(col, where)] = "\n".join("\n".join(mode_lines(f, where)) for f in files(col))
        else:
            _JOINED[(col, where)] = "\n".join("\n".join(f[where]) for f in files(col))
    return _JOINED[(col, where)]


def count_re(col, rx, where="code"):
    return len(re.findall(rx, joined(col, where), re.M))


def samples(col, rx, k=5, where="code"):
    r = re.compile(rx)
    out = []
    for f in files(col):
        for i, l in enumerate(f[where]):
            if r.search(l):
                out.append(f"{f['path']}:{i + 1}: {f['raw'][i].strip()[:110]}")
                if len(out) >= k:
                    return out
    return out


def regex_table(cols, items, where="code"):
    """items: list of (label, regex). Prints absolute count and per-kLOC per column."""
    rows = []
    for label, rx in items:
        row = [label]
        for c in cols:
            n = count_re(c, rx, where)
            row.append(f"{n} ({per_k(n, nb(c))})")
        rows.append(row)
    print(table(["pattern (count, per kLOC)"] + cols, rows))


# ---------------------------------------------------------------------------------------------
def s_baseline(cols):
    print("## baseline")
    rows = []
    for c in cols:
        fs = files(c)
        rows.append([c, len(fs), sum(len(f["raw"]) - (1 if f["raw"] and f["raw"][-1] == "" else 0) for f in fs),
                     nb(c), sum(1 for f in fs if f["is_module"]), len(all_decls(c))])
    print(table(["col", "files", "lines", "nonblank", "`module` files", "decls parsed"], rows))


# ---------------------------------------------------------------------------------------------
KINDS = ["def", "abbrev", "theorem", "instance", "structure", "class", "class inductive", "inductive",
         "opaque", "axiom"]
CASES = ["UpperCamel", "lowerCamel", "lowerword", "snake", "snake+camel", "Upper_snake", "other"]


def s_naming(cols):
    print("## 1 naming: case convention of the last name component, by declaration kind")
    for kind in KINDS + ["namespace"]:
        rows = []
        for c in cols:
            if kind == "namespace":
                names = []
                for f in files(c):
                    for l in f["code"]:
                        m = re.match(r"^\s*namespace\s+(\S+)", l)
                        if m:
                            names.extend(p for p in m.group(1).split(".") if p)
            else:
                names = [last_component(d.name) for d in all_decls(c) if d.kw == kind and d.name]
            cnt = collections.Counter(case_class(n) for n in names)
            tot = len(names)
            rows.append([c, tot] + [pct(cnt[k], tot) for k in CASES])
        print(f"\n### {kind}")
        print(table(["col", "n"] + CASES, rows))

    print("\n### suffixes and primes (last component; defs = def/abbrev/opaque, thms = theorem)")
    suffix_rx = [
        ("ends `'` (primed)", r"'$"), ("ends `?`", r"\?$"), ("ends `!`", r"!$"),
        ("ends lower+`D` (getD-style)", r"[a-z]D$"), ("ends `Impl`", r"Impl$"), ("ends `Aux`", r"Aux$"),
        ("ends `Core`", r"Core$"), ("ends `Unsafe`/`unsafe`", r"[Uu]nsafe$"), ("ends `TR`", r"TR$"),
        ("ends lower+`M` (monadic)", r"[a-z]M$"), ("is `go`", r"^go$"), ("is `loop`", r"^loop$"),
        ("is `aux`", r"^aux$"), ("ends `_eq`", r"_eq$"), ("ends `_iff`", r"_iff$"),
        ("ends `_def`", r"_def$"), ("contains `_of_`", r"_of_"), ("ends `_spec`", r"_spec$"),
    ]
    for group, kinds in (("defs", {"def", "abbrev", "opaque"}), ("thms", {"theorem"})):
        rows = []
        for label, rx in suffix_rx:
            r = re.compile(rx)
            row = [label]
            for c in cols:
                names = [last_component(d.name) for d in all_decls(c) if d.kw in kinds and d.name]
                k = sum(1 for x in names if r.search(x))
                row.append(f"{k} ({pct(k, len(names))})")
            rows.append(row)
        print(f"\n#### {group}")
        print(table(["suffix (count, % of kind)"] + cols, rows))

    print("\n### `?`/`!`/`D` families among defs (qualified names)")
    rows = []
    for c in cols:
        names = {d.qname for d in all_decls(c) if d.kw in ("def", "abbrev", "opaque") and d.qname}
        q = {x[:-1] for x in names if x.endswith("?")}
        bang = {x[:-1] for x in names if x.endswith("!")}
        dd = {x[:-1] for x in names if re.search(r"[a-z]D$", x)}
        rows.append([c, len(q), len(bang), len(dd),
                     sum(1 for b in q if b in bang), sum(1 for b in q if b in dd),
                     sum(1 for b in q if b in names), sum(1 for b in bang if b + "?" not in names),
                     sum(1 for b in q if b in bang and b in dd and b in names)])
    print(table(["col", "X? defs", "X! defs", "XD defs", "X? with X!", "X? with XD", "X? with plain X",
                 "X! without X?", "all four"], rows))
    for c in cols[:2]:
        names = {d.qname for d in all_decls(c) if d.kw in ("def", "abbrev", "opaque") and d.qname}
        full = sorted(b for b in {x[:-1] for x in names if x.endswith("?")}
                      if b + "!" in names and b + "D" in names and b in names)
        print(f"\n{c} complete families (sample): {', '.join(full[:25])}")


# ---------------------------------------------------------------------------------------------
_FUN = re.compile(r"(?<![\w.'])fun\b|λ")


def _fun_arrows(f):
    """For each `fun`/`λ`, find whether it ends its binders with `=>`, `↦`, or starts with `|`."""
    text = "\n".join(f["code"])
    res = collections.Counter()
    for m in _FUN.finditer(text):
        res["λ" if m.group(0) == "λ" else "fun"] += 1
        k = m.end()
        while k < len(text) and text[k] in " \n\t":
            k += 1
        if text.startswith("|", k):
            res["match-lambda (`fun |`)"] += 1
            continue
        depth = 0
        while k < len(text) and k < m.end() + 400:
            ch = text[k]
            if ch in "([{⟨⦃":
                depth += 1
            elif ch in ")]}⟩⦄":
                depth -= 1
                if depth < 0:
                    break
            elif depth == 0 and text.startswith("=>", k):
                res["=>"] += 1
                break
            elif depth == 0 and ch == "↦":
                res["↦"] += 1
                break
            k += 1
    return res


def s_lambda(cols):
    print("## 2 lambda syntax")
    rows = []
    for c in cols:
        tot = collections.Counter()
        for f in files(c):
            tot += _fun_arrows(f)
        n = nb(c)
        sec = count_re(c, r"(?<=\S)[^\S\n]*·|\(·")  # `·` not first on its line
        dot_any = count_re(c, r"·")
        focus = count_re(c, r"^[ \t]*·")
        cdot_sec = count_re(c, r"\(\s*·|·\s*\)|[^\s(]\s*·(?!\s*$)")
        fl = tot["fun"] + tot["λ"]
        rows.append([c, f"{tot['fun']} ({per_k(tot['fun'], n)})", f"{tot['λ']} ({per_k(tot['λ'], n)})",
                     f"{tot['=>']} ({pct(tot['=>'], fl)})", f"{tot['↦']} ({pct(tot['↦'], fl)})",
                     f"{tot['match-lambda (`fun |`)']} ({pct(tot['match-lambda (`fun |`)'], fl)})",
                     f"{dot_any - focus} ({per_k(dot_any - focus, n)})", f"{focus} ({per_k(focus, n)})"])
    print(table(["col", "`fun` (per k)", "`λ` (per k)", "binder ends `=>` (% of fun+λ)",
                 "binder ends `↦`", "`fun |` alts", "`·` not line-initial (≈ sections) (per k)",
                 "`·` line-initial (focus dot) (per k)"], rows))


# ---------------------------------------------------------------------------------------------
_WHERE_ALONE = re.compile(r"^(?P<ind>[ \t]*)where(?:\s*$|\s+(?P<rest>\S.*))")
_HELPER_NAME = re.compile(r"^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|partial|unsafe|nonrec|noncomputable)\s+)*"
                          r"(?P<name>[^\s(\[{:⦃|@]+)")
_KEYWORDS = {"else", "then", "if", "let", "have", "case", "match", "finally", "·", "show", "exact", "simp", "grind",
             "fun", "do", "return", "for", "unless", "try", "catch", "next", "rw", "omega", "intro", "cases",
             "induction", "refine", "apply", "obtain", "by", "calc", "with", "termination_by", "decreasing_by"}
_TRAILING_WHERE = re.compile(r"^(?P<ind>[ \t]*)(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|public|partial|unsafe|"
                             r"noncomputable|nonrec)\s+)*(?:def|theorem|abbrev)\b.*:=.*\bwhere\s*$")
_LETREC = re.compile(r"\blet\s+rec\s+(?:@\[[^\]]*\]\s*)?(?P<name>[^\s(\[{:⦃]+)")


def where_helpers(f):
    """Yield (line, helper_name) for `where` clauses that follow a def/theorem body."""
    code = f["code"]
    n = len(code)
    for i, l in enumerate(code):
        m = _WHERE_ALONE.match(l)
        if not m:
            t = _TRAILING_WHERE.match(l)
            if t:  # `def f … := body where` with helpers on the following lines
                ind = len(t.group("ind"))
                hind = None
                for k in range(i + 1, n):
                    s = code[k]
                    if not s.strip():
                        continue
                    ci = len(s) - len(s.lstrip())
                    if ci <= ind:
                        break
                    if hind is None:
                        hind = ci
                    if ci == hind:
                        st = s.strip()
                        if st.startswith(("|", "termination_by", "decreasing_by", "partial_fixpoint")):
                            continue
                        hm = _HELPER_NAME.match(st)
                        if hm and hm.group("name") not in _KEYWORDS:
                            yield k, hm.group("name")
            continue
        # previous code must contain `:=` since the last declaration keyword (i.e. a body exists)
        ok = False
        for p in range(i - 1, max(-1, i - 400), -1):
            if ":=" in code[p] or re.match(r"^\s*\|", code[p]):
                ok = True
                break
            if re.match(r"^\s*(?:@\[.*\]\s*)?(?:[a-z]+\s+)*(def|theorem|instance|structure|class|inductive)\b",
                        code[p]):
                break
        if not ok:
            continue
        ind = len(m.group("ind"))
        hind = None
        if m.group("rest"):
            if m.group("rest").startswith("finally"):
                continue  # `where finally` discharges `?_` goals; not a helper
            hm = _HELPER_NAME.match(m.group("rest"))
            if hm and hm.group("name") not in _KEYWORDS:
                yield i, hm.group("name")
            hind = m.start("rest")
        for k in range(i + 1, n):
            s = code[k]
            if not s.strip():
                continue
            ci = len(s) - len(s.lstrip())
            if ci <= ind:
                break
            if hind is None:
                hind = ci
            if ci == hind:
                st = s.strip()
                if st.startswith(("|", "termination_by", "decreasing_by", "partial_fixpoint")):
                    continue
                hm = _HELPER_NAME.match(st)
                if hm and hm.group("name") not in _KEYWORDS:
                    yield k, hm.group("name")


def s_helpers(cols):
    print("## 3 local helpers")
    rows = []
    names_by = {}
    for c in cols:
        n = nb(c)
        wh_clauses = 0
        wnames = collections.Counter()
        lr = collections.Counter()
        for f in files(c):
            seen = set()
            for i, name in where_helpers(f):
                wnames[name] += 1
            for i, l in enumerate(f["code"]):
                if _WHERE_ALONE.match(l):
                    seen.add(i)
                for m in _LETREC.finditer(l):
                    lr[m.group("name")] += 1
            wh_clauses += len(seen)
        ds = all_decls(c)
        defs = [d for d in ds if d.kw in ("def", "abbrev", "opaque")]
        priv_defs = [d for d in defs if "private" in d.mods]
        dotted_aux = [d for d in defs if "." in d.name and last_component(d.name) in ("go", "loop", "aux")]
        whn, lrn = sum(wnames.values()), sum(lr.values())
        names_by[c] = (wnames, lr)
        rows.append([c, f"{whn} ({per_k(whn, n)})", f"{lrn} ({per_k(lrn, n)})",
                     f"{len(priv_defs)} ({pct(len(priv_defs), len(defs))} of defs)",
                     len(dotted_aux),
                     pct(wnames["go"] + lr["go"], whn + lrn), pct(wnames["loop"] + lr["loop"], whn + lrn),
                     pct(wnames["aux"] + lr["aux"], whn + lrn)])
    print(table(["col", "`where` helpers (per k)", "`let rec` (per k)", "private defs",
                 "top-level `X.go`/`X.loop`/`X.aux` defs", "`go` share", "`loop` share", "`aux` share"], rows))
    for c in cols:
        wnames, lr = names_by[c]
        print(f"\n{c} where-helper names top: {wnames.most_common(8)}; let rec top: {lr.most_common(6)}")


# ---------------------------------------------------------------------------------------------
_MATCH_WITH = re.compile(r"\bmatch\b(?!.*\bmatch\b).*\bwith\s*$")


def s_format(cols):
    print("## 4 formatting")
    # line lengths
    rows = []
    for c in cols:
        lens = sorted(len(l) for f in files(c) for l in f["raw"] if l.strip())
        tot = len(lens)
        over100 = sum(1 for x in lens if x > 100)
        over120 = sum(1 for x in lens if x > 120)
        tabs = sum(1 for f in files(c) for l in f["raw"] if "\t" in l)
        trail = sum(1 for f in files(c) for l in f["raw"] if l.strip() and l != l.rstrip())
        rows.append([c, quantile(lens, .5), quantile(lens, .95), quantile(lens, .99), lens[-1] if lens else 0,
                     f"{over100} ({pct(over100, tot)})", f"{over120} ({pct(over120, tot)})", tabs, trail])
    print("### line length (code points, nonblank raw lines incl. comments)")
    print(table(["col", "p50", "p95", "p99", "max", ">100", ">120", "lines with tab", "trailing ws"], rows))

    # indentation
    rows = []
    for c in cols:
        odd = tot = 0
        deltas = collections.Counter()
        for f in files(c):
            prev = None
            for l in f["code"]:
                if not l.strip():
                    continue
                ind = len(l) - len(l.lstrip(" "))
                tot += 1
                odd += ind % 2
                if prev is not None and ind > prev:
                    deltas[ind - prev] += 1
                prev = ind
        dt = sum(deltas.values())
        rows.append([c, pct(odd, tot), pct(deltas[2], dt), pct(deltas[4], dt),
                     pct(dt - deltas[2] - deltas[4], dt)])
    print("\n### indentation (code lines; deltas = increase from previous code line)")
    print(table(["col", "odd indent", "+2", "+4", "other increase"], rows))

    # match layout
    rows = []
    for c in cols:
        cat = collections.Counter()
        aligned = arms = inline = 0
        for f in files(c):
            code = f["code"]
            for i, l in enumerate(code):
                if re.search(r"\bmatch\b.*\bwith\s*\|", l):
                    inline += 1
                st = l.lstrip()
                if st.startswith("|") and "=>" in st:
                    arms += 1
                    if re.search(r"\S {2,}=>", st):
                        aligned += 1
                m = _MATCH_WITH.search(l)
                if not m:
                    continue
                k = i + 1
                while k < len(code) and not code[k].strip():
                    k += 1
                if k >= len(code) or not code[k].lstrip().startswith("|"):
                    continue
                li = len(l) - len(l.lstrip())
                ai = len(code[k]) - len(code[k].lstrip())
                mc = l.rfind("match", 0, m.end())
                mcol = re.search(r"\bmatch\b", l[m.start():]).start() + m.start()
                first = l.lstrip().startswith("match")
                key = "match-first" if first else "match-midline"
                if ai == li:
                    cat[key + ": `|` at line indent"] += 1
                elif ai == li + 2:
                    cat[key + ": `|` at line indent+2"] += 1
                elif not first and ai == mcol:
                    cat[key + ": `|` under `match`"] += 1
                else:
                    cat[key + ": other"] += 1
        tf = sum(v for k, v in cat.items() if k.startswith("match-first"))
        tm = sum(v for k, v in cat.items() if k.startswith("match-midline"))
        rows.append([c, tf, pct(cat["match-first: `|` at line indent"], tf),
                     pct(cat["match-first: `|` at line indent+2"], tf), tm,
                     pct(cat["match-midline: `|` at line indent"], tm),
                     pct(cat["match-midline: `|` at line indent+2"], tm),
                     pct(cat["match-midline: `|` under `match`"], tm), inline,
                     f"{aligned}/{arms} ({pct(aligned, arms)})"])
    print("\n### `match ... with` followed by `|` arms on the next line")
    print(table(["col", "match starts line: n", "`|` = match col", "`|` +2", "match mid-line: n",
                 "`|` = line indent", "`|` = line indent+2", "`|` under `match`", "`match … with |` inline",
                 "arms with padded `=>` (aligned)"], rows))

    # equation-style definitions: decl line followed by `|`
    rows = []
    for c in cols:
        cat = collections.Counter()
        ind = collections.Counter()
        for f in files(c):
            code = f["code"]
            for d in fdecls(f):
                if d.kw not in ("def", "abbrev", "instance", "inductive"):
                    continue
                last = d.line + d.header_lines - 1
                k = last + 1
                while k < len(code) and not code[k].strip():
                    k += 1
                if k < len(code) and code[k].lstrip().startswith("|") and ":=" not in d.header:
                    ai = len(code[k]) - len(code[k].lstrip())
                    (ind if d.kw == "inductive" else cat)[ai - d.indent] += 1
        t = sum(cat.values())
        ti = sum(ind.values())
        rows.append([c, t, pct(cat[2], t), pct(cat[0], t), pct(t - cat[2] - cat[0], t),
                     ti, pct(ind[2], ti), pct(ind[0], ti), pct(ti - ind[2] - ind[0], ti)])
    print("\n### `|` lines directly after a def/abbrev/instance header (equation compiler) and after `inductive`")
    print(table(["col", "def arms: n", "+2", "+0", "other", "inductive ctors: n", "+2", "+0", "other"], rows))

    # multi-line headers
    rows = []
    for c in cols:
        cont = collections.Counter()
        colon_start = colon_end = multi = body = 0
        bodyd = collections.Counter()
        for f in files(c):
            code = f["code"]
            for d in fdecls(f):
                if d.kw in ("structure", "class", "inductive", "class inductive", "example"):
                    pass
                hl = d.header.split("\n")
                if len(hl) > 1:
                    multi += 1
                    second = next((x for x in hl[1:] if x.strip()), None)
                    if second is not None:
                        cont[(len(second) - len(second.lstrip())) - d.indent] += 1
                    for x in hl[1:]:
                        if re.match(r"^\s*:(?!=)", x):
                            colon_start += 1
                            break
                    if any(re.search(r"\s:\s*$", x) for x in hl):
                        colon_end += 1
                lastl = hl[-1]
                if re.search(r":=\s*(by|do)?\s*$", lastl):
                    k = d.line + len(hl)
                    while k < len(code) and not code[k].strip():
                        k += 1
                    if k < len(code):
                        body += 1
                        bodyd[(len(code[k]) - len(code[k].lstrip())) - d.indent] += 1
        t = sum(cont.values())
        rows.append([c, multi, pct(cont[4], t), pct(cont[2], t), pct(t - cont[4] - cont[2], t),
                     f"{colon_start}", f"{colon_end}", body, pct(bodyd[2], body),
                     pct(body - bodyd[2], body)])
    print("\n### declaration headers split over lines")
    print(table(["col", "multi-line headers", "2nd line +4", "2nd line +2", "other", "header line starting `:`",
                 "header line ending ` :`", "bodies after `:=`/`:= by`/`:= do` EOL", "body +2", "body other"],
                rows))


# ---------------------------------------------------------------------------------------------
def s_do(cols):
    print("## 5 do notation (program code: lines inside def/abbrev/instance/opaque/type declarations)")
    items = [
        ("`do`", r"(?<![\w.'])do\b"),
        ("`Id.run do`", r"\bId\.run\s+do\b"),
        ("`let mut`", r"\blet\s+mut\b"),
        ("`for … in`", r"(?<![\w.'])for\s+[^\n]*?\bin\b"),
        ("`while`", r"(?<![\w.'])while\b"),
        ("`repeat` (term/do)", r"(?<![\w.'])repeat\b"),
        ("`break`", r"(?<![\w.'])break\b"),
        ("`continue`", r"(?<![\w.'])continue\b"),
        ("`return`", r"(?<![\w.'])return\b"),
        ("`pure`", r"(?<![\w.'])pure\b"),
        ("guard return `then return`/`do return`", r"\b(?:then|do)\s+return\b"),
        ("`(← …)` nested action", r"\(←"),
        ("`←` total", r"←"),
        ("`<-` ASCII", r"<-"),
        ("`unless`", r"(?<![\w.'])unless\b"),
        ("`if let`", r"\bif\s+let\b"),
        ("`if h :`", r"\bif\s+[\w'₀-₉]+\s*:"),
        ("`match ← `/`match (← `", r"\bmatch\s+\(?←"),
        ("`let some x ← … |` (let-else)", r"\blet\s+(?:some|\.some|\.ok|⟨)[^\n]*←[^\n]*\|"),
        ("`let … := … |` (pure let-else)", r"\blet\s+(?:some|\.some|\.ok|⟨)[^\n←]*:=[^\n]*\|"),
        ("`try`", r"(?<![\w.'])try\b(?!\s*\()"),
        ("`catch`", r"(?<![\w.'])catch\b"),
        ("`finally`", r"(?<![\w.'])finally\b"),
    ]
    regex_table(cols, items, where="prog")
    # multi-line early return heuristic
    rows = []
    stop = re.compile(r"^\s*(else|\||catch|finally|where|termination_by|decreasing_by|deriving|end\b|@\[|"
                      r"(private|protected|public|partial|unsafe|noncomputable)?\s*(def|theorem|instance|abbrev)\b|\))")
    for c in cols:
        early = 0
        for f in files(c):
            code = mode_lines(f, "prog")
            for i, l in enumerate(code):
                if not re.match(r"^\s*return\b", l):
                    continue
                k = i + 1
                while k < len(code) and not code[k].strip():
                    k += 1
                if k >= len(code):
                    continue
                ri = len(l) - len(l.lstrip())
                ni = len(code[k]) - len(code[k].lstrip())
                if 0 < ni < ri and not stop.match(code[k]):
                    early += 1
        rows.append([c, f"{early} ({per_k(early, nb(c))})"])
    print("\n### line-initial `return` followed by less-indented continuing code (≈ early return, approximate)")
    print(table(["col", "count (per k)"], rows))


# ---------------------------------------------------------------------------------------------
def s_errors(cols):
    print("## 6 error handling (program code only; see second table for theorem statements)")
    items = [
        ("`Except` (type/namespace)", r"\bExcept\b"),
        ("`ExceptT`", r"\bExceptT\b"),
        ("`EIO`", r"\bEIO\b"),
        ("`IO` (type)", r"(?<![\w.])IO\b(?!\.)"),
        ("`IO.Error`", r"\bIO\.Error\b"),
        ("`.userError`", r"\.userError\b"),
        ("`throw`", r"(?<![\w.'])throw\b"),
        ("`throwError`", r"\bthrowError\b"),
        ("`MonadExcept`", r"\bMonadExcept\b"),
        ("`Option` (type)", r"\bOption\b"),
        ("`panic!`", r"\bpanic!"),
        ("`unreachable!`", r"\bunreachable!"),
        ("`assert!`", r"\bassert!"),
        ("`dbg_trace`/`dbgTrace`", r"\bdbg_?[tT]race"),
        ("`sorry`", r"(?<![\w.'])sorry\b"),
        ("`.get!`", r"\.get!"),
        ("`.getD`", r"\.getD\b"),
        ("`.get?`", r"\.get\?"),
        ("`[i]!`", r"\]!"),
        ("`[i]?`", r"\]\?"),
        ("`[i]'h`", r"\]'"),
        ("other `x!` calls", r"(?<![\w!])(?!panic!|unreachable!|assert!|s!|m!|f!|throwError!)[a-z][\w.]*!(?=[\s)\]])"),
        ("`Inhabited` (derive/inst/binder)", r"\bInhabited\b"),
    ]
    regex_table(cols, items, where="prog")
    print("\n### same accessors inside theorem/example declarations")
    regex_table(cols, [x for x in items if x[0] in ("`.get!`", "`.getD`", "`.get?`", "`[i]!`", "`[i]?`", "`[i]'h`",
                                                     "other `x!` calls", "`Option` (type)")], where="thm")


# ---------------------------------------------------------------------------------------------
def s_termination(cols):
    print("## 7 termination")
    rows = []
    for c in cols:
        ds = all_decls(c)
        defs = [d for d in ds if d.kw in ("def", "abbrev", "opaque", "instance")]
        part = sum(1 for d in ds if "partial" in d.mods)
        uns = sum(1 for d in ds if "unsafe" in d.mods)
        nonrec = sum(1 for d in ds if "nonrec" in d.mods)
        n = nb(c)
        tb = count_re(c, r"^\s*termination_by\b")
        tbs = count_re(c, r"^\s*termination_by\s+structural\b")
        db = count_re(c, r"^\s*decreasing_by\b")
        pf = count_re(c, r"^\s*partial_fixpoint\b")
        ib = count_re(c, r"\bimplemented_by\b")
        fuel = count_re(c, r"\bfuel\b")
        rows.append([c, len(defs), f"{part} ({pct(part, len(defs))})", f"{tb} ({per_k(tb, n)})", tbs,
                     f"{db} ({per_k(db, n)})", pf, f"{uns} ({pct(uns, len(defs))})", ib, nonrec, fuel])
    print(table(["col", "defs+instances", "`partial`", "`termination_by` (per k)", "… `structural`",
                 "`decreasing_by` (per k)", "`partial_fixpoint`", "`unsafe` decls", "`implemented_by`",
                 "`nonrec`", "`fuel` tokens"], rows))


# ---------------------------------------------------------------------------------------------
def s_data(cols):
    print("## 8 data modelling")
    rows = []
    der = {}
    for c in cols:
        ds = all_decls(c)
        k = collections.Counter(d.kw for d in ds)
        inst = [d for d in ds if d.kw == "instance"]
        named = sum(1 for d in inst if d.instance_named)
        named_inst_prefix = sum(1 for d in inst if d.instance_named and last_component(d.name).startswith("inst"))
        types_abbrev = sum(1 for d in ds if d.kw == "abbrev" and case_class(last_component(d.name)).startswith("Upper"))
        types_def = sum(1 for d in ds if d.kw == "def" and case_class(last_component(d.name)).startswith("Upper"))
        cnt = collections.Counter()
        clauses = 0
        for f in files(c):
            text = "\n".join(f["code"])
            for m in re.finditer(r"(?m)^\s*deriving\s+(?!instance\b)([^\n]*)", text):
                clauses += 1
                for x in split_top(m.group(1)):
                    cnt[x.split()[0].split("(")[0]] += 1
            for m in re.finditer(r"(?m)^\s*deriving\s+instance\s+(.*?)\s+for\b", text):
                clauses += 1
                for x in split_top(m.group(1)):
                    cnt[x.split()[0]] += 1
        der[c] = (clauses, cnt)
        nstruct = k["structure"] + k["class"]
        rows.append([c, k["structure"], k["inductive"], k["class"], k["class inductive"], k["abbrev"],
                     types_abbrev, types_def, len(inst), f"{named} ({pct(named, len(inst))})",
                     f"{named_inst_prefix}", clauses])
    print(table(["col", "structure", "inductive", "class", "class inductive", "abbrev", "abbrev UpperCamel (≈type)",
                 "def UpperCamel (≈type)", "instances", "named instances", "named `inst…`",
                 "deriving clauses"], rows))
    print("\n### derived classes (top 12)")
    for c in cols:
        clauses, cnt = der[c]
        print(f"- {c}: " + ", ".join(f"{k} {v}" for k, v in cnt.most_common(12)))


# ---------------------------------------------------------------------------------------------
def _attr_key(a):
    toks = a.split()
    if not toks:
        return "", ""
    pref = ""
    while toks and toks[0] in ("local", "scoped"):
        pref = toks.pop(0)
    if not toks:
        return "", ""
    name = toks[0].split("(")[0]
    variant = " ".join(toks[1:2]) if name in ("grind", "simp") else ""
    return name, variant


def s_attrs(cols):
    print("## 9 attributes (`@[…]` on declarations plus `attribute […]` commands)")
    keys = ["inline", "always_inline", "noinline", "macro_inline", "specialize", "simp", "grind", "extern",
            "implemented_by", "csimp", "reducible", "irreducible", "semireducible", "expose", "inherit_doc",
            "export", "instance", "ext", "deprecated", "builtin_doc", "spec", "simps", "to_additive",
            "match_pattern", "never_extract", "init", "builtin_init", "elab_as_elim", "induction_eliminator",
            "cases_eliminator", "wf_preprocess", "congr", "norm_cast", "aesop", "nospecialize", "local", "scoped"]
    per = {}
    for c in cols:
        cnt, grindv, simpv = collections.Counter(), collections.Counter(), collections.Counter()
        for f in files(c):
            text = "\n".join(f["code"])
            blocks = re.findall(r"@\[((?:[^\[\]]|\[[^\[\]]*\])*)\]", text)
            blocks += re.findall(r"(?m)^\s*attribute\s+\[((?:[^\[\]]|\[[^\[\]]*\])*)\]", text)
            for b in blocks:
                for a in split_top(b):
                    toks = a.split()
                    if toks and toks[0] in ("local", "scoped"):
                        cnt[toks[0]] += 1
                    name, var = _attr_key(a)
                    if not name:
                        continue
                    cnt[name] += 1
                    if name == "grind":
                        grindv[var or "(plain)"] += 1
                    if name == "simp":
                        simpv[var or "(plain)"] += 1
        per[c] = (cnt, grindv, simpv)
    rows = []
    for k in keys:
        rows.append([f"`{k}`"] + [f"{per[c][0][k]} ({per_k(per[c][0][k], nb(c))})" for c in cols])
    print(table(["attribute (count, per kLOC)"] + cols, rows))
    print("\n### grind variants (top 10)")
    for c in cols:
        print(f"- {c}: " + ", ".join(f"`{k}` {v}" for k, v in per[c][1].most_common(10)))
    print("\n### other modifiers (decl counts)")
    rows = []
    for c in cols:
        ds = all_decls(c)
        rows.append([c, sum("unsafe" in d.mods for d in ds), sum("noncomputable" in d.mods for d in ds),
                     count_re(c, r"^\s*noncomputable\s+section\b"),
                     count_re(c, r"^\s*attribute\s+\["), count_re(c, r"\(priority\s*:=")])
    print(table(["col", "`unsafe` decls", "`noncomputable` decls", "`noncomputable section`",
                 "`attribute [..]` cmds", "`(priority := …)`"], rows))


# ---------------------------------------------------------------------------------------------
def s_visibility(cols):
    print("## 10 visibility and scoping")
    rows = []
    for c in cols:
        ds = all_decls(c)
        nd = len(ds)
        n = nb(c)
        fs = files(c)
        rows.append([c, nd, f"{sum('private' in d.mods for d in ds)} ({pct(sum('private' in d.mods for d in ds), nd)})",
                     f"{sum('protected' in d.mods for d in ds)} ({pct(sum('protected' in d.mods for d in ds), nd)})",
                     f"{sum('public' in d.mods for d in ds)} ({pct(sum('public' in d.mods for d in ds), nd)})",
                     f"{sum(1 for d in ds if d.public)} ({pct(sum(1 for d in ds if d.public), nd)})",
                     sum(1 for f in fs if any(re.match(r"^(?:@\[[^\]]*\]\s*)?public\s+(?:(?:meta|noncomputable)\s+)*section\b", l)
                                             for l in f["code"])),
                     sum(1 for f in fs if any(re.match(r"^@\[expose\]\s*public\s+(?:(?:meta|noncomputable)\s+)*section\b", l)
                                             for l in f["code"]))])
    print(table(["col", "decls", "`private`", "`protected`", "explicit `public`", "effectively public (est.)",
                 "files with `public section`", "files with `@[expose] public section`"], rows))
    print()
    items = [
        ("top-level `open X` (not `in`)", r"^open\b(?![^\n]*\bin\s*$)(?![^\n]*\bin\s+\S)"),
        ("`open … in` (line ends `in` or `in decl`)", r"^\s*open\b[^\n]*\bin(?:\s*$|\s+\S)"),
        ("indented `open … in` (inside terms)", r"^[ \t]+open\b[^\n]*\bin\b"),
        ("`open scoped`", r"\bopen\s+scoped\b"),
        ("`namespace`", r"^\s*namespace\b"),
        ("`section`", r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:public|noncomputable|meta)\s+)*section\b"),
        ("`variable`", r"^\s*variable\b"),
        ("`universe`", r"^\s*universe\b"),
        ("`set_option … in`", r"^\s*set_option\b[^\n]*\bin\s*$"),
        ("top-level `set_option`", r"^set_option\b(?![^\n]*\bin\s*$)"),
        ("`prelude`", r"^prelude\b"),
        ("`public import`", r"^public\s+import\b"),
        ("`public meta import`", r"^public\s+meta\s+import\b"),
        ("`meta import`", r"^meta\s+import\b"),
        ("plain `import`", r"^import\b"),
        ("`import all`", r"^(?:public\s+)?import\s+all\b"),
    ]
    regex_table(cols, items)
    rows = []
    for c in cols:
        sizes = sorted(len([l for l in f["raw"] if l.strip()]) for f in files(c))
        rows.append([c, len(sizes), quantile(sizes, .5), quantile(sizes, .9), quantile(sizes, .99), sizes[-1],
                     sum(1 for s in sizes if s > 1000), sum(1 for s in sizes if s > 1500)])
    print("\n### file size (nonblank lines per file)")
    print(table(["col", "files", "p50", "p90", "p99", "max", ">1000", ">1500"], rows))


# ---------------------------------------------------------------------------------------------
def s_docs(cols):
    print("## 11 documentation")
    rows = []
    fw = {}
    for c in cols:
        ds = [d for d in all_decls(c) if d.public and d.name]
        row = [c]
        for kinds in (("def", "abbrev", "opaque"), ("structure", "class", "inductive", "class inductive"),
                      ("theorem",), ("instance",)):
            sel = [d for d in ds if d.kw in kinds]
            doc = sum(1 for d in sel if d.doc is not None)
            inh = sum(1 for d in sel if d.doc is None and d.inherit_doc)
            row.append(f"{doc}/{len(sel)} ({pct(doc, len(sel))}) +{inh} inherit_doc")
        priv = [d for d in all_decls(c) if not d.public and d.kw in ("def", "abbrev", "opaque") and d.name]
        row.append(pct(sum(1 for d in priv if d.doc is not None), len(priv)))
        fs = files(c)
        withmd = sum(1 for f in fs if f["moddocs"])
        mds = [m for f in fs for m in f["moddocs"]]
        heading = sum(1 for m in mds if re.match(r"\s*#", m[3]))
        row += [f"{withmd}/{len(fs)} ({pct(withmd, len(fs))})", f"{len(mds) / max(1, len(fs)):.2f}",
                pct(heading, len(mds))]
        rows.append(row)
        docs = [d.doc for d in all_decls(c) if d.doc is not None and d.kw in ("def", "abbrev", "opaque")]
        words = collections.Counter()
        third = imper = code_first = noun = 0
        for t in docs:
            t2 = t.strip()
            m = re.match(r"[`(]?([A-Za-z][A-Za-z'-]*)", t2)
            if t2.startswith("`"):
                code_first += 1
            if m:
                w = m.group(1)
                words[w] += 1
        bt = sum(1 for t in docs if "`" in t)
        one = sum(1 for t in docs if "\n" not in t.strip())
        period = sum(1 for t in docs if t.strip().endswith((".", ".)", "`.")))
        own_line = sum(1 for t in docs if t.startswith("\n") or t.startswith(" \n") or t[:1] == "\n")
        fw[c] = (len(docs), words, bt, one, period, code_first, own_line)
    print(table(["col", "public defs documented", "public types documented", "public theorems documented",
                 "public named instances documented", "private defs documented", "files with module doc",
                 "module docs per file", "module docs starting with `#`"], rows))
    print("\n### def docstring form")
    rows = []
    for c in cols:
        n, words, bt, one, period, code_first, own_line = fw[c]
        rows.append([c, n, pct(bt, n), pct(one, n), pct(own_line, n), pct(period, n), pct(code_first, n),
                     ", ".join(f"{w} {k}" for w, k in words.most_common(10))])
    print(table(["col", "def docstrings", "contain backticks", "single-line", "text starts on next line",
                 "end with period", "start with code", "top first words"], rows))


# ---------------------------------------------------------------------------------------------
def s_tests(cols):
    print("## 12 tests inside library code")
    items = [
        ("`#guard_msgs`", r"^\s*#guard_msgs\b"),
        ("`#guard`", r"^\s*#guard\b(?!_)"),
        ("`#eval`", r"^\s*#eval\b"),
        ("`#check`", r"^\s*#check\b"),
        ("`#print`", r"^\s*#print\b"),
        ("`example`", r"^\s*(?:@\[[^\]]*\]\s*)?example\b"),
        ("`#exit`", r"^#exit\b"),
    ]
    regex_table(cols, items)


# ---------------------------------------------------------------------------------------------
def s_proofs(cols):
    print("## 13 proofs about programs")
    rows = []
    for c in cols:
        only_t = only_d = mixed = 0
        lemmas_files = 0
        for f in files(c):
            ds = fdecls(f)
            t = sum(1 for d in ds if d.kw == "theorem")
            p = sum(1 for d in ds if d.kw in ("def", "abbrev", "opaque", "structure", "inductive", "class",
                                              "instance"))
            if os.path.basename(f["path"]) == "Lemmas.lean" or "/Lemmas/" in f["path"]:
                lemmas_files += 1
            if t and not p:
                only_t += 1
            elif p and not t:
                only_d += 1
            elif p and t:
                mixed += 1
        ds = all_decls(c)
        nt = sum(1 for d in ds if d.kw == "theorem")
        npg = sum(1 for d in ds if d.kw in ("def", "abbrev", "opaque"))
        rows.append([c, nt, npg, f"{nt / max(1, npg):.2f}", only_t, only_d, mixed, lemmas_files])
    print(table(["col", "theorems", "defs", "thm/def", "files: theorems only", "files: defs only", "files: mixed",
                 "`Lemmas.lean` or `Lemmas/`"], rows))
    print()
    items = [
        ("subtype `{ x // p }`", r"\{\s*[^{}\n]*?//"),
        ("`Subtype`", r"\bSubtype\b"),
        ("`WF` token", r"\bWF\b|\.WF\b"),
        ("`Raw` token", r"\bRaw\b"),
        ("`Valid`/`Balanced`/`Ordered` tokens", r"\b(?:Valid|Balanced|Ordered)\b"),
        ("`structure … where` with `h…`/`…_lt`/`wf` proof field (≈)", r"^\s+(?:h\w*|\w+_(?:lt|le|eq|pos)|wf|valid|property|invariant)\s*:\s*[^\n]*(?:<|≤|=|∀|∈)"),
        ("`:= by` occurrences (tactic bodies)", r":=\s*by\b"),
    ]
    regex_table(cols, items)


# ---------------------------------------------------------------------------------------------
def s_unicode(cols):
    print("## 14 data structures and Unicode")
    rows = []
    for c in cols:
        cnt = collections.Counter()
        for d in all_decls(c):
            if d.kw not in ("def", "abbrev", "opaque", "instance"):
                continue
            h = d.header
            for tok in ("Array", "List", "ByteArray", "String", "Subarray", "Vector", "HashMap", "Std.HashMap",
                        "Substring", "Iterator"):
                cnt[tok] += len(re.findall(r"(?<![\w.])" + re.escape(tok) + r"\b", h))
        tot = cnt["Array"] + cnt["List"]
        rows.append([c, cnt["Array"], cnt["List"], pct(cnt["Array"], tot), cnt["ByteArray"], cnt["Vector"],
                     cnt["HashMap"] + cnt["Std.HashMap"], cnt["String"], cnt["Subarray"], cnt["Substring"]])
    print("### type names in def/abbrev/opaque/instance headers")
    print(table(["col", "Array", "List", "Array share", "ByteArray", "Vector", "HashMap", "String", "Subarray",
                 "Substring"], rows))
    print()
    pairs = [
        ("`→`", r"→"), ("`->`", r"->"),
        ("`←`", r"←"), ("`<-`", r"<-"),
        ("`↦`", r"↦"), ("`=>`", r"=>"),
        ("`×`", r"×"), ("`Prod ` (prefix)", r"\bProd\s+[^\s.]"),
        ("`∀`", r"∀"), ("`forall`", r"\bforall\b"),
        ("`∃`", r"∃"), ("`exists`/`Exists`", r"\b[Ee]xists\b"),
        ("`≠`", r"≠"), ("`!=` (Bool)", r"!="),
        ("`¬`", r"¬"), ("`Not `", r"\bNot\b"),
        ("`≤`", r"≤"), ("`<=`", r"<="),
        ("`∘`", r"∘"),
        ("`⟨…⟩`", r"⟨"), ("`.mk`", r"\.mk\b"),
        ("`<|`", r"<\|"), ("`$`", r"(?<![\w$])\$(?![\w\"{])"), ("`|>.`", r"\|>\."), ("`|>`", r"\|>(?!\.)"),
        ("`λ`", r"λ"), ("`fun`", r"(?<![\w.'])fun\b"),
    ]
    regex_table(cols, pairs)
    rows = []
    for c in cols:
        cnt = collections.Counter()
        for f in files(c):
            for m in re.finditer(r"[{(⦃\[]\s*([^\s:{}()\[\]⦃⦄,][^:{}()\[\]⦃⦄]*?)\s*:\s*(?:Type|Sort)\b",
                                 "\n".join(f["code"])):
                for v in m.group(1).split():
                    if re.match(r"^[α-ωΑ-Ω][₀-₉']*$", v):
                        cnt["greek"] += 1
                    elif re.match(r"^[a-zA-Z][₀-₉']*$", v):
                        cnt["latin1"] += 1
                    else:
                        cnt["longer"] += 1
        t = sum(cnt.values())
        rows.append([c, t, pct(cnt["greek"], t), pct(cnt["latin1"], t), pct(cnt["longer"], t)])
    print("\n### names bound with `: Type …`/`: Sort …` in binders")
    print(table(["col", "n", "Greek letter", "single Latin letter", "longer name"], rows))


SECTIONS = {
    "baseline": s_baseline, "naming": s_naming, "lambda": s_lambda, "helpers": s_helpers,
    "format": s_format, "do": s_do, "errors": s_errors, "termination": s_termination, "data": s_data,
    "attrs": s_attrs, "visibility": s_visibility, "docs": s_docs, "tests": s_tests, "proofs": s_proofs,
    "unicode": s_unicode,
}


def main(argv):
    cols = COLS
    if "--cols" in argv:
        i = argv.index("--cols")
        cols = argv[i + 1].split(",")
        argv = argv[:i] + argv[i + 2:]
    if "--samples" in argv:  # --samples COL REGEX [K]
        i = argv.index("--samples")
        col, rx = argv[i + 1], argv[i + 2]
        k = int(argv[i + 3]) if len(argv) > i + 3 else 8
        print("\n".join(samples(col, rx, k)))
        return
    secs = argv or list(SECTIONS)
    for s in secs:
        SECTIONS[s](cols)
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
