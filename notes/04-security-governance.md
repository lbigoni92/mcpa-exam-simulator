# Dominio 4 — Security & Governance (24%)

> Competenze ufficiali LF: **Trust Boundaries · Permissions & Consent · Risk & Safety Controls · Auditability & Observability**
> Spec di riferimento: MCP `2026-07-28`. Fonti locali in `sources/` (percorsi indicati in ogni sezione).
> Questo è il dominio con più profondità: OAuth 2.1, discovery, registrazione client, token handling, attacchi noti.

---

## 0. Mappa rapida (cosa chiede l'esame, cosa dice la spec)

| Competenza | Dove sta nella spec / docs |
|---|---|
| Trust Boundaries | `spec/index.md` (Security and Trust & Safety), `architecture/index.md` (principio 3), auth `security-considerations.md`, `docs/tutorials/security/security_best_practices.md` (token passthrough, confused deputy) |
| Permissions & Consent | `index.md` Key Principles, `server/tools.md` (human in the loop), `client/elicitation.md`, auth scope / step-up, best practices (per-client consent, one-click local server consent) |
| Risk & Safety Controls | best practices (SSRF, session/state hijacking, local server compromise, URL validation), `basic/index.md` ($ref, icons), MRTR `requestState` integrity, `server/utilities/caching.md` (cacheScope) |
| Auditability & Observability | `tools.md` (log tool usage), `basic/index.md` (OpenTelemetry `traceparent`/`tracestate`/`baggage`), logging deprecato → stderr / OpenTelemetry, token passthrough → audit trail |

---

## 1. Principi di sicurezza della spec (spec `index.md` §Security and Trust & Safety)

MCP **non può imporre** la sicurezza a livello di protocollo: la responsabilità è degli implementatori (host/client/server). I tre principi chiave:

1. **User Consent and Control** – l'utente deve acconsentire esplicitamente e capire ogni accesso ai dati e ogni operazione; deve mantenere il controllo su cosa viene condiviso e su quali azioni vengono eseguite; servono UI chiare per revisionare/autorizzare.
2. **Data Privacy** – l'host deve ottenere consenso esplicito **prima** di esporre dati utente ai server; non deve trasmettere i dati delle resources altrove senza consenso; access control appropriati.
3. **Tool Safety** – i tool sono **esecuzione arbitraria di codice**; le descrizioni del comportamento dei tool (es. **annotations**) vanno considerate **untrusted** salvo che provengano da un server fidato; l'host deve ottenere consenso esplicito prima di invocare qualsiasi tool.

Implementation guidelines (SHOULD): flussi di consenso/autorizzazione robusti, documentazione delle implicazioni di sicurezza, access control e data protection, best practice, privacy by design.

### Trust boundaries architetturali (`architecture/index.md`)
- L'**host** applica policy di sicurezza e requisiti di consenso, gestisce le decisioni di autorizzazione dell'utente, coordina l'integrazione LLM e aggrega il contesto.
- Ogni **client** ha relazione **1:1** con un server e "mantiene i confini di sicurezza tra server".
- Design principle 3: *i server non devono poter leggere l'intera conversazione né "vedere dentro" altri server*. Ricevono solo il contesto necessario; la cronologia completa resta all'host; le interazioni cross-server sono controllate dall'host.
- `clientInfo` / `serverInfo` sono **self-reported, non verificati**: SHOULD NOT essere usati per decisioni di sicurezza né per cambiare comportamento.

---

## 2. Authorization — quadro generale (`basic/authorization/index.md`)

### 2.1 Ambito
- L'autorizzazione è **OPTIONAL** in MCP.
- Transport HTTP → **SHOULD** conformarsi alla spec di autorizzazione.
- **STDIO → SHOULD NOT** seguire questa spec: le credenziali si prendono **dall'ambiente** (env vars, config).
- Transport alternativi → MUST seguire le best practice del proprio protocollo.
- Client e server MAY negoziare strategie custom.
- L'autorizzazione opera **a livello di transport** (HTTP), non dentro i messaggi JSON-RPC.

### 2.2 Standard su cui si basa (memorizzare!)
| Standard | A cosa serve in MCP |
|---|---|
| **OAuth 2.1** (draft-ietf-oauth-v2-1-13) | Base: authorization code + **PKCE** obbligatorio, niente implicit grant, bearer token |
| **RFC 6750** Bearer Token Usage | Header `Authorization: Bearer`, `WWW-Authenticate`, `error="insufficient_scope"` |
| **RFC 8414** Authorization Server Metadata | Discovery dell'AS (`/.well-known/oauth-authorization-server`) |
| **RFC 7591** Dynamic Client Registration (DCR) | Registrazione dinamica — **deprecata nella 2026-07-28** |
| **RFC 8707** Resource Indicators | Parametro `resource` → audience binding del token |
| **RFC 9728** Protected Resource Metadata (PRM) | Il server MCP indica il suo AS (`/.well-known/oauth-protected-resource`) |
| **RFC 9207** AS Issuer Identification | Parametro `iss` nella authorization response → anti **mix-up** (novità 2026-07-28) |
| **Client ID Metadata Documents (CIMD)** draft-ietf-oauth-client-id-metadata-document-00 | `client_id` = URL HTTPS di un documento JSON — meccanismo raccomandato |
| **OpenID Connect Discovery 1.0** | Alternativa a RFC 8414 (`/.well-known/openid-configuration`) |
| **OIDC Dynamic Client Registration 1.0** | `application_type` (native/web) durante DCR |

