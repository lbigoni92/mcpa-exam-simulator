"""Domande originali sui fatti verificati che l'analisi di copertura del 2026-11-22 ha trovato scoperti.
Fonti: spec 2026-07-28 locale (sources/spec-2026-07-28), docs/learn, community/design-principles.md,
docs/tutorials/security/local-server-security.md, registry/, extensions/.
Scrive content/questions-hard-gaps.json. Uso: python3 site/build/gen_gaps.py"""
import json, os
OUT = os.path.join(os.path.dirname(__file__), "..", "content", "questions-hard-gaps.json")
qs = []; cnt = {}


def A(t, q, o, c, x, d=2):
    dom = t[:2]; cnt[dom] = cnt.get(dom, 0) + 1
    qs.append({"id": f"o-G-{dom}-{cnt[dom]:02d}", "t": t, "d": d if len(c) == 1 else 3, "type": "multi" if len(c) > 1 else "single",
               "q": {"it": q[0], "en": q[1]}, "o": [{"it": a, "en": b} for a, b in o], "c": c, "x": {"it": x[0], "en": x[1]}})


# ---------------- D1 ----------------
A("D1-09", ("Una SEP propone un secondo meccanismo di autorizzazione, alternativo a quello esistente, \"per dare più scelta agli implementatori\". Quale principio di design del progetto gioca contro?",
            "A SEP proposes a second authorization mechanism, alternative to the existing one, \"to give implementers more choice\". Which project design principle argues against it?"),
  [("Pragmatism over purity", "Pragmatism over purity"),
   ("Demonstration over deliberation", "Demonstration over deliberation"),
   ("Convergence over choice", "Convergence over choice"),
   ("Capability over compensation", "Capability over compensation")], [2],
  ("Convergence over choice: in MCP ci dovrebbe essere un solo modo di risolvere un problema; più approcci paralleli frammentano l'ecosistema. Le estensioni sono il posto dove si mette alla prova la convergenza, la spec dove la si consolida.",
   "Convergence over choice: there should be one way to solve a problem in MCP; several parallel approaches fragment the ecosystem. Extensions are where convergence gets tested, the specification is where it gets committed."))
A("D1-09", ("Perché, secondo i design principles del progetto, un \"no\" a una nuova feature è spesso preferibile a un \"sì\"?",
            "Why, according to the project design principles, is a \"no\" to a new feature often preferable to a \"yes\"?"),
  [("Ogni aggiunta è un impegno permanente, mentre un no lascia la porta aperta", "Every addition is a permanent commitment, while a no leaves the door open"),
   ("Le feature nuove devono prima passare 12 mesi nello stato Deprecated", "New features must first spend 12 months in the Deprecated state"),
   ("Solo l'AAIF può approvare feature nuove, i maintainer possono solo rifiutare", "Only AAIF can approve new features, maintainers can only reject"),
   ("Le feature nuove rompono sempre la retrocompatibilità con la Current", "New features always break backward compatibility with the Current revision")], [0],
  ("Stability over velocity: aggiungere a un protocollo molto adottato è facile, togliere è quasi impossibile. Ogni aggiunta è permanente e ha un costo per chi implementa i client; le rimozioni seguono la Feature Lifecycle policy.",
   "Stability over velocity: adding to a widely adopted protocol is easy, removing is nearly impossible. Every addition is permanent and costs client implementers; removals follow the Feature Lifecycle policy."))
A("D1-09", ("Quali affermazioni sui design principles del progetto MCP sono corrette? (scegli 2)",
            "Which statements about the MCP project design principles are correct? (choose 2)"),
  [("Quando due principi sono in conflitto si bilanciano, non c'è una gerarchia", "When two principles conflict they are weighed, there is no ranking"),
   ("Sono gli stessi design principles architetturali descritti nella spec", "They are the same architectural design principles described in the spec"),
   ("I pattern nuovi conviene sperimentarli prima nelle estensioni", "New patterns are best tried in extensions first"),
   ("Valgono per i server, non per le SEP o le estensioni", "They apply to servers, not to SEPs or extensions")], [0, 2],
  ("I principi guidano la valutazione di SEP ed estensioni, sono distinti dai design principles architetturali della spec e in caso di conflitto si bilanciano senza ordine. Standardization over innovation: si standardizzano pattern già provati, quelli nuovi si provano nelle estensioni.",
   "The principles guide how SEPs and extensions are evaluated, are distinct from the spec's architectural design principles, and when they conflict they are weighed, not ranked. Standardization over innovation: proven patterns get standardized, new ones are tried in extensions."))
