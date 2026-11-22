# -*- coding: utf-8 -*-
"""Controlli di coerenza ripetibili. Uso: python3 site/build/check_consistency.py
1. struttura delle domande (id, topic, dominio, opzioni, risposte corrette, tipo single/multi)
2. italiano/inglese: campi presenti, stesso numero di opzioni e punti, stessi token tecnici
3. file sorgente (content/) -> bank.json
4. bank.json -> database SQLite creato da zero con le migrazioni (server.migrate + import_bank)
Esce con codice 1 se trova errori (gli avvisi non bloccano)."""
import glob, json, os, re, sys, tempfile, importlib.util
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = os.path.join(ROOT, "site"); C = os.path.join(SITE, "content")
errors, warns = [], []
def E(m): errors.append(m)
CROSS = []
def W(m): warns.append(m)

bank = json.load(open(os.path.join(SITE, "bank.json"), encoding="utf-8"))
topics = {t["id"]: t for d in bank["course"] for t in d["topics"]}

# token tecnici che devono essere identici in IT e EN
TOK = re.compile(r"(?<![A-Za-z])-?\d{4,6}\b|\b\d+(?:\.\d+)?\s?%|\b[a-z]+(?:/[a-zA-Z_]+)+\b|\b[a-z]+[A-Z][A-Za-z]+\b|\bio\.modelcontextprotocol/[a-z-]+|\b(?:MUST NOT|SHOULD NOT|MUST|SHOULD|MAY)\b|\bRFC ?\d+|\bSEP-\d+")
IGN = {"and/or", "e/o", "code/spec", "codice/spec", "maiuscole/minuscole", "user/server", "utente/server"}
def toks(s):
    s = re.sub(r"(?<=\d)-(?=\d{4})", " ", s or "")  # 2025-2026 non è un codice di errore negativo
    return Counter(t.replace(" ", "") for t in TOK.findall(s) if t not in IGN)
def cmp_tokens(where, it, en):
    a, b = toks(it), toks(en)
    if a != b:
        miss_it = b - a; miss_en = a - b
        W(f"{where}: token diversi IT/EN  solo EN={dict(miss_it)} solo IT={dict(miss_en)}")

# ---------- 1-2 domande ----------
ids = Counter(q["id"] for q in bank["questions"])
for i, n in ids.items():
    if n > 1: E(f"id duplicato {i}")
stems = Counter((q["q"].get("en") or "").strip().lower() for q in bank["questions"])
for s, n in stems.items():
    if n > 1 and s: W(f"testo duplicato ({n}x): {s[:80]}")
MULTI_HINT = re.compile(r"(?:scegli|choose|select|seleziona|selezionane)\s+(?:the\s+|le\s+)?(?:\d|two|three|four|due|tre|quattro|all|tutte)", re.I)
for q in bank["questions"]:
    qid = q["id"]
    if q["t"] not in topics: E(f"{qid}: topic {q['t']} inesistente")
    elif q["dom"] != q["t"][:2]:
        # per le domande esterne il dominio è quello dichiarato dalla fonte, il topic è il link alla teoria: può differire
        (E if q["src"] == "original" else lambda m: CROSS.append(m))(f"{qid}: dominio {q['dom']} diverso dal topic {q['t']}")
    n = len(q["o"])
    if n < 2: E(f"{qid}: meno di 2 opzioni")
    if not q["c"] or any(not (0 <= c < n) for c in q["c"]): E(f"{qid}: indici corretti non validi {q['c']}")
    if len(set(q["c"])) != len(q["c"]): E(f"{qid}: risposta corretta ripetuta")
    if (q["type"] == "single") != (len(q["c"]) == 1): E(f"{qid}: type={q['type']} ma {len(q['c'])} risposte corrette")
    opts_en = [(o.get("en") or "").strip().lower() for o in q["o"]]
    if len(set(opts_en)) != len(opts_en): E(f"{qid}: opzioni duplicate")
    bilingual = q["src"] == "original"
    langs = ["it", "en"] if bilingual else ["en"]
    for L in langs:
        if not (q["q"].get(L) or "").strip(): E(f"{qid}: testo {L} mancante")
        if not (q["x"].get(L) or "").strip(): E(f"{qid}: spiegazione {L} mancante")
        for k, o in enumerate(q["o"]):
            if not (o.get(L) or "").strip(): E(f"{qid}: opzione {k} {L} mancante")
    if len(q["c"]) > 1:
        for L in langs:
            m = MULTI_HINT.search(q["q"].get(L) or "")
            if not m: W(f"{qid}: domanda multipla senza indicazione '(scegli N)' in {L}")
            else:
                W2N = {"two": 2, "due": 2, "three": 3, "tre": 3, "four": 4, "quattro": 4}
                w = re.findall(r"\d|two|three|four|due|tre|quattro", m.group(0).lower())
                num = (int(w[0]) if w[0].isdigit() else W2N[w[0]]) if w else None
                if num and num != len(q["c"]): E(f"{qid}: dice di sceglierne {num.group(0)} ma le corrette sono {len(q['c'])} ({L})")
    if bilingual:
        cmp_tokens(f"{qid} testo", q["q"]["it"], q["q"]["en"])
        cmp_tokens(f"{qid} spiegazione", q["x"]["it"], q["x"]["en"])
        for k, o in enumerate(q["o"]):
            cmp_tokens(f"{qid} opzione {k}", o["it"], o["en"])

