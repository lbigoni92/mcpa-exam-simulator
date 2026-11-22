# -*- coding: utf-8 -*-
"""Integrazione della teoria delle 34 lezioni rohitg00 (certifications/mcpa/lessons/*/docs, outputs).

Ogni punto qui sotto è un fatto presente nelle lezioni e MANCANTE nel nostro corso,
verificato sulla spec 2026-07-28 (o sulla fonte ufficiale indicata nel commento).
I punti delle lezioni che contraddicono la spec NON sono stati importati (vedi REVISIONE-lezioni.md).

Idempotente: aggiunge un punto solo se il testo inglese non è già presente.
Uso: python3 site/build/lesson_points.py  (poi build_data.py)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "..", "content")

# topic_id -> [(it, en)]
POINTS = {
    # ---------------- D1 ----------------
    "D1-01": [  # spec index, BCP 14
        ("Parole chiave equivalenti: MUST = SHALL = REQUIRED; SHOULD = RECOMMENDED; MAY = OPTIONAL; MUST NOT = SHALL NOT.",
         "Equivalent keywords: MUST = SHALL = REQUIRED; SHOULD = RECOMMENDED; MAY = OPTIONAL; MUST NOT = SHALL NOT."),

    ],
    "D1-06": [  # SEP-2596, community/feature-lifecycle
        ("La finestra di deprecazione (almeno 12 mesi) parte dal rilascio della revisione che marca la feature Deprecated, non dalla data del SEP.",
         "The deprecation window (at least 12 months) starts at the release of the revision that marks the feature Deprecated, not at the SEP's date."),
        ("Rimozione più precoce: la prima revisione rilasciata come Current alla scadenza della finestra o dopo; la rimozione vera richiede comunque una decisione dei Core Maintainer.",
         "Earliest removal: the first revision released as Current on or after the window elapses; actual removal still needs a Core Maintainer decision."),
        ("Per le deprecazioni della 2026-07-28 (roots, sampling, logging, DCR) la rimozione più precoce è la prima revisione dal 2027-07-28 in poi: una data esatta di rimozione è un distrattore.",
         "For 2026-07-28 deprecations (roots, sampling, logging, DCR) the earliest removal is the first revision on or after 2027-07-28: an exact removal date is a distractor."),
        ("Una feature Deprecated può tornare Active con un SEP che sostituisce quello di deprecazione.",
         "A Deprecated feature can be restored to Active by a SEP that supersedes the deprecation SEP."),
    ],
    "D1-08": [  # spec-2025-11-25/changelog, spec-2026-07-28/changelog
        ("2024-11-05 aveva i trasporti stdio e HTTP+SSE; HTTP+SSE è deprecato dalla 2025-03-26 (sostituito da Streamable HTTP).",
         "2024-11-05 had the stdio and HTTP+SSE transports; HTTP+SSE has been deprecated since 2025-03-26 (replaced by Streamable HTTP)."),
        ("2025-03-26 ha aggiunto anche l'audio content; il batching JSON-RPC, aggiunto in questa revisione, è stato rimosso nella successiva senza finestra di deprecazione.",
         "2025-03-26 also added audio content; JSON-RPC batching, added in this revision, was removed in the next one with no deprecation window."),
        ("2025-06-18 ha aggiunto anche i resource link e ha classificato il server MCP come OAuth resource server.",
         "2025-06-18 also added resource links and classified the MCP server as an OAuth resource server."),
        ("2025-11-25 ha aggiunto anche il consenso incrementale degli scope (SEP-835), la guida sui nomi dei tool (SEP-986) e gli errori di validazione degli input come tool execution error (SEP-1303).",
         "2025-11-25 also added incremental scope consent (SEP-835), tool name guidance (SEP-986) and input validation errors as tool execution errors (SEP-1303)."),
    ],
    # ---------------- D2 ----------------
    "D2-02": [  # spec basic/index, discover
        ("Chiave assente nelle capabilities = feature non offerta; {} = supportata senza impostazioni.",
         "Missing capabilities key = feature not offered; {} = supported with no settings."),
        ("-32021 porta data.requiredCapabilities (stessa forma di ClientCapabilities); -32022 porta data.supported e data.requested. Entrambi HTTP 400.",
         "-32021 carries data.requiredCapabilities (shaped like ClientCapabilities); -32022 carries data.supported and data.requested. Both are HTTP 400."),
        ("Dopo -32021 o -32022: nuovo id, si cambia solo ciò che l'errore chiede, e l'errore non va messo in cache come un risultato.",
         "After -32021 or -32022: new id, change only what the error asks for, and never cache the error as a result."),
        ("Chiedere una versione più vecchia con la forma moderna di _meta non rende il client legacy: un client legacy invia initialize.",
         "Requesting an older version through the modern _meta shape does not make a client legacy: a legacy client sends initialize."),
    ],
    "D2-03": [  # stdio.md
        ("Il client SHOULD NOT considerare l'output su stderr come segnale di errore.",
         "The client SHOULD NOT treat stderr output as an error signal."),
        ("Se il processo termina inaspettatamente le richieste in corso sono perse; dopo il riavvio il client reinvia subscriptions/listen.",
         "If the process exits unexpectedly, in-flight requests are lost; after the restart the client resends subscriptions/listen."),
    ],
    "D2-05": [  # streamable-http.md, SEP-2243
        ("Il valore di x-mcp-header deve essere un nome di header HTTP valido e unico (senza distinzione maiuscole/minuscole) tra i valori dello stesso inputSchema.",
         "The x-mcp-header value must be a valid HTTP field name, unique (case-insensitively) among the values in the same inputSchema."),
        ("Nomi degli header case-insensitive (mcp-method va accettato); valori case-sensitive (Mcp-Method: TOOLS/CALL va rifiutato).",
         "Header names are case-insensitive (mcp-method must be accepted); values are case-sensitive (Mcp-Method: TOOLS/CALL must be rejected)."),
        ("Base64 (=?base64?…?=) obbligatorio se il valore ha caratteri fuori dall'ASCII visibile, spazi iniziali o finali, o se assomiglia già al pattern sentinella.",
         "Base64 (=?base64?…?=) is required when the value has characters outside visible ASCII, leading or trailing whitespace, or already matches the sentinel pattern."),
        ("Mcp-Name vale params.name per tools/call e prompts/get, params.uri per resources/read. Il body resta la fonte di verità.",
         "Mcp-Name is params.name for tools/call and prompts/get, params.uri for resources/read. The body stays the source of truth."),
    ],
    "D2-06": [  # SEP-2106
        ("outputSchema accetta qualsiasi JSON Schema valido (array, primitivi, composizioni): il vincolo type: object vale solo per inputSchema.",
         "outputSchema accepts any valid JSON Schema (arrays, primitives, compositions): the type: object constraint applies only to inputSchema."),
        ("Un'eventuale modalità che scarica $ref di rete deve essere opt-in e disattivata di default; uno schema con $ref esterno non risolto SHOULD essere rifiutato, non trattato come permissivo.",
         "Any mode that fetches network $refs must be opt-in and disabled by default; a schema with an unresolved external $ref SHOULD be rejected, not treated as permissive."),
    ],
    "D2-07": [  # basic/index _meta, icons
        ("Riservati: io.modelcontextprotocol/, dev.mcp/, org.modelcontextprotocol.api/, com.mcp.tools/. Non riservati: com.example.mcp/ e mcp.example/ (mcp è solo la prima label).",
         "Reserved: io.modelcontextprotocol/, dev.mcp/, org.modelcontextprotocol.api/, com.mcp.tools/. Not reserved: com.example.mcp/ and mcp.example/ (mcp is only the first label)."),
        ("Chiavi _meta riservate: progressToken (senza prefisso), protocolVersion, clientCapabilities, clientInfo, logLevel (deprecata) nelle request; serverInfo nei result; subscriptionId nelle notifiche di listen.",
         "Reserved _meta keys: progressToken (no prefix), protocolVersion, clientCapabilities, clientInfo, logLevel (deprecated) on requests; serverInfo on results; subscriptionId on listen notifications."),
        ("Icone: verificare che l'URI sia della stessa origine del server, scaricarle senza credenziali (niente cookie o Authorization) e trattare gli SVG come potenzialmente eseguibili.",
         "Icons: check the URI has the same origin as the server, fetch without credentials (no cookies or Authorization) and treat SVG as potentially executable."),
    ],
    "D2-09": [  # client best practices, tools.md
        ("Il modello non vede mai dettagli di trasporto (status HTTP, header). Una chiamata negata dall'utente non arriva mai sul wire.",
         "The model never sees transport details (HTTP status, headers). A call the user denies never reaches the wire."),
        ("Non riordinare la lista dei tool tra un turno e l'altro: l'ordine stabile preserva la prompt cache del provider LLM.",
         "Do not re-sort the tool list between turns: a stable order preserves the LLM provider's prompt cache."),
        ("Dopo un errore JSON-RPC (es. tool sconosciuto, -32602) non si reinvia la stessa identica richiesta.",
         "After a JSON-RPC error (e.g. unknown tool, -32602) the identical request is not resent."),
    ],
    "D2-10": [  # extensions/overview, SEP-2133, sep-guidelines
        ("Il prefisso nell'identificatore è obbligatorio: my-extension senza prefisso non è valido e non si attiva.",
         "The prefix in the identifier is mandatory: my-extension without a prefix is invalid and never activates."),
        ("Le estensioni sono versionate indipendentemente dal core. Una modifica incompatibile mantiene l'identificatore; uno nuovo (es. …-v2) serve solo se vecchio e nuovo comportamento devono coesistere nella stessa revisione.",
         "Extensions version independently of the core. A breaking change keeps the identifier; a new one (e.g. …-v2) is used only when old and new behavior must coexist under one revision."),
        ("Un Extensions Track SEP accettato porta l'estensione a Beta, un secondo la porta a Stable. Prima di un SEP si può sperimentare in un repository experimental-ext-.",
         "An accepted Extensions Track SEP moves the extension to Beta, a second one to Stable. Before a SEP, ideas can be tried in an experimental-ext- repository."),
        ("Nelle fasi Experimental e Beta una modifica incompatibile aggiunge o incrementa una stringa revision nelle impostazioni: un peer che riceve una revision sconosciuta non attiva l'estensione.",
         "In the Experimental and Beta stages a breaking change adds or increments a revision string in the settings: a peer that receives an unknown revision should not enable the extension."),
        ("Estensione obbligatoria per la chiamata ma non dichiarata dal client: errore -32021, non -32601 né -32602.",
         "Extension mandatory for the call but not declared by the client: error -32021, not -32601 or -32602."),
    ],
    "D2-11": [  # server instructions blog + security
        ("Istruzioni con ordini rivolti al modello (\"ignora le indicazioni precedenti\", \"nascondi X all'utente\") vanno trattate come tentativo di prompt injection.",
         "Instructions that give orders to the model (\"ignore previous guidance\", \"hide X from the user\") should be treated as a prompt injection attempt."),
    ],
    # ---------------- D3 ----------------
    "D3-01": [  # basic/index
        ("Un resultType non riconosciuto dal client MUST essere considerato invalido; un valore di estensione (task) è valido solo se la capability è stata dichiarata.",
         "A resultType the client does not recognize MUST be considered invalid; an extension value (task) is valid only if the capability was declared."),
        ("Un error response omette l'id solo se l'id non era leggibile (es. -32700 Parse error su body non JSON).",
         "An error response omits the id only when the id could not be read (e.g. -32700 Parse error on a non-JSON body)."),
    ],
    "D3-02": [  # basic/index, SEP-2575/2567
        ("tools/list, resources/list e prompts/list non possono variare per connessione né come effetto collaterale di una chiamata precedente; possono variare solo in base all'autorizzazione della richiesta.",
         "tools/list, resources/list and prompts/list must not vary per connection or as a side effect of an earlier call; they may vary only by the request's authorization."),
        ("Rimossi nella 2026-07-28: initialize, notifications/initialized, Mcp-Session-Id e le capabilities legate alla connessione.",
         "Removed in 2026-07-28: initialize, notifications/initialized, Mcp-Session-Id and connection-scoped capabilities."),
    ],
    "D3-03": [  # versioning.md
        ("Probe HTTP: si prova una richiesta moderna; su 4xx si legge il body. Errore moderno riconosciuto = server moderno (correggi e riprova); body vuoto o non riconosciuto = legacy, fallback a initialize ed eventualmente a HTTP+SSE.",
         "HTTP probe: try a modern request; on a 4xx read the body. Recognized modern error = modern server (fix and retry); empty or unrecognized body = legacy, fall back to initialize and possibly to HTTP+SSE."),
        ("Matrice: moderno con legacy fallisce; legacy con solo-moderno fallisce (i client legacy non possono passare al moderno da soli); dual-era da una delle due parti funziona.",
         "Matrix: modern with legacy fails; legacy with modern-only fails (legacy clients cannot fall forward); dual-era on either side works."),
        ("Un server solo moderno dovrebbe indicare le versioni supportate anche quando rifiuta un initialize legacy: può essere l'unica diagnostica per l'utente.",
         "A modern-only server should state its supported versions even when rejecting a legacy initialize: it may be the user's only diagnostic."),
    ],
    "D3-04": [  # mrtr.md
        ("Ogni voce di inputRequests è esattamente una tra elicitation/create, sampling/createMessage e roots/list, con una chiave scelta dal server.",
         "Each inputRequests entry is exactly one of elicitation/create, sampling/createMessage or roots/list, under a server-chosen key."),
        ("Il server non deve dare per scontato che il client riprovi né tenere risorse aperte in attesa del retry.",
         "The server must not assume the client will retry, nor hold resources open waiting for the retry."),
        ("Senza inputRequests il client può riprovare subito; requestState si rimanda solo se il server l'ha inviato, identico e senza interpretarlo.",
         "Without inputRequests the client may retry immediately; requestState is echoed only if the server sent it, unchanged and uninterpreted."),
        ("inputResponses e requestState valgono solo per il retry di quella richiesta, mai per altre chiamate in parallelo.",
         "inputResponses and requestState apply only to the retry of that request, never to other parallel calls."),
    ],
    "D3-05": [  # subscriptions.md
        ("Fine di una subscription: cancellazione del client; chiusura gradevole del server (SHOULD rispondere alla richiesta subscriptions/listen con un result complete, poi chiudere); oppure caduta del trasporto, che non porta nessuna risposta.",
         "A subscription ends by client cancellation; by graceful server closure (SHOULD answer the subscriptions/listen request with a complete result, then close); or by a transport drop, which carries no response."),
        ("Più subscription contemporanee sono permesse: il client le distingue tramite subscriptionId.",
         "Several concurrent subscriptions are allowed: the client tells them apart by subscriptionId."),
    ],
    "D3-06": [  # cancellation.md, progress.md
        ("Le race sono normali: una cancellazione può arrivare dopo la fine della richiesta e una risposta dopo la cancellazione; entrambe le parti MUST gestirle senza errori.",
         "Races are normal: a cancellation may arrive after the request finished and a response after the cancellation; both sides MUST handle them gracefully."),
        ("Dopo uno stream interrotto la richiesta va reinviata con un nuovo id; prima di ripetere un tool con effetti collaterali, idempotentHint resta solo un indizio.",
         "After a broken stream the request is reissued with a new id; before repeating a side-effecting tool, idempotentHint is only a hint."),
    ],
    "D3-07": [  # caching.md, pagination.md
        ("Chiave di cache: metodo più parametri rilevanti (uri, cursor); le voci private vanno separate per contesto di autorizzazione.",
         "Cache key: method plus relevant parameters (uri, cursor); private entries are partitioned by authorization context."),
        ("Un result input_required non è mai cacheabile e non porta ttlMs né cacheScope.",
         "An input_required result is never cacheable and carries neither ttlMs nor cacheScope."),
        ("Freschezza verificata quando serve, non con polling; se il re-fetch fallisce il client MAY servire la copia scaduta.",
         "Freshness is checked when needed, not by polling; if the re-fetch fails the client MAY serve the stale copy."),
        ("Stesso cacheScope su tutte le pagine di una lista (ttlMs può variare); cursor non valido: scartare le pagine in cache e ripartire dall'inizio.",
         "Same cacheScope on every page of a listing (ttlMs may vary); invalid cursor: discard cached pages and restart from the beginning."),
        ("La dimensione della pagina la decide il server: il client MUST NOT assumerla fissa. Conta la presenza di nextCursor, non il suo valore.",
         "Page size is decided by the server: the client MUST NOT assume a fixed one. What matters is whether nextCursor is present, not its value."),
    ],
    "D3-08": [  # basic/index error codes
        ("-32700 Parse error: body non JSON valido (id null).",
         "-32700 Parse error: body is not valid JSON (id null)."),
        ("-32000..-32019: nuovi codici MUST NOT, uso SHOULD NOT; -32020..-32099: MUST NOT emettere codici non definiti dalla spec.",
         "-32000..-32019: new codes MUST NOT be allocated and SHOULD NOT be used; -32020..-32099: undefined codes MUST NOT be emitted."),
        ("Codici applicativi nuovi SHOULD stare fuori da -32768..-32000; prima però si preferisce isError.",
         "New application codes SHOULD sit outside -32768..-32000; but isError is preferred first."),
        ("Livello di log non valido: -32602. Gli errori locali (es. timeout nell'SDK) non hanno codici e non devono sembrare errori del peer.",
         "Invalid log level: -32602. Local errors (e.g. an SDK timeout) have no codes and must not look like errors from the peer."),
    ],
    "D3-09": [  # tools.md, SEP-1303
        ("Validazione (il tool esiste?) produce solo errori di protocollo; esecuzione produce isError, e -32603 solo per un guasto inatteso non causato dall'input.",
         "Validation (does the tool exist?) only produces protocol errors; execution produces isError, and -32603 only for an unexpected fault not caused by the input."),
        ("I prompt non hanno un canale isError: nome sconosciuto o argomento mancante sono sempre -32602.",
         "Prompts have no isError channel: unknown name or missing argument is always -32602."),
        ("Un rifiuto per policy (rate limit, consenso negato) va in un result con isError, non in un codice di errore inventato.",
         "A policy refusal (rate limit, consent withheld) goes in a result with isError, not in an invented error code."),
    ],
    "D3-11": [  # tools.md
        ("content è sempre presente (può essere vuoto). Le annotations di un content block (audience, priority, lastModified) stanno accanto ai campi del blocco, non dentro resource.",
         "content is always present (may be empty). A content block's annotations (audience, priority, lastModified) sit beside the block's fields, not inside resource."),
        ("resource_link richiede uri e name; resource incorpora uri, mimeType e text o blob.",
         "resource_link requires uri and name; resource embeds uri, mimeType and text or blob."),
    ],
    "D3-14": [  # SEP-2663 tasks extension
        ("Solo tools/call può diventare un task. Il server decide richiesta per richiesta: un client che dichiara l'estensione deve gestire sia un result normale sia resultType task.",
         "Only tools/call can become a task. The server decides per request: a client that declares the extension must handle both a normal result and resultType task."),
        ("Client senza l'estensione e lavoro impossibile senza task: -32021 con data.requiredCapabilities (anche per tasks/get, tasks/update, tasks/cancel).",
         "Client without the extension and work impossible without a task: -32021 with data.requiredCapabilities (also for tasks/get, tasks/update, tasks/cancel)."),
        ("CreateTaskResult: taskId generato dal server, status (di solito working), createdAt, lastUpdatedAt, ttlMs (null = illimitato), pollIntervalMs, statusMessage opzionale.",
         "CreateTaskResult: server-generated taskId, status (usually working), createdAt, lastUpdatedAt, ttlMs (null = unlimited), pollIntervalMs, optional statusMessage."),
        ("Il server MUST NOT restituire il taskId prima che il task sia creato in modo durevole (cioè prima che tasks/get lo trovi).",
         "The server MUST NOT return the taskId before the task is durably created (i.e. before tasks/get would find it)."),
        ("tasks/get ha resultType complete; lo stato è nel campo status. completed include il result originale, failed include l'errore JSON-RPC.",
         "tasks/get has resultType complete; the state is in the status field. completed inlines the original result, failed inlines the JSON-RPC error."),
        ("Un result con isError: true porta il task a completed, non a failed (failed è solo per errori JSON-RPC).",
         "A result with isError: true takes the task to completed, not failed (failed is only for JSON-RPC errors)."),
        ("Input a metà esecuzione: tasks/update con inputResponses, senza ripetere tools/call. Le chiavi di inputRequests sono uniche per tutta la vita del task.",
         "Mid-execution input: tasks/update with inputResponses, without repeating tools/call. inputRequests keys are unique for the task's whole life."),
        ("Per cancellare un task si usa tasks/cancel: notifications/cancelled MUST NOT essere usata per i task.",
         "Cancelling a task uses tasks/cancel: notifications/cancelled MUST NOT be used for tasks."),
        ("Differenze dalla 2025-11-25 sperimentale: taskId ora generato dal server (prima dal client), capability per richiesta invece che all'inizializzazione, niente tasks/result e tasks/list.",
         "Differences from the experimental 2025-11-25 version: taskId now server-generated (was client-generated), per-request capability instead of at initialization, no tasks/result or tasks/list."),
    ],
    "D3-15": [  # resources.md
        ("Risorsa non trovata: -32602 con data.uri; un errore interno è -32603. I client accettano ancora -32002 dai server più vecchi.",
         "Resource not found: -32602 with data.uri; an internal failure is -32603. Clients still accept -32002 from older servers."),
        ("Una sola resources/read può restituire più elementi in contents.",
         "A single resources/read may return several items in contents."),
        ("Schemi URI: https:// solo se il client può scaricare la risorsa direttamente dal web; file:// non deve per forza essere un filesystem reale; git:// per contenuti versionati; schemi custom conformi a RFC 3986.",
         "URI schemes: https:// only if the client can fetch the resource directly from the web; file:// need not be a real filesystem; git:// for versioned content; custom schemes must follow RFC 3986."),
        ("Validare ogni URI e autorizzare ogni lettura: comparire in resources/list non rende una risorsa leggibile da chiunque.",
         "Validate every URI and authorize every read: appearing in resources/list does not make a resource readable by anyone."),
    ],
    "D3-16": [  # prompts.md, caching.md
        ("prompts/list è cacheable; prompts/get no (niente ttlMs e cacheScope).",
         "prompts/list is cacheable; prompts/get is not (no ttlMs or cacheScope)."),
        ("I messaggi possono contenere text, image, audio, resource_link o resource incorporata.",
         "Messages can contain text, image, audio, resource_link or an embedded resource."),
    ],
    "D3-17": [  # completion.md
        ("completion/complete non è cacheable e non usa cursor: hasMore indica che le corrispondenze superano i 100 valori.",
         "completion/complete is not cacheable and uses no cursor: hasMore means matches exceed the 100 values."),
    ],
    "D3-18": [  # elicitation.md, changelog
        ("Nella 2026-07-28 la URL mode ha solo mode, message e url: elicitationId e notifications/elicitation/complete sono stati rimossi (con -32042).",
         "In 2026-07-28 URL mode has only mode, message and url: elicitationId and notifications/elicitation/complete were removed (along with -32042)."),
        ("Lo schema form supporta string, number, integer, boolean ed enum a scelta singola o multipla; decline e cancel non sono errori.",
         "The form schema supports string, number, integer, boolean and single or multi select enums; decline and cancel are not errors."),
    ],
    "D3-19": [  # deprecated.md, logging.md
        ("Rimozione più precoce di roots, sampling, logging e DCR: prima revisione dal 2027-07-28. includeContext thisServer/allServers è deprecato dalla 2025-11-25.",
         "Earliest removal of roots, sampling, logging and DCR: first revision on or after 2027-07-28. includeContext thisServer/allServers has been deprecated since 2025-11-25."),
        ("roots/list e sampling/createMessage restano validi come voci di inputRequests MRTR, se il client dichiara la capability.",
         "roots/list and sampling/createMessage stay valid as MRTR inputRequests entries, if the client declares the capability."),
        ("logLevel per richiesta: notifications/message solo sullo stream di quella richiesta, al livello richiesto o superiore, finché è in corso.",
         "Per-request logLevel: notifications/message only on that request's own stream, at or above the requested level, while it is in flight."),
        ("Rimossi del tutto anche resources/subscribe e resources/unsubscribe (si usa subscriptions/listen).",
         "Also removed entirely: resources/subscribe and resources/unsubscribe (use subscriptions/listen)."),
    ],
    # ---------------- D4 ----------------
    "D4-01": [  # security best practices
        ("Contenuti non fidati che arrivano al modello: nome, descrizione, icone e annotations dei tool, risultati, contenuti delle risorse, instructions.",
         "Untrusted content reaching the model: tool names, descriptions, icons and annotations, results, resource contents, instructions."),
        ("Un'istruzione contenuta nell'output di un server non giustifica da sola una chiamata ai tool di un altro server.",
         "An instruction inside one server's output does not by itself justify a call to another server's tools."),
    ],
    "D4-04": [  # authorization-server-discovery.md
        ("Issuer con path (https://auth.example.com/tenant1): 1) /.well-known/oauth-authorization-server/tenant1, 2) /.well-known/openid-configuration/tenant1, 3) /tenant1/.well-known/openid-configuration.",
         "Issuer with a path (https://auth.example.com/tenant1): 1) /.well-known/oauth-authorization-server/tenant1, 2) /.well-known/openid-configuration/tenant1, 3) /tenant1/.well-known/openid-configuration."),
        ("Issuer senza path: prima /.well-known/oauth-authorization-server, poi /.well-known/openid-configuration. Se l'issuer del documento non coincide, MUST NOT usarlo.",
         "Issuer with no path: first /.well-known/oauth-authorization-server, then /.well-known/openid-configuration. If the document's issuer does not match, it MUST NOT be used."),
    ],
    "D4-05": [  # authorization/index
        ("Il client SHOULD limitare i tentativi di step-up e tracciarli, per evitare cicli infiniti.",
         "The client SHOULD limit and track step-up attempts to avoid infinite loops."),
        ("Una lista di tool che dipende dagli scope del chiamante va in cache come private.",
         "A tool list that depends on the caller's scopes is cached as private."),
    ],
    "D4-06": [  # client-registration.md, SEP-991, SEP-837
        ("Il client_id nel documento CIMD deve coincidere esattamente con l'URL da cui è stato scaricato; l'AS deve proteggersi da SSRF quando lo scarica.",
         "The client_id in the CIMD must exactly match the URL it was fetched from; the AS must guard against SSRF when fetching it."),
        ("DCR application_type: native per app desktop, mobile, CLI e app locali su localhost; web per app nel browser. Serve perché gli AS che assumevano web rifiutavano i redirect localhost (SEP-837).",
         "DCR application_type: native for desktop, mobile, CLI and localhost apps; web for browser apps. It exists because ASs defaulting to web rejected localhost redirects (SEP-837)."),
    ],
    "D4-08": [  # authorization/index
        ("La verifica di iss vale anche per le risposte di errore: se non coincide, il client MUST NOT usare né mostrare error, error_description o error_uri.",
         "The iss check also applies to error responses: on mismatch the client MUST NOT act on or display error, error_description or error_uri."),
        ("URI canonico per resource: scheme e host minuscoli, senza fragment (es. https://mcp.example.com/mcp); per robustezza si accettano anche maiuscole.",
         "Canonical URI for resource: lowercase scheme and host, no fragment (e.g. https://mcp.example.com/mcp); uppercase is accepted for robustness."),
    ],
    "D4-09": [
        ("Un token valido e non scaduto ma emesso per un'altra audience va rifiutato con 401.",
         "A valid, unexpired token issued for another audience is rejected with 401."),
    ],
    "D4-12": [  # mrtr.md security
        ("requestState va legato a tre cose, verificate a ogni retry: principal autenticato (non clientInfo), scadenza breve, e metodo più digest dei parametri della richiesta originale.",
         "requestState is bound to three things, checked on every retry: the authenticated principal (not clientInfo), a short expiry, and the method plus a digest of the original request's parameters."),
        ("Firma e scadenza non bastano contro il replay di un token ancora valido: l'uso singolo va imposto lato server.",
         "Signature and expiry alone do not stop replay of a still-valid token: single use must be enforced server-side."),
    ],
    "D4-13": [  # W3C Trace Context, SEP-414
        ("traceparent (W3C): versione (2 hex) - trace id (32 hex) - parent id (16 hex) - flags (2 hex); id tutti a zero non validi.",
         "traceparent (W3C): version (2 hex) - trace id (32 hex) - parent id (16 hex) - flags (2 hex); all-zero ids are invalid."),
        ("A ogni salto si mantiene il trace id e si genera un nuovo parent id: il trace id è il valore che collega i log di servizi diversi.",
         "At every hop the trace id is kept and a new parent id is minted: the trace id is what joins logs across services."),
        ("Un record di audit registra chi (principal autenticato), cosa (argomenti sensibili oscurati prima della scrittura), quando, esito (complete, isError o errore di protocollo) e correlazione.",
         "An audit record captures who (authenticated principal), what (sensitive arguments redacted before writing), when, outcome (complete, isError or protocol error) and correlation."),
    ],
    "D4-14": [  # ext-auth EMA
        ("Flusso EMA: il client scambia l'ID token SSO con un ID-JAG presso l'IdP aziendale, poi scambia l'ID-JAG con un access token MCP presso l'AS del server.",
         "EMA flow: the client exchanges the SSO ID token for an ID-JAG at the enterprise IdP, then exchanges the ID-JAG for an MCP access token at the server's AS."),
    ],
    "D4-15": [  # sep-guidelines, SEP-2484
        ("Quattro tipi di SEP: Standards Track, Informational, Process, Extensions Track.",
         "Four SEP types: Standards Track, Informational, Process, Extensions Track."),
        ("Stati SEP: draft, in-review, accepted, final; altri esiti rejected, withdrawn, dormant, superseded. Final richiede testo della spec, implementazione di riferimento e test di conformità.",
         "SEP states: draft, in-review, accepted, final; other outcomes rejected, withdrawn, dormant, superseded. Final requires spec text, a reference implementation and conformance tests."),
    ],
    # ---------------- D5 ----------------
    "D5-01": [
        ("Lo stesso MUST può cambiare responsabile con la forma del deployment: la validazione di Origin spetta all'autore del server, ma dietro un gateway spetta all'operatore del gateway.",
         "The same MUST can change owner with the deployment shape: Origin validation belongs to the server author, but behind a gateway it belongs to the gateway operator."),
    ],
    "D5-04": [  # streamable-http, caching
        ("Ordine in un gateway: controllare _meta, confrontare header e body (-32020 se diversi), instradare sull'header, autorizzare, inoltrare una richiesta nuova senza il token del chiamante, restituire resultType, ttlMs e cacheScope invariati.",
         "Gateway order: check _meta, compare headers with body (-32020 if different), route on the header, authorize, forward a fresh request without the caller's token, return resultType, ttlMs and cacheScope unchanged."),
    ],
    "D5-06": [  # community/sdk-tiers
        ("Tier 2: triage entro un mese, bug critici entro due settimane, almeno un rilascio stabile. Tier 1: rilascio stabile e roadmap pubblicata obbligatori.",
         "Tier 2: triage within a month, critical bugs within two weeks, at least one stable release. Tier 1: stable release and published roadmap required."),
        ("Retrocessione Tier 2 → 3 se oltre il 20% dei test di conformità fallisce per 4 settimane; anche issue ignorate per due mesi possono causarla.",
         "Tier 2 → 3 relegation if more than 20% of conformance tests fail for 4 weeks; issues left unaddressed for two months can also trigger it."),
    ],
    "D5-07": [  # registry docs
        ("packages: npm, PyPI, NuGet, Cargo, OCI, MCPB; remotes: streamable-http o sse (deprecato). Possono coesistere nella stessa voce.",
         "packages: npm, PyPI, NuGet, Cargo, OCI, MCPB; remotes: streamable-http or sse (deprecated). Both can be on one entry."),
        ("Proprietà per PyPI e NuGet: stringa mcp-name nel README. Il $schema di server.json (es. 2025-12-11) è la versione del formato dei metadati, non la versione del protocollo MCP.",
         "Ownership for PyPI and NuGet: mcp-name string in the README. server.json's $schema (e.g. 2025-12-11) is the metadata format version, not the MCP protocol version."),
        ("Il registry non scansiona il codice: delega la sicurezza ai registri dei pacchetti e agli aggregatori. In preview sono possibili reset dei dati.",
         "The registry does not scan code: it delegates security to package registries and aggregators. During preview, data resets are possible."),
    ],
}

NEW_TOPICS = {
    "D5": [{
        "after": "D5-08",
        "topic": {
            "id": "D5-15",
            "title": {"it": "MCP Apps nel dettaglio", "en": "MCP Apps in detail"},
            "summary": {
                "it": "L'estensione io.modelcontextprotocol/ui permette a un tool di indicare un'interfaccia HTML che l'host mostra in un iframe sandbox. Le regole su mimeType, visibility, CSP e permessi sono frequenti nelle domande di scenario.",
                "en": "The io.modelcontextprotocol/ui extension lets a tool point at an HTML interface that the host renders in a sandboxed iframe. The rules on mimeType, visibility, CSP and permissions come up often in scenario questions.",
            },
            "points": {
                "it": [
                    "Il tool indica la UI con _meta.ui.resourceUri (risorsa ui://), letta con una normale resources/read.",
                    "mimeType MUST essere text/html;profile=mcp-app: un semplice text/html non è un'app.",
                    "_meta.ui.visibility vale [\"model\", \"app\"] se omesso. Senza \"model\" l'host MUST NOT mostrare il tool nella lista del modello; senza \"app\" l'app non può chiamarlo.",
                    "_meta.ui.csp è un oggetto con connectDomains, resourceDomains, frameDomains e baseUriDomains. Senza frameDomains vale frame-src 'none'; senza baseUriDomains vale base-uri 'self'.",
                    "_meta.ui.permissions (camera, microphone, geolocation, clipboardWrite): l'host MAY concederli con l'attributo allow dell'iframe; l'app SHOULD NOT darli per scontati.",
                    "Un host web MUST passare da un sandbox proxy su un'origine diversa; app e host comunicano via postMessage con metodi ui/ (es. ui/initialize, che non è l'initialize rimosso dal core).",
                    "Il tool restituisce sempre anche un content testuale: un host senza l'estensione usa quello e non legge mai la risorsa ui://.",
                ],
                "en": [
                    "The tool points at the UI with _meta.ui.resourceUri (a ui:// resource), read with an ordinary resources/read.",
                    "mimeType MUST be text/html;profile=mcp-app: plain text/html is not an app.",
                    "_meta.ui.visibility defaults to [\"model\", \"app\"]. Without \"model\" the host MUST NOT show the tool in the model's list; without \"app\" the app cannot call it.",
                    "_meta.ui.csp is an object with connectDomains, resourceDomains, frameDomains and baseUriDomains. Without frameDomains, frame-src is 'none'; without baseUriDomains, base-uri is 'self'.",
                    "_meta.ui.permissions (camera, microphone, geolocation, clipboardWrite): the host MAY grant them through the iframe allow attribute; the app SHOULD NOT assume they are granted.",
                    "A web host MUST go through a sandbox proxy on a different origin; app and host talk via postMessage with ui/ methods (e.g. ui/initialize, which is not the initialize removed from the core).",
                    "The tool always also returns text content: a host without the extension uses that and never reads the ui:// resource.",
                ],
            },
            "source": {"label": "MCP Apps spec 2026-01-26", "url": "https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx"},
        },
    }],
}


def main():
    added = 0
    for D in ["D1", "D2", "D3", "D4", "D5"]:
        p = os.path.join(CONTENT, f"course-{D}.json")
        c = json.load(open(p, encoding="utf-8"))
        ids = [t["id"] for t in c["topics"]]
        for nt in NEW_TOPICS.get(D, []):
            if nt["topic"]["id"] not in ids:
                i = ids.index(nt["after"]) + 1
                c["topics"].insert(i, nt["topic"])
                ids.insert(i, nt["topic"]["id"])
                added += len(nt["topic"]["points"]["en"])
        for t in c["topics"]:
            for it, en in POINTS.get(t["id"], []):
                if en not in t["points"]["en"]:
                    t["points"]["it"].append(it)
                    t["points"]["en"].append(en)
                    added += 1
        json.dump(c, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    missing = set(POINTS) - {t for D in "D1 D2 D3 D4 D5".split() for t in [x["id"] for x in json.load(open(os.path.join(CONTENT, f"course-{D}.json"), encoding="utf-8"))["topics"]]}
    print("points added:", added, "unknown topic ids:", sorted(missing))


if __name__ == "__main__":
    main()