A("D1-01", ("Nel testo della spec una frase dice che il client \"should retry later\", in minuscolo. Che valore normativo ha?",
            "A sentence in the spec text says the client \"should retry later\", in lowercase. What normative weight does it have?"),
  [("È equivalente a SHOULD secondo RFC 2119", "It is equivalent to SHOULD under RFC 2119"),
   ("È equivalente a MAY, perché è in minuscolo", "It is equivalent to MAY, because it is lowercase"),
   ("È un MUST implicito, perché riguarda il client", "It is an implicit MUST, because it concerns the client"),
   ("Nessuno: le parole chiave BCP 14 valgono solo in maiuscolo", "None: BCP 14 keywords only apply in all capitals")], [3],
  ("La spec interpreta MUST, SHOULD, MAY e simili come in BCP 14 (RFC 2119 e RFC 8174) solo quando sono scritte tutte in maiuscolo. In minuscolo sono parole normali.",
   "The spec interprets MUST, SHOULD, MAY and the like as in BCP 14 (RFC 2119 and RFC 8174) only when they appear in all capitals. In lowercase they are ordinary words."))
A("D1-06", ("Una revisione della spec è descritta come \"passata, completa, non verrà più modificata\". In che stato si trova?",
            "A spec revision is described as \"past, complete, will not be changed\". Which state is it in?"),
  [("Draft", "Draft"),
   ("Final", "Final"),
   ("Current", "Current"),
   ("Deprecated", "Deprecated")], [1],
  ("Le revisioni hanno tre stati: Draft (in lavorazione, non pronta), Current (la versione in uso, può ricevere modifiche retrocompatibili) e Final (passata e completa, non cambia più). Deprecated è uno stato delle feature, non delle revisioni.",
   "Revisions have three states: Draft (in progress, not ready), Current (in use, may receive backward-compatible changes) and Final (past and complete, never changes). Deprecated is a feature state, not a revision state."))
A("D1-03", ("Quali di questi aspetti appartengono al transport layer di MCP? (scegli 2)",
            "Which of these belong to MCP's transport layer? (choose 2)"),
  [("Il framing dei messaggi sul canale", "Message framing on the channel"),
   ("La discovery di capability e versione", "Capability and version discovery"),
   ("L'autorizzazione della connessione", "Authorization of the connection"),
   ("Le primitive tools, resources e prompts", "The tools, resources and prompts primitives")], [0, 2],
  ("Il data layer (strato interno) definisce il protocollo JSON-RPC: discovery di capability e versione, primitive e notifiche. Il transport layer (strato esterno) definisce canali, framing dei messaggi e autorizzazione.",
   "The data layer (inner) defines the JSON-RPC protocol: capability and version discovery, primitives and notifications. The transport layer (outer) defines channels, message framing and authorization."))

# ---------------- D2 ----------------
A("D2-05", ("Quali valori devono essere inviati in un header Mcp-Param-* con la codifica =?base64?...?=? (scegli 2)",
            "Which values must be sent in an Mcp-Param-* header with the =?base64?...?= encoding? (choose 2)"),
  [("La stringa \"us-west1\"", "The string \"us-west1\""),
   ("La stringa \"Città di Milano\"", "The string \"Città di Milano\""),
   ("La stringa \" padded \" con spazi iniziali e finali", "The string \" padded \" with leading and trailing spaces"),
   ("Il numero intero 42", "The integer 42")], [1, 2],
  ("Vanno codificati in Base64 i valori non sicuri per un header: caratteri non ASCII, spazi iniziali o finali, caratteri di controllo come i newline, e anche un testo ASCII che somiglia al marcatore =?base64?...?=. \"us-west1\" e 42 passano in chiaro.",
   "Values unsafe for a header must be Base64-encoded: non-ASCII characters, leading or trailing spaces, control characters such as newlines, and also ASCII text that looks like the =?base64?...?= marker. \"us-west1\" and 42 go in plain text."))
