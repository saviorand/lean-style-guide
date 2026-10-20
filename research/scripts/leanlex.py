"""Shared helpers for the stdlib style survey.

Run every survey script from `research/vendor/repos` (the scripts locate this module via
their own directory). Nothing here is Lean-accurate: it is a regex/line-based approximation
whose error modes are documented in `research/stdlib-survey.md`.
"""
import os
import pickle
import re
import subprocess

# Columns of every table. Each column is a list of directories relative to research/vendor/repos.
SUBTREES = [
    ("Init", ["lean4/src/Init"]),
    ("Std", ["lean4/src/Std"]),
    ("Lake", ["lean4/src/lake/Lake"]),
    ("Lean", ["lean4/src/Lean"]),
    ("Batteries", ["batteries/Batteries"]),
    ("Mathlib", ["mathlib4/Mathlib"]),
    ("Wild", ["lean-regex/regex/Regex", "lean-regex/correctness/RegexCorrectness",
              "lean4-parser/Parser", "lean4-cli/Cli"]),
]
COLS = [name for name, _ in SUBTREES]

# Opt-in columns, left out of COLS so default runs reproduce stdlib-survey.md; select with --cols.
# FPIL: the book's example code (without its Verso/test infrastructure ExampleSupport.lean). It
# includes deliberately broken examples and successive drafts of the same definition.
EXTRA_SUBTREES = [
    ("FPIL", ["fp-lean/examples/Examples", "fp-lean/examples/douglib", "fp-lean/examples/early-return",
              "fp-lean/examples/feline", "fp-lean/examples/first-lake", "fp-lean/examples/hello-name",
              "fp-lean/examples/second-lake", "fp-lean/examples/simple-hello"]),
]

# Opt-in per-author columns of FRO program code, written by `authors.py --write-columns`.
_AUTHOR_COLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "author-columns.json")
if os.path.exists(_AUTHOR_COLS):
    import json
    with open(_AUTHOR_COLS) as _fh:
        EXTRA_SUBTREES += [(c, paths) for c, paths in json.load(_fh)]

GITHUB = {
    "lean4": "leanprover/lean4",
    "batteries": "leanprover-community/batteries",
    "mathlib4": "leanprover-community/mathlib4",
    "lean-regex": "pandaman64/lean-regex",
    "lean4-parser": "fgdorais/lean4-parser",
    "lean4-cli": "leanprover/lean4-cli",
    "fp-lean": "leanprover/fp-lean",
    "verso": "leanprover/verso",
    "doc-gen4": "leanprover/doc-gen4",
}

_SHA = {}


def sha(repo):
    if repo not in _SHA:
        _SHA[repo] = subprocess.check_output(["git", "-C", repo, "rev-parse", "HEAD"], text=True).strip()
    return _SHA[repo]


def permalink(path, a, b=None):
    """path is relative to research/vendor/repos, lines are 1-based."""
    repo, rel = path.split("/", 1)
    frag = f"#L{a}" if b is None or b == a else f"#L{a}-L{b}"
    return f"https://github.com/{GITHUB[repo]}/blob/{sha(repo)}/{rel}{frag}"


def lean_files(dirs):
    out = []
    for d in dirs:
        if os.path.isfile(d):
            if d.endswith(".lean"):
                out.append(d)
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(".lean"):
                    out.append(os.path.join(root, f))
    return sorted(out)


# ---------------------------------------------------------------------------------------------
# Lexing: blank out comments and string/char literal contents, keep line structure and columns.

_SPECIAL = re.compile(r"--|/-|\"|'|(?<![\w'])r#*\"")
_BLOCK = re.compile(r"/-|-/")
_CHARLIT = re.compile(r"'(?:\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|[^\n])|[^'\\\n])'")
_STRING_END = re.compile(r'(?:[^"\\]|\\.)*"', re.S)


def _blank(chunk):
    return re.sub(r"[^\n]", " ", chunk)


def _ident_char(c):
    return c.isalnum() or c in "_'!?"


class FileInfo:
    __slots__ = ("path", "raw", "code", "docs", "moddocs", "is_module")


