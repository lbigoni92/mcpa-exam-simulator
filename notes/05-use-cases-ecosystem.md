# Dominio 5 — Use Cases & Ecosystem (20%)

> Competenze ufficiali LF: **Roles, Responsibilities & Adoption · Operational Use Cases · Ecosystem & Portability**
> Fonti: `sources/docs/getting-started/intro.md`, `docs/learn/*`, `docs/develop/*` (client best practices, connect local/remote), `sources/extensions/*`, `sources/registry/*`, `sources/community/*` (governance, sdk-tiers, feature-lifecycle, roadmap), `sources/blog/*`.

---

## 1. Roles, Responsibilities & Adoption

### 1.1 Ruoli tecnici nel protocollo
| Ruolo | Responsabile di |
|---|---|
| **Host** (app AI) | orchestrazione, consenso utente, policy di sicurezza, integrazione LLM, aggregazione del contesto, UI per approvazioni, disambiguazione tool tra server, caching, progressive discovery |
| **Client** | una connessione per server, `_meta` su ogni richiesta, gestione MRTR/subscriptions, validazione risultati, PKCE/`resource`/`iss` nel flusso OAuth |
| **Server author** | tool/resources/prompts ben progettati (nomi, description, schema, annotations), validazione input, access control, rate limit, sanitizzazione output, `ttlMs`/`cacheScope` corretti, handle di stato sicuri, nessun token passthrough |
| **Authorization server** | OAuth 2.1, metadata (RFC 8414/OIDC), PKCE S256, `iss`, CIMD, validazione redirect URI esatti, token short-lived |
| **Utente finale** | consenso, approvazione delle azioni, scelta dei prompt (user-controlled) |
| **Operatore / security team** | sandbox dei server locali, egress control, gateway (routing/rate limit su `Mcp-Method`/`Mcp-Name`), IdP aziendale (EMA), audit |

### 1.2 Ruoli nel progetto open source (`community/governance.md`)
- MCP è "Model Context Protocol a Series of LF Projects, LLC". **Donato da Anthropic all'Agentic AI Foundation (AAIF)**, directed fund della Linux Foundation (9 dicembre 2025). AAIF co-fondata da **Anthropic, Block e OpenAI** (con supporto di Google, Microsoft, AWS, Cloudflare, Bloomberg); progetti fondatori: **MCP, goose (Block), AGENTS.md (OpenAI)**. Il board AAIF decide strategia/budget, **MCP mantiene piena autonomia tecnica**.
- Gerarchia: **Lead Maintainers (BDFL)** – decisione finale, veto; **Core Maintainers** – direzione della spec, veto a maggioranza sulle decisioni dei Maintainer; **Maintainers** – SDK, docs, Working Groups; **Contributors**. Maintainer + Core + Lead = **Steering Group**. Membership **individuale**, non per azienda.
- **Interest Groups** identificano problemi; **Working Groups** producono soluzioni (SEP, implementazioni). Esempi di WG: Transports, SDK, Registry, Apps, Tasks & Events, Skills over MCP, Server Card, Interceptors, Inspector v2, File uploads, Filesystems, Progressive disclosure, Governance, Infrastructure.
- **SEP** = Specification Enhancement Proposal: meccanismo per proporre modifiche alla spec; workflow PR-based in `seps/` (SEP-1850); le SEP "Final" richiedono conformance test (SEP-2484).
- Licenze: codice e spec **Apache 2.0**; documentazione **CC-BY 4.0**.