A("D2-05", ("Un server riceve Mcp-Name: =?base64?Y2VyY2E=?= e nel corpo params.name vale \"cerca\". Cosa deve fare?",
            "A server receives Mcp-Name: =?base64?Y2VyY2E=?= and params.name in the body is \"cerca\". What must it do?"),
  [("Rispondere 400 HeaderMismatch, perché le due stringhe sono diverse", "Answer 400 HeaderMismatch, because the two strings differ"),
   ("Decodificare l'header e poi confrontarlo con il corpo: qui coincidono", "Decode the header and then compare it with the body: here they match"),
   ("Ignorare l'header, perché i nomi dei tool non vanno mai codificati", "Ignore the header, because tool names are never encoded"),
   ("Rispondere 400, perché il marcatore deve essere in maiuscolo", "Answer 400, because the marker must be uppercase")], [1],
  ("Il server MUST decodificare un Mcp-Name o Mcp-Param-* codificato prima di confrontarlo con il valore nel corpo. I marcatori =?base64? e ?= sono case-sensitive e vanno in minuscolo. Y2VyY2E= è \"cerca\", quindi non c'è mismatch.",
   "The server MUST decode an encoded Mcp-Name or Mcp-Param-* before comparing it with the body value. The =?base64? and ?= markers are case-sensitive and lowercase. Y2VyY2E= is \"cerca\", so there is no mismatch."))
A("D2-04", ("Che cosa deve contenere l'header Accept di un POST JSON-RPC su Streamable HTTP?",
            "What must the Accept header of a JSON-RPC POST over Streamable HTTP contain?"),
  [("Solo application/json, perché la risposta è un singolo oggetto", "Only application/json, because the response is a single object"),
   ("Solo text/event-stream, perché ogni risposta è uno stream SSE", "Only text/event-stream, because every response is an SSE stream"),
   ("application/json e text/event-stream, e il client deve gestirli entrambi", "application/json and text/event-stream, and the client must handle both"),
   ("application/json-rpc, il tipo registrato per MCP", "application/json-rpc, the type registered for MCP")], [2],
  ("Il client MUST elencare sia application/json sia text/event-stream. Per una richiesta il server sceglie se rispondere con un singolo oggetto JSON o con uno stream SSE dedicato a quella richiesta, e il client MUST supportare entrambi.",
   "The client MUST list both application/json and text/event-stream. For a request the server chooses between a single JSON object and an SSE stream scoped to that request, and the client MUST support both."))
A("D2-13", ("Quale di questi nomi di tool rispetta tutte le raccomandazioni (SHOULD) della spec?",
            "Which of these tool names follows all the spec's recommendations (SHOULD)?"),
  [("get user", "get user"),
   ("export,csv", "export,csv"),
   ("admin.tools.list", "admin.tools.list"),
   ("ricerca-città", "ricerca-città")], [2],
  ("Nomi da 1 a 128 caratteri, case-sensitive, solo lettere ASCII, cifre, underscore, trattino e punto; niente spazi, virgole o altri caratteri speciali. \"admin.tools.list\" è proprio uno degli esempi validi della spec; \"à\" non è ASCII.",
   "Names of 1 to 128 characters, case-sensitive, only ASCII letters, digits, underscore, hyphen and dot; no spaces, commas or other special characters. \"admin.tools.list\" is one of the spec's valid examples; \"à\" is not ASCII."))
A("D2-01", ("Secondo l'architettura della spec, chi gestisce le decisioni di autorizzazione dell'utente e aggrega il contesto tra più server?",
            "According to the spec architecture, who handles the user's authorization decisions and aggregates context across servers?"),
  [("Ogni client, per il proprio server", "Each client, for its own server"),
   ("L'host", "The host"),
   ("Il server più privilegiato tra quelli collegati", "The most privileged connected server"),
   ("L'authorization server OAuth", "The OAuth authorization server")], [1],
  ("L'host crea e gestisce i client, applica le policy di sicurezza e di consenso, gestisce le decisioni di autorizzazione dell'utente, coordina l'LLM e aggrega il contesto. Ogni client parla con un solo server, allega versione e capability a ogni richiesta e mantiene i confini tra server.",
   "The host creates and manages clients, enforces security and consent policies, handles the user's authorization decisions, coordinates the LLM and aggregates context. Each client talks to exactly one server, attaches version and capabilities to every request and keeps boundaries between servers."))
