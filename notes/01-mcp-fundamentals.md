# Dominio 1 — MCP Fundamentals (16%)

> Competenze ufficiali LF: **MCP Purpose & Scope · Core MCP Concepts · Interoperability & Value**
> Fonti: `sources/docs/getting-started/intro.md`, `sources/docs/learn/architecture.md`, `sources/spec-2026-07-28/index.md`, `architecture/index.md`, `basic/versioning.md`, `sources/docs/learn/versioning.md`.

---

## 1. Purpose & Scope

**Definizione** (intro): MCP è uno **standard open-source per connettere applicazioni AI a sistemi esterni** — data source (file, database), tool (motori di ricerca, calcolatrici) e workflow (prompt specializzati).
**Analogia ufficiale**: MCP è come una **porta USB-C per le applicazioni AI**.
**Ispirazione**: il **Language Server Protocol (LSP)** — come LSP standardizza il supporto ai linguaggi negli IDE, MCP standardizza l'integrazione di contesto e tool nelle applicazioni AI.

Secondo la spec (`index.md`), MCP fornisce un modo standard per:
- condividere informazioni contestuali con i modelli linguistici;
- esporre tool e capability ai sistemi AI;
- costruire integrazioni e workflow componibili.

**Cosa MCP NON fa** (architecture doc): si occupa **solo del protocollo di scambio del contesto**; **non** stabilisce come l'applicazione AI usa gli LLM o gestisce il contesto ricevuto.

**Il "progetto" MCP comprende**:
- la **Specification** (requisiti di implementazione);
- gli **SDK** ufficiali;
- **strumenti di sviluppo** (es. **MCP Inspector**);
- **reference server implementations** (`modelcontextprotocol/servers`).

**Base tecnica**: messaggi **JSON-RPC 2.0**. Fonte di verità del protocollo: lo **schema TypeScript** (`schema.ts`); il JSON Schema (`schema.json`) è generato automaticamente da esso.

**Parole chiave normative**: MUST/SHOULD/MAY secondo **BCP 14** (RFC 2119 + RFC 8174), solo se in maiuscolo.

---

## 2. Core Concepts

### 2.1 Partecipanti
| Ruolo | Definizione |
|---|---|
| **Host** | l'applicazione AI (es. Claude Desktop, Claude Code, VS Code) che crea e coordina uno o più client |
| **Client** | componente nell'host che mantiene la connessione con **un solo** server (rapporto **1:1**) |
| **Server** | programma che fornisce contesto e capability; **locale** (tipicamente stdio, serve un solo client) o **remoto** (Streamable HTTP, serve molti client) |

"Server" indica il programma indipendentemente da dove gira. Esempio ufficiale: VS Code (host) che si connette al server Sentry (remoto) e al filesystem server (locale) crea **due** oggetti client.

### 2.2 Due layer
- **Data layer** (interno): protocollo JSON-RPC — discovery di versioni e capability (`server/discover`), primitive server (tools, resources, prompts), primitive client (elicitation), utility (notifiche, progress).
- **Transport layer** (esterno): canali e meccanismi di comunicazione — connessione, framing, **autorizzazione**. Due transport standard: **stdio** e **Streamable HTTP**.

### 2.3 Primitive
| Lato | Primitiva | Controllo | Metodi |
|---|---|---|---|
| Server | **Tools** | model-controlled | `tools/list`, `tools/call` |
| Server | **Resources** | application-controlled | `resources/list`, `resources/read`, `resources/templates/list` |
| Server | **Prompts** | user-controlled | `prompts/list`, `prompts/get` |
| Client | **Elicitation** | — | `elicitation/create` (via MRTR) |
| Client (deprecata) | Sampling | — | `sampling/createMessage` |
| Client (deprecata) | Roots | — | `roots/list` |

Ogni primitiva server ha un metodo `*/list` per la discovery e uno di retrieval (`resources/read`, `prompts/get`) o esecuzione (`tools/call`). Le liste sono **dinamiche**.
Esempio ufficiale: un server per un database espone **tool** per interrogarlo, una **resource** con lo schema, un **prompt** con esempi few-shot.

### 2.4 Proprietà chiave del protocollo (2026-07-28)
- **Stateless**: richieste auto-contenute; nessuna sessione di protocollo.
- **Capability negotiation per richiesta**: il client dichiara le sue capability nel `_meta` di ogni richiesta; il server le pubblica in `server/discover`.
- **Feature progressive**: core minimo + capability/estensioni opzionali.
- Componenti obbligatori per tutte le implementazioni: **base protocol, versioning, message patterns**. Il resto (auth, feature server/client, utility) è MAY in base ai bisogni.

### 2.5 Design principles (`architecture/index.md`)
1. **I server devono essere estremamente facili da costruire** (l'orchestrazione complessa sta nell'host).
2. **I server devono essere altamente componibili** (funzionalità focalizzate, combinabili).
3. **I server non devono leggere l'intera conversazione né "vedere dentro" altri server** (isolamento, l'host controlla).
4. **Le feature si aggiungono progressivamente** (negoziazione, evoluzione indipendente, retrocompatibilità).

Esistono anche i "community design principles" in `sources/community/design-principles.md`.

---

