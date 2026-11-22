# SUPERATO dalla revisione del 2026-11-22: la fonte valida è content/questions-D*.json (vedi review_fixes.py). Non rieseguire.
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from qhelper import Q, save
qs=[]; D="D5"
def A(*a, **k): Q(qs, D, len(qs)+1, *a, **k)

A("D5-01",2,("Chi è responsabile di validare l'audience del token e autorizzare ogni uso di un handle?","Who is responsible for validating token audience and authorizing every use of a handle?"),
 [("L'host","The host"),("L'autore del server MCP","The MCP server author"),("Il registry","The registry"),("L'utente finale","The end user")],[1],
 ("Validazione input, controllo accessi, rate limit, PRM, validazione token e autorizzazione degli handle spettano al server.","Input validation, access control, rate limiting, PRM, token validation and handle authorization belong to the server."))
A("D5-01",2,("Quali compiti spettano all'host/client? (scegli 2)","Which tasks belong to the host/client? (choose 2)"),
 [("Raccogliere il consenso e mostrare le approvazioni","Collect consent and show approvals"),("Emettere i token di accesso","Issue access tokens"),("Usare la cache in modo coerente con cacheScope","Use caching consistently with cacheScope"),("Moderare le voci del registry","Moderate registry entries")],[0,2],
 ("I token li emette l'authorization server; la moderazione è del registry. L'host gestisce consenso, UI, _meta e caching.","Tokens are issued by the authorization server; moderation is the registry's job. The host handles consent, UI, _meta and caching."))
A("D5-01",3,("In un'azienda con Enterprise-Managed Authorization, chi decide a quali server MCP può accedere un dipendente?","In a company using Enterprise-Managed Authorization, who decides which MCP servers an employee can reach?"),
 [("Il dipendente, server per server","The employee, server by server"),("L'IdP aziendale","The enterprise IdP"),("L'autore del client","The client author"),("Il registry ufficiale","The official registry")],[1],
 ("Con EMA l'IdP aziendale decide l'accesso con policy e revoca centralizzate (ID-JAG).","With EMA the enterprise IdP decides access with centralized policy and revocation (ID-JAG)."))
A("D5-02",1,("Chi ha co-fondato l'Agentic AI Foundation (AAIF)?","Who co-founded the Agentic AI Foundation (AAIF)?"),
 [("Anthropic, Block e OpenAI","Anthropic, Block and OpenAI"),("Google, Microsoft e Amazon","Google, Microsoft and Amazon"),("Solo Anthropic","Anthropic alone"),("La CNCF","The CNCF")],[0],
 ("AAIF è stata co-fondata da Anthropic, Block e OpenAI sotto la Linux Foundation; progetti fondativi: MCP, goose, AGENTS.md.","AAIF was co-founded by Anthropic, Block and OpenAI under the Linux Foundation; founding projects: MCP, goose, AGENTS.md."))
A("D5-02",2,("Con quali licenze sono distribuiti codice/spec e documentazione di MCP?","Under which licenses are MCP code/spec and documentation distributed?"),
 [("MIT per tutto","MIT for everything"),("Apache 2.0 per codice e spec, CC-BY 4.0 per la documentazione","Apache 2.0 for code and spec, CC-BY 4.0 for documentation"),("GPL v3 e CC0","GPL v3 and CC0"),("Proprietaria","Proprietary")],[1],
 ("Codice e spec Apache 2.0, documentazione CC-BY 4.0. La membership nella governance è individuale.","Code and spec Apache 2.0, documentation CC-BY 4.0. Governance membership is individual."))