A("D2-12", ("Quali meccanismi suggerisce la documentazione MCP per mantenere il controllo umano sui tools? (scegli 2)",
            "Which mechanisms does the MCP documentation suggest to keep human control over tools? (choose 2)"),
  [("Un dialog di approvazione per la singola esecuzione", "An approval dialog for each individual execution"),
   ("Un activity log con tutte le esecuzioni e i loro risultati", "An activity log with all executions and their results"),
   ("Un picker ad albero obbligatorio imposto dal protocollo", "A mandatory tree picker imposed by the protocol"),
   ("La sostituzione del modello con un elenco statico di tool", "Replacing the model with a static list of tools")], [0, 1],
  ("I tools sono controllati dal modello, ma l'applicazione può offrire: scelta dei tool disponibili, dialog di approvazione per singola esecuzione, permessi per pre-approvare operazioni sicure e activity log. Il protocollo non impone una UI specifica.",
   "Tools are model-controlled, but the application can offer: choosing which tools are available, approval dialogs per execution, permissions to pre-approve safe operations and activity logs. The protocol does not mandate a specific UI."))

# ---------------- D3 ----------------
A("D3-10", ("Un client invia una notifica JSON-RPC via POST e il server la accetta. Cosa risponde il server?",
            "A client sends a JSON-RPC notification via POST and the server accepts it. What does the server answer?"),
  [("200 OK con una risposta JSON-RPC vuota", "200 OK with an empty JSON-RPC response"),
   ("204 No Content", "204 No Content"),
   ("200 OK con uno stream SSE aperto", "200 OK with an open SSE stream"),
   ("202 Accepted senza body", "202 Accepted with no body")], [3],
  ("Per una notifica accettata il server MUST rispondere 202 Accepted senza body. Le notifiche non hanno risposta JSON-RPC.",
   "For an accepted notification the server MUST answer 202 Accepted with no body. Notifications have no JSON-RPC response."))
A("D3-10", ("Il server non può accettare una notifica ricevuta via POST. Quale risposta è conforme?",
            "The server cannot accept a notification received via POST. Which answer complies?"),
  [("Uno status di errore HTTP, ad esempio 400, con un eventuale errore JSON-RPC senza id", "An HTTP error status, e.g. 400, optionally with a JSON-RPC error that has no id"),
   ("202 Accepted subito, e poi l'errore inviato più tardi su un nuovo stream GET dedicato", "202 Accepted right away, then the error sent later on a new dedicated GET stream"),
   ("200 OK con un errore JSON-RPC che riporta l'id della notifica", "200 OK with a JSON-RPC error carrying the notification's id"),
   ("Nessuna risposta HTTP: le notifiche rifiutate si scartano in silenzio senza status", "No HTTP response: rejected notifications are silently dropped with no status")], [0],
  ("Se non accetta la notifica, il server MUST restituire uno status di errore HTTP (ad esempio 400). Il body MAY contenere una risposta di errore JSON-RPC senza id, perché le notifiche non hanno id. Nella 2026-07-28 non esistono stream GET.",
   "If it cannot accept the notification, the server MUST return an HTTP error status (e.g. 400). The body MAY contain a JSON-RPC error response with no id, because notifications have no id. In 2026-07-28 there are no GET streams."))
A("D3-17", ("Un client chiede suggerimenti per l'argomento di un prompt chiamato code_review. Quale riferimento usa in completion/complete?",
            "A client asks for suggestions for an argument of a prompt named code_review. Which reference does it use in completion/complete?"),
  [("{\"type\": \"ref/tool\", \"name\": \"code_review\"}", "{\"type\": \"ref/tool\", \"name\": \"code_review\"}"),
   ("{\"type\": \"ref/prompt\", \"name\": \"code_review\"}", "{\"type\": \"ref/prompt\", \"name\": \"code_review\"}"),
   ("{\"type\": \"ref/resource\", \"name\": \"code_review\"}", "{\"type\": \"ref/resource\", \"name\": \"code_review\"}"),
   ("{\"type\": \"ref/argument\", \"uri\": \"code_review\"}", "{\"type\": \"ref/argument\", \"uri\": \"code_review\"}")], [1],
  ("Esistono due tipi di riferimento: ref/prompt (un prompt per nome) e ref/resource (un URI o un URI template). La completion non si applica ai tool.",
   "There are two reference types: ref/prompt (a prompt by name) and ref/resource (a URI or URI template). Completion does not apply to tools."))