### 2.6 Principi di design del **progetto** (`sources/community/design-principles.md`)
Da non confondere con i design principles **architetturali** della spec (§2.5). Questi servono ai Core Maintainer per accettare o rifiutare le SEP e le estensioni. Quando due principi sono in conflitto, si bilanciano: non c'è una gerarchia.
| Principio | Significato |
|---|---|
| **Convergence over choice** | un solo modo di risolvere un problema; le estensioni sono il banco di prova, la spec è dove si consolida |
| **Composability over specificity** | primitive di base (resources, tools, prompts); niente feature per casi costruibili con quelle (i pattern emergenti diventano estensioni: MCP Apps, Tasks) |
| **Interoperability over optimization** | feature che degradano con grazia; la capability negotiation adatta il protocollo invece di presumere |
| **Stability over velocity** | ogni aggiunta è permanente; si ottimizza "per decenni, non per trimestri"; le rimozioni seguono la Feature Lifecycle policy |
| **Capability over compensation** | niente struttura permanente per aggirare limiti temporanei dei modelli |
| **Demonstration over deliberation** | implementazioni funzionanti prima dei dibattiti; una SEP richiede un **prototipo** per essere accettata |
| **Pragmatism over purity** | compromessi pratici a favore dell'adozione |
| **Standardization over innovation** | si standardizzano pattern già provati; i nuovi si sperimentano prima nelle estensioni |

## 3. Versioning (`docs/learn/versioning.md`, `spec/basic/versioning.md`)
- Formato **`YYYY-MM-DD`** = data dell'**ultima modifica backwards-incompatible**. Non cambia per modifiche compatibili.
- Stati delle revisioni: **Draft** (in lavorazione), **Current** (in uso, può ricevere modifiche compatibili), **Final** (chiusa).
- **Current = `2026-07-28`**. Revisioni precedenti: `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05`.
- Stati delle feature (SEP-2596): **Active**, **Deprecated** (≥ 12 mesi, o ≥ 90 giorni con expedited removal), **Removed**.
- Negoziazione: ogni richiesta porta `io.modelcontextprotocol/protocolVersion` (+ header `MCP-Protocol-Version` su HTTP); il server accetta o rifiuta **ogni richiesta** indipendentemente; se non supporta la versione → `UnsupportedProtocolVersionError` (-32022) con `supported`. Client e server MAY supportare più versioni.
- **Ere**: **Modern** (≥ 2026-07-28, metadata per richiesta), **Legacy** (≤ 2025-11-25, handshake `initialize`), **Dual-era** (supporta entrambe).

---

## 4. Interoperability & Value
**Valore per attore** (intro):
- **Sviluppatori**: meno tempo e complessità per costruire/integrare app e agenti AI.
- **Applicazioni AI / agenti**: accesso a un ecosistema di data source, tool e app.
- **Utenti finali**: app più capaci che accedono ai loro dati e agiscono per loro quando serve.

**Interoperabilità** — perché funziona:
- problema **N×M** → **N+M**: ogni host implementa MCP una volta, ogni servizio espone un server una volta;
- protocollo **vendor-neutral** (governato da AAIF/Linux Foundation), stesso formato su tutti i transport;
- capability negotiation + estensioni opt-in con fallback al core;
- SDK ufficiali in 10 linguaggi con conformance test;
- registry ufficiale con namespace verificati;
- supporto da client come Claude, ChatGPT, VS Code, Cursor e molti altri.

Esempi d'uso dall'intro: agenti che accedono a Google Calendar e Notion; Claude Code che genera un'app web da un design Figma; chatbot aziendali su più database; modelli che creano design 3D in Blender e li stampano.

---

## 5. Cronologia essenziale delle revisioni
| Revisione | Novità principali |
|---|---|
| **2024-11-05** | prima spec pubblica: initialize/lifecycle, tools/resources/prompts, sampling, roots, logging, transport **stdio + HTTP+SSE** |
| **2025-03-26** | **Streamable HTTP** (sostituisce HTTP+SSE), framework di autorizzazione **OAuth 2.1**, tool annotations, audio content, completions capability, JSON-RPC batching (poi rimosso) |
| **2025-06-18** | rimosso il **batching**, **structured tool output** (`outputSchema`/`structuredContent`), server come **OAuth Resource Server** (RFC 9728), **Resource Indicators** obbligatori (RFC 8707), **elicitation**, **resource links**, header **`MCP-Protocol-Version`**, campo `title` |
| **2025-11-25** | OIDC Discovery, **icons**, step-up scope via `WWW-Authenticate`, linee guida nomi tool, **URL mode elicitation**, **tools nel sampling**, **CIMD**, **tasks** sperimentali, JSON Schema 2020-12 default, input validation = tool execution error, governance formale (SEP-932), SDK tiers |
| **2026-07-28** | **stateless** (via `initialize` e sessioni), `server/discover`, **MRTR**, `resultType`, `subscriptions/listen`, header `Mcp-Method`/`Mcp-Name`/`x-mcp-header`, **caching** `ttlMs`/`cacheScope`, Tasks come estensione, RFC 9207, DCR deprecata, deprecazione roots/sampling/logging, policy di deprecazione |

Dettagli completi in `notes/10-novita-2026-07-28.md`.
