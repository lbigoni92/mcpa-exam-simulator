"""Simulatore MCPA: server locale con database SQLite.

Avvio: doppio clic su avvia.bat (Windows) oppure `python server.py`.
Usa solo la libreria standard di Python 3.8+. Il database e' il file mcpa.db (creato al primo avvio)
accanto a questo script: domande, opzioni, corso, sessioni, risposte e ripasso.
All'avvio applica le migrazioni (cartella migrations/) e importa bank.json se e' cambiato,
senza toccare sessioni e risposte. `python server.py --migrate` fa solo questo ed esce.
"""
import hashlib, json, mimetypes, os, sqlite3, sys, threading, time, webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.environ.get("MCPA_DB") or os.path.join(HERE, "mcpa.db")  # MCPA_DB: percorso del database (Docker: /data/mcpa.db)
BANK = os.path.join(HERE, "bank.json")
# Domande personali: file local/questions-*.json, esclusi da git. Si importano solo se presenti.
LOCAL = os.environ.get("MCPA_LOCAL") or os.path.join(HERE, "local")
HOST, PORT = "127.0.0.1", int(os.environ.get("MCPA_PORT", "8765"))
BIND = os.environ.get("MCPA_BIND", HOST)  # Docker: 0.0.0.0 (la porta va pubblicata solo su 127.0.0.1 dell'host)
STATIC = {"index.html", "app.js", "app.css"}
DOMS = ["D1", "D2", "D3", "D4", "D5"]

MIGRATIONS = os.path.join(HERE, "migrations")


def now():
    return datetime.now().isoformat(timespec="seconds")


def connect():
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    return c


def migrate():
    """Applica in ordine i file migrations/NNNN_*.sql non ancora registrati in schema_migrations.
    Ogni migrazione gira in una transazione; un ALTER TABLE ADD COLUMN gia' presente (database
    creati prima delle migrazioni) viene considerato applicato."""
    files = sorted(f for f in os.listdir(MIGRATIONS) if f.endswith(".sql") and f[:4].isdigit())
    applied_now = []
    c = connect()
    c.isolation_level = None  # transazioni gestite a mano (BEGIN/COMMIT)
    try:
        c.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, name TEXT, applied_at TEXT)")
        done = {r[0] for r in c.execute("SELECT version FROM schema_migrations")}
        for f in files:
            v = int(f[:4])
            if v in done:
                continue
            sql = open(os.path.join(MIGRATIONS, f), encoding="utf-8").read()
            try:
                c.execute("BEGIN")
                for stmt in [x.strip() for x in sql.split(";")]:
                    body = "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--")).strip()
                    if not body:
                        continue
                    try:
                        c.execute(body)
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" not in str(e):
                            raise
                c.execute("INSERT INTO schema_migrations VALUES (?,?,?)", (v, f, now()))
                c.execute("COMMIT")
                applied_now.append(f)
            except Exception:
                c.execute("ROLLBACK")
                raise
    finally:
        c.close()
    return applied_now


def local_files():
    if not os.path.isdir(LOCAL):
        return []
    return sorted(os.path.join(LOCAL, f) for f in os.listdir(LOCAL) if f.startswith("questions-") and f.endswith(".json"))


def local_questions():
    """Domande personali nello stesso formato di content/questions-*.json (id, t, type, q, o, c, x)."""
    out = []
    for f in local_files():
        try:
            items = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print("Domande locali ignorate (" + os.path.basename(f) + "):", e)
            continue
        for q in items:
            q = dict(q); q["dom"] = q["t"][:2]; q["src"] = "original"; q["set"] = "utente"
            out.append(q)
    return out