A("D5-03",2,("Un'azienda vuole offrire un server MCP a migliaia di utenti, aggiornabile in un unico punto. Quale scelta è più adatta?","A company wants to offer an MCP server to thousands of users, patched in one place. Which choice fits best?"),
 [("Server locale stdio distribuito come pacchetto","Local stdio server distributed as a package"),("Server remoto Streamable HTTP con OAuth 2.1","Remote Streamable HTTP server with OAuth 2.1"),("Server locale HTTP su 0.0.0.0","Local HTTP server on 0.0.0.0"),("Un bundle MCPB per ogni utente","An MCPB bundle per user")],[1],
 ("Il server remoto serve molti client e si aggiorna in un solo punto; il locale serve quando bisogna raggiungere file o strumenti della macchina.","A remote server serves many clients and is patched in one place; local is needed to reach the machine's files or tools."))
A("D5-03",2,("Un server deve leggere file del progetto sul laptop dello sviluppatore. Cosa si sceglie e con quale rischio principale?","A server must read project files on the developer's laptop. What do you choose and with what main risk?"),
 [("Remoto; rischio SSRF","Remote; SSRF risk"),("Locale stdio; codice eseguito con i privilegi dell'utente","Local stdio; code running with the user's privileges"),("Remoto; rischio mix-up","Remote; mix-up risk"),("Locale; nessun rischio perché stdio è isolato","Local; no risk because stdio is isolated")],[1],
 ("Per accedere a risorse locali serve un server locale; mitigazioni: sandbox, provenienza, consenso one-click.","Reaching local resources needs a local server; mitigations: sandboxing, provenance, one-click consent."))
A("D5-04",2,("Un server 2026-07-28 gira su 10 istanze dietro un load balancer round-robin. Cosa serve per funzionare?","A 2026-07-28 server runs on 10 instances behind a round-robin load balancer. What does it need to work?"),
 [("Sticky sessions sull'Mcp-Session-Id","Sticky sessions on Mcp-Session-Id"),("Nulla di particolare: ogni istanza può servire ogni richiesta","Nothing special: any instance can serve any request"),("Una cache condivisa delle sessioni initialize","A shared cache of initialize sessions"),("Un solo stream GET per client","A single GET stream per client")],[1],
 ("Il protocollo è stateless: niente sessioni né sticky routing. Lo stato applicativo passa con handle espliciti.","The protocol is stateless: no sessions or sticky routing. Application state travels via explicit handles."))
A("D5-04",2,("Un gateway vuole applicare rate limit specifici al tool delete_repo senza leggere il corpo JSON. Su cosa si basa?","A gateway wants a specific rate limit on the delete_repo tool without parsing the JSON body. What does it use?"),
 [("Sull'header Mcp-Name","The Mcp-Name header"),("Sull'header Mcp-Session-Id","The Mcp-Session-Id header"),("Sul campo clientInfo","The clientInfo field"),("Sul cookie di sessione","The session cookie")],[0],
 ("Mcp-Method e Mcp-Name (su tools/call, resources/read, prompts/get) permettono routing e rate limit a livello HTTP; il server verifica che corrispondano al corpo (-32020).","Mcp-Method and Mcp-Name (on tools/call, resources/read, prompts/get) allow HTTP-level routing and rate limiting; the server checks they match the body (-32020)."))
A("D5-04",3,("Quale combinazione è corretta per un caso d'uso? (scegli 2)","Which pairing of use case and mechanism is correct? (choose 2)"),
 [("Job lungo avviato dal client → Tasks","Long job started by the client → Tasks"),("Notificare un agente non presidiato di un evento upstream → Events","Notify an unattended agent of an upstream event → Events"),("Comunicazione M2M → elicitation","M2M communication → elicitation"),("Stato tra chiamate → sticky sessions","State across calls → sticky sessions")],[0,1],
 ("Tasks per risultati di operazioni lunghe, Events per attività upstream, Client Credentials per M2M, handle per lo stato.","Tasks for long-operation results, Events for upstream activity, Client Credentials for M2M, handles for state."))
