"""Controllo mensile delle fonti ufficiali: confronta sources/ con i repository di oggi.

Scarica (clone superficiale, solo lettura) modelcontextprotocol/modelcontextprotocol e
modelcontextprotocol/ext-apps in una cartella temporanea e riporta:
  - il commit di riferimento salvato in sources/SOURCES.md e quello attuale;
  - i file .mdx cambiati, nuovi o spariti rispetto alle copie .md in sources/ (spec 2026-07-28, docs 2026-07-28,
    extensions, registry, community, seps) e la spec stabile di MCP Apps;
  - nuove revisioni della spec (cartelle in docs/specification) e di MCP Apps (cartelle in specification/).
Non modifica nulla: chi lo esegue decide cosa aggiornare nel corso e nelle domande.
Uso: python3 site/build/check_sources.py [--keep DIR]   (codice di uscita 1 se qualcosa è cambiato)
"""
import filecmp, os, re, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "sources")
# cartella in sources/ -> cartella nel repo principale
MAP = {"spec-2026-07-28": "docs/specification/2026-07-28", "docs": "docs/docs/2026-07-28", "extensions": "docs/extensions",
       "registry": "docs/registry", "community": "docs/community", "seps": "seps"}
APPS_STABLE = "2026-01-26"


def clone(url, dest):
    env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")
    subprocess.run(["git", "clone", "-q", "--depth", "1", url, dest], check=True, env=env, timeout=900)
    return subprocess.run(["git", "-C", dest, "log", "-1", "--format=%H %cs"], capture_output=True, text=True).stdout.strip()


def compare(src_dir, repo_dir, only_existing=False):
    """Differenze tra le copie .md in sources/ e i .mdx/.md del repo."""
    changed, new, gone = [], [], []
    have = set()
    for dp, _, fs in os.walk(repo_dir):
        for f in fs:
            if not f.endswith((".mdx", ".md")):
                continue
            rel = os.path.relpath(os.path.join(dp, f), repo_dir)
            mine = os.path.join(src_dir, re.sub(r"\.mdx?$", ".md", rel))
            have.add(os.path.normpath(mine))
            if os.path.exists(mine):
                if not filecmp.cmp(os.path.join(dp, f), mine, shallow=False):
                    changed.append(rel)
            elif not only_existing:
                new.append(rel)
    for dp, _, fs in os.walk(src_dir):
        for f in fs:
            p = os.path.normpath(os.path.join(dp, f))
            if f.endswith(".md") and p not in have:
                gone.append(os.path.relpath(p, src_dir))
    return changed, new, gone


def main():
    keep = sys.argv[sys.argv.index("--keep") + 1] if "--keep" in sys.argv else None
    tmp = keep or tempfile.mkdtemp(prefix="mcpa-sources-")
    ref = re.search(r"commit `([0-9a-f]{40})`", open(os.path.join(SRC, "SOURCES.md"), encoding="utf-8").read())
    main_repo = os.path.join(tmp, "modelcontextprotocol")
    head = clone("https://github.com/modelcontextprotocol/modelcontextprotocol", main_repo)
    print("Repo spec: riferimento", ref.group(1)[:7] if ref else "?", "| oggi", head)
    dirty = False
    for mine, theirs in MAP.items():
        # docs e community in sources/ sono una selezione: i file nuovi del repo non sono segnalati
        c, n, g = compare(os.path.join(SRC, mine), os.path.join(main_repo, theirs), only_existing=mine in ("docs", "community"))
        g = [x for x in g if (mine, x) != ("community", "roadmap.md")]  # roadmap.md viene da docs/development
        n = [x for x in n if (mine, x) != ("spec-2026-07-28", "schema.mdx")]  # pagina generata: in sources/ c'è schema.ts
        if mine == "community":
            r = os.path.join(main_repo, "docs/development/roadmap.mdx")
            if os.path.exists(r) and not filecmp.cmp(r, os.path.join(SRC, "community/roadmap.md"), shallow=False):
                c.append("../development/roadmap.mdx")
        for label, items in (("CAMBIATI", c), ("NUOVI", n), ("SPARITI", g)):
            if items:
                dirty = True
                print(f"  {mine}: {label} {len(items)}: " + ", ".join(sorted(items)[:15]) + (" ..." if len(items) > 15 else ""))
    for f in ("schema.ts", "schema.json"):  # fonte di verità della spec, nel repo sotto schema/
        if not filecmp.cmp(os.path.join(main_repo, "schema/2026-07-28", f), os.path.join(SRC, "spec-2026-07-28", f), shallow=False):
            dirty = True
            print(f"  spec-2026-07-28: CAMBIATO {f}")
    revs = sorted(d for d in os.listdir(os.path.join(main_repo, "docs/specification")) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d))
    newer = [r for r in revs if r > "2026-07-28"]
    if newer:
        dirty = True
        print("  NUOVE revisioni della spec:", ", ".join(newer))
    apps_repo = os.path.join(tmp, "ext-apps")
    print("Repo ext-apps: oggi", clone("https://github.com/modelcontextprotocol/ext-apps", apps_repo))
    spec = os.path.join(apps_repo, "specification")
    a = os.path.join(spec, APPS_STABLE, "apps.mdx")
    if not filecmp.cmp(a, os.path.join(SRC, "ext-apps", APPS_STABLE, "apps.md"), shallow=False):
        dirty = True
        print(f"  MCP Apps {APPS_STABLE}: CAMBIATA")
    stable = sorted(d for d in os.listdir(spec) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d))
    if stable and stable[-1] > APPS_STABLE:
        dirty = True
        print("  NUOVA revisione stabile di MCP Apps:", stable[-1])
    print("Esito:", "da aggiornare (vedi sopra)" if dirty else "nessun cambiamento")
    if not keep:
        subprocess.run(["rm", "-rf", tmp])
    sys.exit(1 if dirty else 0)


if __name__ == "__main__":
    main()