def lex(path):
    """Return a FileInfo with raw lines, code lines (comments/literals blanked), and comments.

    docs: list of (start_line, end_line, end_col, text) for `/-- -/` comments (0-based lines).
    moddocs: same for `/-! -/` comments.
    """
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    out = []
    docs, moddocs = [], []
    i, n = 0, len(text)
    while i < n:
        m = _SPECIAL.search(text, i)
        if not m:
            out.append(text[i:])
            break
        j = m.start()
        tok = m.group(0)
        out.append(text[i:j])
        if tok == "--":
            k = text.find("\n", j)
            k = n if k < 0 else k
            out.append(_blank(text[j:k]))
            i = k
        elif tok == "/-":
            depth, k = 1, j + 2
            while depth and k < n:
                b = _BLOCK.search(text, k)
                if not b:
                    k = n
                    break
                depth += 1 if b.group(0) == "/-" else -1
                k = b.end()
            chunk = text[j:k]
            kind = text[j + 2] if j + 2 < n else ""
            if kind in "-!" and not chunk.startswith("/--/"):
                sl = text.count("\n", 0, j)
                el = sl + chunk.count("\n")
                ec = k - (text.rfind("\n", 0, k) + 1)
                body = chunk[3:-2] if len(chunk) >= 5 else ""
                (docs if kind == "-" else moddocs).append((sl, el, ec, body))
            out.append(_blank(chunk))
            i = k
        elif tok == "'":
            if j > 0 and _ident_char(text[j - 1]):
                out.append("'")
                i = j + 1
                continue
            c = _CHARLIT.match(text, j)
            if c:
                out.append("'" + " " * (len(c.group(0)) - 2) + "'")
                i = c.end()
            else:
                out.append("'")
                i = j + 1
        elif tok == '"':
            e = _STRING_END.match(text, j + 1)
            k = e.end() if e else n
            out.append('"' + _blank(text[j + 1:k - 1]) + '"')
            i = k
        else:  # raw string r#"..."#
            hashes = tok.count("#")
            close = '"' + "#" * hashes
            k = text.find(close, m.end())
            k = n if k < 0 else k + len(close)
            out.append(tok + _blank(text[m.end():k - len(close)]) + close)
            i = k
    code = "".join(out)
    fi = FileInfo()
    fi.path = path
    fi.raw = text.split("\n")
    fi.code = code.split("\n")
    fi.docs = docs
    fi.moddocs = moddocs
    fi.is_module = any(l.strip() == "module" for l in fi.code[:40])
    return fi


_CACHE_DIR = os.environ.get("SURVEY_CACHE", "../survey-cache")


def load(col):
    """Lex every file of a column (cached by repo SHAs)."""
    dirs = dict(SUBTREES + EXTRA_SUBTREES)[col]
    key = "-".join(sha(d.split("/")[0])[:10] for d in dirs)
    if len(dirs) > 8:  # file-list columns: one SHA per repo plus a digest of the list
        import hashlib
        key = "-".join(sorted({sha(d.split("/")[0])[:10] for d in dirs}))
        key += "-" + hashlib.sha1("\n".join(dirs).encode()).hexdigest()[:10]
    cache = os.path.join(_CACHE_DIR, f"{col}-{key}.pickle")
    if os.path.exists(cache):
        with open(cache, "rb") as fh:
            return pickle.load(fh)
    files = []
    for p in lean_files(dirs):
        fi = lex(p)
        files.append({k: getattr(fi, k) for k in FileInfo.__slots__})
    os.makedirs(_CACHE_DIR, exist_ok=True)
    with open(cache, "wb") as fh:
        pickle.dump(files, fh)
    return files


def nonblank(lines):
    return sum(1 for l in lines if l.strip())


# ---------------------------------------------------------------------------------------------
# Declarations

_KW = (r"(?P<kw>theorem|lemma|def|abbrev|instance|structure|class\s+inductive|class\s+abbrev|class|"
       r"inductive|coinductive|opaque|axiom|example)")
