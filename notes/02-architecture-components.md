# Dominio 2 — Architecture & Components (14%)

> Competenze ufficiali LF: **Schemas & Structured Data · MCP Hosts, Clients and Servers · Model Interaction Flow**
> Fonti: `sources/spec-2026-07-28/architecture/index.md`, `basic/index.md`, `basic/transports/*`, `server/discover.md`, `schema.ts`, `sources/docs/learn/architecture.md`.

---

## 1. Hosts, Clients, Servers (`architecture/index.md`)

Architettura **client-host-server**: un host gestisce più client; ogni client parla con **esattamente un** server.

```
┌────────────── Application Host Process ──────────────┐
│ Host ──> Client 1 ──────> Server 1 (Files & Git)  [locale, stdio]
│      ──> Client 2 ──────> Server 2 (Database)     [locale]
│      ──> Client 3 ──────> Server 3 (External APIs)[remoto, Streamable HTTP]
└──────────────────────────────────────────────────────┘
```

| Componente | Responsabilità (spec) |
|---|---|
| **Host** | crea e gestisce più client; controlla permessi e ciclo di vita delle connessioni; **applica policy di sicurezza e consenso**; gestisce le decisioni di autorizzazione dell'utente; coordina integrazione AI/LLM; **aggrega il contesto** tra client |
| **Client** | creato dall'host; 1 server; **allega versione e capability a ogni richiesta**; instrada i messaggi; gestisce sottoscrizioni e notifiche; mantiene i confini di sicurezza tra server |
| **Server** | espone resources, tools, prompts; opera in modo indipendente e focalizzato; chiede input al client (elicitation) tramite **`InputRequiredResult`** in una risposta; rispetta i vincoli di sicurezza; processo locale o servizio remoto |

Server locali stdio → tipicamente **un** client; server remoti Streamable HTTP → **molti** client.
Un host può aprire anche **più client verso lo stesso server** (diagramma docs: Client 3 e Client 4 → Server C).

## 2. Capability negotiation (2026-07-28)
- Client: capability in `_meta["io.modelcontextprotocol/clientCapabilities"]` in **ogni** richiesta.
- Server: capability nel risultato di **`server/discover`** (che il server MUST implementare; il client MAY chiamarlo).
- Entrambi devono rispettare le capability dichiarate. Estensioni tramite il campo `extensions`.

**ClientCapabilities** (`schema.ts`): `experimental?`, `roots?` (deprecata), `sampling? {context?, tools?}` (deprecata), `elicitation? {form?, url?}`, `extensions?`.
**ServerCapabilities**: `experimental?`, `logging?` (deprecata), `completions?`, `prompts? {listChanged?}`, `resources? {subscribe?, listChanged?}`, `tools? {listChanged?}`, `extensions?`.
Non è un insieme chiuso: si possono definire capability aggiuntive.

### `server/discover` (`server/discover.md`)
Richiesta senza parametri oltre `_meta`. Risposta `DiscoverResult`:
```json
{ "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": { "tools": {}, "resources": {} },
  "_meta": { "io.modelcontextprotocol/serverInfo": { "name": "ExampleServer", "version": "1.0.0" } },
  "instructions": "This server provides weather and resource utilities.",
  "ttlMs": 3600000, "cacheScope": "public" }
```
- `instructions`: guida in linguaggio naturale per l'LLM su come usare il server.
- Cacheable (`ttlMs`, `cacheScope`).
- Usi: presentare identità/capability in un colpo solo; **probe di retrocompatibilità su stdio**.

## 3. Model Interaction Flow
Flusso tipico end-to-end (spec + docs):
```
1. [opz.] Client → server/discover → versioni, capability, instructions
2. Client → tools/list (prompts/list, resources/list) → mette in cache (ttlMs/cacheScope)
3. Host passa al modello le definizioni dei tool (name, description, inputSchema)
4. Utente scrive → LLM decide di chiamare un tool (model-controlled)
5. Host chiede conferma all'utente (human in the loop), mostra gli input
6. Client → tools/call (con _meta: protocolVersion, clientCapabilities, clientInfo)
7. Server:
   a) risponde subito (complete) oppure
   b) InputRequiredResult (es. elicitation) → Host chiede all'utente → Client riprova con inputResponses
   c) [estensione Tasks] task handle → polling
8. Client valida il risultato (outputSchema) → Host lo inserisce nel contesto del modello
9. LLM produce la risposta finale all'utente
10. [opz.] subscriptions/listen → notifiche di cambi di liste/risorse → invalidazione cache → ri-list
```
Il contesto completo della conversazione resta **nell'host**; i server ricevono solo il necessario.
Resources: l'**applicazione** decide come includerle (picker, ricerca, inclusione automatica). Prompts: l'**utente** li sceglie (es. slash command).

