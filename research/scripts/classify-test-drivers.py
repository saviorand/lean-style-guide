import base64, json, re, subprocess, sys, os
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1])]
os.makedirs("lakefiles", exist_ok=True)
for repo, fork, path in rows:
    f = "lakefiles/" + repo.replace("/", "_") + ".toml"
    if not os.path.exists(f) or os.path.getsize(f) == 0:
        r = subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}", "--jq", ".content"], capture_output=True, text=True)
        open(f, "w").write(base64.b64decode(r.stdout or "").decode("utf-8", "replace"))
    s = open(f).read()
    m = re.search(r'^\s*testDriver\s*=\s*"([^"]*)"', s, re.M)
    drv = m.group(1) if m else "?"
    d = drv.split("/")[-1]
    kind = "dep" if "/" in drv else "?"
    for b in re.split(r"\n(?=\[\[)", s):
        mm = re.match(r"\[\[(lean_exe|lean_lib|script)\]\]", b)
        if mm and re.search(r'name\s*=\s*"' + re.escape(d) + r'"', b):
            kind = mm.group(1)
    deps = sorted(set(x.lower() for x in re.findall(r'(?i)"(lspec|plausible|batteries|mathlib|aesop|verso)"', s)))
    print(f"{repo:44} {drv:24} {kind:9} {','.join(deps)}")