# lunghezza della risposta corretta (indizio involontario), solo domande originali a risposta singola
orig_single = [q for q in bank["questions"] if q["src"] == "original" and len(q["c"]) == 1]
longest = [q["id"] for q in orig_single if max(range(len(q["o"])), key=lambda k: len(q["o"][k]["en"])) == q["c"][0]
           and len(q["o"][q["c"][0]]["en"]) > 1.25 * sorted(len(o["en"]) for o in q["o"])[-2]]
pos = Counter(q["c"][0] for q in orig_single)

# corso IT/EN
for tid, t in topics.items():
    for f in ("title", "summary"):
        if not (t[f].get("it") and t[f].get("en")): E(f"{tid}: {f} IT/EN mancante")
    if len(t["points"]["it"]) != len(t["points"]["en"]): E(f"{tid}: {len(t['points']['it'])} punti IT vs {len(t['points']['en'])} EN")
    for k, (a, b) in enumerate(zip(t["points"]["it"], t["points"]["en"])):
        cmp_tokens(f"{tid} punto {k+1}", a, b)
    if t.get("trap"): cmp_tokens(f"{tid} trap", t["trap"]["it"], t["trap"]["en"])

# ---------- 3 content -> bank ----------
src = []
for f in sorted(glob.glob(f"{C}/questions-D*.json")) + sorted(glob.glob(f"{C}/questions-hard*.json")):
    src += json.load(open(f, encoding="utf-8"))
bq = {q["id"]: q for q in bank["questions"]}
for q in src:
    b = bq.get(q["id"])
    if not b: E(f"{q['id']}: nei file sorgente ma non in bank.json"); continue
    for k in ("q", "o", "c", "x", "type", "t"):
        if q[k] != b[k]: E(f"{q['id']}: campo {k} diverso tra content/ e bank.json")
n_orig = sum(1 for q in bank["questions"] if q["src"] == "original")
if n_orig != len(src): E(f"bank.json ha {n_orig} domande originali, i file sorgente {len(src)}")
for D in "D1 D2 D3 D4 D5".split():
    cc = json.load(open(f"{C}/course-{D}.json", encoding="utf-8"))
    bd = next(d for d in bank["course"] if d["id"] == D)
    if cc["topics"] != bd["topics"]: E(f"course-{D}.json diverso dal corso in bank.json (rigenerare con build_data.py)")

# ---------- 4 bank -> database nuovo ----------
tmp = tempfile.mkdtemp()
os.environ["MCPA_DB"] = os.path.join(tmp, "check.db")
os.environ["MCPA_LOCAL"] = os.path.join(tmp, "no-local")  # il controllo riguarda solo i contenuti pubblicati
spec = importlib.util.spec_from_file_location("srv", os.path.join(SITE, "server.py")); srv = importlib.util.module_from_spec(spec); spec.loader.exec_module(srv)
srv.migrate(); srv.import_bank()
with srv.connect() as c:
    mig = [r[0] for r in c.execute("SELECT name FROM schema_migrations ORDER BY version")]
    files = sorted(f for f in os.listdir(os.path.join(SITE, "migrations")) if f.endswith(".sql"))
    if mig != files: E(f"migrazioni registrate {mig} diverse dai file {files}")
    rows = {r["id"]: r for r in c.execute("SELECT * FROM questions WHERE active=1")}
    if set(rows) != set(bq): E(f"DB: {len(rows)} domande attive vs {len(bq)} in bank.json")
    for qid, q in bq.items():
        r = rows.get(qid)
        if not r: continue
        exp = (q["t"], q["dom"], q["src"], q["set"], q["type"], q["q"].get("it"), q["q"].get("en"), q["x"].get("it"), q["x"].get("en"))
        got = (r["topic_id"], r["domain_id"], r["source"], r["set_name"], r["type"], r["stem_it"], r["stem_en"], r["explanation_it"], r["explanation_en"])
        if exp != got: E(f"DB {qid}: campi diversi da bank.json")
        opts = c.execute("SELECT idx,text_it,text_en,is_correct FROM options WHERE question_id=? ORDER BY idx", (qid,)).fetchall()
        if [(o["text_it"], o["text_en"]) for o in opts] != [(o.get("it"), o.get("en")) for o in q["o"]]: E(f"DB {qid}: opzioni diverse")
        if [o["idx"] for o in opts if o["is_correct"]] != sorted(q["c"]): E(f"DB {qid}: risposte corrette diverse")
    nt = c.execute("SELECT count(*) FROM topics").fetchone()[0]
    if nt != len(topics): E(f"DB: {nt} topic vs {len(topics)}")
    data = srv.get_data(c)
    if len(data["questions"]) != len(bq): E("API /api/data: numero di domande diverso")

# ---------- report ----------
q_all = bank["questions"]
print(f"Domande: {len(q_all)} ({Counter(q['src'] for q in q_all)})")
print(f"  a risposta multipla: {sum(1 for q in q_all if len(q['c'])>1)}; originali a risposta singola: {len(orig_single)}")
print(f"  posizione della risposta corretta (originali singole): {dict(sorted(pos.items()))}")
print(f"  risposta corretta nettamente più lunga delle altre: {len(longest)} {longest[:20]}")
print(f"  domande esterne con teoria in un altro dominio (voluto): {len(CROSS)}")
print(f"Topic: {len(topics)}; migrazioni: {mig}")
print(f"ERRORI: {len(errors)}"); [print("  E", e) for e in errors]
print(f"AVVISI: {len(warns)}"); [print("  W", w) for w in warns]
sys.exit(1 if errors else 0)