A("D3-17", ("Per un argomento ci sono 350 valori possibili. Cosa restituisce al massimo il server in una risposta di completion?",
            "An argument has 350 possible values. What does the server return at most in one completion response?"),
  [("Tutti i 350 valori, ordinati per rilevanza", "All 350 values, ranked by relevance"),
   ("Un cursor per paginare i valori con completion/list", "A cursor to page through values with completion/list"),
   ("Fino a 100 valori, con il totale opzionale e un flag di altri risultati", "Up to 100 values, with an optional total and a more-results flag"),
   ("Solo il valore più probabile, come fa l'autocompletamento", "Only the most likely value, like autocomplete")], [2],
  ("La risposta contiene un array di valori ordinati per rilevanza, con un massimo di 100 elementi, il numero totale opzionale e un booleano che indica se ci sono altri risultati.",
   "The response contains an array of values ranked by relevance, at most 100 items, an optional total and a boolean saying whether more results exist."))
A("D3-18", ("Durante una elicitation l'utente chiude il dialog con Esc senza scegliere. Quale action restituisce il client?",
            "During an elicitation the user closes the dialog with Escape without choosing. Which action does the client return?"),
  [("decline, con content vuoto", "decline, with empty content"),
   ("accept, con i valori di default dello schema", "accept, with the schema's default values"),
   ("Un errore JSON-RPC -32800", "A JSON-RPC error -32800"),
   ("cancel, di solito senza content", "cancel, usually without content")], [3],
  ("Tre azioni: accept (l'utente approva e invia i dati), decline (rifiuta esplicitamente, es. \"No\") e cancel (chiude senza una scelta esplicita: Esc, clic fuori, dialog chiuso). Il server dovrebbe gestire cancel ad esempio richiedendo più tardi.",
   "Three actions: accept (the user approves and submits data), decline (explicitly rejects, e.g. \"No\") and cancel (dismisses without an explicit choice: Escape, click outside, dialog closed). The server should handle cancel e.g. by asking again later."))
A("D3-18", ("Quali formati può avere una proprietà string nel requestedSchema di una elicitation in form mode? (scegli 2)",
            "Which formats can a string property have in a form-mode elicitation requestedSchema? (choose 2)"),
  [("email", "email"),
   ("phone", "phone"),
   ("date-time", "date-time"),
   ("ipv4", "ipv4")], [0, 2],
  ("Per le stringhe la spec ammette i formati email, uri, date e date-time. Lo schema è piatto e contiene solo primitive.",
   "For strings the spec allows the email, uri, date and date-time formats. The schema is flat and contains only primitives."))
A("D3-18", ("Una richiesta di elicitation non specifica il campo mode. Come va interpretata?",
            "An elicitation request does not set the mode field. How should it be interpreted?"),
  [("Come form mode", "As form mode"),
   ("Come url mode", "As url mode"),
   ("Come richiesta non valida: mode è obbligatorio", "As an invalid request: mode is required"),
   ("Il client sceglie liberamente il mode", "The client freely picks the mode")], [0],
  ("mode vale form o url ed è opzionale per il form mode: se manca vale \"form\". Allo stesso modo, la capability elicitation: {} equivale al supporto del solo form mode.",
   "mode is form or url and is optional for form mode: when omitted it defaults to \"form\". Likewise, the elicitation: {} capability means form mode only."))
A("D3-11", ("Un tool ha name \"db_query\", annotations.title \"Query DB\" e title \"Esegui query\". Quale nome dovrebbe mostrare il client all'utente?",
            "A tool has name \"db_query\", annotations.title \"Query DB\" and title \"Run query\". Which name should the client show the user?"),
  [("db_query, perché name è l'identificativo stabile e va sempre mostrato", "db_query, because name is the stable identifier and must always be shown"),
   ("Query DB, perché le annotations hanno la precedenza", "Query DB, because annotations take precedence"),
   ("Esegui query, perché title viene prima di annotations.title e di name", "Run query, because title comes before annotations.title and name"),
   ("Tutti e tre insieme, separati da una barra, perché nessuno ha la precedenza", "All three together, separated by a slash, because none takes precedence")], [2],
  ("L'ordine di precedenza per il display name dei tool è: title, poi annotations.title, poi name. name resta l'identificativo usato in tools/call.",
   "The display name precedence for tools is: title, then annotations.title, then name. name remains the identifier used in tools/call."))
