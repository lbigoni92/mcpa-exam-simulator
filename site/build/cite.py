"""Trova per ogni domanda la frase della documentazione ufficiale che giustifica la risposta corretta.

Indicizza le frasi (paragrafi, voci di elenco, righe di tabella) di sources/spec-2026-07-28, docs, community,
extensions, registry, seps e blog; per ogni domanda cerca con BM25 la frase più vicina a risposta corretta +
spiegazione, con un peso extra per i token tecnici (codici d'errore, header, metodi, campi, RFC).

Scrive site/build/citations.json: {id: {"text", "src", "url", "lvl", "score"}}.
lvl: "spec" (spec 2026-07-28), "docs" (docs, community, extensions, registry, SEP), "blog" (post del blog MCP).
Le correzioni manuali dopo l'audit stanno in site/build/citation_overrides.json, id ->
  {"src": file, "find": regex}  frase del file che contiene la regex (paragrafo o voce d'elenco; una voce
                                corta prende anche la frase che introduce l'elenco)
  {"src": file, "text": testo}  testo esplicito (estratto letterale della fonte)
  {"lvl": "blog"}               nessun riscontro normativo: la domanda resta nella pratica ma esce dagli esami
Uso: python3 site/build/cite.py  (poi build_data.py)"""
import json, math, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "sources")
DIRS = {"spec-2026-07-28": "spec", "spec-older-changelogs": "spec", "docs": "docs", "community": "docs", "extensions": "docs",
        "registry": "docs", "seps": "docs", "blog": "blog"}
# spec-2025-11-25 è citabile solo con un override (es. il suo changelog): non entra nell'indice BM25, che
# altrimenti sceglierebbe testo superato per le domande sulla 2026-07-28
LVL = dict(DIRS, **{"spec-2025-11-25": "spec"})
STOP = set("the a an of to and or in on for is are be with by as at it its this that which what when how does do from not no can "
           "must should may their they your you will any all one only than then into more over per new each other there these those "
           "has have was were been being but if so such also using use used via".split())
TECH = re.compile(r"-32\d{3}|\b(?:mcp|www)-[a-z-]+|\b[a-z]+/[a-z_/]+|\b[a-z]+[A-Z][A-Za-z]+\b|\brfc ?\d{3,4}|\bsep-\d+|\b[1-5]\d\d\b", re.I)


def url_of(rel):
    p = rel[:-3]
    if p.endswith("/index"):
        p = p[:-6]
    top, rest = (p.split("/", 1) + [""])[:2]
    if top.startswith("spec-20"):
        return f"https://modelcontextprotocol.io/specification/{top[5:]}/" + rest
    if top == "spec-older-changelogs":
        return f"https://modelcontextprotocol.io/specification/{rest[:10]}/changelog"
    if top == "blog":
        return "https://blog.modelcontextprotocol.io/posts/" + rest.split("/")[0] + "/"
    return f"https://modelcontextprotocol.io/{top}/{rest}".rstrip("/")


def toks(s):
    s = s.replace("`", "")
    return [w for w in re.findall(r"[a-z0-9][a-z0-9_/\-.]*[a-z0-9]|[a-z0-9]", s.lower()) if w not in STOP and len(w) > 1]


def clean(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)          # link markdown -> testo
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\*\*|__", "", s)
    s = re.sub(r"\s*\|\s*", " | ", s).strip(" |")
    return re.sub(r"\s+", " ", s).strip()


def sentences():
    out = []
    for top, lvl in DIRS.items():
        base = os.path.join(SRC, top)
        for dp, _, fs in os.walk(base):
            if "aaif" in dp:
                continue  # sintesi in italiano dei post AAIF: non citabili
            for f in fs:
                if not f.endswith(".md"):
                    continue
                path = os.path.join(dp, f); rel = os.path.relpath(path, SRC)
                text = open(path, encoding="utf-8").read()
                text = re.sub(r"^---.*?---", "", text, flags=re.S)
                text = re.sub(r"```.*?```", "", text, flags=re.S)
                for block in re.split(r"\n\s*\n", text):
                    lines = [l for l in block.split("\n") if l.strip()]
                    if not lines or lines[0].lstrip().startswith(("#", "import ", "<")) and len(lines) == 1:
                        continue
                    # elenchi e tabelle: una voce per riga; paragrafi: un blocco
                    if all(re.match(r"\s*([-*]|\d+\.|\|)", l) for l in lines):
                        items = lines
                    else:
                        items = [" ".join(lines)]
                    for it in items:
                        c = clean(re.sub(r"^\s*([-*]|\d+\.)\s*", "", it))
                        if 40 <= len(c) <= 600 and not re.fullmatch(r"[-| :]+", c):
                            out.append({"text": c, "src": rel, "lvl": lvl})
    return out


