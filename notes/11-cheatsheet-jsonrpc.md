# Cheat sheet — metodi, notifiche, errori, header, `_meta` (spec 2026-07-28)

## Metodi (request, tutti client → server)
| Metodo | Capability server | Pagination | Caching | MRTR | Note |
|---|---|---|---|---|---|
| `server/discover` | (sempre, MUST) | — | ✔ | ✘ | `supportedVersions`, `capabilities`, `serverInfo`, `instructions` |
| `tools/list` | `tools` | ✔ | ✔ | ✘ | ordine deterministico SHOULD |
| `tools/call` | `tools` | — | ✘ | ✔ | header `Mcp-Name` = nome tool |
| `resources/list` | `resources` | ✔ | ✔ | ✘ | |
| `resources/templates/list` | `resources` | ✔ | ✔ | ✘ | URI template RFC 6570 |
| `resources/read` | `resources` | — | ✔ | ✔ | `Mcp-Name` = URI; non trovata → `-32602` |
| `prompts/list` | `prompts` | ✔ | ✔ | ✘ | |
| `prompts/get` | `prompts` | — | ✘ | ✔ | `Mcp-Name` = nome prompt |
| `completion/complete` | `completions` | — | ✘ | ✘ | max 100 valori |
| `subscriptions/listen` | (liste/`subscribe`) | — | ✘ | ✘ | stream long-lived |
| `tasks/get`, `tasks/update`, `tasks/cancel` | estensione `io.modelcontextprotocol/tasks` | | | | |

Richieste **annidate in `inputRequests`** (non inviate come JSON-RPC indipendenti): `elicitation/create`, `sampling/createMessage` *(deprecato)*, `roots/list` *(deprecato)*.

## Notifiche
| Notifica | Direzione | Dove viaggia |
|---|---|---|
| `notifications/cancelled` | client→server (stdio); server→client solo per chiudere una `subscriptions/listen` | stdio |
| `notifications/progress` | server→client | stream della richiesta |
| `notifications/message` *(logging deprecato)* | server→client | stream della richiesta, solo se `_meta.logLevel` |
| `notifications/subscriptions/acknowledged` | server→client | stream di listen (primo messaggio) |
| `notifications/tools/list_changed` | server→client | stream di listen |
| `notifications/prompts/list_changed` | server→client | stream di listen |
| `notifications/resources/list_changed` | server→client | stream di listen |
| `notifications/resources/updated` | server→client | stream di listen (`resourceSubscriptions`) |

## Codici d'errore
`-32700` parse · `-32600` invalid request · `-32601` method not found (HTTP 404) · `-32602` invalid params (anche resource not found, `_meta` mancanti, tool sconosciuto, cursore invalido) · `-32603` internal · `-32020` HeaderMismatch · `-32021` MissingRequiredClientCapability (`data.requiredCapabilities`) · `-32022` UnsupportedProtocolVersion (`data.supported`, `data.requested`) · legacy `-32000..-32019` · riservati spec `-32020..-32099` · non più emessi: `-32002`, `-32042`.

## `_meta` riservati
`progressToken` · `io.modelcontextprotocol/protocolVersion` (req, obbl.) · `io.modelcontextprotocol/clientCapabilities` (req, obbl.) · `io.modelcontextprotocol/clientInfo` (req, SHOULD) · `io.modelcontextprotocol/logLevel` (req, opz.) · `io.modelcontextprotocol/serverInfo` (result, SHOULD) · `io.modelcontextprotocol/subscriptionId` (notifiche di listen, MUST) · `traceparent`, `tracestate`, `baggage` (OTel).
Prefissi riservati: secondo label = `modelcontextprotocol` o `mcp`.

## Header Streamable HTTP
`Accept: application/json, text/event-stream` · `Content-Type: application/json` · `MCP-Protocol-Version` (ogni POST) · `Mcp-Method` (tutte le richieste) · `Mcp-Name` (`tools/call`, `resources/read`, `prompts/get`) · `Mcp-Param-{Name}` (`x-mcp-header`) · `Authorization: Bearer <token>` · risposta SSE: `X-Accel-Buffering: no` · 401: `WWW-Authenticate: Bearer resource_metadata="…", scope="…"` · 403: `error="insufficient_scope"`. Sentinella Base64: `=?base64?…?=`.
**Non più usati**: `Mcp-Session-Id`, `Last-Event-ID`.

## HTTP status
200 (JSON/SSE) · 202 (notifica accettata) · 400 (`_meta` mancanti, header mismatch, versione, capability, auth request malformata) · 401 (token) · 403 (Origin invalido, scope) · 404 (metodo, con `-32601`) · 405 (GET/DELETE).

## Capability
Client: `elicitation {form, url}`, `sampling {context, tools}`*, `roots`*, `experimental`, `extensions` (*deprecate).
Server: `tools {listChanged}`, `resources {subscribe, listChanged}`, `prompts {listChanged}`, `completions`, `logging`*, `experimental`, `extensions`.

## Well-known URI
- PRM (RFC 9728): `/.well-known/oauth-protected-resource[/<path MCP>]` (prima path-specific, poi root)
- AS (RFC 8414): `/.well-known/oauth-authorization-server[/<path issuer>]`
- OIDC: `/.well-known/openid-configuration` (path insertion poi path appending)

## Metadata OAuth da ricordare
PRM: `resource`, `authorization_servers` (≥1), `scopes_supported`.
AS: `issuer`, `authorization_endpoint`, `token_endpoint`, `registration_endpoint` (DCR), `code_challenge_methods_supported` (assente ⇒ niente PKCE ⇒ stop), `client_id_metadata_document_supported` (CIMD), `authorization_response_iss_parameter_supported` (RFC 9207), `scopes_supported`.
CIMD: `client_id` (= URL), `client_name`, `redirect_uris` (obbligatori), `grant_types`, `response_types`, `token_endpoint_auth_method`.

## Numeri da ricordare
- Nomi tool: 1–128 caratteri, `[A-Za-z0-9_.-]`.
- Completion: max 100 valori.
- Priority annotation: 0.0–1.0.
- Sampling priorities: 0–1.
- `ttlMs` ≥ 0 (ms); assente o negativo ⇒ 0.
- `x-mcp-header` integer: ±(2^53 − 1).
- Deprecazione: ≥ 12 mesi (expedited ≥ 90 giorni).
- SDK conformance: Tier 1 100%, Tier 2 80%.
- Progressive discovery: soglia 1–5% della context window.
- Esame: 5 domini, 16/14/26/24/20%; 90 minuti (pagina LF).