### 1.3 Adoption
- Numeri ufficiali (blog AAIF, dic 2025): >97 milioni di download SDK al mese, ~10.000 server attivi, supporto in ChatGPT, Claude, Cursor, Gemini, Microsoft Copilot, VS Code…
- Blog spec 2026-07-28: quasi mezzo miliardo di download/mese tra gli SDK Tier 1; SDK TypeScript e Python oltre 1 miliardo di download totali.
- **Feature lifecycle** (SEP-2596) per pianificare gli upgrade: deprecazione con finestra minima **12 mesi**; gli SDK Tier 1 devono segnalare le deprecazioni.
- **Release cycle** e roadmap (`community/roadmap.md`): priorità — agentic messaging primitives, unificazione/hardening del transport HTTP-native, agent identity ed enterprise-ready security, primitive migliorate, DX degli SDK.

---

## 2. Operational Use Cases

### 2.1 Esempi ufficiali
- Agenti con accesso a Google Calendar e Notion (assistente personale).
- Claude Code che genera un'app web da un design Figma.
- Chatbot aziendali connessi a più database.
- Modelli che creano design 3D in Blender e li stampano.
- Server di riferimento: **filesystem**, git, ecc. (repo `modelcontextprotocol/servers`); server remoti di terze parti (es. Sentry).
- Esempio "travel planning" multi-server nelle docs (tools per prenotare, resources per contesto, prompts per workflow).

### 2.2 Locale vs remoto
| | Server locale | Server remoto |
|---|---|---|
| Transport | **stdio** (il client lancia il processo) | **Streamable HTTP** |
| Client serviti | tipicamente uno | molti |
| Autenticazione | credenziali dall'**ambiente** | **OAuth 2.1** (spec authorization) o estensioni |
| Rischi tipici | esecuzione di codice con i privilegi dell'utente, comandi di avvio malevoli, DNS rebinding se esposto su HTTP | SSRF, token passthrough, confused deputy, mix-up |
| Mitigazioni | consenso one-click con comando completo, **sandbox/container**, filesystem e rete limitati, provenienza | HTTPS, PKCE, `resource`, `iss`, audience validation, scope minimi |
| Esempio | filesystem server lanciato da Claude Desktop | Sentry MCP, "Custom Connectors" in Claude |

Guida `local-server-security.md`: chiedersi se deve davvero girare in locale; verificare la provenienza; trattare le definizioni dei tool come input non fidato; ambiente isolato; isolare credenziali; limitare filesystem ed egress; gestione a livello di organizzazione.

### 2.3 Pattern operativi dalla 2026-07-28
- **Scalabilità orizzontale**: richieste auto-descrittive ⇒ qualsiasi istanza dietro un **round-robin load balancer** può servire qualsiasi richiesta; MRTR evita storage condiviso.
- **Gateway/WAF/rate limiter** instradano e autorizzano su header `Mcp-Method`, `Mcp-Name`, `Mcp-Param-*` senza parsare il body.
- **Caching** di cataloghi tool (`ttlMs`, `cacheScope`, ordine deterministico) → meno polling e **prompt cache** dell'LLM più stabili.
- **Stato applicativo** con handle espliciti (carrello, transazione, browser context).
- **Operazioni lunghe** (CI, batch, approvazioni umane) → estensione **Tasks**.
- **Machine-to-machine** (daemon, CI/CD) → estensione **OAuth Client Credentials**.
- **Enterprise SSO/policy centralizzate** → **Enterprise-Managed Authorization**.
- **Eventi upstream** (nuova email, push, incident) → estensione **Events** (poll/push/webhook, cursori, resumption).
- **UI interattive** inline → **MCP Apps**.
- **Workflow riutilizzabili** → **Skills over MCP**.
- **Osservabilità**: OpenTelemetry (`traceparent`…), log su stderr.

