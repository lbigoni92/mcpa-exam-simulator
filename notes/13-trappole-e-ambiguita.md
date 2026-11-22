# Trappole, distrattori e ambiguità della spec

> Pensato per la generazione delle domande: ogni voce è un buon **distrattore** o un punto su cui costruire una domanda "qual è l'affermazione corretta?".

## A. Distrattori "da versione vecchia" (sbagliati nella 2026-07-28)
1. "Il client deve inviare `initialize` come prima richiesta" → falso, non esiste più.
2. "Il server può inviare `sampling/createMessage` su uno stream SSE" → falso, solo via MRTR.
3. "Le notifiche di cambio lista arrivano su un GET SSE standalone" → falso, `subscriptions/listen`.
4. "Per riprendere uno stream si usa `Last-Event-ID`" → falso, niente resumability.
5. "Il server assegna `Mcp-Session-Id`" → falso; va ignorato, mai creato né rimandato.
6. "Risorsa non trovata = `-32002`" → falso, `-32602` (il client accetta ancora `-32002` per retrocompatibilità).
7. "Il livello di log si imposta con `logging/setLevel`" → falso, `_meta.io.modelcontextprotocol/logLevel` per richiesta.
8. "Si usa `ping` per verificare la connessione" → rimosso.
9. "DCR è il meccanismo di registrazione raccomandato" → falso: CIMD raccomandato, DCR deprecata.
10. "`structuredContent` deve essere un oggetto" → falso, qualsiasi valore JSON.
11. "Tasks fa parte del core" → falso, è un'estensione (Beta, verso core).
12. "Sampling e roots sono stati rimossi" → falso: **deprecati**, ancora funzionanti (via MRTR) per ≥ 12 mesi.
13. "`notifications/elicitation/complete` comunica la fine di una URL elicitation" → rimosso; l'esito si scopre col retry.

## B. MUST vs SHOULD — dettagli facili da sbagliare
- `server/discover`: **server MUST implementare**, **client MAY chiamare**.
- `clientInfo`: SHOULD (non obbligatorio). `protocolVersion` e `clientCapabilities`: obbligatori.
- `serverInfo` nei result: SHOULD.
- Autorizzazione: OPTIONAL in generale; HTTP SHOULD conformarsi; stdio SHOULD NOT.
- AS: `iss` SHOULD; client: validazione MUST. CIMD SHOULD; DCR MAY (deprecata). PRM: server MUST, client MUST usarlo.
- Client MUST supportare **sia** RFC 8414 **sia** OIDC Discovery; AS MUST almeno uno.
- PKCE: client MUST; `S256` MUST quando tecnicamente possibile; `code_challenge_methods_supported` assente ⇒ MUST rifiutare di procedere.
- `resource`: MUST in authorization **e** token request, anche se l'AS non lo supporta.
- `Origin` invalido ⇒ 403 (MUST); bind su localhost (SHOULD).
- Human in the loop per i tool: SHOULD (non MUST). Consenso esplicito prima di invocare tool: principio ("must") nei Key Principles, non applicabile dal protocollo.
- `outputSchema` presente ⇒ server MUST conformarsi, client SHOULD validare.
- Ordine deterministico di `tools/list`: SHOULD.
- `ttlMs`/`cacheScope`: MUST sui result cacheabili.
- `x-mcp-header`: server MAY usarlo; client HTTP MUST supportarlo.
- Form elicitation per segreti: MUST NOT.
- Progress: il valore MUST crescere; total opzionale; float ammessi.
- Cancellazione su HTTP: chiusura dello stream (no notifica); su stdio: `notifications/cancelled` MUST.