### 3.1 Server instructions (`server/discover` → `instructions`; blog 2025-11-03)
- Campo **opzionale** di `server/discover` (prima stava nell'`InitializeResult`): testo in linguaggio naturale per l'LLM su **come usare il server nel suo insieme**. Esempi: ordine dei tool (`validate_schema` → `create_backup` → `migrate_schema`), rate limit, dipendenze tra tool, fallback se l'elicitation non è supportata.
- Il host lo inietta tipicamente nel **system prompt**. Vantaggio rispetto alle descrizioni dei tool (spazio limitato, ripetizione) e ai prompts (vanno scelti dall'utente).
- Anti-pattern: ripetere le descrizioni dei tool; claim di marketing; istruzioni comportamentali generiche ("parla come un pirata"); manuali lunghi.
- **Non garantiscono** un comportamento: mai usarle per azioni critiche di sicurezza o privacy, che richiedono regole deterministiche o hook. Non compensano un cattivo design dei tool e non cambiano la personalità del modello.
- Client: mostrare all'utente le instructions iniettate (trasparenza) e permettere di rivederle, abilitarle o disabilitarle.

### 3.2 Modello di interazione utente per primitiva (`docs/learn/server-concepts.md`)
| Primitiva | Chi controlla | Pattern UI tipici |
|---|---|---|
| Tools | **modello** (scoperta e invocazione automatica) con supervisione umana | elenco dei tool abilitabili per interazione, **dialog di approvazione** per singola esecuzione, permessi per pre-approvare operazioni sicure, **activity log** delle esecuzioni |
| Resources | **applicazione** | albero o lista tipo cartelle, ricerca e filtri, inclusione automatica o suggerimenti, selezione manuale o multipla; la spec **non impone** UI |
| Prompts | **utente** (invocazione esplicita) | **slash command** (`/plan-vacation`), command palette, pulsanti dedicati, menu contestuali; il template deve essere visibile |
| Elicitation | server chiede, **utente** risponde | form o URL; accept, decline o cancel |

### 3.3 Più server insieme e nomi dei tool (`server/tools.md` §Tool Names)
- Esempio ufficiale "travel planner": tre server (Travel, Weather, Calendar/Email). L'utente avvia un **prompt** (`prompts/get` "plan-vacation"), l'app aggiunge **resources** (calendario, preferenze), il modello chiama **tools** di server diversi. Il host orchestra; i server non si parlano tra loro.
- Nomi dei tool: **SHOULD** 1–128 caratteri, case-sensitive, solo `A-Z a-z 0-9 _ - .`, senza spazi o virgole, **univoci nel server** (es. `getUser`, `DATA_EXPORT_v2`, `admin.tools.list`).
- L'unicità vale **solo all'interno di un server**. Client e proxy che aggregano più server possono avere collisioni (due `search`) e **SHOULD** disambiguare, ad esempio con un **prefisso** che identifica il server.
- `serverInfo.name` **non** è garantito univoco e **SHOULD NOT** essere usato per disambiguare.

## 4. Transports (`basic/transports/*`)
Un transport è un **binding**: definisce framing, consegna, trasporto dei metadata, cancellazione e terminazione; **non** il significato dei messaggi. Messaggi **UTF-8**. Direzioni ammesse: client→server request/notification; server→client response/notification.

### 4.1 stdio
- Il client **lancia il server come subprocess**; server legge da `stdin`, scrive su `stdout`.
- Un messaggio JSON-RPC per riga, delimitato da newline; **MUST NOT** contenere newline interne.
- Server MAY scrivere log UTF-8 su **`stderr`**; il client MAY catturarli/ignorarli e SHOULD NOT considerarli errori.
- Su `stdout` **solo** messaggi MCP validi; su `stdin` solo messaggi MCP validi.
- Il server MUST NOT scrivere request su stdout. Unico canale condiviso: le notifiche di subscription si correlano con `subscriptionId`.
- Metadata solo nel body (nessun layer di header).
- Cancellazione: `notifications/cancelled`.
- **Shutdown**: il client chiude lo stdin del server → attende l'uscita → se non esce, termina forzatamente (POSIX: SIGTERM → SIGKILL; Windows: `TerminateProcess`/Job Objects). Il server SHOULD uscire su EOF di stdin. Il server MAY chiudere il suo stdout e uscire.
- Terminazione inattesa: il client SHOULD riavviarlo; richieste in volo perse (retry); ristabilire le subscription.
- Il framing stdio SHOULD essere riusato per transport custom su byte stream (Unix socket, TCP).
- Autorizzazione: **non** la spec OAuth; credenziali dall'ambiente.

### 4.2 Streamable HTTP (introdotto nella 2025-03-26, cambiato nella 2026-07-28)
- **Un solo endpoint** (MCP endpoint, es. `https://example.com/mcp`) che accetta **POST**.
- Ogni messaggio del client = **una nuova POST**; `Accept: application/json, text/event-stream` (entrambi MUST).
- Body = una singola request o notification (mai response).
- Notification accettata → **202 Accepted** senza body; rifiutata → errore HTTP (es. 400).
- Request → risposta `Content-Type: application/json` **oppure** `text/event-stream` (SSE scoped alla richiesta); il client MUST supportare entrambi.
- Su SSE: notifiche relative alla richiesta prima della risposta finale; **niente request** del server; la risposta finale SHOULD chiudere lo stream; header `X-Accel-Buffering: no` SHOULD; keep-alive con commenti SSE (`:`) incoraggiati sugli stream lunghi.
- **Niente resumability** (`Last-Event-ID` non supportato): stream interrotto ⇒ richiesta persa ⇒ ri-emettere con **nuovo id**.
- **Niente GET**, **niente sessioni** (`Mcp-Session-Id`), **niente DELETE**. Un server solo-2026-07-28 risponde **405** a GET/DELETE, ignora `Mcp-Session-Id` (senza crearne o rimandarne) e `Last-Event-ID`.
- Cancellazione = chiusura dello stream SSE.
- Sicurezza: validazione `Origin` (403), bind su 127.0.0.1 in locale, autenticazione.

#### Header di richiesta (mirroring del body per intermediari)
| Header | Fonte | Obbligatorio per |
|---|---|---|
| `MCP-Protocol-Version` | `_meta.io.modelcontextprotocol/protocolVersion` | ogni POST |
| `Mcp-Method` | `method` | tutte le richieste |
| `Mcp-Name` | `params.name` o `params.uri` | `tools/call`, `resources/read`, `prompts/get` |
| `Mcp-Param-{Name}` | parametri marcati `x-mcp-header` | quando il valore è presente (né null né assente) |
| `Authorization: Bearer …` | token OAuth | ogni richiesta verso server protetto |

- Header **names** case-insensitive, **values** case-sensitive.
- Il body è la **fonte di verità**; mismatch o header mancanti → **400 + `HeaderMismatch` (-32020)**. Confronto numerico per gli interi (`42.0` = `42`).
- Versione non supportata → **400 + `UnsupportedProtocolVersionError`**; metodo non implementato → **404 + `-32601`**.
- Header assente `MCP-Protocol-Version`: un server che supporta client < 2025-06-18 MAY assumere `2025-03-26`, altrimenti rifiuta.
- **Valori non ASCII-safe** (non-ASCII, controlli, spazi iniziali/finali, o che sembrano la sentinella) → `=?base64?{Base64(UTF-8)}?=` (marker minuscoli, case-sensitive); vale anche per `Mcp-Name`.

#### `x-mcp-header`
- Va nello schema della proprietà dentro `inputSchema`; il valore è la parte `{name}` di `Mcp-Param-{name}`.
- Vincoli: non vuoto; token HTTP valido (RFC 9110 `1*tchar`); niente CR/LF; unico (case-insensitive) nello schema; solo tipi **integer, string, boolean** (no `number`; interi nel range sicuro ±(2^53−1)); solo proprietà **staticamente raggiungibili** tramite catena di `properties` (non attraverso `items`, `oneOf/anyOf/allOf/not`, `if/then/else`, `$ref`).
- Il client HTTP **MUST** supportarlo; tool con `x-mcp-header` invalido → **escluso** dal risultato di `tools/list` (con warning), gli altri tool restano. Su stdio MAY ignorarlo.
- Conversione: string as-is, integer decimale, boolean `true`/`false` minuscolo.
- Intermediari che non riconoscono `Mcp-Param-*` MUST inoltrarlo e ignorarlo.
- Esempio: `"region": {"type":"string","x-mcp-header":"Region"}` → `Mcp-Param-Region: us-west1`.

#### Retrocompatibilità HTTP
- Client dual-era: tenta una richiesta modern; su **400** ispeziona il body: errore modern riconosciuto ⇒ server modern (correggi/riprova); body vuoto/non riconosciuto ⇒ fallback a `initialize` (legacy).
- Verso il vecchio **HTTP+SSE (2024-11-05, deprecato)**: POST fallisce con 400/404/405 **senza** errore modern → GET all'URL, attende evento `endpoint`.

### 4.3 Transport custom
MAY; devono preservare formato JSON-RPC, message patterns e modello di metadata per richiesta; SHOULD documentare connessione, framing, cancellazione.

## 5. Schemas & Structured Data

### 5.1 Schema del protocollo
- **`schema.ts`** (TypeScript) = **fonte di verità** di tutti i messaggi; **`schema.json`** generato da esso. Nella 2026-07-28: `LATEST_PROTOCOL_VERSION = "2026-07-28"`, `JSONRPC_VERSION = "2.0"`.

### 5.2 JSON Schema in MCP
- Dialetto di default **JSON Schema 2020-12** quando manca `$schema` (dalla 2025-11-25, SEP-1613); MAY dichiarare altri dialetti (es. draft-07); MUST supportare almeno 2020-12; dialetti non supportati → errore appropriato.
- 2026-07-28 (SEP-2106): `inputSchema`/`outputSchema` accettano **qualsiasi keyword 2020-12**; `structuredContent` qualsiasi valore JSON; regole su `$ref` (niente dereferenziazione di rete automatica) e limiti sulle composizioni.
- `inputSchema`: oggetto con `type: "object"` alla radice (gli argomenti sono sempre oggetti). Con composizioni: dichiarare `properties` alla radice e usare i rami solo per asserzioni di presenza (`required`).
- **Elicitation `requestedSchema`**: sottoinsieme ristretto, **oggetto piatto di primitive** (string/number/integer/boolean/enum), niente oggetti annidati o array di oggetti.

### 5.3 Structured tool output
- `outputSchema` (opzionale) → il server MUST produrre `structuredContent` conforme; il client SHOULD validare.
- `structuredContent` può essere oggetto, array, stringa, numero, boolean o null.
- Retrocompatibilità: includere anche il JSON serializzato in un blocco `text`.

### 5.4 Strutture comuni
- **`_meta`**: chiavi con prefisso opzionale (label separate da punti + `/`, reverse DNS consigliato) + nome. Prefissi con **secondo label `modelcontextprotocol` o `mcp`** sono **riservati** (`io.modelcontextprotocol/`, `dev.mcp/`…); `com.example.mcp/` **non** è riservato. Eccezione: `traceparent`, `tracestate`, `baggage`.
- **Chiavi riservate**: `progressToken`, `io.modelcontextprotocol/{protocolVersion, clientInfo, clientCapabilities, logLevel, serverInfo, subscriptionId}`, `traceparent`, `tracestate`, `baggage`.
- **`Implementation`** (clientInfo/serverInfo): `name`, `version`, `title?`, `description?`, `icons?`… self-reported.
- **`icons`**: `src` (HTTPS o `data:`), `mimeType?`, `sizes?` (`["48x48"]`, `["any"]` per SVG), `theme?` (`light`/`dark`). Client che li mostrano MUST supportare PNG e JPEG, SHOULD SVG e WebP. Su `Implementation`, `Tool`, `Prompt`, `Resource`.
- **`BaseMetadata`**: `name` (programmatico) + `title` (display, dalla 2025-06-18).
- **Content blocks**: `TextContent`, `ImageContent`, `AudioContent`, `ResourceLink`, `EmbeddedResource` (+ `ToolUseContent`/`ToolResultContent` nel sampling).
- **Annotations** (content/resources): `audience`, `priority`, `lastModified`.
- **ToolAnnotations**: `title`, `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`.
- **Cursor** opaco, **`CacheableResult`** (`ttlMs`, `cacheScope`).

## 6. Estensioni (architettura)
- Opzionali, opt-in, supporto esplicito da entrambe le parti; negoziate tramite `capabilities.extensions` (client per richiesta, server in `server/discover`).
- Identificatore `{vendor-prefix}/{extension-name}` con prefisso **obbligatorio** (regole delle chiavi `_meta`), es. `io.modelcontextprotocol/tasks`, `io.modelcontextprotocol/ui` (MCP Apps), `com.example/…`.
- Valore = oggetto di impostazioni (`{}` = supporto senza impostazioni).
- Se una parte non supporta l'estensione: l'altra MUST tornare al comportamento core o rifiutare con errore; le estensioni SHOULD documentare il fallback.
- Lifecycle (SEP-3392): **Experimental → Beta → Stable** (o promozione nel core). Repo ufficiali con prefisso `ext-`.

## 7. Differenze con le versioni precedenti (dominio 2)
| Tema | Prima | 2026-07-28 |
|---|---|---|
| Lifecycle | fasi Initialization → Operation → Shutdown | nessuna fase: richieste indipendenti |
| Capability | scambiate una volta in `initialize` | client: per richiesta; server: `server/discover` |
| Server identity | `serverInfo` nella risposta a initialize | `_meta.io.modelcontextprotocol/serverInfo` in ogni result |
| Streamable HTTP | POST + GET (stream standalone) + DELETE (fine sessione), `Mcp-Session-Id`, resumability | solo POST, niente sessioni, niente resumability, header `Mcp-Method`/`Mcp-Name` |
| HTTP+SSE (2024-11-05) | deprecato dal 2025-03-26 | classificato formalmente Deprecated (SEP-2596) |
| JSON Schema | 2025-11-25: default 2020-12 | qualsiasi keyword 2020-12, `$ref` sicuro |
| Estensioni | informali | campo `extensions` nelle capability, lifecycle formale |