_MODS = r"(?P<mods>(?:(?:private|protected|public|noncomputable|partial|unsafe|nonrec|meta)\s+)*)"
DECL_RE = re.compile(r"^(?P<ind>[ \t]*)" + _MODS + r"(?P<akind>(?:scoped|local)\s+)?" + _KW +
                     r"(?=[\s(\[{:⦃]|$)(?P<rest>.*)$")
SCOPE_RE = re.compile(r"^\s*(?:(?P<pub>public)\s+)?(?:(?:noncomputable|meta)\s+)*(?P<cmd>namespace|section)\b\s*(?P<name>[^\s]*)")
MUTUAL_RE = re.compile(r"^\s*mutual\s*$")
END_RE = re.compile(r"^\s*end\b\s*(?P<name>[^\s]*)\s*$")
NAME_RE = re.compile(r"^\s*(?P<name>«[^»]*»|[^\s(\[{:⦃]+)")
_PRIO = re.compile(r"^\s*\(priority\s*:=[^)]*\)")


def split_top(s, sep=","):
    parts, depth, cur = [], 0, []
    for c in s:
        if c in "([{⟨":
            depth += 1
        elif c in ")]}⟩":
            depth -= 1
        if c == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def _scan_attrs(code, i, col):
    """Starting at code[i][col] == '@', consume one or more `@[...]` blocks (possibly multi-line).
    Returns (list_of_attr_strings, line, col_after)."""
    attrs = []
    line, c = i, col
    while True:
        s = code[line]
        while c < len(s) and s[c] in " \t":
            c += 1
        if not s.startswith("@[", c):
            break
        depth, buf, c = 0, [], c + 1
        while True:
            s = code[line]
            if c >= len(s):
                buf.append(" ")
                line += 1
                c = 0
                if line >= len(code):
                    return attrs, line - 1, 0
                continue
            ch = s[c]
            if ch == "[":
                depth += 1
                if depth > 1:
                    buf.append(ch)
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    c += 1
                    break
                buf.append(ch)
            else:
                buf.append(ch)
            c += 1
        attrs.extend(split_top("".join(buf)))
    return attrs, line, c


class Decl:
    __slots__ = ("file", "line", "start", "kw", "mods", "akind", "attrs", "name", "qname", "indent",
                 "public", "doc", "inherit_doc", "header", "header_lines", "instance_named")


