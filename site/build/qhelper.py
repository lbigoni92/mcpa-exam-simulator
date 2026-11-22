import json
def Q(qs, dom, n, t, d, q, o, c, x, typ=None):
    qs.append({"id":f"o-{dom}-{n:02d}","t":t,"d":d,"type":typ or ("multi" if len(c)>1 else "single"),
      "q":{"it":q[0],"en":q[1]},"o":[{"it":a,"en":b} for a,b in o],"c":c,"x":{"it":x[0],"en":x[1]}})
def save(qs, path):
    ids=[q["id"] for q in qs]; assert len(ids)==len(set(ids))
    for q in qs:
        assert len(q["o"])>=3 and all(0<=i<len(q["o"]) for i in q["c"]), q["id"]
    json.dump(qs, open(path,"w"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(path, len(qs), Counter(i for q in qs for i in q["c"]))