## C. Ambiguità/incoerenze interne della spec (da evitare come risposta "unica corretta")
1. **Chiusura delle subscription lato server**: `subscriptions.md` dice che il server **SHOULD** inviare una *risposta di successo* alla `subscriptions/listen` prima di chiudere; `cancellation.md` dice che il server **MUST** inviare `notifications/cancelled` riferito alla listen quando abbatte lo stream (ed è l'unico uso lecito di `notifications/cancelled` lato server). Nelle domande evitare di contrapporre le due cose; usare formulazioni coerenti con entrambe (es. "l'unico caso in cui il server può inviare `notifications/cancelled`").
2. **Notifiche client→server su HTTP**: la spec dice che la revisione non definisce notifiche client→server su Streamable HTTP, ma descrive comunque la meccanica (202 Accepted).
3. **Elicitation URL "New feature" 2025-11-25**: la nota nella pagina 2026-07-28 la chiama ancora "introdotta nella 2025-11-25", corretto storicamente.
4. **Durata esame**: **90 min** (pagina MCPA + FAQ/Important Instructions LF). I 120 min del press release e del blog AAIF sono precedenti al lancio; nelle pagine LF attuali 120 è la durata del CNPA. Risolto: si usa 90.
5. Gli esempi `schema`/docs talvolta mostrano `_meta` senza `protocolVersion` (blog GA) — la regola normativa è che è obbligatorio.

## D. Confusioni concettuali tipiche
- **Prompts user-controlled** = l'utente decide *quando* usarli, il contenuto lo definisce il server.
- **Resources application-controlled** ≠ model-controlled.
- **URL elicitation ≠ MCP authorization**: serve per credenziali/autorizzazioni verso **terze parti**; il token del client verso il server MCP non cambia.
- **`accept` su URL elicitation** = consenso ad aprire l'URL, non completamento.
- **Errore di validazione input** ⇒ tool execution error (`isError: true`), **non** protocol error. **Tool sconosciuto** ⇒ protocol error `-32602`.
- **PKCE non previene il mix-up**; serve `iss`.
- **`cacheScope: public` non è un controllo d'accesso**.
- **Possesso di un handle ≠ autenticazione**.
- **`clientInfo`/`serverInfo` non sono verificati**: mai per decisioni di sicurezza.
- **Le liste possono variare per autorizzazione (scope) ma non per connessione**.
- **`subscriptionId` = id JSON-RPC della `subscriptions/listen`**, non un id generato dal server.
- **MRTR retry = nuova richiesta con nuovo `id`**, non la stessa.
- **`InputRequiredResult` solo su `tools/call`, `resources/read`, `prompts/get`** (non su `tools/list`, `completion/complete`, ecc.).
- **Server stdio: log su stderr, mai su stdout**.
- **Il client stdio cancella con `notifications/cancelled`; il client HTTP chiude lo stream**.
- **Scope challenge**: il server elenca tutti gli scope necessari in una volta; l'unione con quelli precedenti la fa il **client**.
- **`offline_access`**: il client MAY richiederlo se l'AS lo supporta; il server MCP SHOULD NOT pubblicizzarlo.
- **Prefisso riservato**: `com.example.mcp/` NON è riservato; `dev.mcp/` sì.
- **Registry**: ospita metadata, non binari; non supporta server privati; versioni immutabili; niente range.

## E. Errori osservati nelle domande di terze parti (vedi `practice-questions/`)
Raccolti analizzando le fonti gratuite non ufficiali: sono i distrattori "naturali" che i candidati hanno già visto. Fonte principale: CertSafari e la exam guide di Cloud Soft Solutions.
- "MCP è un protocollo **stateful** / mantiene una sessione tra le chiamate" → falso nella 2026-07-28.
- "La negoziazione delle capability avviene nell'handshake `initialize`", "`initialize` deve essere il primo messaggio" → rimosso.
- "Il client può aprire un GET SSE e il server invia richieste su quello stream" → rimosso.
- "Il server chiede al client sampling, roots o elicitation con una richiesta JSON-RPC" → solo via MRTR (`InputRequiredResult`); sampling e roots deprecati.
- "Il consenso per i roots è un controllo chiave" → roots deprecati (domanda datata, non sbagliata in sé).
- "In una Resource solo `uri` è obbligatorio" → falso: anche `name` è obbligatorio (`BaseMetadata`).
- "I tool MCP devono restituire stringhe" (quiz HF, specifico di un progetto) → falso: content blocks + `structuredContent` (qualsiasi JSON).
- "L'SDK Python ufficiale è mantenuto da Anthropic" → gli SDK sono nell'org `modelcontextprotocol`, sotto governance AAIF, classificati per tier.
- "`Mcp-Name` è obbligatorio su ogni POST" → solo su `tools/call`, `resources/read`, `prompts/get`; su ogni POST sono obbligatori `MCP-Protocol-Version` e `Mcp-Method`.
- "Esame da 120 minuti", "soglia 80%" → 90 minuti; la soglia MCPA non è pubblicata (le regole LF generiche per gli esami MC dicono 75%).
- "DCR è stata deprecata da SEP-2577" → SEP-2577 depreca roots, sampling e logging; DCR è deprecata dalla PR #2858 (stessa revisione 2026-07-28).
- "`-32002` era già stato ritirato prima della 2026-07-28" → la sostituzione con `-32602` avviene **nella** 2026-07-28 (SEP-2164).
- "La 2026-07-28 formalizza session handle e handshake di inizializzazione" (post AAIF sui settori regolati, 2026-07-02, scritto prima della release finale) → falso: niente sessioni e niente `initialize`; lo stato applicativo usa handle espliciti passati come argomenti dei tool.
- "Roots, sampling e logging sono solo proposti per la deprecazione" (post AAIF basati sulla release candidate) → nella 2026-07-28 finale sono **deprecati** (funzionano ancora, rimozione non prima della revisione successiva al 2027-07-28).
