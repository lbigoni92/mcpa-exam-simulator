# Post del blog AAIF su MCP: sintesi (letti il 2026-11-22)

La pagina ufficiale dell'esame MCPA indica tra le risorse di preparazione i "community blog posts" su https://aaif.io/projects/model-context-protocol/.
Questi post **non sono normativi**. Molti sono opinioni o pezzi di autori legati a vendor. Qui ci sono solo sintesi parafrasate, non copie. Se contraddicono la spec 2026-07-28, vale la spec.

| # | Post | Autore, data | Tipo | Affidabilità per l'esame |
|---|---|---|---|---|
| 1 | [MCP 2026-07-28: What's Changing and How to Migrate](https://aaif.io/blog/mcp-2026-07-28-whats-changing-and-how-to-migrate) | A. Jaiswal, 2026-07-21 | guida alla migrazione scritta sulla release candidate | media: chiama "proposte" le deprecazioni, che sono definitive; non cita CIMD |
| 2 | [The enterprise MCP scaling paradox](https://aaif.io/blog/the-enterprise-mcp-scaling-paradox-why-every-agent-needs-a-tailored-backend) | M. Salatino, L. Broudoux, 2026-08-06 | opinione, autori legati a vendor | concetti operativi (D5), nessuna regola di protocollo |
| 3 | [Productionizing MCP for Regulated Industries](https://aaif.io/blog/productionizing-mcp-for-regulated-industries-three-hard-constraints-for-enterprise-engineering/) | sintesi AAIF di un talk Wipro, 2026-07-02 | pratica di un vendor | ⚠️ **contraddice la spec**: parla di session handle e handshake di inizializzazione "formalizzati" e di routing di sessione. Validi i pattern su PII e correlation ID |
| 4 | [MCP Graduates to Enterprise Infrastructure](https://aaif.io/blog/mcp-graduates-to-enterprise-infrastructure-stateless-architecture-formal-governance-and-security) | C. McCaffrey (core maintainer), 2026-07-28 | annuncio | alta, coerente con la spec |
| 5 | [Governance as Infrastructure](https://aaif.io/blog/governance-as-infrastructure-what-the-mcp-2026-07-28-migration-actually-demands-of-permissions-a) | A. Nwodo, A. Garg, 2026-07-30 | position paper | coerente; utile per ruoli e responsabilità |
| 6 | [MCP Is Growing Up](https://aaif.io/blog/mcp-is-growing-up) | A. Jones (AAIF), 2026-05-27 | opinione sulla release candidate | coerente |
| 7 | [Non-blocking human-in-the-loop agents with MRTR](https://aaif.io/blog/non-blocking-human-in-the-loop-agents-re-engineering-agentic-runloops-and-state-machines-with-mr) | V. Caldeira, 2026-08-07 | tutorial con demo | coerente; HMAC e TTL di 5 minuti sono scelte della demo, non requisiti |
| 8 | [Enterprise Interest Group Charter](https://modelcontextprotocol.io/community/interest-groups/enterprise) | facilitatori del gruppo, filed 2026-04-13 | documento di governance ufficiale, non vincolante | alta (governance) |

## Punti chiave per il dominio D5 (parafrasati)

**Scalare MCP in azienda** (post 2, 5, 8)
- Il problema è operativo: delimitare, governare, distribuire e osservare un parco crescente di server.
- I server dei vendor tendono a essere "massimalisti", con cataloghi di tool enormi: più token, più latenza, più superficie d'attacco.
- I server interni soffrono di ownership poco chiara e di server "shadow".
- Quattro approcci: **gateway-centrico**; generazione da OpenAPI, AsyncAPI o gRPC; uno strato **Backend-for-Agents** con tool stretti e contestuali; governance a livello di piattaforma.
- Il gateway che filtra su `Mcp-Method`/`Mcp-Name` è un **filtro grossolano**: i controlli fini (per argomenti e risorse) restano **dentro il tool**.
- Telemetria: OpenTelemetry (convenzioni GenAI). Il trace context W3C serve a **correlare**, **non è l'audit trail**: serve un record di audit durevole per ogni richiesta.
- Ciclo di vita: registro dei connettori, `cacheScope` trattato come controllo di tenancy, consolidamento degli ambienti.

**Statelessness e responsabilità** (post 1, 4, 5, 6)
- Identità, autorizzazione e correlazione si spostano dalla sessione a **ogni richiesta**. L'autorizzazione è per tool call, lungo una catena di delega (utente → agente → workload → tool).
- Gli **handle** sono capability: vanno autorizzati a ogni chiamata, con scope, validazione e scadenza.
- I server dietro load balancer standard non hanno bisogno di sticky session.
- Ruoli: client e host lasciano initialize e `Mcp-Session-Id`, gestiscono consenso e UI. Il server author verifica e autorizza gli handle. La piattaforma gestisce gateway e registro. L'IAM gestisce validazione di `iss`, binding delle credenziali all'issuer ed EMA.

**Settori regolati** (post 3, 8)
- PII fuori dai payload del modello: un proxy fuori banda conserva i dati e li sostituisce con un token di riferimento, poi li inietta solo al momento della tool call.
- Un correlation ID immutabile segue la richiesta in ogni passaggio. Server MCP "sottili" che instradano; RBAC, consenso e mutazioni nei servizi interni.
- Casi d'uso sanitari (PHI) ancora solo "pianificati" dall'Enterprise IG.

**Human in the loop senza blocchi** (post 7)
- Con MRTR il server chiude la risposta con `input_required` invece di tenere aperto uno stream; il client riprova con un nuovo id JSON-RPC.
- Il server può chiedere input solo mentre gestisce una richiesta del client. MRTR **non sostituisce** Tasks per i lavori lunghi.
- Il gateway resta stateless e instrada sugli header.

**Enterprise Interest Group** (post 8)
- Raccoglie lacune per le aziende (auth, propagazione dell'identità, audit, gateway, scalabilità, configurazione) e le passa ai working group.
- Vendor-neutral; non scrive né possiede SEP. Le raccomandazioni passano per lazy consensus dopo 7 giorni di revisione.