A("D5-05",2,("Un host ha 400 tool che occupano il 15% della finestra di contesto. Quale pattern è consigliato?","A host has 400 tools taking 15% of the context window. Which pattern is recommended?"),
 [("Caricarli tutti comunque","Load them all anyway"),("Progressive discovery con un meta-tool di ricerca","Progressive discovery with a search meta-tool"),("Dividerli su più sessioni","Split them across sessions"),("Rimuovere le descrizioni","Remove the descriptions")],[1],
 ("Regola pratica: oltre l'1-5% del contesto conviene la progressive discovery (Catalog → Inspect → Execute).","Rule of thumb: beyond 1-5% of context, progressive discovery pays off (Catalog → Inspect → Execute)."))
A("D5-05",2,("Qual è il vantaggio principale del code mode?","What is the main benefit of code mode?"),
 [("Elimina la necessità di autorizzazione","It removes the need for authorization"),("I risultati intermedi restano fuori dal contesto del modello","Intermediate results stay out of the model's context"),("Sostituisce il trasporto stdio","It replaces the stdio transport"),("Rende i tool deterministici","It makes tools deterministic")],[1],
 ("Il modello scrive codice che chiama i tool in una sandbox: meno token e meno dati sensibili nel contesto.","The model writes code that calls tools in a sandbox: fewer tokens and less sensitive data in context."))
A("D5-10",2,("Un team vuole mostrare una dashboard interattiva in tempo reale dentro il client. Quale estensione?","A team wants to show a real-time interactive dashboard inside the client. Which extension?"),
 [("Tasks","Tasks"),("MCP Apps","MCP Apps"),("Skills","Skills"),("Server Cards","Server Cards")],[1],
 ("MCP Apps: UI HTML in iframe sandboxed, comunicazione solo via postMessage, risorse ui://.","MCP Apps: HTML UIs in a sandboxed iframe, postMessage-only communication, ui:// resources."))
A("D5-10",2,("Un'azienda vuole che IT gestisca centralmente accesso e revoca ai server MCP con SSO aziendale. Quale estensione?","A company wants IT to centrally manage access and revocation to MCP servers with corporate SSO. Which extension?"),
 [("OAuth Client Credentials","OAuth Client Credentials"),("Enterprise-Managed Authorization","Enterprise-Managed Authorization"),("Events","Events"),("MCPB","MCPB")],[1],
 ("EMA: policy centralizzate, revoca, SSO e compliance. Client Credentials è per servizi senza utente.","EMA: centralized policy, revocation, SSO and compliance. Client Credentials is for services with no user."))
A("D5-11",2,("Un server serverless non può tenere connessioni aperte. Quale modalità Events è più adatta?","A serverless server cannot hold connections open. Which Events mode fits best?"),
 [("push (events/stream)","push (events/stream)"),("poll (events/poll)","poll (events/poll)"),("Nessuna: Events richiede stdio","None: Events requires stdio"),("subscriptions/listen","subscriptions/listen")],[1],
 ("Poll per server serverless, push per server stdio, webhook per server remoti con client che non tengono connessioni.","Poll for serverless servers, push for stdio servers, webhook for remote servers whose clients can't hold connections."))
A("D5-11",3,("Quali garanzie offre Events? (scegli 2)","Which guarantees does Events offer? (choose 2)"),
 [("Consegna at-least-once con eventId per deduplicare","At-least-once delivery with eventId for deduplication"),("Consegna exactly-once","Exactly-once delivery"),("Ordine garantito per poll e push, best-effort per webhook","Ordering guaranteed for poll and push, best-effort for webhook"),("Ordine garantito anche per webhook","Ordering guaranteed for webhook too")],[0,2],
 ("Cursori opachi e at-least-once: il client deduplica con eventId; maxAgeMs limita il replay.","Opaque cursors and at-least-once: the client deduplicates with eventId; maxAgeMs limits replay."))