A("D3-15", ("Una resource ha annotations audience [\"user\"] e priority 1.0. Cosa comunica?",
            "A resource has annotations audience [\"user\"] and priority 1.0. What does it convey?"),
  [("È destinata all'utente ed è la più importante, in pratica necessaria", "It is meant for the user and is the most important, effectively required"),
   ("È destinata al modello e va inclusa sempre nel prompt", "It is meant for the model and must always be in the prompt"),
   ("Può essere letta solo da utenti autenticati con priorità alta", "Only authenticated users with high priority can read it"),
   ("Il server la invierà per prima nelle notifiche di aggiornamento", "The server will send it first in update notifications")], [0],
  ("Le annotations sono suggerimenti per il client: audience indica a chi serve (user, assistant o entrambi), priority va da 0 (del tutto opzionale) a 1 (la più importante, in pratica necessaria), lastModified è un timestamp ISO 8601. Non sono controlli di accesso.",
   "Annotations are hints for the client: audience says who it is for (user, assistant or both), priority goes from 0 (entirely optional) to 1 (most important, effectively required), lastModified is an ISO 8601 timestamp. They are not access controls."))

# ---------------- D4 ----------------
A("D4-18", ("L'autore di un server locale è onesto, ma un pacchetto nel suo albero di dipendenze viene compromesso. Quale contromisura protegge davvero da questo caso?",
            "A local server's author is honest, but a package in its dependency tree gets compromised. Which countermeasure really protects against this case?"),
  [("Fissare la versione del pacchetto principale con npx o uvx", "Pinning the top-level package version with npx or uvx"),
   ("Fissare l'immagine container per digest (image@sha256:...)", "Pinning the container image by digest (image@sha256:...)"),
   ("Controllare che il nome del pacchetto non sia un typosquat", "Checking that the package name is not a typosquat"),
   ("Approvare il server una sola volta al primo avvio", "Approving the server once at first launch")], [1],
  ("Con npx o uvx il pin fissa solo il pacchetto principale: le dipendenze transitive si risolvono di nuovo all'installazione, ed è lì che arriva una dipendenza compromessa. Un'immagine fissata per digest congela tutto l'albero.",
   "With npx or uvx the pin fixes only the top-level package: transitive dependencies are resolved fresh at install time, which is exactly where a compromised dependency arrives. An image pinned by digest freezes the whole tree."))
A("D4-18", ("Un server locale ha firme verificate, un SBOM e compare in un catalogo curato. Cosa garantiscono questi segnali?",
            "A local server has verified signatures, an SBOM and appears in a curated catalog. What do these signals guarantee?"),
  [("Che il server non esfiltrerà dati", "That the server will not exfiltrate data"),
   ("Che il catalogo si assume la responsabilità di ciò che esegui", "That the catalog takes responsibility for what you run"),
   ("Che si può saltare la sandbox", "That the sandbox can be skipped"),
   ("Di chi ti stai fidando, non che la fiducia sia meritata", "Who you are trusting, not that the trust is warranted")], [3],
  ("Nessun controllo prova cosa farà un server. Provenienza (repository, firme, SBOM, listing curati) dice di chi ti fidi; il contenimento (privilegi minimi, sandbox) decide quanto costa una scelta sbagliata. I cataloghi curati descrivono il loro vetting come best-effort.",
   "No check proves what a server will do. Provenance (repository, signatures, SBOM, curated listings) tells you who you are trusting; containment (least privilege, sandbox) decides what a bad choice costs. Curated catalogs describe their vetting as best-effort."))
A("D4-16", ("La descrizione di un tool del server A contiene istruzioni nascoste su come usare il tool send_email del server B. Il tool di A non viene mai chiamato. Quali affermazioni sono corrette? (scegli 2)",
            "A tool description on server A hides instructions on how to use server B's send_email tool. A's tool is never called. Which statements are correct? (choose 2)"),
  [("L'attacco può funzionare anche se il tool di A non viene mai invocato", "The attack can work even though A's tool is never invoked"),
   ("Non è un rischio: i server sono isolati e non vedono i tool degli altri", "It is not a risk: servers are isolated and cannot see each other's tools"),
   ("È un caso di tool shadowing, una forma di tool poisoning", "It is a case of tool shadowing, a form of tool poisoning"),
   ("Un pin della versione del server A lo impedisce in modo definitivo", "Pinning server A's version prevents it for good")], [0, 2],
  ("Nomi e descrizioni dei tool sono istruzioni lette dal modello: un catalogo avvelenato orienta l'agente senza che il tool venga chiamato, anche sui tool di altri server (tool shadowing). Tutti i server condividono il contesto del modello, e le definizioni possono cambiare dopo l'approvazione (rug pull), quindi pin e consenso iniziale non bastano.",
   "Tool names and descriptions are instructions the model reads: a poisoned catalog steers the agent without the tool being called, including on other servers' tools (tool shadowing). All servers share the model context, and definitions can change after approval (rug pull), so pinning and one-time consent are not enough."))