### 2.3b Quando usare quale estensione (dalle pagine ufficiali "When to use")
| Esigenza | Estensione | Note |
|---|---|---|
| esplorare dati complessi (mappe, drill-down), configurazioni con molte opzioni, media ricchi (PDF, 3D), monitoraggio in tempo reale, workflow a più passi (approvazioni, review) | **MCP Apps** | iframe **sandbox**: niente accesso a DOM, cookie o storage del host; comunicazione solo via **postMessage**; il host decide quali capability (es. quali tool, `sendOpenLink`) |
| servizi in background, pipeline **CI/CD**, integrazioni server-to-server, daemon senza utente | **OAuth Client Credentials** | asserzioni **JWT bearer** raccomandate rispetto ai client secret; se c'è un utente che deve autorizzare, usare il flusso standard |
| ambiente aziendale con IT che gestisce gli accessi, policy organizzative, revoca centralizzata, compliance e audit, **SSO** aziendale senza flussi per servizio | **Enterprise-Managed Authorization** | IdP aziendale + ID-JAG |
| reagire ad attività upstream (messaggi, push, pagamenti, incident), agenti **non presidiati**, stream filtrati ("P1 per il servizio X") | **Events** | per il risultato di un'operazione lunga avviata dal client usare **Tasks**, non Events |
| workflow riutilizzabili che combinano tool o richiedono documenti di supporto (code review, elaborazione documenti) | **Skills** | |

**Events, dettagli**:
- Perché non bastano le notifiche: nessun parametro o payload, serve una connessione viva (`subscriptions/listen`), nessuna ripresa.
- **3 modalità di consegna**, nessuna obbligatoria: **poll** (`events/poll`, server senza stato per client, adatto a serverless), **push** (`events/stream`, richiesta lunga, adatto a stdio), **webhook** (`events/subscribe`, callback `https` firmata con TTL rinnovabile, adatto a server remoti e client senza connessione persistente). Gli SDK preferiscono webhook > push > poll.
- **Cursori** opachi → consegna **at-least-once** se l'upstream è durevole. Replay opzionale per tipo (`cursor: null` = niente storico). `maxAgeMs` limita il replay. `eventId` stabile per la deduplicazione. Ordine garantito per poll e push; best-effort per webhook (si usa `timestamp`). Le subscription sono **del client** (nessun metodo server per elencarle).

**Skills, dettagli**:
- Una skill è una directory con `SKILL.md` e file di supporto (Agent Skills specification).
- Il server **MUST** dichiarare la capability `resources` e l'estensione `io.modelcontextprotocol/skills` in `server/discover`.
- URI con schema `skill://` (SHOULD). `skills/list` restituisce per ogni file URI, **digest SHA-256** e dimensione, per verificarne l'integrità (`ttlMs`/`cacheScope` non garantiscono l'integrità).
- Leggere `SKILL.md` con `resources/read` **non attiva** la skill: il host la carica dopo verifica ed eventuale approvazione dell'utente. La skill può essere scelta dal modello o dall'utente.

### 2.3c Pattern enterprise e responsabilità (blog AAIF, risorsa indicata dalla pagina d'esame)
> Fonte: `sources/blog/aaif/README.md`. Sono **post non normativi**: qui ci sono solo i punti coerenti con la spec 2026-07-28. Il post sui settori regolati contiene errori (sessioni e handshake), segnalati in `13-trappole`.
- **Problema di scala**: in azienda la difficoltà è operativa (ownership, governance, deploy, osservabilità del parco server), non di protocollo. I server "massimalisti" con cataloghi enormi aumentano token, latenza e superficie d'attacco. Rimedi: tool stretti e contestuali (strato **Backend-for-Agents**, generazione da OpenAPI), **gateway**, governance di piattaforma, progressive discovery lato client (§2.4).
- **Difesa a strati**: il gateway filtra su `Mcp-Method`/`Mcp-Name`/`Mcp-Param-*` (controllo grossolano, rate limit, routing). L'autorizzazione fine (su argomenti, risorse, handle) resta nel **tool/server**, a ogni chiamata.
- **Correlazione ≠ audit**: `traceparent` correla i passaggi. Per l'audit serve un **record durevole per richiesta** con chi (utente), quale agente, quale tool, con quale autorizzazione.
- **Settori regolati**: dati sensibili (PII, PHI) fuori dal contesto del modello quando possibile (tokenizzazione/proxy), correlation ID end-to-end, server sottili e policy nei servizi interni, `cacheScope: private` per dati per utente o tenant.
- **Matrice delle responsabilità** (sintesi):
| Attore | Responsabilità tipiche |
|---|---|
| Host / client | consenso e UI, approvazioni (human in the loop via MRTR o elicitation), invio di `_meta` per richiesta, eco esatto di `requestState`, limite ai round trip, cache coerente con `cacheScope` |
| Server author | PRM e validazione dei token (audience), autorizzazione per tool e per handle, verifica di `requestState`, annotations oneste, `ttlMs`/`cacheScope` corretti |
| Operatore / piattaforma | gateway e policy, registro interno o subregistry, sandbox dei server locali, egress, osservabilità e audit |
| IAM / IdP | authorization server, validazione di `iss` (lato client), binding delle credenziali all'issuer, **EMA** per l'accesso aziendale |
| Utente finale | approva tool, consensi ed elicitation; sceglie i prompts |
| Publisher sul registry | `server.json`, namespace verificato, versioni immutabili |
- **Interest Group Enterprise** (ufficiale): raccoglie i requisiti aziendali (auth, identità, audit, gateway) e li passa ai Working Group. Non scrive SEP.

