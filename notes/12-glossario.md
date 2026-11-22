# Glossario (IT/EN) — termini MCP 2026-07-28

| Termine | Significato |
|---|---|
| **AAIF** | Agentic AI Foundation, directed fund della Linux Foundation che ospita MCP (da dic 2025) e rilascia l'esame MCPA |
| **Annotations** (content) | `audience`, `priority`, `lastModified` su resources e content block |
| **Annotations** (tool) | hint `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`, `title`; untrusted salvo server fidati |
| **Authorization server (AS)** | emette i token OAuth; può essere separato dal server MCP |
| **Cache scope** | `cacheScope`: `public` (condivisibile tra utenti) o `private` (stesso contesto di autorizzazione) |
| **Capability** | feature dichiarata: client nel `_meta` di ogni richiesta, server in `server/discover` |
| **CIMD** | Client ID Metadata Document: `client_id` = URL HTTPS di un JSON di metadata; registrazione raccomandata |
| **Client** | componente dell'host connesso a un solo server |
| **Confused deputy** | attacco a proxy MCP con client ID statico + consent cookie; mitigazione: consenso per-client |
| **DCR** | Dynamic Client Registration (RFC 7591), deprecata nella 2026-07-28 |
| **Dual-era** | implementazione che supporta sia versioni legacy (initialize) sia modern |
| **Elicitation** | richiesta del server di input all'utente; modalità `form` e `url`; via MRTR |
| **EMA** | Enterprise-Managed Authorization (estensione), IdP aziendale + ID-JAG |
| **Extension** | funzionalità opzionale fuori dal core, ID `{vendor-prefix}/{name}`, negoziata in `capabilities.extensions` |
| **Handle (state handle)** | identificatore esplicito di stato applicativo passato come argomento dei tool |
| **Host** | applicazione AI che gestisce i client, il consenso e il contesto |
| **ID-JAG** | Identity Assertion JWT Authorization Grant (EMA) |
| **InputRequiredResult** | risultato `resultType: "input_required"` con `inputRequests` e/o `requestState` |
| **Legacy / Modern** | ≤ 2025-11-25 (handshake) / ≥ 2026-07-28 (metadata per richiesta) |
| **listChanged** | sub-capability: il server notifica cambi della lista |
| **MCP Apps** | estensione `io.modelcontextprotocol/ui`: UI HTML in iframe sandbox |
| **MCP endpoint** | unico path HTTP (POST) del transport Streamable HTTP |
| **MCP Inspector** | tool di riferimento per test/debug (web, CLI, TUI) |
| **Mix-up attack** | un AS malevolo si fa consegnare code/token di un AS onesto; mitigazione `iss` (RFC 9207) |
| **MRTR** | Multi Round-Trip Requests: il server chiede input con `InputRequiredResult`, il client riprova |
| **PKCE** | Proof Key for Code Exchange; obbligatorio, metodo `S256` |
| **PRM** | Protected Resource Metadata (RFC 9728), pubblicato dal server MCP |
| **Primitive** | tools, resources, prompts (server); elicitation (client) |
| **Progressive discovery** | caricare le definizioni dei tool su richiesta tramite meta-tool di ricerca |
| **Registry** | registro ufficiale di metadata dei server pubblici (`server.json`) |
| **requestState** | stringa opaca del server nel MRTR, attacker-controlled, da proteggere (HMAC/AEAD) |
| **Resource indicator** | parametro `resource` (RFC 8707) = canonical URI del server MCP |
| **Resource template** | resource parametrica con URI template (RFC 6570) |
| **resultType** | `complete` / `input_required` (/ `task` con estensione) |
| **SEP** | Specification Enhancement Proposal |
| **Server** | programma che espone contesto; locale (stdio) o remoto (HTTP) |
| **Step-up authorization** | nuova autorizzazione con l'unione degli scope dopo un `insufficient_scope` |
| **Streamable HTTP** | transport HTTP POST + SSE per richiesta (dal 2025-03-26) |
| **structuredContent** | output strutturato del tool, qualsiasi valore JSON, conforme a `outputSchema` |
| **Subscription** | stream aperto con `subscriptions/listen`, identificato dall'id della richiesta |
| **Token passthrough** | anti-pattern vietato: inoltrare a valle token non emessi per il server |
| **ttlMs** | freshness hint in millisecondi (come `max-age`) |
| **x-mcp-header** | annotazione di una proprietà dell'`inputSchema` per rispecchiarla in `Mcp-Param-{name}` |