A("D5-14",2,("Un gateway filtra le richieste per header Mcp-Method. Basta per l'autorizzazione?","A gateway filters requests by the Mcp-Method header. Is that enough for authorization?"),
 [("Sì, il gateway è sufficiente","Yes, the gateway is enough"),("No: l'autorizzazione fine resta nel server, a ogni chiamata","No: fine-grained authorization stays in the server, on every call"),("Sì, se c'è TLS","Yes, with TLS"),("Sì, se cacheScope è private","Yes, if cacheScope is private")],[1],
 ("Il gateway filtra in modo grossolano; il server autorizza ogni chiamata, inclusi gli handle.","The gateway filters coarsely; the server authorizes every call, handles included."))
A("D5-14",2,("In un settore regolamentato, quali pratiche sono raccomandate? (scegli 2)","In a regulated industry, which practices are recommended? (choose 2)"),
 [("Tenere i dati sensibili fuori dal contesto del modello quando possibile","Keep sensitive data out of the model context when possible"),("Usare cacheScope public per ridurre i costi","Use cacheScope public to cut costs"),("ID di correlazione end-to-end e un audit trail durevole","End-to-end correlation IDs and a durable audit trail"),("Affidarsi solo al trace context come audit","Rely only on trace context as audit")],[0,2],
 ("Il trace context correla ma non è un audit trail; dati sensibili con cacheScope private.","Trace context correlates but is not an audit trail; sensitive data with cacheScope private."))
A("D5-06",1,("Quale SDK è Tier 2?","Which SDK is Tier 2?"),
 [("Python","Python"),("Java","Java"),("Swift","Swift"),("Go","Go")],[1],
 ("Tier 1: TypeScript, Python, C#, Go, Rust, Ruby. Tier 2: Java. Tier 3: Swift, PHP, Kotlin.","Tier 1: TypeScript, Python, C#, Go, Rust, Ruby. Tier 2: Java. Tier 3: Swift, PHP, Kotlin."))
A("D5-06",2,("Quali requisiti valgono per un SDK Tier 1? (scegli 2)","Which requirements apply to a Tier 1 SDK? (choose 2)"),
 [("100% dei test di conformance","100% of conformance tests"),("Supporto obbligatorio a tutte le estensioni","Mandatory support for all extensions"),("Triage entro 2 giorni lavorativi","Triage within 2 business days"),("Nuove feature entro 6 mesi","New features within 6 months")],[0,2],
 ("Tier 1: 100% conformance, feature prima del rilascio della spec, triage in 2 giorni lavorativi, bug critici in 7 giorni. Le estensioni non sono richieste.","Tier 1: 100% conformance, features before the spec release, triage in 2 business days, critical bugs in 7 days. Extensions are not required."))
A("D5-06",3,("Un SDK Tier 1 fallisce un test di conformance per 4 settimane consecutive. Cosa succede?","A Tier 1 SDK fails a conformance test for 4 consecutive weeks. What happens?"),
 [("Nulla","Nothing"),("Viene retrocesso a Tier 2","It is relegated to Tier 2"),("Viene rimosso dall'organizzazione","It is removed from the organization"),("Passa a Tier 3","It moves to Tier 3")],[1],
 ("Retrocessione dopo 4 settimane di fallimenti continui: Tier 1 → 2 se fallisce anche un solo test.","Relegation after 4 weeks of continuous failures: Tier 1 → 2 if any test fails."))
A("D5-07",2,("Quale versione è valida in un server.json del registry?","Which version is valid in a registry server.json?"),
 [("^1.2.3","^1.2.3"),("1.2.3","1.2.3"),(">=1.0","> =1.0".replace(' ','')),("latest","latest")],[1],
 ("Versione unica e immutabile, niente range. Il nome è in reverse DNS (es. io.github.utente/server).","Unique, immutable version, no ranges. The name is reverse DNS (e.g. io.github.user/server)."))
