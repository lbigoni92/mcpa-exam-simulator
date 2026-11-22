# Inventario delle fonti

Tutte le fonti sono **ufficiali** salvo dove indicato. Raccolte il 2026-11-22.

## Specifica e documentazione (repo GitHub `modelcontextprotocol/modelcontextprotocol`)
- Clone del branch `main`, commit `862397cec702e8f828713071da501cf56158e8fc` (2026-11-21).
- I file `.md` sono copie dei sorgenti `.mdx` del sito modelcontextprotocol.io (contengono componenti JSX come `<Note>`, `<Warning>`: leggibili come markdown).
- Corrispondenza URL: `sources/spec-2026-07-28/X.md` → `https://modelcontextprotocol.io/specification/2026-07-28/X`
  (es. `basic/patterns/mrtr.md` → `/specification/2026-07-28/basic/patterns/mrtr`; `index.md` di una cartella → URL della cartella).
- `sources/docs/X.md` → `https://modelcontextprotocol.io/docs/X` (versione docs 2026-07-28).
- `sources/extensions/X.md` → `https://modelcontextprotocol.io/extensions/X`
- `sources/registry/X.md` → `https://modelcontextprotocol.io/registry/X`
- `sources/community/X.md` → `https://modelcontextprotocol.io/community/X` (`roadmap.md` → `/development/roadmap`)
- `sources/seps/` → `https://modelcontextprotocol.io/seps/` (tutte le SEP in formato file)
- `sources/blog/` → `https://blog.modelcontextprotocol.io/posts/…`

| Cartella | Contenuto |
|---|---|
| `spec-2026-07-28/` | **spec di riferimento** completa (prosa) + `schema.ts` (fonte di verità) + `schema.json` |
| `spec-2025-11-25/` | spec precedente completa, per i diff (lifecycle/initialize, sessioni, tasks core…) |
| `spec-older-changelogs/` | changelog 2025-06-18 e 2025-03-26 |
| `docs/` | learn (architecture, concepts, versioning), develop (build server/client, client best practices, connect local/remote), tools (inspector, debugging), tutorials security (authorization, security best practices, local server security), sdk |
| `extensions/` | overview, tasks, apps, auth (client credentials, EMA), events, skills, client matrix |
| `registry/` | about, package types, remote servers, authentication, versioning, aggregators, FAQ, ToS, moderation |
| `community/` | governance, feature lifecycle, SDK tiers, design principles, SEP guidelines, working/interest groups, roadmap |
| `seps/` | tutte le SEP (es. 2322 MRTR, 2575 stateless, 2567 sessionless, 2549 TTL, 2243 headers, 2468 iss, 2577 deprecations, 2596 lifecycle, 2663 tasks) |
| `blog/` | post ufficiali dal 2025-11 (AAIF, release 2026-07-28, SDK, roadmap, extensions, tool annotations) |
| `exam/` | info pubbliche sull'esame (pagina LF, press release, blog LF/AAIF) |

## Pagina esame
Vedi `exam/lf-exam-page.md`. Il training portal LF (`trainingportal.linuxfoundation.org`) richiede login e **non** è stato consultato.
Seconda passata (2026-11-22), lette anche:
- FAQ esami MC: https://docs.linuxfoundation.org/tc-docs/certification/faq-mc
- Important Instructions MC: https://docs.linuxfoundation.org/tc-docs/certification/important-instructions-mc
- Certification Agreement: https://docs.linuxfoundation.org/tc-docs/certification/lf-cert-agreement/
- Candidate Handbook: https://docs.linuxfoundation.org/tc-docs/certification/lf-handbook2 (solo introduzione)
- Pagina progetto AAIF: https://aaif.io/projects/model-context-protocol/ (nessun dettaglio sull'esame)
- Ricontrollata la pagina MCPA (modificata 2026-09-16): 90 min confermati.
- Repo spec ricontrollato: nessun cambiamento dopo `862397c`.

## Fonti non ufficiali
Usate solo come mappa dei temi (nessun contenuto copiato): devopscube.com MCPA guide. Ogni affermazione nelle dispense è verificata sulla spec.

## Blog AAIF (risorsa indicata dalla pagina d'esame)
`blog/aaif/README.md`: sintesi parafrasate di 7 post AAIF su MCP e del charter dell'Enterprise Interest Group, letti il 2026-11-22. Non normativi: usati per il dominio D5 solo dove coerenti con la spec.

## Domande di pratica (non ufficiali)
In `../practice-questions/`, con licenze e attribuzioni. Copiati integralmente solo contenuti con licenza aperta:
- rohitg00/ai-engineering-from-scratch (MIT, commit `9712e32`);
- huggingface/mcp-course (Apache-2.0, commit `dbfa79b`).

Le altre fonti sono solo catalogate (argomenti parafrasati ed errori rispetto alla spec).

## Non raccolto (perché)
- Domande d'esame reali/dump: vietati dal LF Certification & Confidentiality Agreement.
- Codice degli SDK: non necessario per un esame concettuale; i link sono in `docs/sdk.md`.