### 2.3 Ruoli
- **MCP server** = OAuth 2.1 **resource server** (accetta richieste con access token).
- **MCP client** = OAuth 2.1 **client** (agisce per conto del resource owner).
- **Authorization server (AS)** = interagisce con l'utente ed emette i token. Può essere co-ospitato col resource server o separato; i dettagli implementativi sono fuori scope.

### 2.4 Requisiti di sintesi (§Overview)
1. AS **MUST** implementare OAuth 2.1 per client confidential e public.
2. AS e client **SHOULD** supportare **CIMD**.
3. AS e client **MAY** supportare **DCR** (RFC 7591) — deprecata, solo per retrocompatibilità.
4. Server MCP **MUST** implementare **RFC 9728 (PRM)**; client **MUST** usare PRM per la discovery dell'AS.
5. AS **MUST** offrire almeno uno tra RFC 8414 e OIDC Discovery; i client **MUST** supportarli **entrambi**.

---

## 3. Flusso completo di autorizzazione (sequenza da sapere a memoria)

```
1. Client → MCP server: richiesta senza token
2. MCP server → 401 Unauthorized + WWW-Authenticate: Bearer resource_metadata="…", scope="…"
3. Client → GET Protected Resource Metadata (RFC 9728) → ottiene authorization_servers
4. Client sceglie l'AS → GET AS metadata (RFC 8414 / OIDC Discovery, endpoint in ordine di priorità)
5. Registrazione: pre-registrato | CIMD | DCR
6. Client genera PKCE (S256), include `resource`, applica la scope selection strategy,
   REGISTRA l'issuer atteso insieme al code_verifier (e state)
7. Browser → AS: authorization request (+ code_challenge + resource)
8. Utente autorizza → redirect al callback con `code` + `iss`
9. Client valida `iss` contro l'issuer registrato (RFC 9207) PRIMA di riscattare il code
10. Client → AS token endpoint: code + code_verifier + resource → access token (+ refresh token)
11. Client → MCP server: richieste con Authorization: Bearer <token> (in OGNI richiesta HTTP)
```

### 3.1 Discovery del Protected Resource Metadata (`authorization-server-discovery.md`)
Il server **MUST** implementare almeno uno di:
1. **`WWW-Authenticate`** con `resource_metadata` nella risposta 401 (RFC 9728 §5.1);
2. **Well-known URI**:
   - con path dell'endpoint: `https://example.com/public/mcp` → `https://example.com/.well-known/oauth-protected-resource/public/mcp`
   - alla root: `https://example.com/.well-known/oauth-protected-resource`

Il client **MUST** supportare entrambi: usa l'URL dall'header se presente, altrimenti prova i well-known **nell'ordine sopra** (prima path-specific, poi root).
Il documento PRM **MUST** includere `authorization_servers` con almeno un AS. Se ce ne sono più di uno, la scelta spetta al **client** (RFC 9728 §7.6); ogni AS è indipendente: registrazioni/credenziali/token separati per AS.

### 3.2 Discovery dell'Authorization Server Metadata
MCP usa il suffisso standard `oauth-authorization-server` (RFC 8414 §3.1), **nessun suffisso MCP-specifico**.

Issuer **con path** (`https://auth.example.com/tenant1`) — ordine obbligatorio:
1. `https://auth.example.com/.well-known/oauth-authorization-server/tenant1` (OAuth, path insertion)
2. `https://auth.example.com/.well-known/openid-configuration/tenant1` (OIDC, path insertion)
3. `https://auth.example.com/tenant1/.well-known/openid-configuration` (OIDC, path appending)

Issuer **senza path** (`https://auth.example.com`):
1. `/.well-known/oauth-authorization-server`
2. `/.well-known/openid-configuration`

**Validazione del metadata**: il campo `issuer` del documento **MUST** essere identico all'issuer usato per costruire l'URL well-known, altrimenti il documento **MUST NOT** essere usato (es. documento da `attacker.example` con `"issuer":"https://honest.example"` → rifiutato).

### 3.3 Scope Selection Strategy
- Il server **SHOULD** indicare `scope` nel `WWW-Authenticate` (RFC 6750 §3) → least privilege.
- Il set di scope della challenge **può** essere uguale, sottoinsieme, superinsieme o diverso da `scopes_supported`: il client **MUST NOT** assumere relazioni e **MUST** trattare gli scope della challenge come **autorevoli** per l'operazione corrente.
- Priorità per la richiesta iniziale (SHOULD):
  1. `scope` dall'header `WWW-Authenticate` della 401;
  2. altrimenti **tutti** gli scope di `scopes_supported` del PRM; se `scopes_supported` è assente → omettere `scope`.