A("D4-08", ("Quale valore del parametro resource identifica correttamente un server MCP secondo la spec?",
            "Which resource parameter value correctly identifies an MCP server according to the spec?"),
  [("mcp.example.com/mcp", "mcp.example.com/mcp"),
   ("https://mcp.example.com/mcp", "https://mcp.example.com/mcp"),
   ("https://mcp.example.com/mcp#tools", "https://mcp.example.com/mcp#tools"),
   ("mcp://mcp.example.com/mcp", "mcp://mcp.example.com/mcp")], [1],
  ("Il canonical URI (RFC 8707) deve avere lo scheme e non può contenere un fragment; meglio senza slash finale, salvo che sia significativo. Un path è ammesso quando serve a identificare il server.",
   "The canonical URI (RFC 8707) must have a scheme and cannot contain a fragment; preferably without a trailing slash unless it is meaningful. A path is allowed when it is needed to identify the server."))
A("D4-09", ("Quali comportamenti di un client MCP sui refresh token sono corretti? (scegli 2)",
            "Which MCP client behaviors around refresh tokens are correct? (choose 2)"),
  [("Tenere i refresh token riservati in transito e a riposo", "Keeping refresh tokens confidential in transit and at rest"),
   ("Dare per scontato che l'AS emetta sempre un refresh token", "Assuming the AS always issues a refresh token"),
   ("Inviare il refresh token al server MCP insieme all'access token", "Sending the refresh token to the MCP server along with the access token"),
   ("Non contare sul refresh token: l'AS decide se emetterlo", "Not relying on a refresh token: the AS decides whether to issue it")], [0, 3],
  ("Il client MUST tenere i refresh token riservati, SHOULD dichiarare refresh_token nei grant_types, MAY chiedere offline_access se l'AS lo supporta e MUST NOT dare per scontato di riceverli. Il server MCP riceve solo l'access token.",
   "The client MUST keep refresh tokens confidential, SHOULD declare refresh_token in grant_types, MAY request offline_access if the AS supports it and MUST NOT assume it will receive them. The MCP server only receives the access token."))

# ---------------- D5 ----------------
A("D5-07", ("Quali server vengono rimossi dal registry ufficiale MCP secondo la moderation policy? (scegli 2)",
            "Which servers does the official MCP registry remove under its moderation policy? (choose 2)"),
  [("Un server che contiene malware, anche se a scopo di ricerca", "A server containing malware, even for research purposes"),
   ("Un server con una vulnerabilità di sicurezza nota", "A server with a known security vulnerability"),
   ("Lo stesso server pubblicato più volte con nomi diversi", "The same server published several times under different names"),
   ("Un server che fa la stessa cosa di un altro già presente", "A server that does the same as one already listed")], [0, 2],
  ("Il registry è volutamente permissivo: rimuove contenuti illegali, malware, spam (come duplicati con nomi diversi) e server non funzionanti. Non rimuove server di bassa qualità, con vulnerabilità o duplicati funzionali: la moderazione più fine spetta ai subregistry.",
   "The registry is permissive on purpose: it removes illegal content, malware, spam (such as duplicates under different names) and non-functioning servers. It does not remove low-quality, vulnerable or functionally duplicate servers: finer moderation belongs to subregistries."))