A("D5-07",2,("Come dimostra un autore la proprietà di un pacchetto npm pubblicato nel registry?","How does an author prove ownership of an npm package published to the registry?"),
 [("Con il campo mcpName in package.json","With the mcpName field in package.json"),("Con un label OCI","With an OCI label"),("Con mcp-name nel README","With mcp-name in the README"),("Con un record DNS TXT","With a DNS TXT record")],[0],
 ("npm: mcpName in package.json; PyPI: mcp-name nel README; OCI: label io.modelcontextprotocol.server.name. Il DNS verifica il namespace, non il pacchetto.","npm: mcpName in package.json; PyPI: mcp-name in the README; OCI: io.modelcontextprotocol.server.name label. DNS verifies the namespace, not the package."))
A("D5-07",3,("Dopo la pubblicazione, cosa si può modificare di una voce del registry?","After publishing, what can be changed in a registry entry?"),
 [("La descrizione","The description"),("Gli URL dei pacchetti","Package URLs"),("Solo lo status (es. deprecated, deleted)","Only the status (e.g. deprecated, deleted)"),("Il nome","The name")],[2],
 ("I metadati sono immutabili tranne lo status; per altre modifiche si pubblica una nuova versione.","Metadata is immutable except status; for other changes a new version is published."))
A("D5-08",1,("Quale estensione ufficiale espone metadati del server prima della connessione?","Which official extension exposes server metadata before connecting?"),
 [("Server Cards","Server Cards"),("Tasks","Tasks"),("Skills","Skills"),("MCP Apps","MCP Apps")],[0],
 ("Server Cards: metadati disponibili prima della connessione.","Server Cards: metadata available before connecting."))
A("D5-13",2,("Un host legge SKILL.md con resources/read. La skill è attiva?","A host reads SKILL.md with resources/read. Is the skill active?"),
 [("Sì, la lettura la attiva","Yes, reading activates it"),("No: l'host la carica dopo verifica ed eventuale approvazione","No: the host loads it after verification and any approval"),("Sì, se il digest coincide","Yes, if the digest matches"),("Dipende dal server","It depends on the server")],[1],
 ("Leggere non attiva. skills/list fornisce URI, digest SHA-256 e dimensione per verificare l'integrità.","Reading does not activate. skills/list provides URI, SHA-256 digest and size to verify integrity."))
A("D5-12",2,("Quale file è obbligatorio in un bundle .mcpb?","Which file is required in an .mcpb bundle?"),
 [("server.json","server.json"),("manifest.json","manifest.json"),("package.json","package.json"),("SKILL.md","SKILL.md")],[1],
 ("MCPB (ex DXT di Claude Desktop) richiede manifest.json; supporta server Node.js, Python e binari; si pubblica nel registry con registryType mcpb.","MCPB (formerly Claude Desktop's DXT) requires manifest.json; supports Node.js, Python and binary servers; published to the registry with registryType mcpb."))
A("D5-09",1,("Un server stdio scrive messaggi di debug su stdout. Cosa succede?","A stdio server writes debug messages to stdout. What happens?"),
 [("Nulla, il client li ignora","Nothing, the client ignores them"),("Rompe il protocollo: i log vanno su stderr","It breaks the protocol: logs go to stderr"),("Vengono mostrati come notifiche","They are shown as notifications"),("Il client li salva come audit","The client saves them as audit")],[1],
 ("Su stdio stdout è riservato ai messaggi JSON-RPC; i log vanno su stderr.","Over stdio, stdout is reserved for JSON-RPC messages; logs go to stderr."))
A("D5-09",2,("Quale strumento ufficiale si usa per testare e fare debug di un server MCP?","Which official tool is used to test and debug an MCP server?"),
 [("MCP Inspector","MCP Inspector"),("Postman MCP","Postman MCP"),("MCPB CLI","MCPB CLI"),("Registry validator","Registry validator")],[0],
 ("MCP Inspector esiste in versione web, --cli e --tui.","MCP Inspector comes in web, --cli and --tui versions."))
save(qs, "/mnt/project-files/mcpa-kb/site/content/questions-D5.json")