def decls(f):
    """Yield Decl objects for one lexed file (dict from load())."""
    code = f["code"]
    doc_end = {}
    for idx, (sl, el, ec, body) in enumerate(f["docs"]):
        doc_end[el] = (ec, body)
    is_module = f["is_module"]
    scopes = []  # (kind, nameparts, exporting)
    pending, pending_start = [], None
    out = []
    i, n = 0, len(code)
    while i < n:
        s = code[i]
        st = s.strip()
        if not st:
            i += 1
            continue
        start = i if pending_start is None else pending_start
        if st.startswith("@["):
            col = s.index("@[")
            attrs, j, c = _scan_attrs(code, i, col)
            pending.extend(attrs)
            pending_start = start
            rest = code[j][c:] if j < n else ""
            if not rest.strip():
                i = j + 1
                continue
            s = " " * c + rest
            i = j
        exporting = scopes[-1][2] if scopes else False
        m = SCOPE_RE.match(s)
        if m and not DECL_RE.match(s):
            parts = [p for p in m.group("name").split(".") if p] if m.group("name") else []
            if m.group("cmd") == "namespace":
                scopes.append(("ns", parts, exporting))
            else:
                scopes.append(("sec", parts, exporting or bool(m.group("pub"))))
            pending, pending_start = [], None
            i += 1
            continue
        if MUTUAL_RE.match(s):
            scopes.append(("mutual", [], exporting))
            i += 1
            continue
        m = END_RE.match(s)
        if m:
            want = len([p for p in m.group("name").split(".") if p])
            if want == 0:
                if scopes:
                    scopes.pop()
            else:
                got = 0
                while scopes and got < want:
                    got += len(scopes.pop()[1])
            pending, pending_start = [], None
            i += 1
            continue
        m = DECL_RE.match(s)
        if m:
            d = Decl()
            d.file = f["path"]
            d.line = i
            d.start = start
            d.kw = re.sub(r"\s+", " ", m.group("kw"))
            if d.kw == "lemma":
                d.kw = "theorem"
            d.mods = m.group("mods").split()
            d.akind = (m.group("akind") or "").strip()
            d.attrs = pending
            d.indent = len(code[start]) - len(code[start].lstrip())
            rest = m.group("rest")
            d.instance_named = None
            if d.kw == "instance":
                r2 = _PRIO.sub("", rest)
                nm = NAME_RE.match(r2)
                tok = nm.group("name") if nm else ""
                named = bool(tok) and (tok[0].isalpha() or tok[0] in "_«") and tok not in ("where",)
                d.instance_named = named
                d.name = tok if named else ""
            elif d.kw == "example":
                d.name = ""
            else:
                nm = NAME_RE.match(rest)
                d.name = nm.group("name") if nm else ""
            ns = [p for sc in scopes if sc[0] == "ns" for p in sc[1]]
            if d.name.startswith("_root_."):
                d.qname = d.name[len("_root_."):]
            else:
                d.qname = ".".join(ns + [d.name]) if d.name else ""
            if "private" in d.mods:
                d.public = False
            elif "public" in d.mods or not is_module:
                d.public = True
            else:
                d.public = exporting
            # documentation: a doc comment ending on the start line (before the code) or on the
            # previous non-blank line.
            d.doc = None
            first_code_col = len(code[start]) - len(code[start].lstrip())
            if start in doc_end and doc_end[start][0] <= first_code_col:
                d.doc = doc_end[start][1]
            else:
                p = start - 1
                while p >= 0 and not f["raw"][p].strip():
                    p -= 1
                if p >= 0 and p in doc_end and not code[p][doc_end[p][0]:].strip():
                    d.doc = doc_end[p][1]
            d.inherit_doc = any(a.split()[0] == "inherit_doc" for a in pending if a.split())
            # header: up to the first `:=`, a trailing `where`, or a following `|` line
            hdr, k = [], i
            while k < n and k < i + 25:
                line = code[k] if k != i else s
                if k > i and line.strip() and (line.lstrip().startswith("|") or DECL_RE.match(line)
                                               or line.lstrip().startswith("deriving")):
                    break
                if (k > i and line.strip() and len(line) - len(line.lstrip()) <= d.indent
                        and not line.lstrip().startswith(":")):
                    break  # back at top level: header had no body (e.g. `opaque`, `axiom`)
                hdr.append(line)
                if ":=" in line or re.search(r"\bwhere\s*$", line):
                    break
                k += 1
            d.header = "\n".join(hdr)
            d.header_lines = len(hdr)
            out.append(d)
            pending, pending_start = [], None
            i += 1
            continue
        pending, pending_start = [], None
        i += 1
    return out


def last_component(name):
    name = name.strip("«»")
    parts = [p for p in name.split(".") if p]
    return parts[-1] if parts else name


def case_class(name):
    """Classify the case convention of one identifier component."""
    core = re.sub(r"[?!'₀-₉ᵢ]+$", "", name)
    core = core.rstrip("?!'")
    if not core or not (core[0].isalpha() or core[0] == "_"):
        return "other"
    if core.startswith("_"):
        return "other"
    has_us = "_" in core
    has_upper = any(c.isupper() for c in core[1:])
    if core[0].isupper():
        return "Upper_snake" if has_us else "UpperCamel"
    if not core[0].islower():
        return "other"  # e.g. Greek capital-less scripts, digits
    if has_us:
        return "snake+camel" if has_upper else "snake"
    return "lowerCamel" if has_upper else "lowerword"


def pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "–"


def per_k(count, nb):
    return f"{1000.0 * count / nb:.2f}" if nb else "–"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def quantile(sorted_vals, q):
    if not sorted_vals:
        return 0
    k = min(len(sorted_vals) - 1, int(round(q * (len(sorted_vals) - 1))))
    return sorted_vals[k]
