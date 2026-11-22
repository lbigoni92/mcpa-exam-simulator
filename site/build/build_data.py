"""Unisce corso, domande originali e domande open-licensed in site/bank.json (letto dal server, che lo importa in SQLite).
Uso: python3 site/build/build_data.py   (dalla radice del progetto)"""
import json, re, os
from collections import Counter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
C = os.path.join(ROOT, "site", "content")
DOMS = [("D1","MCP Fundamentals","Fondamenti di MCP",16,12),("D2","Architecture & Components","Architettura e componenti",14,15),
        ("D3","Interactions & Execution","Interazioni ed esecuzione",26,29),("D4","Security & Governance","Sicurezza e governance",24,27),
        ("D5","Use Cases & Ecosystem","Casi d'uso ed ecosistema",20,17)]
course=[]; topics={}
for did,en,it,w,sw in DOMS:
    c=json.load(open(f"{C}/course-{did}.json"))
    for t in c["topics"]: topics[t["id"]]=t
    course.append({"id":did,"title":{"en":en,"it":it},"weight":w,"studyWeight":sw,"topics":c["topics"]})
qs=[]
import glob
for f in sorted(glob.glob(f"{C}/questions-D*.json"))+sorted(glob.glob(f"{C}/questions-hard*.json")):
    for q in json.load(open(f)):
        did=q["id"].split("-")[-2] if q["id"].startswith("o-H-") else q["id"].split("-")[1]
        q=dict(q); q["dom"]=q["t"][:2]; q["src"]="original"; q["set"]="hard" if q["id"].startswith("o-H-") else ("utente" if q["id"].startswith("o-U-") else "original"); qs.append(q)

STOP=set("the a an of to and or in on for is are be with by as at it its this that which what when how does do from not no can must should may their they your you will any all one only than then into more over per new".split())
def toks(s): return [w for w in re.findall(r"[a-z0-9/_\-]+", s.lower()) if w not in STOP and len(w)>2]
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lesson_points import POINTS as _LP
from course_gaps import POINTS as _CG
LESSON_EN={en for v in list(_LP.values())+list(_CG.values()) for _,en in v}
tvec={}
for tid,t in topics.items():
    # i punti aggiunti dalle lezioni rohitg00 (lesson_points.py) non entrano nel matching, per non spostare i link già revisionati
    pts=[p for p in t["points"]["en"] if p not in LESSON_EN]
    parts=[t["title"]["en"]]*3+[t["summary"]["en"]]+pts+([t["trap"]["en"]] if t.get("trap") else [])
    parts+=[q["q"]["en"]+" "+q["x"]["en"] for q in qs if q["t"]==tid]
    tvec[tid]=Counter(toks(" ".join(parts)))
df=Counter(w for v in tvec.values() for w in v)
import math
def best_topic(text, dom):
    v=Counter(toks(text)); best=None; bs=-1
    for tid,tv in tvec.items():
        s=sum(min(v[w],3)*math.log(1+len(tvec)/df[w]) for w in v if w in tv)
        if dom and tid.startswith(dom): s*=1.15
        if s>bs: bs, best = s, tid
    return best