def import_bank(force=False):
    raw = open(BANK, "rb").read()
    for f in local_files():
        raw += b"\0" + os.path.basename(f).encode() + b"\0" + open(f, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    with connect() as c:
        row = c.execute("SELECT value FROM meta WHERE key='bank_sha256'").fetchone()
        if row and row[0] == digest and not force:
            return False
        bank = json.load(open(BANK, encoding="utf-8"))
        topic_ids = {t["id"] for d in bank["course"] for t in d["topics"]}
        loc = [q for q in local_questions() if q["t"] in topic_ids and q["id"] not in {b["id"] for b in bank["questions"]}]
        bank["questions"] = bank["questions"] + loc
        for i, d in enumerate(bank["course"]):
            c.execute("INSERT OR REPLACE INTO domains (id,name_it,name_en,weight,study_weight,ord,objectives_json) VALUES (?,?,?,?,?,?,?)",
                      (d["id"], d["title"]["it"], d["title"]["en"], d["weight"], d["studyWeight"], i,
                       json.dumps(d["objectives"], ensure_ascii=False) if d.get("objectives") else None))
            for j, t in enumerate(d["topics"]):
                c.execute("INSERT OR REPLACE INTO topics VALUES (?,?,?,?,?,?)",
                          (t["id"], d["id"], j, t["title"]["it"], t["title"]["en"], json.dumps(t, ensure_ascii=False)))
        c.execute("UPDATE questions SET active=0")
        for q in bank["questions"]:
            c.execute("""INSERT INTO questions (id,topic_id,domain_id,source,set_name,set_title,difficulty,type,
                         stem_it,stem_en,explanation_it,explanation_en,review_json,active)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,1)
                         ON CONFLICT(id) DO UPDATE SET topic_id=excluded.topic_id, domain_id=excluded.domain_id,
                         source=excluded.source, set_name=excluded.set_name, set_title=excluded.set_title,
                         difficulty=excluded.difficulty, type=excluded.type, stem_it=excluded.stem_it,
                         stem_en=excluded.stem_en, explanation_it=excluded.explanation_it,
                         explanation_en=excluded.explanation_en, review_json=excluded.review_json, active=1""",
                      (q["id"], q["t"], q["dom"], q["src"], q["set"], q.get("setTitle", ""), q.get("d"), q["type"],
                       q["q"].get("it"), q["q"].get("en"), q["x"].get("it"), q["x"].get("en"),
                       json.dumps(q["review"], ensure_ascii=False) if q.get("review") else None))
            c.execute("DELETE FROM options WHERE question_id=?", (q["id"],))
            for i, o in enumerate(q["o"]):
                c.execute("INSERT INTO options VALUES (?,?,?,?,?)",
                          (q["id"], i, o.get("it"), o.get("en"), 1 if i in q["c"] else 0))
        c.execute("INSERT OR REPLACE INTO meta VALUES ('bank_sha256',?)", (digest,))
        c.execute("INSERT OR REPLACE INTO meta VALUES ('bank_imported_at',?)", (now(),))
        c.execute("INSERT OR REPLACE INTO meta VALUES ('spec',?)", (bank.get("spec", ""),))
    return True


# ---------- queries ----------
def get_data(c):
    course = []
    for d in c.execute("SELECT * FROM domains ORDER BY ord"):
        topics = [json.loads(r["data_json"]) for r in c.execute("SELECT data_json FROM topics WHERE domain_id=? ORDER BY ord", (d["id"],))]
        course.append({"id": d["id"], "title": {"it": d["name_it"], "en": d["name_en"]}, "weight": d["weight"],
                       "studyWeight": d["study_weight"], "topics": topics,
                       "objectives": json.loads(d["objectives_json"]) if d["objectives_json"] else None})
    opts = {}
    for o in c.execute("SELECT * FROM options ORDER BY question_id, idx"):
        opts.setdefault(o["question_id"], []).append(o)
    qs = []
    for q in c.execute("SELECT * FROM questions WHERE active=1"):
        os_ = opts.get(q["id"], [])
        item = {"id": q["id"], "t": q["topic_id"], "dom": q["domain_id"], "src": q["source"], "set": q["set_name"],
                "setTitle": q["set_title"], "d": q["difficulty"], "type": q["type"],
                "q": {k: v for k, v in (("it", q["stem_it"]), ("en", q["stem_en"])) if v},
                "x": {k: v for k, v in (("it", q["explanation_it"]), ("en", q["explanation_en"])) if v},
                "o": [{k: v for k, v in (("it", o["text_it"]), ("en", o["text_en"])) if v} for o in os_],
                "c": [o["idx"] for o in os_ if o["is_correct"]]}
        if q["review_json"]:
            item["review"] = json.loads(q["review_json"])
        qs.append(item)
    return {"spec": meta(c, "spec"), "course": course, "questions": qs}


def meta(c, key):
    r = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return r[0] if r else None


def check_answer(c, qid, selected):
    corr = sorted(r[0] for r in c.execute("SELECT idx FROM options WHERE question_id=? AND is_correct=1", (qid,)))
    return 1 if sorted(int(x) for x in selected) == corr and corr else 0


def record_answer(c, sid, qid, selected, time_ms, review=True):
    q = c.execute("SELECT domain_id FROM questions WHERE id=?", (qid,)).fetchone()
    if not q:
        raise ValueError("domanda sconosciuta")
    ok = check_answer(c, qid, selected) if selected else 0
    c.execute("""INSERT INTO answers (session_id,question_id,domain_id,selected_json,correct,time_ms,answered_at)
                 VALUES (?,?,?,?,?,?,?) ON CONFLICT(session_id,question_id) DO UPDATE SET
                 selected_json=excluded.selected_json, correct=excluded.correct, time_ms=excluded.time_ms,
                 answered_at=excluded.answered_at""",
              (sid, qid, q["domain_id"], json.dumps(selected), ok, int(time_ms or 0), now()))
    # coda di ripasso: errore -> dentro; due giuste di fila -> fuori
    if not review:
        return ok
    if not ok:
        c.execute("INSERT INTO review_queue VALUES (?,0,?) ON CONFLICT(question_id) DO UPDATE SET streak=0", (qid, now()))
    else:
        r = c.execute("SELECT streak FROM review_queue WHERE question_id=?", (qid,)).fetchone()
        if r is not None:
            if r[0] + 1 >= 2:
                c.execute("DELETE FROM review_queue WHERE question_id=?", (qid,))
            else:
                c.execute("UPDATE review_queue SET streak=streak+1 WHERE question_id=?", (qid,))
    return ok


def by_domain(c, sid):
    out = {}
    for r in c.execute("""SELECT q.domain_id d, COUNT(*) n, COALESCE(SUM(a.correct),0) ok FROM session_questions sq
                          JOIN questions q ON q.id=sq.question_id
                          LEFT JOIN answers a ON a.session_id=sq.session_id AND a.question_id=sq.question_id
                          WHERE sq.session_id=? GROUP BY q.domain_id""", (sid,)):
        out[r["d"]] = {"n": r["n"], "ok": r["ok"]}
    return out


def finish_session(c, sid, time_up=False):
    s = c.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
    if not s:
        raise ValueError("sessione sconosciuta")
    n = c.execute("SELECT COUNT(*) FROM session_questions WHERE session_id=?", (sid,)).fetchone()[0]
    ok = c.execute("SELECT COALESCE(SUM(correct),0) FROM answers WHERE session_id=?", (sid,)).fetchone()[0]
    # le domande dell'esame lasciate senza risposta contano come errori (ma non riempiono il ripasso)
    if s["mode"] == "exam":
        for r in c.execute("""SELECT question_id FROM session_questions WHERE session_id=? AND question_id NOT IN
                              (SELECT question_id FROM answers WHERE session_id=?)""", (sid, sid)).fetchall():
            record_answer(c, sid, r[0], [], 0, review=False)
    started = datetime.fromisoformat(s["started_at"])
    dur = int((datetime.now() - started).total_seconds())
    pct = round(100.0 * ok / n, 1) if n else 0
    c.execute("""UPDATE sessions SET ended_at=?, duration_s=?, n_questions=?, n_correct=?, score_pct=?, passed=?, time_up=?
                 WHERE id=?""", (now(), dur, n, ok, pct, 1 if pct >= 75 else 0, 1 if time_up else 0, sid))
    return session_summary(c, sid)


def session_summary(c, sid):
    s = dict(c.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone())
    s["byDom"] = by_domain(c, sid)
    return s


def stats(c):
    sessions = []
    for s in c.execute("SELECT * FROM sessions WHERE ended_at IS NOT NULL ORDER BY id"):
        d = dict(s); d["byDom"] = by_domain(c, s["id"]); sessions.append(d)
    totals = {d: {"n": 0, "ok": 0} for d in DOMS}
    for r in c.execute("SELECT domain_id d, COUNT(*) n, SUM(correct) ok FROM answers GROUP BY domain_id"):
        if r["d"] in totals:
            totals[r["d"]] = {"n": r["n"], "ok": r["ok"] or 0}
    # ultime 30 risposte per dominio: misura dello stato attuale
    recent = {}
    for d in DOMS:
        rows = c.execute("SELECT correct FROM answers WHERE domain_id=? ORDER BY id DESC LIMIT 30", (d,)).fetchall()
        recent[d] = {"n": len(rows), "ok": sum(r[0] for r in rows)}
    weak = [dict(r) for r in c.execute("""SELECT t.id, t.title_it, t.title_en, t.domain_id, COUNT(*) n, SUM(a.correct) ok
        FROM answers a JOIN questions q ON q.id=a.question_id JOIN topics t ON t.id=q.topic_id
        GROUP BY t.id HAVING n>=3 ORDER BY (1.0*SUM(a.correct)/COUNT(*)) ASC, n DESC LIMIT 8""")]
    qstats = {r["question_id"]: {"n": r["n"], "ok": r["ok"], "last": r["last"]} for r in c.execute(
        """SELECT question_id, COUNT(*) n, SUM(correct) ok,
           (SELECT correct FROM answers a2 WHERE a2.question_id=a.question_id ORDER BY id DESC LIMIT 1) last
           FROM answers a GROUP BY question_id""")}
    review = {r["question_id"]: r["streak"] for r in c.execute("SELECT * FROM review_queue")}
    return {"sessions": sessions, "totals": totals, "recent": recent, "weakTopics": weak, "qstats": qstats, "review": review}


def session_detail(c, sid):
    s = session_summary(c, sid)
    s["items"] = [dict(r) for r in c.execute(
        """SELECT sq.position, sq.question_id, a.selected_json, a.correct, a.time_ms FROM session_questions sq
           LEFT JOIN answers a ON a.session_id=sq.session_id AND a.question_id=sq.question_id
           WHERE sq.session_id=? ORDER BY sq.position""", (sid,))]
    return s


# ---------- HTTP ----------
class H(BaseHTTPRequestHandler):
    server_version = "MCPA/1"

    def log_message(self, fmt, *a):
        pass

    def _host_ok(self):
        h = (self.headers.get("Host") or "").split(":")[0]
        return h in ("127.0.0.1", "localhost")

    def _origin_ok(self):
        # accetta solo pagine servite da localhost/127.0.0.1 (qualsiasi porta: con Docker la porta dell'host può cambiare)
        o = self.headers.get("Origin")
        if o is None:
            return True
        u = urlparse(o)
        return u.scheme == "http" and u.hostname in ("127.0.0.1", "localhost")

    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}") if n else {}

    def do_GET(self):
        if not self._host_ok():
            return self._json({"error": "host non consentito"}, 403)
        u = urlparse(self.path); p = u.path
        try:
            if p == "/api/data":
                with connect() as c: return self._json(get_data(c))
            if p == "/api/stats":
                with connect() as c: return self._json(stats(c))
            if p.startswith("/api/sessions/"):
                with connect() as c: return self._json(session_detail(c, int(p.rsplit("/", 1)[1])))
            name = "index.html" if p in ("/", "") else p.lstrip("/")
            if name in STATIC:
                b = open(os.path.join(HERE, name), "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", (mimetypes.guess_type(name)[0] or "text/plain") + "; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers(); self.wfile.write(b); return
            self._json({"error": "non trovato"}, 404)
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def do_POST(self):
        if not self._host_ok() or not self._origin_ok():
            return self._json({"error": "origine non consentita"}, 403)
        p = urlparse(self.path).path
        try:
            body = self._body()
            with connect() as c:
                if p == "/api/sessions":
                    ids = [q for q in body.get("questions", []) if isinstance(q, str)]
                    if not ids:
                        return self._json({"error": "nessuna domanda"}, 400)
                    cur = c.execute("INSERT INTO sessions (mode,pool,started_at) VALUES (?,?,?)",
                                    (body.get("mode", "study"), body.get("pool", ""), now()))
                    sid = cur.lastrowid
                    c.executemany("INSERT INTO session_questions VALUES (?,?,?)", [(sid, i, q) for i, q in enumerate(ids)])
                    return self._json({"id": sid})
                if p == "/api/answers":
                    ok = record_answer(c, int(body["session_id"]), body["question_id"], body.get("selected", []), body.get("time_ms"))
                    return self._json({"correct": ok})
                if p.startswith("/api/sessions/") and p.endswith("/finish"):
                    sid = int(p.split("/")[3])
                    for a in body.get("answers", []):
                        record_answer(c, sid, a["question_id"], a.get("selected", []), a.get("time_ms"))
                    return self._json(finish_session(c, sid, bool(body.get("time_up"))))
                if p.startswith("/api/sessions/") and p.endswith("/delete"):
                    c.execute("DELETE FROM sessions WHERE id=?", (int(p.split("/")[3]),))
                    return self._json({"ok": True})
            self._json({"error": "non trovato"}, 404)
        except (KeyError, ValueError) as e:
            self._json({"error": str(e)}, 400)
        except Exception as e:
            self._json({"error": str(e)}, 500)


def main():
    if not os.path.exists(BANK):
        sys.exit("bank.json non trovato accanto a server.py: rigeneralo con python site/build/build_data.py")
    first = not os.path.exists(DB)
    applied = migrate()
    changed = import_bank()
    if first:
        print("Primo avvio: database creato in", DB)
    for f in applied:
        print("Migrazione applicata:", f)
    print("Database:", DB, "(domande importate da bank.json)" if changed else "(gia' aggiornato)")
    if "--migrate" in sys.argv:
        return
    try:
        srv = ThreadingHTTPServer((BIND, PORT), H)
    except OSError:
        url = f"http://{HOST}:{PORT}/"
        print("Il simulatore sembra gia' avviato:", url)
        webbrowser.open(url); return
    url = f"http://{HOST}:{PORT}/"
    print("Simulatore MCPA attivo su", url)
    print("Lascia aperta questa finestra mentre studi. Per chiudere: Ctrl+C o chiudi la finestra.")
    if "--no-browser" not in sys.argv and not os.environ.get("MCPA_NO_BROWSER"):
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