- `scopes_supported` dovrebbe rappresentare il **set minimo** per la funzionalità base; gli altri scope si ottengono incrementalmente (step-up).

### 3.4 Validazione della authorization response — RFC 9207 (NOVITÀ 2026-07-28, SEP-2468)
- Prima del redirect, il client **MUST** registrare l'`issuer` dal metadata validato e associarlo allo stesso record del PKCE code_verifier (e `state`).
- AS **SHOULD** includere `iss` nelle authorization response (anche negli errori). Se lo fanno **MUST** pubblicizzarlo con `authorization_response_iss_parameter_supported: true`.
- Il client **MUST** validare **prima** di inviare il code a qualsiasi token endpoint:

| `authorization_response_iss_parameter_supported` | `iss` presente? | Azione client |
|---|---|---|
| `true` | sì | confronto stringa semplice con issuer registrato |
| `true` | **no** | **rifiuta** la risposta |
| `false`/assente | sì | confronto comunque (local policy RFC 9207 §2.4) |
| `false`/assente | no | procedi |

- Nessuna normalizzazione (case folding, porta di default, trailing slash, percent-encoding) prima del confronto.
- Su mismatch anche per risposte di errore: **MUST NOT** agire su/mostrare `error`, `error_description`, `error_uri`.
- Una revisione futura porterà `iss` da SHOULD a MUST per gli AS.

### 3.5 Resource Indicators — RFC 8707
- Il client **MUST** includere `resource` **sia** nella authorization request **sia** nella token request.
- Deve identificare il server MCP con il suo **canonical URI** (lowercase scheme/host preferito, ma accettare uppercase).
- **MUST** inviarlo **anche se l'AS non lo supporta**.
- Validi: `https://mcp.example.com/mcp`, `https://mcp.example.com`, `https://mcp.example.com:8443`, `https://mcp.example.com/server/mcp`.
- Non validi: `mcp.example.com` (manca lo scheme), `https://mcp.example.com#fragment` (fragment).
- Preferire la forma **senza trailing slash**.

### 3.6 Uso dell'access token
- Header `Authorization: Bearer <access-token>` (OAuth 2.1 §5.1.1) in **ogni** richiesta HTTP client→server (anche se fanno parte della stessa "operazione").
- **MUST NOT** mettere il token nella query string.
- Il server **MUST** validare il token (OAuth 2.1 §5.2) e verificare che sia stato emesso **per lui** come audience (RFC 8707). Token invalido/scaduto → **HTTP 401**.
- Il client **MUST NOT** inviare token che non siano stati emessi dall'AS del server MCP.
- Il server **MUST NOT accettare né far transitare** altri token (→ niente token passthrough).

### 3.7 Refresh token
Client:
- MUST tenere riservati i refresh token (transito e storage);
- SHOULD includere `refresh_token` nei `grant_types`;
- MAY aggiungere `offline_access` allo scope **se** presente in `scopes_supported` dell'AS;
- MUST NOT assumere che verranno emessi.
Server MCP: SHOULD NOT includere `offline_access` nel `WWW-Authenticate` o in `scopes_supported` del PRM (il refresh token non è un requisito della risorsa).
AS: per client **public** MUST **ruotare** i refresh token (OAuth 2.1 §4.3.1); SHOULD emettere access token **short-lived**.

### 3.8 Errori HTTP di autorizzazione
| Status | Uso |
|---|---|
| **401** Unauthorized | autorizzazione richiesta o token invalido/scaduto |
| **403** Forbidden | scope insufficienti / permessi insufficienti |
| **400** Bad Request | authorization request malformata |

### 3.9 Scope challenge a runtime e Step-Up
Risposta a token con scope insufficiente (SHOULD):
```http
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
                         scope="files:write",
                         resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         error_description="File write permission required for this operation"
```
- Il server include **tutti** gli scope necessari all'operazione in **una sola** challenge (non incrementalmente uno per volta). Non è obbligato a includere gli scope già concessi.
- L'**accumulo** degli scope è responsabilità del **client**: step-up = **unione** degli scope richiesti in precedenza + scope della challenge.
- Step-up: parse errore → calcolo unione → (ri)autorizzazione → retry **poche volte**, poi fallimento permanente. Retry limits e tracking dei tentativi (SHOULD).
- Client per conto utente: SHOULD tentare lo step-up. Client `client_credentials`: MAY tentare o abortire subito.
- Il server **MUST** tenere conto delle gerarchie di scope (uno scope ampio implica quelli più stretti).

---

## 4. Client Registration (`client-registration.md`)