A("D5-07", ("Un publisher vuole pubblicare nel registry un server remoto. Quale scelta per remotes[].type è corretta?",
            "A publisher wants to list a remote server in the registry. Which choice for remotes[].type is correct?"),
  [("Solo \"sse\", perché è il transport più diffuso", "Only \"sse\", because it is the most widespread transport"),
   ("\"stdio\", indicando l'URL nel campo command", "\"stdio\", with the URL in the command field"),
   ("\"websocket\", per avere comunicazione bidirezionale", "\"websocket\", for bidirectional communication"),
   ("\"streamable-http\"; \"sse\" solo per supportare client esistenti", "\"streamable-http\"; \"sse\" only to support existing clients")], [3],
  ("I server remoti dovrebbero usare Streamable HTTP. Il transport SSE è deprecato: si pubblica un remote \"sse\" solo per i client esistenti, eventualmente in parallelo su un URL diverso.",
   "Remote servers should use Streamable HTTP. The SSE transport is deprecated: publish an \"sse\" remote only for existing clients, possibly side by side at a different URL."))
A("D5-07", ("Il registry rimuove un server per malware. Che cosa succede ai suoi metadata?",
            "The registry removes a server for malware. What happens to its metadata?"),
  [("Vengono cancellati subito e l'API risponde 404", "They are deleted at once and the API answers 404"),
   ("Lo status diventa \"deleted\", ma restano leggibili dall'API", "The status becomes \"deleted\", but they stay readable via the API"),
   ("Passano a un subregistry di quarantena", "They move to a quarantine subregistry"),
   ("Restano invariati: decide il package registry upstream", "They stay unchanged: the upstream package registry decides")], [1],
  ("Alla rimozione lo status del server diventa \"deleted\", ma i metadata restano accessibili dall'API del registry; gli aggregatori possono poi toglierlo dai loro indici. Solo in casi estremi (metadata illeciti) vengono sovrascritti o cancellati.",
   "On removal the server's status becomes \"deleted\", but its metadata stays accessible via the registry API; aggregators may then drop it from their indexes. Only in extreme cases (unlawful metadata) is it overwritten or erased."))
A("D5-15", ("Perché un host può mostrare una MCP App di un server di terze parti senza fidarsi del tutto del suo autore?",
            "Why can a host render a third-party server's MCP App without fully trusting its author?"),
  [("Perché il registry ufficiale verifica il codice di ogni MCP App pubblicata", "Because the official registry verifies the code of every published MCP App"),
   ("Perché le MCP App girano solo su server locali stdio, mai su server remoti", "Because MCP Apps only run on local stdio servers, never on remote ones"),
   ("Perché gira in un iframe sandbox: niente accesso alla pagina host o ai cookie", "Because it runs in a sandboxed iframe: no access to the host page or cookies"),
   ("Perché l'app non può chiamare i tool del server né ricevere dati dall'host", "Because the app cannot call the server's tools or receive data from the host")], [2],
  ("Le MCP App girano in un iframe sandbox controllato dall'host, con CSP deny-by-default: non accedono alla pagina padre, non rubano cookie e non escono dal contenitore. Possono comunque chiamare i tool del server e delegare azioni all'host, con il consenso dell'utente.",
   "MCP Apps run in a host-controlled sandboxed iframe with a deny-by-default CSP: they cannot access the parent page, steal cookies or escape their container. They can still call the server's tools and delegate actions to the host, with user consent."))
A("D5-10", ("Una pipeline CI notturna deve chiamare tool MCP senza nessun utente presente. Quale soluzione indica la documentazione ufficiale?",
            "A nightly CI pipeline must call MCP tools with no user present. Which solution does the official documentation point to?"),
  [("L'estensione OAuth Client Credentials, preferibilmente con JWT bearer assertion", "The OAuth Client Credentials extension, preferably with a JWT bearer assertion"),
   ("Il flusso authorization code con PKCE, salvando il token dell'ultimo utente", "The authorization code flow with PKCE, storing the last user's token"),
   ("Disattivare l'autorizzazione per gli IP della pipeline", "Disabling authorization for the pipeline's IPs"),
   ("Un token personale di uno sviluppatore passato come variabile", "A developer's personal token passed as a variable")], [0],
  ("OAuth Client Credentials serve per servizi in background, CI/CD, integrazioni server-to-server e daemon: il client si autentica con credenziali dell'applicazione (JWT bearer assertion, RFC 7523, raccomandata, oppure client secret). Se c'è un utente che deve autorizzare, si usa il flusso standard.",
   "OAuth Client Credentials is for background services, CI/CD, server-to-server integrations and daemons: the client authenticates with application credentials (a JWT bearer assertion, RFC 7523, recommended, or a client secret). If a user must authorize, use the standard flow."))

json.dump(qs, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(qs), "domande scritte in", OUT, cnt)
