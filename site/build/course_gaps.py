# -*- coding: utf-8 -*-
"""Punti di teoria mancanti trovati nella revisione del corso del 2026-11-22 (confronto topic per topic con i
key_facts del manifest e con i fatti usati dalle domande). Ogni punto è verificato sulla fonte indicata.

Idempotente: aggiunge un punto in fondo al topic solo se il testo inglese non c'è già (gli id delle
flashcard, topic:indice, restano stabili). Uso: python3 site/build/course_gaps.py  (poi build_data.py)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "..", "content")

POINTS = {
    "D2-03": [  # basic/transports/stdio.md, Backward Compatibility
        ("Probe dual-era: DiscoverResult → server modern; errore modern riconosciuto (es. UnsupportedProtocolVersionError) → server modern, si sceglie tra le versioni supportate senza tornare a initialize; qualsiasi altro errore o timeout → server legacy, fallback a initialize.",
         "Dual-era probe: DiscoverResult → modern server; a recognized modern error (e.g. UnsupportedProtocolVersionError) → modern server, pick one of its supported versions without falling back to initialize; any other error or a timeout → legacy server, fall back to initialize."),
        ("Il fallback a initialize MUST NOT dipendere da un codice d'errore specifico: i server legacy rispondono in modo diverso alle richieste sconosciute prima di initialize.",
         "The fallback to initialize MUST NOT be keyed to one specific error code: legacy servers answer unknown pre-initialize requests in implementation-defined ways."),
    ],
    "D2-13": [  # server/tools.md, Tool Names
        ("L'unicità dei nomi (SHOULD) vale solo all'interno di un singolo server: le collisioni tra server sono normali e le risolve chi aggrega.",
         "Name uniqueness (SHOULD) is scoped to a single server: collisions across servers are normal and the aggregator resolves them."),
    ],
    "D3-11": [  # server/tools.md, inputSchema
        ("Tool senza parametri: inputSchema {\"type\": \"object\", \"additionalProperties\": false} è la forma raccomandata (accetta solo oggetti vuoti).",
         "Tool with no parameters: inputSchema {\"type\": \"object\", \"additionalProperties\": false} is the recommended form (it accepts only empty objects)."),
    ],
    "D4-05": [  # basic/authorization/index.md, Scope Challenge Handling
        ("Il server MUST tenere conto delle gerarchie di scope (uno scope più ampio implica quelli più ristretti) quando decide se un token basta.",
         "The server MUST account for scope hierarchies (a broader scope implies narrower ones) when deciding whether a token is sufficient."),
    ],
    "D4-09": [  # basic/authorization/index.md, Refresh Tokens
        ("Refresh token lato client: MUST tenerli riservati in transito e a riposo, SHOULD dichiarare refresh_token nei grant_types, MUST NOT dare per scontato che l'AS li emetta.",
         "Client-side refresh tokens: MUST keep them confidential in transit and at rest, SHOULD declare refresh_token in grant_types, MUST NOT assume the AS will issue them."),
    ],
    "D4-13": [  # basic/transports/streamable-http.md, request metadata
        ("Gli header Mcp-Method e Mcp-Name permettono a gateway e strumenti di osservabilità di misurare, filtrare e autorizzare le richieste senza leggere il corpo JSON.",
         "The Mcp-Method and Mcp-Name headers let gateways and observability tools meter, filter and authorize requests without parsing the JSON body."),
    ],
    "D5-08": [  # extensions/skills/overview.md, extensions/events/overview.md
        ("Skills: chi dichiara l'estensione MUST implementare skills/list e skills/get; i file delle skill si leggono con resources/read.",
         "Skills: a server declaring the extension MUST implement skills/list and skills/get; skill files are read with resources/read."),
        ("Events: il client scopre i tipi di evento con events/list e li legge con events/poll, che usa un cursor.",
         "Events: the client discovers event types with events/list and reads them with events/poll, which uses a cursor."),
    ],
}


def main():
    added = 0
    known = set()
    for D in ["D1", "D2", "D3", "D4", "D5"]:
        p = os.path.join(CONTENT, f"course-{D}.json")
        c = json.load(open(p, encoding="utf-8"))
        for t in c["topics"]:
            known.add(t["id"])
            for it, en in POINTS.get(t["id"], []):
                if en not in t["points"]["en"]:
                    t["points"]["it"].append(it)
                    t["points"]["en"].append(en)
                    added += 1
        json.dump(c, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("points added:", added, "unknown topic ids:", sorted(set(POINTS) - known))


if __name__ == "__main__":
    main()