# Collegamenti alla teoria corretti a mano dopo la revisione (id -> topic)
OVERRIDE = json.load(open(os.path.join(os.path.dirname(__file__),"topic_overrides.json"))) if os.path.exists(os.path.join(os.path.dirname(__file__),"topic_overrides.json")) else {}
# Errata: correzioni a domande MIT (licenza consente modifiche), mostrate come nota nel sito.
ERRATA = {
 "ext-rg-mcpa-f-m2-003": ({"stem": "The deprecated features registry lists Dynamic Client Registration as deprecated in the 2026-07-28 revision, with no removal date yet announced. What can a reader conclude about its earliest possible removal?"},
   "Testo corretto: l'originale attribuiva la deprecazione di DCR a SEP-2577, che invece depreca roots, sampling e logging. DCR è deprecata nella stessa revisione 2026-07-28 da un'altra modifica (PR #2858). / Fixed: the original attributed the DCR deprecation to SEP-2577, which deprecates roots, sampling and logging."),
 "ext-rg-quiz-06-06": ({"options": {"C": "It disambiguates the collision, for example by prefixing the second search with a server identifier"},
                        "explanation": "Tool name uniqueness is scoped to a single server, so collisions across servers are normal. The specification says aggregating clients SHOULD implement a disambiguation strategy such as prefixing tool names with a server identifier, and SHOULD NOT rely on serverInfo.name, which is not guaranteed unique. Merging, overwriting or dropping a tool would hide a real tool from the model."},
   "Opzione C e spiegazione allineate alla spec: la spec chiede una strategia di disambiguazione (per esempio un prefisso con l'identificatore del server), non impone di tenere il primo nome come canonico. / Aligned with the spec: it asks for a disambiguation strategy such as a server-id prefix, it does not mandate keeping the first name canonical."),
 "ext-rg-quiz-18-01": ({"explanation": "An unknown tool is a protocol error reported as -32602 Invalid params; -32601 means the method itself was not found. -32002 (resource not found) is retired in 2026-07-28 itself, replaced by -32602 (SEP-2164)."},
   "Spiegazione corretta: -32002 è ritirato proprio nella 2026-07-28 (SEP-2164), non prima. / Fixed: -32002 is retired in 2026-07-28 itself, not before."),
 "ext-rg-quiz-18-03": ({"options": {"D": "-32002 and -32042, both codes from earlier revisions"},
                        "explanation": "2026-07-28 retires -32002 (resource not found up to 2025-11-25, now -32602) and -32042 (URL elicitation required, 2025-11-25 only). -32020 to -32022 are current and the standard JSON-RPC codes remain in use."},
   "Opzione D e spiegazione corrette: -32002 viene ritirato nella 2026-07-28, non prima. / Fixed: -32002 is retired in 2026-07-28, not before."),
 "ext-rg-quiz-30-06": ({"stem": "An official extension's maintainers need to remove a field, and the old and new behavior must keep working side by side under the same protocol revision. What should they do?",
                        "explanation": "Per the extensions overview, a breaking change normally keeps the extension's identifier (Experimental and Beta extensions add or increment a revision string in their settings). A new identifier, for example with a -v2 suffix, is used only when old and new behavior must coexist under one protocol revision, as in this scenario."},
   "Domanda riformulata: l'originale diceva che ogni modifica incompatibile richiede un nuovo identificatore, ma la pagina ufficiale sulle estensioni dice che l'identificatore resta lo stesso e ne serve uno nuovo solo se vecchio e nuovo comportamento devono coesistere. / Reworded: the original said every breaking change needs a new identifier; the official extensions page says the identifier is kept unless old and new behavior must coexist."),
 "ext-rg-mcpa-f-m3-007": ({"options": {"B": "HTTP+SSE has been deprecated since 2025-03-26, and SEP-2596 gives it its own floor: three months after SEP-2596 reaches Final"},
                           "explanation": "Each deprecated feature carries its own origin and removal floor rather than one shared date. Roots, sampling, logging and Dynamic Client Registration were deprecated in 2026-07-28 with an earliest removal on or after 2027-07-28. HTTP+SSE has been described as deprecated since 2025-03-26, before the lifecycle policy existed; SEP-2596 reclassified it as Deprecated under the transition provisions, with earliest removal three months after SEP-2596 reaches Final."},
   "Opzione B e spiegazione corrette sulla tabella delle feature deprecate: HTTP+SSE è deprecato dalla 2025-03-26 e SEP-2596 lo riclassifica, con rimozione più precoce tre mesi dopo che SEP-2596 diventa Final. / Fixed per the deprecated-features table: HTTP+SSE deprecated since 2025-03-26, reclassified by SEP-2596, earliest removal three months after SEP-2596 reaches Final."),
 "ext-rg-quiz-00-03": ({}, "Domanda sul curriculum, non sull'esame. La discrepanza è risolta: le pagine LF attuali indicano 90 minuti. / About the curriculum, not the exam: current LF pages state 90 minutes."),
}
# Track rohitg00 (tracks/mcpa-f.json): mappa lezione -> domini e obiettivi per dominio (non ufficiali)
TRACK_P=os.path.join(ROOT,"practice-questions/open-licensed/rohitg00-mcpa/tracks/mcpa-f.json")
TRACK=json.load(open(TRACK_P)) if os.path.exists(TRACK_P) else None
TDOM={"mcp-fundamentals":"D1","architecture-and-components":"D2","interactions-and-execution":"D3","security-and-governance":"D4","use-cases-and-ecosystem":"D5"}
LESSON_DOMS={l["path"].rsplit("/",1)[1]:[TDOM[x] for x in l["domains"]] for l in TRACK["lessons"]} if TRACK else {}
if TRACK:
    for d in TRACK["domains"]:
        for c in course:
            if c["id"]==TDOM[d["id"]]: c["objectives"]={"en":d["objectives"],"source":"rohitg00/ai-engineering-from-scratch, tracks/mcpa-f.json (MIT)"}