Tre meccanismi:
| Meccanismo | Quando | Stato |
|---|---|---|
| **Client ID Metadata Documents (CIMD)** | nessuna relazione pregressa client↔server (caso più comune) | **SHOULD** (raccomandato) |
| **Pre-registration** | relazione esistente | SHOULD supportare credenziali statiche |
| **Dynamic Client Registration (DCR, RFC 7591)** | retrocompatibilità | **MAY, Deprecated** (PR #2858) |

**Ordine di priorità** per client che supportano tutto (SHOULD):
1. credenziali **pre-registrate** se disponibili;
2. **CIMD** se l'AS espone `client_id_metadata_document_supported: true`;
3. **DCR** se l'AS espone `registration_endpoint`;
4. chiedere all'utente di inserire le info client.

### 4.1 CIMD
- `client_id` = **URL HTTPS con path** (es. `https://example.com/client.json`) che punta a un JSON di metadata.
- Il documento **MUST** contenere almeno `client_id`, `client_name`, `redirect_uris`; `client_id` deve coincidere **esattamente** con l'URL.
- Client MAY usare `private_key_jwt` (con JWKS) per autenticarsi al token endpoint.
- AS: SHOULD fare fetch su `client_id` in formato URL; MUST validare che `client_id` del documento = URL; SHOULD cache rispettando HTTP cache headers; MUST validare i redirect URI rispetto al documento; MUST validare JSON e campi richiesti.
- Esempio: `{"client_id":"https://app.example.com/oauth/client-metadata.json","client_name":"Example MCP Client","redirect_uris":["http://127.0.0.1:3000/callback"],"grant_types":["authorization_code"],"response_types":["code"],"token_endpoint_auth_method":"none"}`
- I `client_id` CIMD sono **portabili** tra AS (nessuna ri-registrazione se l'AS cambia).

### 4.2 Pre-registration
Client ID (e secret) hardcodati per quell'AS, oppure UI in cui l'utente inserisce i dati dopo aver registrato da sé un client OAuth.

### 4.3 DCR (deprecata) e `application_type` (SEP-837, novità)
- I client **MUST** specificare `application_type` durante DCR: se omesso, sotto OIDC il default è `"web"`, che può confliggere con redirect URI nativi (`localhost`).
- `native` → desktop, mobile, CLI, web app locali su `localhost`; `web` → app browser servite da host non locale.
- Gestire i fallimenti di registrazione dovuti ai vincoli sui redirect URI (errore significativo, MAY riprovare).

### 4.4 Authorization Server Binding (SEP-2352, novità)
- Credenziali pre-registrate o ottenute con DCR **MUST** essere associate all'AS che le ha emesse, **chiavate per `issuer`**.
- Se l'AS cambia (PRM aggiornato): **MUST NOT** riusare le credenziali e **MUST** ri-registrarsi. Per credenziali pre-registrate: SHOULD mostrare un errore invece di provarle.
- I client ID sono unici per l'AS che li ha emessi (RFC 6749 §2.2).

---

## 5. Authorization Security Considerations (`security-considerations.md`)

| Minaccia | Mitigazione normativa |
|---|---|
| **Token audience** | client MUST inviare `resource`; server MUST validare che il token sia emesso per lui |
| **Token theft** | storage sicuro (OAuth 2.1 §7.1); AS SHOULD token short-lived; refresh rotation per public client (MUST) |
| **Communication security** | tutti gli endpoint AS su **HTTPS**; redirect URI **`localhost` o HTTPS** |
| **Authorization code interception/injection** | client MUST implementare **PKCE**, MUST usare **`S256`** quando tecnicamente possibile, MUST verificare il supporto PKCE prima di procedere: se `code_challenge_methods_supported` è **assente** nel metadata → **rifiutare di procedere** (vale anche per OIDC; gli AS OIDC MUST includere il campo) |
| **Mix-up attack** | validazione `iss` (RFC 9207). **PKCE da solo non basta** (il verifier finisce al token endpoint dell'attaccante) e i resource indicator non aiutano |
| **Open redirection** | redirect URI registrati; AS MUST validare redirect URI **esatti**; client SHOULD usare e verificare `state`; AS non deve redirigere verso URI non fidati |
| **CIMD: SSRF sull'AS** | l'AS che fa fetch del documento SHOULD considerare SSRF |
| **CIMD: localhost impersonation** | CIMD non prova quale processo ascolta su `localhost`: AS SHOULD mostrare warning per redirect solo-localhost, MAY richiedere attestation, MUST mostrare chiaramente l'hostname del redirect URI |
| **CIMD trust policy** | AS MAY applicare policy per dominio (allowlist, reputazione, età del dominio…) |
| **Confused deputy** | proxy MCP con client ID statico MUST ottenere consenso utente per ogni client registrato dinamicamente prima di inoltrare all'AS di terze parti |
| **Access token privilege restriction** | server MUST accettare solo token per sé (audience claim); verso API upstream il server è un OAuth client separato con token separato; **MUST NOT** passare il token ricevuto dal client |

---

## 6. Attacchi e mitigazioni — Security Best Practices (`docs/tutorials/security/security_best_practices.md`)

### 6.1 Confused Deputy
Scenario: **MCP proxy server** verso API di terze parti con **client ID statico** presso l'AS terzo + i client MCP si registrano dinamicamente + l'AS terzo imposta un **consent cookie** + nessun consenso per-client nel proxy. L'attaccante invia un link con `redirect_uri` malevolo e nuovo client_id: il cookie salta il consent screen e il code finisce all'attaccante.
Mitigazioni (MUST):
- **Consenso per-client**: registry dei `client_id` approvati per utente, controllato **prima** di avviare il flusso verso l'AS terzo.
- Consent UI: nome del client, scope dell'API terza, `redirect_uri`, protezione CSRF, anti-clickjacking (`frame-ancestors` / `X-Frame-Options: DENY`).
- Cookie di consenso: prefisso `__Host-`, `Secure`, `HttpOnly`, `SameSite=Lax`, firmati, legati al `client_id`.
- Redirect URI: match **esatto** (no wildcard), rifiutare cambi senza ri-registrazione.
- `state`: random crittografico, salvato server-side **solo dopo** il consenso, single-use, scadenza breve (es. 10 min), validato al callback.

### 6.2 Token Passthrough (anti-pattern esplicitamente vietato)
Il server accetta token non emessi per sé e li inoltra a valle. Rischi: aggiramento dei controlli (rate limit, validazione), **perdita di accountability e audit trail**, rottura dei trust boundary, rischio futuro. Mitigazione: il server **MUST NOT** accettare token non emessi esplicitamente per sé.

### 6.3 SSRF (lato client durante la OAuth discovery)
URL controllabili da un server malevolo: `resource_metadata`, `authorization_servers`, `token_endpoint`/`authorization_endpoint`… Target: IP interni, **169.254.169.254** (cloud metadata), localhost, DNS rebinding, redirect chain.
Mitigazioni (SHOULD): HTTPS obbligatorio (http solo loopback in dev), bloccare range privati (10/8, 172.16/12, 192.168/16, 127/8, ::1, 169.254/16, fc00::/7, fe80::/10) senza parser artigianali, validare i redirect hop, egress proxy (es. Smokescreen), attenzione al TOCTOU DNS (pinning). Vale anche per l'AS che fa fetch dei CIMD.

### 6.4 State Handle Hijacking (sostituisce "Session Hijacking" della 2025-11-25)
Senza sessioni di protocollo, lo stato si passa con **handle** espliciti (es. `basket_id`). Attacco: indovinare/rubare l'handle di un altro utente.
Mitigazioni: server con autorizzazione **MUST** verificare ogni richiesta e **MUST NOT** trattare il possesso di un handle come autenticazione; handle random sicuri, non sequenziali, con scadenza; **binding server-side** `<user_id>:<handle>` con user_id dal token verificato.

### 6.5 Local MCP Server Compromise
Rischi: comandi di avvio malevoli nella config, payload malevolo, server locale esposto via DNS rebinding.
Se il client supporta configurazione **one-click**: **MUST** mostrare il comando esatto completo (non troncato), segnalarlo come pericoloso, richiedere approvazione esplicita, permettere l'annullamento. SHOULD: evidenziare pattern pericolosi (`sudo`, `rm -rf`…), avvisare che i server girano con gli stessi privilegi del client, **sandbox** con privilegi minimi.
Server locali: preferire **stdio**; se HTTP → token di autorizzazione o unix socket/IPC con accesso ristretto.

### 6.5b Modello di minaccia dei server locali (`docs/tutorials/security/local-server-security.md`)
- **Nessun confine tra client e server stdio**: il server ha già esecuzione di codice sulla macchina perché viene lanciato. Gli SDK assumono **piena fiducia** tra peer stdio. Il transport stdio **non è una sandbox**: l'isolamento è responsabilità del host e di chi gestisce la macchina.
- Le decisioni di sicurezza vere avvengono **prima del lancio**: cosa installi (provenienza) e come lo esegui (isolamento).
- Il trust domain è **cumulativo**: tutti i server condividono lo stesso contesto del modello, quindi un server malevolo può influenzare l'uso dei tool di tutti gli altri.
- **5 minacce**:
  1. server malevolo (typosquatting, repository sosia, progetto abbandonato e rilevato da un nuovo publisher);
  2. server che raccoglie troppo (variabili d'ambiente, file, traffico), anche spinto da **prompt injection**;
  3. dipendenza compromessa (**supply chain**);
  4. **catalogo di tool avvelenato** (tool poisoning / tool shadowing, rug pull);
  5. server o bridge vulnerabile (bridge stdio→remoto, tool locali in ascolto su una porta e sfruttati da una pagina web).
- Principio guida: "**nessun controllo prova cosa farà un server**". I segnali di provenienza (signature, SBOM, listing curati) dicono **di chi ti fidi**, non che la fiducia sia meritata. Trattare un server locale di terze parti come **codice non fidato con esattamente i privilegi che gli dai**, i minimi.
- Mitigazioni:
  - preferire la versione **remota** se il server non ha bisogno della macchina locale;
  - verificare publisher e nome esatto del pacchetto;
  - **pinnare la versione**: con `npx`/`uvx` il pin copre solo il pacchetto top-level, le dipendenze transitive si risolvono all'installazione; un'immagine container per **digest** (`@sha256:`) congela tutto l'albero;
  - preferire artefatti firmati, con attestazioni e SBOM;
  - **leggere l'elenco dei tool** prima di affidarsi al server;
  - isolamento (container, sandbox, VM), credenziali separate, filesystem ed **egress** limitati, gestione a livello di organizzazione.

### 6.6 OAuth Authorization URL Validation
Rischi: `javascript:` URL (XSS), command injection se l'URL è aperto via shell, escalation a RCE via proxy stdio.
Client **MUST**: accettare solo `http(s)` (http solo loopback in dev), rifiutare `javascript:`, `data:`, `file:`, `vbscript:`; **non** aprire URL via shell (`cmd.exe`, `sh`, PowerShell); sanitizzare. SHOULD: allowlist, CSP (`script-src 'self'`).

### 6.7 Altri
- **Mix-up attacks** → validazione `iss`.
- **Localhost redirect URI impersonation** con CIMD → warning dell'AS, hostname ben visibile.
- **Scope minimization** → scope iniziali minimi (es. `mcp:tools-basic`), elevazione incrementale via `WWW-Authenticate scope="…"`, tolleranza al down-scoping; evitare scope omnibus (`files:*`, `admin:*`).

---

### 6.8 Tool poisoning, rug pull, lethal trifecta e limiti delle annotations
- **Tool poisoning**: nomi e descrizioni dei tool sono **istruzioni lette dal modello**. Un server può nasconderci direttive che guidano l'agente, anche sull'uso dei tool di **altri** server (**tool shadowing**), **senza che il tool avvelenato venga mai invocato**.
- **Rug pull**: il server cambia le definizioni **dopo** l'approvazione. Consenso una tantum e pin del pacchetto **non** coprono questo rischio. Mitigazioni: rileggere e confrontare le definizioni (es. hash), ri-approvare i cambiamenti; `notifications/tools/list_changed` segnala che la lista è cambiata.
- **Lethal trifecta** (citata nel blog ufficiale sulle tool annotations, 2026-03-16): **accesso a dati privati** + **esposizione a contenuti non fidati** + **capacità di comunicare all'esterno** = condizioni per l'esfiltrazione via prompt injection. Il rischio è una **proprietà della sessione**, non del singolo server: in MCP è facile combinare tool di più server.
- **Tool annotations** (dalla 2025-03-26): `title`, `readOnlyHint` (default `false`), `destructiveHint` (default `true`), `idempotentHint` (default `false`), `openWorldHint` (default `true`). I default sono **pessimisti**: un tool senza annotations è considerato modificante, potenzialmente distruttivo, non idempotente e open-world.
  - `destructiveHint` e `idempotentHint` contano solo se `readOnlyHint` è `false`.
  - `openWorldHint`: l'output di tool "esterni" va trattato come **contenuto non fidato**.
  - **Possono**: guidare le conferme (read-only da server fidato → auto-approvazione; distruttivo → conferma), **fiducia graduata** (server interni vs installati da internet), UX, input per **policy engine** (es. bloccare tool open-world in sessioni che hanno letto dati privati).
  - **Non possono**: rendere il modello resistente alla prompt injection; impedire a un server non fidato di **mentire** (i client **MUST** trattarle come non fidate se il server non è fidato); fare **enforcement** (per garanzie servono controlli di rete o sandbox); descrivere il rischio di combinazioni di tool.
- Stesso principio delle server instructions: **mai segnali "soft" dove servono garanzie "hard"**.

## 7. Sicurezza a livello di transport (`basic/transports/streamable-http.md`)
- Server **MUST** validare l'header **`Origin`** su tutte le connessioni (anti **DNS rebinding**); `Origin` presente e invalido → **HTTP 403**.
- In locale SHOULD bind solo su **127.0.0.1**, non `0.0.0.0`.
- SHOULD autenticare tutte le connessioni.
- Validazione header↔body (`MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`, `Mcp-Param-*`): mismatch → `400` + **`HeaderMismatch` (-32020)**. Motivo di sicurezza: evitare che componenti diversi (load balancer vs server) si basino su fonti di verità diverse.
- Gli intermediari che applicano policy sugli header SHOULD verificare che `MCP-Protocol-Version` sia una versione che richiede validazione header–body, altrimenti rifiutare.
- **`x-mcp-header`**: SHOULD NOT applicarlo a parametri sensibili (password, API key, token, PII) perché gli header sono visibili agli intermediari. Valori codificati con sentinel Base64 `=?base64?…?=` per evitare injection.
- stdio: niente spec di autorizzazione; credenziali dall'ambiente.

---

## 8. Consenso e controllo umano nelle feature

| Feature | Requisito |
|---|---|
| **Tools** | SHOULD sempre esserci un **human in the loop** con possibilità di negare. UI che mostra quali tool sono esposti, indicatori visivi delle invocazioni, conferme per le operazioni. Client SHOULD mostrare gli input del tool **prima** della chiamata (anti esfiltrazione), validare i risultati prima di passarli all'LLM, timeout, **log per audit**. Server MUST validare input, access control, **rate limit**, sanitizzare output. |
| **Tool annotations** | `readOnlyHint` (default false), `destructiveHint` (default **true**, significativo solo se readOnly=false), `idempotentHint` (default false), `openWorldHint` (default **true**). Sono **hint**: i client MUST considerarle **untrusted** salvo server fidati, e non devono basare decisioni d'uso su annotation di server non fidati. |
| **Elicitation (form)** | Server **MUST NOT** chiedere segreti (password, API key, token, credenziali di pagamento) in form mode. Client MUST: indicare quale server chiede, opzioni chiare decline/cancel, revisione/modifica prima dell'invio. |
| **Elicitation (URL)** | Obbligatoria per dati sensibili. Client MUST NOT pre-fetch dell'URL, MUST NOT aprirlo senza consenso, MUST mostrare l'URL completo, MUST aprirlo in modo che client/LLM non possano ispezionarlo (es. SFSafariViewController sì, WKWebView no). SHOULD evidenziare il dominio, avvisare per Punycode. Server MUST NOT mettere PII/credenziali nell'URL né URL pre-autenticati; MUST verificare che chi apre l'URL sia lo stesso utente che ha generato l'elicitation (anti phishing / account takeover, confronto `sub`). |
| **URL elicitation ≠ MCP authorization** | Serve all'autorizzazione **verso terze parti** (il server MCP è OAuth client di un'altra API). Le credenziali di terze parti **MUST NOT** transitare dal client MCP; il server **MUST NOT** usare il token del client verso la terza parte (passthrough); il server memorizza i token terzi legati all'identità utente (è quindi stateful). |
| **Identità utente** | Server MUST NOT fidarsi di identità dichiarate dal client ("sono joe@example.com"): usare l'autorizzazione (`sub`). |
| **Sampling (deprecato)** | human in the loop, l'utente può rivedere/modificare prompt e risposta. |
| **Roots (deprecato)** | client MUST esporre solo root con permessi appropriati, validare URI (traversal), consenso utente. |
| **Resources** | server MUST validare URI, MUST sanitizzare i path `file://` (directory traversal), SHOULD access control. |
| **Prompts** | MUST validare input/output (injection). |
| **Completion** | MUST validare input, rate limiting, controllare suggerimenti sensibili, evitare information disclosure. |

---

## 9. Rischi di protocollo specifici della 2026-07-28

### 9.1 `requestState` (MRTR) — input controllato dall'attaccante
- Il server **MUST** trattare `requestState` come **attacker-controlled**. Se influenza autorizzazione, accesso alle risorse o business logic: integrità **MUST** (es. **HMAC** o **AEAD**) e rifiuto dello stato non verificato. L'integrità MAY essere omessa solo se la manomissione può causare al massimo il fallimento della richiesta.
- Anti-replay (SHOULD, dentro il payload protetto): **principal autenticato**, **TTL breve**, **identificativo della richiesta originale** (metodo + digest dei parametri).
- Queste misure **non garantiscono single-use**: se serve consumo una-tantum, va imposto server-side (MUST).
- Il client MUST NOT ispezionare/modificare `requestState` e MUST rimandarlo identico.

### 9.2 Caching (`cacheScope`)
- `"public"`: nessun dato utente, cacheabile e condivisibile da gateway/proxy tra utenti — **anche se** la risposta proviene da un endpoint autenticato.
- `"private"`: riusabile solo nello stesso contesto di autorizzazione (token diverso ⇒ cache diversa).
- Il server **MUST NOT** affidarsi a `cacheScope` come controllo d'accesso; MUST applicare access control per primitiva. Stesso `cacheScope` per tutte le pagine di una lista.
- Le liste **MAY variare in base all'autorizzazione** (scope concessi), mai per connessione.

### 9.3 JSON Schema
- **MUST NOT** dereferenziare automaticamente `$ref` verso URI di rete; eventuale opt-in disabilitato di default con allowlist, blocco loopback/link-local/privati, timeout, limiti di dimensione, log. Schemi con `$ref` esterni non risolti SHOULD essere rifiutati.
- Limiti su composizioni (`anyOf`/`oneOf`/`allOf`/`if-then-else`, `$defs`): profondità, numero di sottoschemi, budget di tempo → anti DoS del validatore.

### 9.4 Icons
Trattare metadata e byte come untrusted; solo `https:` o `data:`; rifiutare `javascript:`, `file:`, `ftp:`, `ws:`; niente redirect cross-origin; fetch **senza credenziali**; stessa origin del server; attenzione a SVG con JavaScript; verificare il MIME con magic bytes.

### 9.5 Logging (deprecato)
I log **MUST NOT** contenere credenziali, PII, dettagli interni utili agli attaccanti. `notifications/message` solo se la richiesta include `io.modelcontextprotocol/logLevel`.

---

## 10. Auditability & Observability
- **OpenTelemetry**: chiavi `_meta` riservate `traceparent`, `tracestate` (W3C Trace Context) e `baggage` (W3C Baggage) — eccezione alla regola del prefisso. Esistono semantic conventions OTel per MCP.
- Logging di protocollo **deprecato** (SEP-2577): migrare a **stderr** (stdio) e **OpenTelemetry**.
- Tools: client SHOULD **loggare l'uso dei tool** per audit; cancellation: SHOULD loggare i motivi.
- Token passthrough distrugge l'audit trail (il server non distingue i client; i log a valle mostrano identità sbagliate).
- Scope granulari → audit più chiaro (scope omnibus "mascherano l'intento").
- Header `Mcp-Method` / `Mcp-Name` → gateway e WAF possono instradare, misurare, applicare rate limit e **autorizzare** senza parsare il body.
- `clientInfo`/`serverInfo` utili per **display, logging, debugging**, non per sicurezza.
- Enterprise-Managed Authorization → trail di autorizzazione auditabile e revoca centralizzata.
- MCP Inspector (`npx @modelcontextprotocol/inspector`, varianti `--cli`, `--tui`) per testing/debug.

---

## 11. Estensioni di autorizzazione (`sources/extensions/auth/`)
Repo `modelcontextprotocol/ext-auth`. Estensioni **opzionali, additive, componibili, versionate indipendentemente**, mai attive di default: si negoziano tramite `capabilities.extensions`.

| Estensione | ID | Stage | Uso |
|---|---|---|---|
| **OAuth Client Credentials** | `io.modelcontextprotocol/oauth-client-credentials` | Stable | machine-to-machine: daemon, CI/CD, server-to-server; niente utente. Credenziali: **JWT Bearer Assertion (RFC 7523, raccomandata)** con `aud` = issuer dell'AS, oppure `client_id`+`client_secret`. `grant_type=client_credentials` + `resource`. |
| **Enterprise-Managed Authorization (EMA)** | `io.modelcontextprotocol/enterprise-managed-authorization` | Stable | l'**IdP aziendale** decide l'accesso: SSO → ID Token → scambio per **ID-JAG** (Identity Assertion JWT Authorization Grant) → l'MCP AS emette l'access token. Policy centralizzate, revoca centralizzata, compliance. |

Standard interattivo con utente → nessuna estensione (core spec).

---

## 12. Governance (nel senso di processo del progetto)
Vedi anche dominio 5. Punti da ricordare:
- MCP è stato **donato da Anthropic all'Agentic AI Foundation (AAIF)**, directed fund della **Linux Foundation** (annuncio 2025-12-09). Co-fondatori AAIF: Anthropic, Block, OpenAI; progetti fondatori: MCP, goose, AGENTS.md. Il progetto mantiene autonomia tecnica.
- Struttura tecnica: **Lead Maintainers (BDFL)** → Core Maintainers → Maintainers → Contributors; insieme formano lo Steering Group; membership individuale, non aziendale.
- Modifiche alla spec tramite **SEP** (Specification Enhancement Proposal), workflow PR-based (SEP-1850).
- **Feature lifecycle** (SEP-2596): Active → Deprecated (finestra minima **12 mesi**, o 90 giorni con expedited removal) → Removed. Registry delle feature deprecate.
- Licenze: codice e spec Apache 2.0; documentazione CC-BY 4.0.

---

## 13. Differenze rispetto alle versioni precedenti (security)
| Tema | Prima | 2026-07-28 |
|---|---|---|
| Registrazione client | 2025-03-26 e 2025-06-18: DCR **SHOULD**; 2025-11-25: DCR declassata a **MAY**, aggiunto CIMD raccomandato (SEP-991) | **DCR deprecata** (PR #2858), CIMD SHOULD |
| Issuer validation | assente | **RFC 9207** `iss` (SEP-2468) |
| DCR `application_type` | non richiesto | **MUST** (SEP-837) |
| Binding credenziali↔AS | implicito | **MUST** chiave per issuer, ri-registrazione su cambio AS (SEP-2352) |
| Sessioni | `Mcp-Session-Id`, rischio session hijacking | niente sessioni → **state handle hijacking** |
| Server→client | richieste server-initiated su SSE | **MRTR** + `requestState` (integrità obbligatoria se rilevante) |
| Header | solo `MCP-Protocol-Version` (dal 2025-06-18) | + `Mcp-Method`, `Mcp-Name`, `Mcp-Param-*` con validazione → `HeaderMismatch -32020` |
| Discovery AS | 2025-06-18: RFC 8414 + RFC 9728; 2025-11-25: + OIDC Discovery, WWW-Authenticate opzionale con fallback well-known | invariato + validazione `issuer` del metadata esplicita |
| Scope | 2025-11-25: step-up via `WWW-Authenticate` (SEP-835) | precisazioni: unione degli scope lato client, tutti gli scope in una challenge |
| Resource Indicators | obbligatori dal 2025-06-18 | invariato |
| Elicitation URL | 2025-11-25: introdotta con `elicitationId` e `notifications/elicitation/complete` | rimossi; esito via retry MRTR + `requestState` |
| `-32042` URL elicitation required | 2025-11-25 | rimosso, non emettere |
