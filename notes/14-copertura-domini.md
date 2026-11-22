# Verifica di copertura dei domini (2026-11-22)

## Peso di ogni dominio (riepilogo)
| Dominio | Peso d'esame ufficiale | Domande su 60 | Copertura della base (/10) | Moltiplicatore di difficoltà | **Peso di studio consigliato** | Perché |
|---|---|---|---|---|---|---|
| D1 MCP Fundamentals | 16% | ~10 | 9 | 0,8 | **12%** | concettuale, cambiato poco rispetto alle versioni precedenti |
| D2 Architecture & Components | 14% | ~8 | 9 | 1,1 | **15%** | molte novità della 2026-07-28 (header HTTP, `server/discover`, `x-mcp-header`) |
| D3 Interactions & Execution | 26% | ~16 | 9,5 | 1,2 | **29%** | il più pesante e il più nuovo (MRTR, subscriptions, errori, caching) |
| D4 Security & Governance | 24% | ~14 | 9 | 1,2 | **27%** | denso: OAuth 2.1, RFC, MUST vs SHOULD, attacchi |
| D5 Use Cases & Ecosystem | 20% | ~12 | 8 | 0,9 | **17%** | meno regole da memorizzare, più ragionamento su scenari |

- **Peso di studio** = peso ufficiale × moltiplicatore di difficoltà, rinormalizzato a 100. Il moltiplicatore tiene conto di quanti topic sono nuovi nella 2026-07-28 e di quanti sono a priorità alta nel manifest. È una **stima nostra**, non un dato ufficiale.
- Per la **generazione delle domande** e il **simulatore** si usa invece il **peso d'esame ufficiale** (16/14/26/24/20).
- I 60 quesiti sono un'ipotesi basata sulle regole LF generiche per gli esami a scelta multipla.
- **Copertura** (/10): fatti verificati per domanda prevista, quota di fonti normative e disponibilità di domande di pratica. D5 è a 8 perché una parte del materiale nuovo viene da post non normativi (blog AAIF).


Obiettivo: capire se la base di conoscenza basta per generare **qualche centinaio di domande originali** (ipotesi: 400, ripartite sui pesi ufficiali). Regola pratica: almeno ~0,7 fatti verificati per domanda e nessuna competenza LF scoperta. Più fatti per domanda = meno domande ripetitive.

## Prima e dopo l'integrazione

| Dominio | Peso | Domande su 400 | Fatti prima | Fatti/domanda prima | Fatti ora | Fatti/domanda ora | Verdetto |
|---|---|---|---|---|---|---|---|
| D1 MCP Fundamentals | 16% | 64 | 33 | 0,52 ⚠️ | **56** | 0,88 | **completo** (integrato) |
| D2 Architecture & Components | 14% | 56 | 46 | 0,82 | **63** | 1,13 | **completo** |
| D3 Interactions & Execution | 26% | 104 | 84 | 0,81 | **91** | 0,88 | **completo** |
| D4 Security & Governance | 24% | 96 | 63 | 0,66 ⚠️ | **84** | 0,88 | **completo** (integrato) |
| D5 Use Cases & Ecosystem | 20% | 80 | 34 | 0,43 ❌ | **70** | 0,88 | **completo** (integrato due volte, la seconda con blog AAIF ed Enterprise IG) |
| **Totale** | | 400 | 260 | | **364** (74 topic) | | |

Le dispense coprivano già più del manifest. Le lacune vere erano di due tipi:
1. **fatti presenti nelle dispense ma non nel manifest**, quindi invisibili alla generazione delle domande;
2. **argomenti assenti anche dalle dispense**: tool poisoning, rug pull, lethal trifecta, threat model dei server locali, principi di design del progetto, server instructions, regole sui nomi dei tool, dettagli del registry, Events, Skills, MCPB.

## Per competenza ufficiale LF (dopo l'integrazione)

| Dominio | Competenza | Topic | Fatti | Note |
|---|---|---|---|---|
| D1 | MCP Purpose & Scope | 2 | 15 | + struttura e perimetro della spec (D1-10) |
| D1 | Core MCP Concepts | 6 | 30 | + principi di design del progetto (D1-09), primitive e controllo |
| D1 | Interoperability & Value | 2 | 11 | + N×M, valore per attore |
| D2 | MCP Hosts, Clients and Servers | 6 | 31 | + nomi dei tool e aggregazione multi-server (D2-13) |
| D2 | Schemas & Structured Data | 3 | 13 | sufficiente (JSON Schema 2020-12, `$ref`, structured output, `_meta`) |
| D2 | Model Interaction Flow | 4 | 19 | era la più debole di D2 (6 fatti): + server instructions (D2-11), interazione per primitiva (D2-12), flusso multi-server |
| D3 | Interaction Patterns & Response Handling | 7 | 38 | ok |
| D3 | Error Handling | 3 | 16 | era 9: + status HTTP completi, categorie di errore |
| D3 | Tool Invocation Lifecycle | 4 | 17 | ok |
| D3 | Protocol Primitives | 5 | 20 | ok; prompts e completion restano a 3 fatti l'uno (sono piccoli anche nella spec) |
| D4 | Trust Boundaries | 4 | 18 | + threat model dei server locali e provenienza (D4-18) |
| D4 | Permissions & Consent | 4 | 20 | ok (OAuth, scope, CIMD, consenso per feature) |
| D4 | Risk & Safety Controls | 7 | 32 | + tool poisoning, rug pull, lethal trifecta (D4-16), limiti delle annotations (D4-17) |
| D4 | Auditability & Observability | 3 | 14 | + log d'uso dei tool, attribuzione agente/utente, trace context |
| D5 | Roles, Responsibilities & Adoption | 2 | 11 | + matrice delle responsabilità (server author, host, utente, operatore, publisher) |
| D5 | Operational Use Cases | 6 | 29 | + quale estensione per quale caso (D5-10), Events (D5-11), pattern enterprise da blog AAIF ed Enterprise IG (D5-14) |
| D5 | Ecosystem & Portability | 6 | 30 | + registry operativo, MCPB (D5-12), Skills (D5-13) |

## Limiti residui (noti, accettati)
- **D5** resta il dominio con meno materiale normativo: molte domande saranno di **scenario** ("quale meccanismo/estensione usare"), costruite sui fatti di D3 e D4. Numeri di adozione e liste di client cambiano spesso: evitarli nelle domande.
- **D1** è concettuale per natura: per non ripetersi conviene usare anche versioning, cronologia delle revisioni e confronto legacy/modern (già nel manifest).
- **Prompts e completion** (D3) hanno poco materiale anche nella spec: poche domande e semplici.
- Le estensioni **Beta** (Events, Skills, Server Cards) possono cambiare: domande solo su concetti stabili (scopo, quando usarle), non su nomi di campi.

## Riscontro con le domande di pratica
Le 414 domande rohitg00 (`practice-questions/`) coprono D1 77 · D2 58 · D3 122 · D4 85 · D5 72. I loro obiettivi corrispondono alle competenze sopra; non ho trovato argomenti trattati lì e assenti dalla nostra base, dopo l'integrazione.

## File toccati
- `notes/01` §2.6
- `notes/02` §3.1-3.3
- `notes/04` §6.5b e §6.8
- `notes/05` §2.3b, registry operativo, §3.6
- `knowledge/manifest.json` (rigenerato: `knowledge/build/mk_manifest.py` + `manifest_supplement.py`)