### 2.4 Best practice lato client per grandi cataloghi (`develop/clients/client-best-practices.md`)
- **Progressive Tool Discovery**: invece di iniettare centinaia di definizioni (~150k token) il host espone un meta-tool `search_tools` e carica le definizioni complete solo quando servono (~2k token). Soglia consigliata: quando le definizioni superano l'**1–5% della context window**. Strategie: keyword (BM25/regex), embedding, subagent (modello piccolo/veloce), ibrida. Pattern a tre livelli: **Catalog → Inspect (`get_tool_details`) → Execute**. Estendibile a interi server (connettere/disconnettere su richiesta).
- **Programmatic Tool Calling / "Code Mode"**: il modello scrive codice che chiama i tool in una **sandbox**; i risultati intermedi non passano nel contesto del modello. Il host genera API tipizzate da `inputSchema`/`outputSchema`. Richiede sandbox sicure.

---

## 3. Ecosystem & Portability

### 3.1 SDK ufficiali (`docs/sdk.md`, `community/sdk-tiers.md`)
| Tier | SDK |
|---|---|
| **Tier 1** | **TypeScript, Python, C#, Go, Rust, Ruby** |
| **Tier 2** | **Java** |
| **Tier 3** | **Swift, PHP, Kotlin** |

Requisiti dei tier (SEP-1730):
| Requisito | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Conformance test | **100%** | **80%** | nessun minimo |
| Nuove feature di protocollo | prima del rilascio della nuova spec | entro 6 mesi | nessun impegno |
| Triage issue | 2 giorni lavorativi | entro un mese | — |
| Bug critici (P0) | 7 giorni | 2 settimane | — |
| Stable release | richiesta con versioning chiaro | almeno una | non richiesta |
Relegazione: test falliti per 4 settimane (Tier1→2: qualsiasi fallimento; Tier2→3: >20%), o issue ignorate per 2 mesi. Conformance suite: repo `modelcontextprotocol/conformance`. Decide l'**SDK Working Group**.
Gli SDK adottano le nuove revisioni secondo i propri tempi (es. TypeScript, Python, Go e C# aggiornati al rilascio 2026-07-28; Ruby 1.0 e poi Tier 1 a fine ottobre 2026).

### 3.2 MCP Registry (`sources/registry/`)
- **Registry ufficiale centralizzato di metadata** per server MCP **pubblicamente accessibili** (in **preview**). Sostenuto da Anthropic, GitHub, PulseMCP, Microsoft.
- Ospita **metadata**, non codice: punta ai pacchetti su npm, PyPI, NuGet, Docker/OCI, Cargo, MCPB… o a server **remoti** (`remotes` con `type: "streamable-http"`, URL pubblico).
- Formato **`server.json`**: `name` univoco in **reverse DNS** (`io.github.user/server`, `com.example/server`), `title`, `description`, `version` (**unica e immutabile** per pubblicazione; semver raccomandato; i range come `^1.2.3` sono **vietati**), `packages[]` (`registryType`, `identifier`, `version`, `transport`), `remotes[]`.
- **Namespace authentication**: GitHub (OAuth/OIDC) per `io.github.*`, **DNS** (record TXT `v=MCPv1; k=ed25519; p=…`) o **HTTP** (file `https://<dominio>/.well-known/mcp-registry-auth` con la chiave pubblica) per domini propri. Disponibili anche login via OIDC da GitHub Actions/GCP/Azure per la pubblicazione da CI.
- Verifica di proprietà dei pacchetti: es. npm → `mcpName` in `package.json` deve coincidere col `name` del server.json.
- **Non** supporta server privati. Non pensato per il self-hosting. Pensato per essere consumato dagli **aggregatori a valle** (marketplace), non direttamente dagli host; definisce un'**OpenAPI** che altri registry (anche privati) possono implementare (subregistry).
- Security scanning delegato ai package registry e agli aggregatori; anti-spam: namespace auth, validazione, takedown manuale (moderation policy).

**Registry, dettagli operativi** (`sources/registry/package-types.md`, `remote-servers.md`, `versioning.md`, `registry-aggregators.md`, `moderation-policy.md`):
- `registryType` supportati e verifica di proprietà:
  - **npm**: solo registry pubblico npm; `mcpName` in `package.json` uguale al `name` del server;
  - **pypi**: solo PyPI ufficiale; stringa `mcp-name: <nome>` nel README, anche in un commento;
  - **nuget**: solo NuGet ufficiale;
  - **cargo**;
  - **oci** (Docker Hub, ghcr.io, Quay, Google Artifact Registry, ACR, MCR): label `io.modelcontextprotocol.server.name`; tag anche come digest;
  - **mcpb**: release GitHub o GitLab.
- Server remoti: `remotes[].type` = `streamable-http` (raccomandato) o `sse` (deprecato, solo per client esistenti). Il registry verifica il **namespace** del nome, **non** il controllo dell'URL remoto. Più nomi possono puntare allo stesso URL. I consumatori identificano i record per **nome + versione**, non per URL. Se l'URL è su un tuo dominio conviene l'autenticazione DNS o HTTP.
- Versioni: `version` **obbligatoria**, unica per pubblicazione e immutabile. Semver raccomandato, ma è accettata qualsiasi stringa; una stringa non semver viene sempre marcata "latest". Usare prerelease per aggiornamenti solo-registry.
- Metadata immutabili **tranne `status`** (`deprecated`, `deleted`). `deleted` di solito indica violazione della moderation policy; gli aggregatori dovrebbero rimuovere questi server.
- **Subregistry** = aggregatore che implementa l'OpenAPI del registry e può aggiungere metadata in `_meta` (rating, download, scansioni di sicurezza).
- Moderation policy "permissiva":
  - **rimuove**: contenuti illegali, malware, spam, server non funzionanti;
  - **non rimuove**: server di bassa qualità o buggy, **con vulnerabilità**, duplicati funzionali, contenuti per adulti. La moderazione è spinta verso i subregistry.

### 3.3 Estensioni ufficiali (`sources/extensions/overview.md`, repo `ext-*`)
| Estensione | ID | Stage (nov 2026) | Scopo |
|---|---|---|---|
| OAuth Client Credentials | `io.modelcontextprotocol/oauth-client-credentials` | Stable | M2M |
| Enterprise-Managed Authorization | `io.modelcontextprotocol/enterprise-managed-authorization` | Stable | IdP aziendale, ID-JAG |
| MCP Apps | `io.modelcontextprotocol/ui` | Stable | UI HTML interattive in iframe sandbox; tool con `_meta.ui.resourceUri` → resource `ui://`; MIME `text/html;profile=mcp-app`; dialetto JSON-RPC `ui/*` tra app e host |
| Tasks | `io.modelcontextprotocol/tasks` | Beta, verso Core | operazioni lunghe (`tasks/get`, `tasks/update`, `tasks/cancel`) |
| Skills over MCP | `io.modelcontextprotocol/skills` | Beta | skill (`SKILL.md`) esposte via `skills/list`, `skills/get` + `resources/read` |
| Server Cards | (SEP-2127) | Beta | metadata del server prima di connettersi (discovery HTTP) |
| Events | `io.modelcontextprotocol/events` | Beta | eventi upstream: `events/list`, `events/poll` (+ push/webhook), cursori, `truncated` |

Lifecycle delle estensioni (SEP-3392): **Experimental** (cambia senza preavviso) → **Beta** (Extensions Track SEP; breaking change rari e documentati) → **Stable** (seconda SEP; cambia solo con una nuova revisione core) oppure promozione nel core con Standards Track SEP. L'ID non cambia tra gli stage. Matrice di supporto client in `extensions/client-matrix.md`.

### 3.4 Strumenti
- **MCP Inspector** (`@modelcontextprotocol/inspector`): tool di riferimento per test/debug; tre interfacce in un binario — Web (`npx @modelcontextprotocol/inspector`), CLI (`--cli`, per CI e agenti), TUI (`--tui`). Supporta anche le diverse "ere" di protocollo e flussi di autorizzazione.
- **Debugging**: log su **stderr** per server stdio (mai su stdout!), log lato server per HTTP; OpenTelemetry.
- **Conformance test suite**.

### 3.5 Portabilità
- Stesso protocollo su host diversi (Claude, ChatGPT, VS Code, Cursor…) e su transport diversi (semantica identica).
- Estensioni con **fallback al core** se non supportate dall'altra parte.
- **Compatibilità tra ere**: server **dual-era** servono client legacy (`initialize`) e modern; client dual-era fanno probe (`server/discover` su stdio, analisi del 400 su HTTP) e memorizzano l'era per processo/origin.
- CIMD rende i `client_id` portabili tra authorization server.
- Registry + `server.json` standardizzano installazione/configurazione; OpenAPI comune per registry privati.
- Vendor neutrality garantita dalla governance LF/AAIF.

---

### 3.6 MCP Bundles (MCPB) (blog 2025-11-20)
- Archivio **ZIP** (`.mcpb`) con un server MCP **locale** e un `manifest.json` (obbligatorio). Simile a `.crx` o `.vsix`: installazione **one-click** di server locali.
- Supporta Node.js, Python e binari compilati. Nato da Anthropic come **DXT** per Claude Desktop, poi spostato nel progetto MCP (repo `modelcontextprotocol/mcpb`) per la **portabilità cross-client**.
- Pubblicabile sul registry con `registryType: "mcpb"`.

## 4. Differenze con le versioni precedenti (dominio 5)
| Tema | Prima | 2026-07-28 / oggi |
|---|---|---|
| Governance | 2025-11-25: governance formale (SEP-932), WG/IG (SEP-1302), SDK tiers (SEP-1730) | + feature lifecycle (SEP-2596), workflow SEP PR-based (SEP-1850), extension lifecycle (SEP-3392) |
| Proprietà | progetto avviato da Anthropic (nov 2024) | donato ad AAIF / Linux Foundation (dic 2025) |
| Tasks | core sperimentale | estensione ufficiale |
| Scalabilità remota | sessioni ⇒ sticky routing / storage condiviso | stateless ⇒ round-robin |
| Estensioni | informali | framework formale, repo `ext-*`, capability `extensions` |