def best_topic_in(text, doms):
    v=Counter(toks(text)); best=None; bs=-1
    for tid,tv in tvec.items():
        if tid[:2] not in doms: continue
        s=sum(min(v[w],3)*math.log(1+len(tvec)/df[w]) for w in v if w in tv)
        if s>bs: bs,best=s,tid
    return best
def ext(path):
    d=json.load(open(os.path.join(ROOT,path)))
    for e in d["questions"]:
        text=" ".join([e["stem"]]*2+([e.get("set_title","")]*2 if "lesson-quiz" in e["set"] else [])+[o["text"] for i,o in enumerate(e["options"]) if o["key"] in e["correct"]]+[e.get("explanation") or ""])
        fix, fixnote = ERRATA.get(e["id"], ({}, None))
        if "stem" in fix: e=dict(e, stem=fix["stem"])
        if "explanation" in fix: e=dict(e, explanation=fix["explanation"])
        if "options" in fix: e=dict(e, options=[dict(o, text=fix["options"].get(o["key"], o["text"])) for o in e["options"]])
        dom=e.get("domain")
        lesson=e["set"][12:] if e["set"].startswith("lesson-quiz/") else None
        if lesson and len(LESSON_DOMS.get(lesson,[]))>1:
            # lezione su più domini (track): dominio della domanda = dominio dell'argomento più vicino tra quelli ammessi
            t=OVERRIDE.get(e["id"]) or best_topic_in(text, LESSON_DOMS[lesson])
            dom=t[:2] if t[:2] in LESSON_DOMS[lesson] else LESSON_DOMS[lesson][0]
        else:
            t=OVERRIDE.get(e["id"]) or best_topic(text, dom); dom=dom or t[:2]
        keys=[o["key"] for o in e["options"]]
        x=e.get("explanation") or " ".join(o.get("explain","") for o in e["options"] if o["key"] in e["correct"])
        q={"id":e["id"],"t":t,"dom":dom,"type":"multi" if len(e["correct"])>1 else "single",
           "q":{"en":e["stem"]},"o":[{"en":o["text"]} for o in e["options"]],
           "c":[keys.index(k) for k in e["correct"]],"x":{"en":x},
           "src":e["source"],"set":e["set"],"setTitle":e.get("set_title","")}
        r=e.get("review")
        if fixnote: q["review"]={"status":"corretta","note":fixnote}
        elif r and r.get("status") in ("imprecisa","datata"): q["review"]=r
        qs.append(q)
ext("practice-questions/open-licensed/rohitg00-mcpa/normalizzate.json")
ext("practice-questions/open-licensed/huggingface-mcp-course/normalizzate.json")
assert len({q["id"] for q in qs})==len(qs)
# livello di fonte e citazione (site/build/cite.py -> citations.json): "blog" = nessuna frase di spec o docs
# ufficiali la sostiene, quindi la domanda resta nella pratica ma esce dalle simulazioni d'esame
_cp=os.path.join(ROOT,"site","build","citations.json")
_cites=json.load(open(_cp,encoding="utf-8")) if os.path.exists(_cp) else {}
for q in qs:
    r=_cites.get(q["id"])
    if r:
        q["lvl"]=r["lvl"]
        if r.get("text"): q["cite"]={"text":r["text"],"url":r.get("url","")}
data={"generated":__import__("datetime").date.today().isoformat(),"spec":"2026-07-28","course":course,"questions":qs}
json.dump(data, open(os.path.join(ROOT,"site","bank.json"),"w"), ensure_ascii=False, separators=(",",":"))
print("questions", Counter(q["src"] for q in qs), "topics", len(topics))
print("by dom", Counter(q["dom"] for q in qs))
print("topics w/o any q", sorted(set(topics)-{q["t"] for q in qs}))
