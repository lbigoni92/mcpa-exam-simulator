# Dominio 3 — Interactions & Execution (26%)

> Competenze ufficiali LF: **Interaction Patterns & Response Handling · Error Handling · Tool Invocation Lifecycle · Protocol Primitives**
> È il dominio con il peso maggiore. Quasi tutto è cambiato nella 2026-07-28: niente handshake, MRTR, `subscriptions/listen`, `resultType`, caching.
> Fonti: `sources/spec-2026-07-28/basic/` (index, patterns/*, transports/*), `server/*`, `client/elicitation.md`, `schema.ts`.

---

## 1. Messaggi JSON-RPC 2.0 (`basic/index.md` §Messages)

Tutti i messaggi **MUST** seguire JSON-RPC 2.0 e (sul transport) essere **UTF-8**. Tre tipi:

| Tipo | Direzione (2026-07-28) | Regole chiave |
|---|---|---|
| **Request** | **solo client → server** | `id` string o integer, **MUST NOT** essere `null` (diverso da JSON-RPC base); `id` non riusato tra richieste ancora pendenti dello stesso mittente |
| **Response** (result / error) | **solo server → client** | stesso `id` della request; `result` **MUST** contenere `resultType`; `error` con `code` (intero) + `message` (+ `data` opzionale) |
| **Notification** | entrambe le direzioni, ma nel core client→server esiste solo `notifications/cancelled` (stdio) | **MUST NOT** avere `id`; il ricevente **MUST NOT** rispondere |

**Novità cruciale**: *"Servers MUST NOT initiate JSON-RPC requests, and clients do not send JSON-RPC responses"* (`basic/patterns/index.md`). Ogni interazione inizia dal client.
JSON-RPC **batching**: rimosso già nella 2025-06-18.

### 1.1 `resultType` (novità 2026-07-28, SEP-2322)
- Ogni `result` **MUST** avere `resultType`:
  - `"complete"` → risultato finale;
  - `"input_required"` → `InputRequiredResult` (MRTR), servono altre informazioni.
- Le estensioni MAY aggiungere valori (es. Tasks: `"task"`) solo se negoziati via capabilities.
- Valore non riconosciuto → **invalido**.
- Retrocompatibilità: `resultType` **assente** ⇒ trattare come `"complete"` (server di versioni precedenti).

### 1.2 Statelessness (`basic/index.md` §Statelessness)
- Ogni richiesta è **auto-contenuta**: versione, capabilities, identità del client stanno nel `_meta` di **ogni** richiesta.
- Server **MUST NOT** basarsi su richieste precedenti della stessa connessione per il contesto.
- Server SHOULD gestire richieste di task/thread/conversazioni diverse; SHOULD NOT richiedere di riusare la stessa connessione/processo.
- Client SHOULD NOT usare una conversazione come confine di vita del processo stdio.
- Stato multi-richiesta (task, handle applicativi) **MUST** essere riferito con un **identificatore esplicito** passato a ogni richiesta.
- Una connessione aperta (es. processo stdio) **non** è una sessione/conversazione.
- Le richieste long-lived (`subscriptions/listen`) restano request/response: la risposta è uno stream aperto con stato legato alla richiesta.

### 1.3 Campi `_meta` per richiesta (obbligatori!)
| Chiave | Obbligatoria | Contenuto |
|---|---|---|
| `io.modelcontextprotocol/protocolVersion` | **Sì** | es. `"2026-07-28"` |
| `io.modelcontextprotocol/clientCapabilities` | **Sì** | `ClientCapabilities` rilevanti per la richiesta (anche `{}`) |
| `io.modelcontextprotocol/clientInfo` | No (SHOULD) | `Implementation` {name, version…} |
| `io.modelcontextprotocol/logLevel` | No | livello minimo di log per quella richiesta (logging deprecato) |
| `progressToken` | No | abilita `notifications/progress` |

- Manca un campo obbligatorio ⇒ richiesta malformata ⇒ **`-32602` Invalid params** (su HTTP `400`).
- Il server ha bisogno di una capability non dichiarata ⇒ **`MissingRequiredClientCapabilityError` (-32021)** con `data.requiredCapabilities` (HTTP `400`).
- Risposte: il server SHOULD includere `io.modelcontextprotocol/serverInfo` nel `_meta` di ogni result.
- Notifiche su `subscriptions/listen` ⇒ MUST includere `io.modelcontextprotocol/subscriptionId`.

Esempio richiesta completa:
```json
{
  "jsonrpc": "2.0", "id": 2, "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": { "location": "New York" },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": { "name": "ExampleClient", "version": "1.0.0" },
      "io.modelcontextprotocol/clientCapabilities": {},
      "traceparent": "00-0af7651916cd43dd8448eb211c80319c-00f067aa0ba902b7-01"
    }
  }
}
```

---

## 2. Message patterns (`basic/patterns/index.md`)
Tre pattern, tutti obbligatori da supportare (base protocol + versioning + patterns sono MUST; il resto MAY):

1. **Request and Response** – il server risponde con result o error; durante la richiesta MAY inviare notifiche **scoped** a essa (`notifications/progress`, `notifications/message`).
2. **Multi Round-Trip Requests (MRTR)** – il server risponde `InputRequiredResult`; il client **riprova** la richiesta con `inputResponses`.
3. **Subscribe and Notify** – `subscriptions/listen` apre uno stream long-lived di notifiche scelte.

I transport portano tutti i pattern senza modifiche; nuovi pattern vengono definiti solo in quella pagina.

---

## 3. Multi Round-Trip Requests — MRTR (`basic/patterns/mrtr.md`, SEP-2322) ★ novità

Sostituisce le **richieste server→client** (`elicitation/create`, `sampling/createMessage`, `roots/list`). Breaking change: il vecchio pattern non è più supportato.

### 3.1 Flusso
1. Client invia la richiesta (id: 1).
2. Server risponde `resultType: "input_required"` con `inputRequests` e/o `requestState`. La richiesta 1 è **terminata**.
3. Client raccoglie l'input (utente, LLM…) e **riprova** la richiesta originale con **nuovo id** (id: 2) + `inputResponses` + `requestState` identico.
4. Server completa → `resultType: "complete"` (oppure un nuovo `InputRequiredResult`).

Nessuno storage condiviso tra istanze né load balancing stateful necessario: lo stato viaggia in `requestState`.

### 3.2 Tipi
- **`InputRequests`**: mappa `chiave → richiesta` (chiavi assegnate dal server, uniche nella richiesta). Valori ammessi: `ElicitRequest`, `CreateMessageRequest`, `ListRootsRequest`.
- **`InputResponses`**: mappa con le stesse chiavi → risultati (`ElicitResult`, `CreateMessageResult`, `ListRootsResult`).
- **`InputRequiredResult`**: `inputRequests?` + `requestState?` (stringa opaca); **almeno uno** dei due MUST esserci.

```json
{ "jsonrpc": "2.0", "id": 2,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "github_login": {
        "method": "elicitation/create",
        "params": { "mode": "form", "message": "Please provide your GitHub username",
          "requestedSchema": { "type": "object", "properties": { "name": { "type": "string" } }, "required": ["name"] } }
      }
    },
    "requestState": "eyJsb2NhdGlvbiI6Ik5ldyBZb3JrIn0..."
  } }
```
Retry:
```json
{ "jsonrpc": "2.0", "id": 3, "method": "tools/call",
  "params": { "name": "get_weather", "arguments": { "location": "New York" },
    "inputResponses": { "github_login": { "action": "accept", "content": { "name": "octocat" } } },
    "requestState": "eyJsb2NhdGlvbiI6Ik5ldyBZb3JrIn0..." } }
```

### 3.3 Dove si può usare
Solo su **`tools/call`**, **`resources/read`**, **`prompts/get`**. Su qualunque altra richiesta il server **MUST NOT** restituire `InputRequiredResult`.

### 3.4 Requisiti server
- MAY rispondere `InputRequiredResult` alle richieste supportate.
- Chiavi uniche; valori solo dei tre tipi ammessi.
- `requestState` libero nel formato (base64 JSON, JWT cifrato, binario…), ma è **attacker-controlled**: integrità (HMAC/AEAD) MUST se influenza autorizzazione/accesso/business logic; anti-replay SHOULD (principal, TTL, id richiesta originale); single-use solo con enforcement server-side.
- **MUST NOT** chiedere input che il client non ha dichiarato nelle capabilities (es. niente `elicitation/create` se manca `elicitation`).
- **MUST NOT** assumere che il client soddisfi le richieste o riprovi; MAY richiedere più volte.
- Se mancano dati necessari nel retry → SHOULD rispondere con un nuovo `InputRequiredResult` (non con un errore). Dati extra non riconosciuti → SHOULD ignorarli. `InputResponses` malformato → errore JSON-RPC.

### 3.5 Requisiti client
- Se c'è `inputRequests` → MUST costruire gli input prima del retry; se non c'è → MAY riprovare subito.
- Se c'è `requestState` → MUST rimandarlo **esatto**, senza ispezionarlo/modificarlo; se non c'è → MUST NOT includerne uno.
- Il JSON-RPC `id` **MUST essere diverso** tra richiesta iniziale e retry.
- `inputRequests`/`requestState` valgono **solo** per il retry di quella richiesta, non per richieste parallele.
- I risultati di retry MRTR (con `inputResponses`/`requestState`) **MUST NOT** essere messi in cache.

---

## 4. Subscriptions (`basic/patterns/subscriptions.md`) ★ novità
`subscriptions/listen` sostituisce `resources/subscribe`/`resources/unsubscribe` e l'endpoint **HTTP GET**.

### 4.1 Apertura
```json
{ "jsonrpc": "2.0", "id": 1, "method": "subscriptions/listen",
  "params": { "_meta": { "...": "..." },
    "notifications": { "toolsListChanged": true, "resourceSubscriptions": ["file:///project/config.json"] } } }
```
Filtro (`notifications`), tutti opzionali:
| Campo | Tipo | Notifica |
|---|---|---|
| `toolsListChanged` | boolean | `notifications/tools/list_changed` |
| `promptsListChanged` | boolean | `notifications/prompts/list_changed` |
| `resourcesListChanged` | boolean | `notifications/resources/list_changed` |
| `resourceSubscriptions` | string[] (URI) | `notifications/resources/updated` |

Il server **MUST NOT** inviare tipi non richiesti.

### 4.2 Acknowledgment
- Primo messaggio **MUST** essere `notifications/subscriptions/acknowledged` con `_meta["io.modelcontextprotocol/subscriptionId"]`; nessuna notifica prima.
- Il campo `notifications` dell'ack riflette il **sottoinsieme accettato** (i tipi non supportati sono omessi); il client SHOULD confrontarlo.
- Su stdio l'ordine vale **per subscription ID**, non per canale (possono interfoliarsi messaggi di altre sottoscrizioni).

### 4.3 Notifiche e correlazione
- `subscriptionId` = **JSON-RPC id della richiesta `subscriptions/listen`**.
- Su stdio il client MUST usarlo per demultiplexare. Sottoscrizioni multiple concorrenti ammesse.
- Notifiche **request-scoped** (`notifications/progress`, `notifications/message`) **non** passano dallo stream di listen ma da quello della richiesta a cui si riferiscono.

### 4.4 Fine
- Client: chiude lo stream SSE (HTTP) oppure `notifications/cancelled` con l'id della listen (stdio).
- Server (es. shutdown): SHOULD inviare una **risposta di successo** alla `subscriptions/listen` (`resultType:"complete"` + `subscriptionId`) = chiusura graceful; la pagina Cancellation aggiunge che il server MUST inviare `notifications/cancelled` riferito alla listen quando abbatte lo stream (unico uso lecito di `notifications/cancelled` lato server). *(Vedi `notes/13-trappole-e-ambiguita.md`.)*
- Chiusura del transport senza risposta = disconnessione inattesa → il client MAY riconnettersi. Su stdio dopo riconnessione il client MUST re-inviare `subscriptions/listen` (il server non conserva stato).

---

## 5. Progress e Cancellation

### 5.1 Progress (`basic/patterns/progress.md`)
- Il client mette `progressToken` (string o integer, **unico tra le richieste attive**) in `params._meta`.
- Il server MAY inviare `notifications/progress` con `progressToken`, `progress`, `total?`, `message?`.
- `progress` **MUST aumentare** a ogni notifica (anche con total ignoto); valori MAY essere float.
- Solo token di richieste attive; notifiche MUST fermarsi dopo il completamento; rate limiting SHOULD.
- Il server può non inviarne affatto.

```json
{ "jsonrpc": "2.0", "method": "notifications/progress",
  "params": { "progressToken": "abc123", "progress": 50, "total": 100, "message": "Reticulating splines..." } }
```

### 5.2 Cancellation (`basic/patterns/cancellation.md`)
- **Streamable HTTP**: chiudere lo stream SSE della risposta **è** la cancellazione; il server MUST trattare la disconnessione come cancel; nessun `notifications/cancelled` atteso.
- **stdio**: il client MUST inviare `notifications/cancelled` `{requestId, reason?}`.
- Il server SHOULD smettere di lavorare, liberare risorse, **non** inviare risposta; MAY ignorare se richiesta ignota/completata/non cancellabile.
- Il client SHOULD ignorare risposte arrivate dopo la cancellazione. Race condition da gestire.
- Notifiche di cancel invalide → ignorare (fire-and-forget).
- **Timeouts**: SHOULD per tutte le richieste; allo scadere cancellare (chiudere stream / inviare cancelled). MAY resettare il timer su progress, ma SHOULD esserci un **timeout massimo** assoluto. SDK SHOULD permettere timeout per richiesta.

### 5.3 Rimossi nella 2026-07-28
`ping` (rimosso), `logging/setLevel` (sostituito da `_meta.logLevel` per richiesta), `notifications/roots/list_changed`, `notifications/initialized`, `initialize`.

---

## 6. Primitive server (Protocol Primitives)

### 6.1 Gerarchia di controllo (`server/index.md`)
| Primitiva | Controllo | Esempio |
|---|---|---|
| **Prompts** | **User-controlled** | slash command, voci di menu |
| **Resources** | **Application-controlled** | contenuti di file, git history |
| **Tools** | **Model-controlled** | POST verso API, scrittura file |

Client feature attiva: **Elicitation**. Deprecate: **Sampling**, **Roots** (client), **Logging** (server).
Utility: completion, pagination, caching; progress e cancellation sono pattern di base.

### 6.2 Tools (`server/tools.md`)
- Capability `tools: { listChanged?: boolean }`.
- **`tools/list`** (pagination + caching) → `tools[]`, `nextCursor?`, `ttlMs`, `cacheScope`. Ordine **deterministico** SHOULD (cache client e prompt cache LLM). La lista **MUST NOT** variare per connessione né come effetto collaterale di altre richieste; MAY variare per autorizzazione (scope).
- **`tools/call`** `{name, arguments}` → `CallToolResult` `{content[], structuredContent?, isError?}`; MAY rispondere `InputRequiredResult` (MRTR).
- **Tool definition**: `name`, `title?`, `description`, `icons?`, `inputSchema` (JSON Schema object, `type: "object"` alla radice, MUST non essere `null`; default dialect 2020-12; ora **qualsiasi keyword 2020-12** inclusi `oneOf/anyOf/allOf/not`, `if/then/else`, `$ref/$defs`), `outputSchema?` (qualsiasi JSON Schema 2020-12, anche array), `annotations?`, `_meta?`.
  - Tool senza parametri: `{ "type": "object", "additionalProperties": false }` (**raccomandato**) o `{ "type": "object" }`.
  - Display name: `title` → `annotations.title` → `name`.
- **Nomi** (SHOULD): 1–128 caratteri, case-sensitive, solo `A-Z a-z 0-9 _ - .`, niente spazi/virgole, unici nel server. Esempi: `getUser`, `DATA_EXPORT_v2`, `admin.tools.list`. Collisioni tra server: il client/proxy SHOULD disambiguare (prefisso server); `serverInfo.name` non è garantito unico.
- **Content types** del risultato: `text`, `image` (base64 + mimeType), `audio`, `resource_link` (non garantito in `resources/list`), `resource` (embedded; server SHOULD avere capability `resources`). Tutti con annotations (`audience`, `priority`, `lastModified`).
- **`structuredContent`**: **qualsiasi valore JSON** (novità: prima solo oggetto). Con `outputSchema` il server **MUST** conformarsi e il client **SHOULD** validare. Per retrocompatibilità SHOULD anche includere il JSON serializzato in un `TextContent`. Non c'entra con gli "structured outputs" degli LLM.
- **`x-mcp-header`** (vedi dominio 2): rispecchia parametri primitivi in header `Mcp-Param-{name}`.
- **Stateful tools** (non normativo): niente sessione ⇒ handle espliciti (`create_basket` → `basket_id`), autorizzazione verificata a ogni chiamata, handle opachi, durata dichiarata nella description, errore di tool su handle scaduto.
- **Annotations**: `readOnlyHint` (default false), `destructiveHint` (default true; significativo se non read-only), `idempotentHint` (default false), `openWorldHint` (default true), `title`. Untrusted salvo server fidati.

#### Tool Invocation Lifecycle
```
Discovery: tools/list (+cache ttlMs/cacheScope)
  → selezione da parte dell'LLM (model-controlled)
  → consenso/conferma utente (human in the loop, mostra input)
  → tools/call (+ _meta, header Mcp-Method/Mcp-Name/Mcp-Param-* su HTTP)
  → [opzionale] notifications/progress / notifications/message sullo stream della richiesta
  → [opzionale] InputRequiredResult → raccolta input → retry con nuovo id
  → CallToolResult (content / structuredContent / isError) o errore JSON-RPC
  → client valida e passa il risultato all'LLM; log per audit
Aggiornamenti: subscriptions/listen {toolsListChanged:true} → notifications/tools/list_changed → invalida cache → tools/list
Lunga durata: estensione Tasks (resultType "task", tasks/get, tasks/update, tasks/cancel)
```

### 6.3 Resources (`server/resources.md`)
- Capability `resources: { subscribe?: boolean, listChanged?: boolean }` (indipendenti, anche `{}`).
- `resources/list` (pagination+caching), `resources/read` (caching; MAY MRTR; MAY restituire più `contents`, es. directory), `resources/templates/list` (URI template **RFC 6570**, pagination+caching).
- Contenuto: `text` oppure `blob` (base64). Resource: `uri`, `name`, `title?`, `description?`, `icons?`, `mimeType?`, `size?`.
- Annotations: `audience` (`"user"`, `"assistant"`), `priority` 0.0–1.0 (1 = di fatto richiesto), `lastModified` ISO 8601.
- URI scheme: `https://` (solo se il client può fare fetch da sé), `file://` (anche non fisico; `inode/directory`), `git://`, custom conformi RFC 3986.
- Notifiche: `notifications/resources/list_changed`, `notifications/resources/updated` (via `resourceSubscriptions`).
- Errori: risorsa inesistente → **`-32602`** (prima `-32002`, client SHOULD accettare ancora `-32002`); interno → `-32603`; **MUST NOT** restituire `contents: []` per risorsa inesistente.

### 6.4 Prompts (`server/prompts.md`)
- Capability `prompts: { listChanged?: boolean }`.
- `prompts/list` (pagination+caching), `prompts/get` `{name, arguments}` → `{description?, messages[]}`; MAY MRTR.
- `PromptMessage`: `role` `"user"`|`"assistant"` + content (text, image, audio, resource_link, resource).
- Argomenti completabili via `completion/complete`.
- Errori: nome invalido / argomenti mancanti → `-32602`; interno → `-32603`.
- "User-controlled" = chi decide **quando** usarlo, non chi scrive il contenuto (che è del server).

### 6.5 Utility
- **Completion** (`completion/complete`): capability `completions`; `ref` = `ref/prompt` {name} o `ref/resource` {uri}; `argument {name, value}`; `context.arguments` per argomenti già risolti; risultato `{values (max 100), total?, hasMore?}`. Client SHOULD debounce; server SHOULD rate limit.
- **Pagination**: cursore **opaco**, page size decisa dal server; `nextCursor` assente = fine; stringa vuota è un cursore valido (non è la fine!); cursore invalido → `-32602`. Su `resources/list`, `resources/templates/list`, `prompts/list`, `tools/list`.
- **Caching** (`server/utilities/caching.md`, SEP-2549): `ttlMs` (intero ≥ 0, come `Cache-Control: max-age`) + `cacheScope` (`"public"`/`"private"`) **MUST** su result `complete` di `server/discover`, `tools/list`, `prompts/list`, `resources/list`, `resources/templates/list`, `resources/read`. `ttlMs` 0 = subito stale; assente ⇒ 0; negativo ⇒ 0. Fresh se `now < t_received + ttlMs`. TTL **non** è un intervallo di polling (se si fa polling: jitter + backoff MUST). Notifica `list_changed` invalida la cache. Ogni pagina è cacheabile indipendentemente; stesso `cacheScope` su tutte le pagine; cursore invalido → scartare tutte le pagine. Chiave di cache = metodo + parametri rilevanti.

### 6.6 Client feature: Elicitation (`client/elicitation.md`)
- Capability nel `_meta` di ogni richiesta: `elicitation: { form: {}, url: {} }`; `elicitation: {}` ≡ solo form. Almeno una modalità.
- Arriva **dentro** `InputRequiredResult.inputRequests` come `elicitation/create`; la risposta torna in `inputResponses`.
- Parametri: `mode` (`form` default se omesso | `url`), `message`.
- **Form**: `requestedSchema` = oggetto **piatto** di primitive (string con `format` email/uri/date/date-time, number/integer, boolean, enum single/multi-select con o senza `title` via `oneOf`/`anyOf` + `const`); `default` supportato.
- **URL**: `url`; `accept` significa solo consenso a aprire l'URL, non completamento; l'esito lo scopre il server al retry (via `requestState`).
- Risposte: `accept` (con `content` per form), `decline`, `cancel`.
- Rimossi nella 2026-07-28: `elicitationId`, `notifications/elicitation/complete`, errore `-32042`.

### 6.7 Client feature deprecate (funzionano ancora, via MRTR)
- **Sampling** (`sampling/createMessage`): `messages`, `modelPreferences` (`hints`, `costPriority`, `speedPriority`, `intelligencePriority` 0–1), `systemPrompt`, `maxTokens` (client MUST rispettarlo), `tools` + `toolChoice` (`auto` default / `required` / `none`, richiede capability `sampling.tools`), `includeContext` (`thisServer`/`allServers` deprecati → `none`). Tool result message contiene solo `tool_result`. Migrazione: chiamare direttamente le API dei provider LLM.
- **Roots** (`roots/list`): URI **`file://`**. Migrazione: passare directory/file via parametri dei tool, URI di resource o configurazione.

---

## 7. Error Handling — tabella completa

### 7.1 Codici
| Codice | Nome | Quando |
|---|---|---|
| `-32700` | Parse error | JSON non valido |
| `-32600` | Invalid Request | |
| `-32601` | Method not found | metodo non implementato (su HTTP → **404** + body JSON-RPC); capability non supportata (es. completion) |
| `-32602` | Invalid params | **tool sconosciuto**, `_meta` obbligatori mancanti, **risorsa non trovata** (nuovo), prompt invalido/argomenti mancanti, cursore invalido, logLevel invalido |
| `-32603` | Internal error | errori interni |
| `-32000…-32019` | legacy | non allocare nuovi codici; non assumere significati (eccetto -32002) |
| `-32020` | **HeaderMismatch** | header HTTP ≠ body o header obbligatori mancanti/malformati (HTTP 400) |
| `-32021` | **MissingRequiredClientCapability** | serve una capability non dichiarata; `data.requiredCapabilities` (HTTP 400) |
| `-32022` | **UnsupportedProtocolVersion** | versione non supportata; `data.supported[]`, `data.requested` (HTTP 400) |
| `-32020…-32099` | riservati alla spec MCP | non emettere codici non definiti |
| `-32002` | (ex) resource not found | **non emettere** più; client SHOULD accettarlo da server vecchi |
| `-32042` | (ex) URL elicitation required (solo 2025-11-25) | **non emettere** |

Rinumerazioni avvenute durante il draft: HeaderMismatch `-32001→-32020`, MissingRequiredClientCapability `-32003→-32021`, UnsupportedProtocolVersion `-32004→-32022`.
Codici applicativi nuovi → fuori dal range riservato JSON-RPC (-32768…-32000). Errori puramente locali (timeout SDK) non hanno codici e non devono essere confusi con errori del peer.

### 7.2 Protocol error vs Tool execution error (domanda classica)
| | Protocol Error | Tool Execution Error |
|---|---|---|
| Forma | JSON-RPC `error` | `result` con `isError: true` (resultType `complete`) |
| Casi | tool sconosciuto, richiesta malformata (non rispetta `CallToolRequest`), errori server | **errori di validazione dell'input** (data nel formato sbagliato, valore fuori range — SEP-1303), errori API, errori di business logic, handle scaduto |
| Verso l'LLM | client MAY passarli (meno utili) | client **SHOULD** passarli → **self-correction** |

### 7.3 Status HTTP da ricordare
| Status | Caso |
|---|---|
| 200 | risposta JSON o SSE |
| 202 Accepted (no body) | notifica accettata |
| 400 | `_meta` mancanti, HeaderMismatch, UnsupportedProtocolVersion, MissingRequiredClientCapability, authorization request malformata |
| 401 | token mancante/invalido/scaduto (+ `WWW-Authenticate`) |
| 403 | `Origin` invalido; scope insufficienti (`insufficient_scope`) |
| 404 | metodo non implementato (con body `-32601`); su legacy HTTP+SSE senza body JSON-RPC = indizio di server vecchio |
| 405 | GET/DELETE sull'endpoint MCP di un server solo-2026-07-28 |

---

## 8. Response handling — riepilogo per il client
1. Leggi `resultType` (assente ⇒ `complete`; sconosciuto ⇒ invalido).
2. `complete` → usa il result; per liste salva in cache secondo `ttlMs`/`cacheScope`; segui `nextCursor`.
3. `input_required` → soddisfa `inputRequests` (solo tipi per cui hai dichiarato capability) → retry con nuovo `id`, `inputResponses`, `requestState` identico; **non** cache.
4. `task` (estensione Tasks) → `tasks/get` polling, `tasks/update` per input, `tasks/cancel`.
5. Errore JSON-RPC → `-32022` ⇒ scegli versione da `supported` e riprova; `-32021` ⇒ dichiara la capability; `-32020` ⇒ correggi header (eventualmente rileggi `tools/list` per `x-mcp-header`); `-32602` ⇒ parametri/risorsa.
6. Tool con `isError: true` → passa il messaggio all'LLM per correggersi.
7. Stream interrotto (HTTP) → la richiesta è persa: **ri-emettere con nuovo id** (niente resumability, niente `Last-Event-ID`).

---

## 9. Estensione Tasks (`sources/extensions/tasks/overview.md`, SEP-2663)
- ID `io.modelcontextprotocol/tasks`; stage **Beta, verso Core**. Era "experimental core" nella 2025-11-25.
- Il server decide **per richiesta** se creare un task (nessun opt-in per richiesta: basta la capability dell'estensione).
- `CreateTaskResult` (`resultType: "task"`): `taskId`, stato iniziale, TTL, intervallo di polling suggerito.
- Stati: `working`, `input_required`, `completed`, `failed`, `cancelled`.
- `tasks/get` (polling; nei terminali porta `result` o `error`), `tasks/update` (risposte a `inputRequests` mid-flight), `tasks/cancel` (cooperativo).
- Rimossi rispetto alla 2025-11-25: `tasks/result` bloccante e `tasks/list`.
- Vantaggi: niente connessioni lunghe, resilienza ai crash (handle durevole), visibilità del progresso.

---

## 10. Differenze con le versioni precedenti (dominio 3)
| Tema | ≤ 2025-11-25 | 2026-07-28 |
|---|---|---|
| Avvio | `initialize` → risposta con capabilities/versione → `notifications/initialized` | nessun handshake; `_meta` in ogni richiesta; `server/discover` opzionale per il client (obbligatorio da implementare per il server) |
| Server → client | richieste JSON-RPC server-initiated (`sampling/createMessage`, `elicitation/create`, `roots/list`) | **MRTR** con `InputRequiredResult` |
| Risultati | nessun `resultType` | `resultType` obbligatorio |
| Notifiche di cambiamento | `resources/subscribe`/`unsubscribe`, stream GET | `subscriptions/listen` con filtro e ack |
| Log level | `logging/setLevel` (connessione) | `_meta.logLevel` per richiesta; senza → niente `notifications/message` |
| Liveness | `ping` | rimosso |
| Cancellation | `notifications/cancelled` su tutti i transport | HTTP: chiusura stream; stdio: `notifications/cancelled` |
| Risorsa non trovata | `-32002` | `-32602` |
| Tasks | core experimental (2025-11-25) con `tasks/result`, `tasks/list` | estensione, polling `tasks/get`, `tasks/update` |
| Caching | assente | `ttlMs`/`cacheScope` obbligatori sulle liste |
| `structuredContent` | oggetto | qualsiasi JSON |
| Validazione input | 2025-11-25: chiarito che sono Tool Execution Errors | invariato |