def find_in(rel, rx):
    """Paragrafo o voce d'elenco del file che contiene la regex (codice e frontmatter esclusi)."""
    text = open(os.path.join(SRC, rel), encoding="utf-8").read()
    text = re.sub(r"^---.*?---", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
    for k, block in enumerate(blocks):
        if not re.search(rx, clean(block), re.I | re.S):
            continue
        lines = [l for l in block.split("\n") if l.strip()]
        if len(lines) > 1 and all(re.match(r"\s*([-*]|\d+\.|\|)", l) for l in lines):
            # elenco: la voce che contiene la regex (le righe di continuazione restano unite alla voce)
            for l in lines:
                c = clean(re.sub(r"^\s*([-*]|\d+\.)\s*", "", l))
                if re.search(rx, c, re.I):
                    if len(c) < 60 and k:
                        c = clean(blocks[k - 1]).lstrip("# ").rstrip(":") + ": " + c
                    return c
        items = re.split(r"\n(?=\s*(?:[-*]|\d+\.)\s)", block)
        for it in items:
            c = clean(re.sub(r"^\s*([-*]|\d+\.)\s*", "", " ".join(it.split())))
            if re.search(rx, c, re.I | re.S):
                if len(c) < 60 and k:
                    c = clean(blocks[k - 1]).lstrip("# ").rstrip(":") + ": " + c
                return c[:700]
    print(f"ATTENZIONE override: {rx!r} non trovata in {rel}")
    return None


def main():
    bank = json.load(open(os.path.join(ROOT, "site", "bank.json"), encoding="utf-8"))
    S = sentences()
    docs = [Counter(toks(s["text"])) for s in S]
    tech = [set(m.lower() for m in TECH.findall(s["text"])) for s in S]
    df = Counter(w for d in docs for w in d)
    N = len(docs); avg = sum(sum(d.values()) for d in docs) / N
    idf = {w: math.log(1 + (N - n + .5) / (n + .5)) for w, n in df.items()}
    inv = {}
    for i, d in enumerate(docs):
        for w in d:
            inv.setdefault(w, []).append(i)
    prio = {"spec": 1.15, "docs": 1.0, "blog": 0.85}
    over = json.load(open(os.path.join(HERE, "citation_overrides.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "citation_overrides.json")) else {}
    res = {}
    for q in bank["questions"]:
        en = lambda o: o.get("en") or o.get("it") or ""
        x = q.get("x") or {}
        query = " ".join([en(q["o"][i]) for i in q["c"]] * 2 + [en(x) if isinstance(x, dict) else str(x), en(q["q"])])
        qv = Counter(toks(query)); qt = set(m.lower() for m in TECH.findall(query))
        cand = Counter()
        for w in qv:
            for i in inv.get(w, ()):
                d = docs[i]; L = sum(d.values())
                cand[i] += idf[w] * min(qv[w], 2) * d[w] * 2.2 / (d[w] + 1.2 * (.25 + .75 * L / avg))
        best, bs = None, 0
        for i, s in cand.most_common(60):
            sc = (s + 3.0 * len(qt & tech[i])) * prio[S[i]["lvl"]]
            if sc > bs:
                best, bs = i, sc
        r = dict(S[best]) if best is not None else {"text": "", "src": "", "lvl": "blog"}
        r["score"] = round(bs, 1)
        o = over.get(q["id"])
        if o:
            t = o.get("text") or (find_in(o["src"], o["find"]) if "src" in o else None)
            if "src" in o and t:
                r = {"src": o["src"], "text": t, "lvl": o.get("lvl") or LVL[o["src"].split("/")[0]]}
            elif "src" in o:
                o = None  # regex non trovata: resta la frase BM25 (avviso già stampato)
            elif r.get("lvl") != "blog":
                r = {"src": "", "text": "", "lvl": "blog"}  # la frase trovata non è una fonte valida
            if o:
                r["lvl"] = r["lvl"] if "src" in o else "blog"
                r["score"] = 99
        r["url"] = url_of(r["src"]) if r.get("src") else ""
        res[q["id"]] = r
    json.dump(res, open(os.path.join(HERE, "citations.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    lv = Counter(r["lvl"] for r in res.values())
    print(len(S), "frasi indicizzate;", len(res), "domande;", dict(lv))


if __name__ == "__main__":
    main()
