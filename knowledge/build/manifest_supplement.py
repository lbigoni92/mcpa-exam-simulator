"""Fase 1.2 (2026-11-22): integra il manifest con topic e fatti per le lacune trovate nella verifica di completezza.
Uso: python3 mk_manifest.py && python3 manifest_supplement.py"""
import json,os
M=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','manifest.json')
m=json.load(open(M))
B="https://modelcontextprotocol.io/specification/2026-07-28"; D="https://modelcontextprotocol.io/docs"; S="sources/spec-2026-07-28"
def src(local,url): return {"local":local,"url":url}
def t(id,title,notes,srcs,facts,new=False,prio="normale"):
    return {"id":id,"title":title,"notes":notes,"sources":srcs,"key_facts":facts,"new_in_2026_07_28":new,"priority":prio,"added_in":"fase1.2"}
def comp(did,name):
    d=next(x for x in m['domains'] if x['id']==did); return next(c for c in d['competencies'] if c['name']==name)
def topic(tid):
    for d in m['domains']:
        for c in d['competencies']:
            for tp in c['topics']:
                if tp['id']==tid: return tp
def add(tid,facts,extra_src=None):
    tp=topic(tid); tp['key_facts']+=facts
    if extra_src: tp['sources'].append(extra_src)
SC=src("sources/docs/learn/server-concepts.md",D+"/learn/server-concepts")
DP=src("sources/community/design-principles.md","https://modelcontextprotocol.io/community/design-principles")
SI=src("sources/blog/2025-11-03-using-server-instructions.md","https://blog.modelcontextprotocol.io/posts/2025-11-03-using-server-instructions/")
TA=src("sources/blog/2026-03-16-tool-annotations.md","https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/")
LS=src("sources/docs/tutorials/security/local-server-security.md",D+"/tutorials/security/local-server-security")
TL=src(S+"/server/tools.md",B+"/server/tools")
SH=src(S+"/basic/transports/streamable-http.md",B+"/basic/transports/streamable-http")
# ---------- D1
comp("D1","Core MCP Concepts")['topics'].append(t("D1-09","Principi di design del progetto (governance delle SEP)","notes/01-mcp-fundamentals.md#26-principi-di-design-del-progetto",[DP],[
 "I design principles del progetto guidano l'accettazione di SEP ed estensioni; sono distinti dai design principles architetturali della spec.",
 "Convergence over choice: un solo modo di risolvere un problema; le estensioni testano la convergenza, la spec la consolida.",
 "Composability over specificity: niente feature per casi costruibili con resources, tools e prompts; i pattern emergenti diventano estensioni (MCP Apps, Tasks).",
 "Interoperability over optimization: feature che degradano con grazia; la capability negotiation adatta il protocollo invece di presumere.",
 "Stability over velocity: ogni aggiunta è permanente; le rimozioni seguono la Feature Lifecycle policy.",
 "Demonstration over deliberation: una SEP richiede un prototipo funzionante per essere accettata.",
 "Capability over compensation: niente struttura permanente per aggirare limiti temporanei dei modelli.",
 "Standardization over innovation: si standardizzano pattern già provati; quelli nuovi si sperimentano prima nelle estensioni.",
 "In caso di conflitto i principi si bilanciano tra loro, non sono in ordine gerarchico."]))
add("D1-04",["Tools = azioni (possono avere effetti); resources = dati di contesto in sola lettura identificati da URI; prompts = template riutilizzabili con argomenti.",
 "Il controllo indica chi decide l'uso: il modello per i tools, l'applicazione per le resources, l'utente per i prompts (es. slash command).",
 "Le resources sono identificate da URI e possono essere parametrizzate con resource template (RFC 6570)."],SC)
add("D1-07",["Problema N×M: senza uno standard servono N×M integrazioni custom; con MCP ognuno implementa il protocollo una volta (N+M).",
 "Valore per gli sviluppatori: meno tempo e complessità; per le app AI: accesso a un ecosistema di data source e tool; per gli utenti finali: app più capaci che agiscono per loro.",
 "MCP è vendor-neutral, governato dalla Agentic AI Foundation sotto la Linux Foundation."])
comp("D1","MCP Purpose & Scope")['topics'].append(t("D1-10","Struttura e perimetro della specifica","notes/01-mcp-fundamentals.md#1-purpose--scope",[src(S+"/index.md",B)],[
 "MCP serve a: condividere informazioni di contesto con i modelli, esporre tool e capability ai sistemi AI, costruire integrazioni e workflow componibili.",
 "La spec è autorevole ed è basata sullo schema TypeScript (schema.ts); le guide e gli esempi stanno su modelcontextprotocol.io.",
 "Base protocol della 2026-07-28: formato JSON-RPC, richieste stateless e autocontenute, capability negotiation per richiesta.",
 "Server features: resources (contesto per utente o modello), prompts (messaggi e workflow template per gli utenti), tools (funzioni eseguite dal modello).",
 "Client feature non deprecata: elicitation (il server chiede informazioni aggiuntive all'utente).",
 "Utility: configuration, progress tracking, cancellation, error reporting.",
 "Le estensioni sono sempre opt-in e richiedono il supporto esplicito di client e server, negoziato tramite capabilities.",
 "MCP definisce lo scambio di contesto, non come l'applicazione usa l'LLM o gestisce il contesto ricevuto."]))
# ---------- D2
add("D2-09",["Esempio ufficiale multi-server (travel planner): l'utente avvia un prompt, l'app aggiunge resources, il modello chiama tools di server diversi.",
 "È il host a orchestrare: i server non comunicano tra loro e ricevono solo ciò che serve, mentre il contesto completo resta nell'host.",
 "Prima di inviare tools/call il client SHOULD mostrare all'utente gli input del tool (anti esfiltrazione) e chiedere conferma per le operazioni sensibili.",
 "Il client SHOULD validare il risultato del tool (e structuredContent rispetto a outputSchema) prima di passarlo all'LLM."],SC)
mf=comp("D2","Model Interaction Flow")['topics']
mf.append(t("D2-11","Server instructions","notes/02-architecture-components.md#31-server-instructions",[src(S+"/server/discover.md",B+"/server/discover"),SI],[
 "instructions è un campo opzionale di server/discover (prima nell'InitializeResult) con indicazioni in linguaggio naturale per l'LLM su come usare il server.",
 "Contenuti adatti: relazioni e ordine tra i tool, vincoli (rate limit), fallback; non ripetere le descrizioni dei tool.",
 "Il host di solito inietta le instructions nel system prompt.",
 "Le instructions non garantiscono il comportamento: mai usarle per controlli critici di sicurezza o privacy (servono regole deterministiche o hook).",
 "Client: mostrare all'utente le instructions iniettate e permettere di rivederle o disabilitarle."],new=True))
mf.append(t("D2-12","Modello di interazione utente per primitiva","notes/02-architecture-components.md#32-modello-di-interazione-utente-per-primitiva",[SC],[
 "Tools: dialog di approvazione per singola esecuzione, permessi per pre-approvare operazioni sicure, activity log delle esecuzioni.",
 "Resources: picker ad albero o lista, ricerca e filtri, inclusione automatica; la spec non impone una UI.",
 "Prompts: invocazione esplicita dell'utente, ad esempio slash command o command palette; il template deve essere visibile.",
 "Elicitation: il server chiede, l'utente risponde con accept, decline o cancel."]))
comp("D2","MCP Hosts, Clients and Servers")['topics'].append(t("D2-13","Nomi dei tool e aggregazione multi-server","notes/02-architecture-components.md#33-più-server-insieme-e-nomi-dei-tool",[TL],[
 "Nomi dei tool: SHOULD 1-128 caratteri, case-sensitive, solo A-Z a-z 0-9 _ - . , senza spazi né virgole.",
 "L'unicità dei nomi dei tool vale solo all'interno di un singolo server.",
 "Client e proxy che aggregano più server SHOULD disambiguare le collisioni, ad esempio con un prefisso che identifica il server.",
 "serverInfo.name non è garantito univoco e SHOULD NOT essere usato per la disambiguazione."]))
# ---------- D3
add("D3-10",["202 Accepted senza body: notifica JSON-RPC accettata dal server; nella 2026-07-28 il client MUST NOT inviare risposte JSON-RPC nel POST.",
 "400 Bad Request: HeaderMismatch (-32020), versione non supportata (-32022), capability mancante (-32021), header obbligatorio assente.",
 "404 Not Found con errore JSON-RPC -32601: metodo non implementato; un 404 senza body JSON-RPC suggerisce un server legacy HTTP+SSE.",
 "405 Method Not Allowed: GET o DELETE sull'endpoint MCP di un server che supporta solo la 2026-07-28.",
 "403 Forbidden: Origin non valido (protezione da DNS rebinding) oppure scope insufficienti; 401: token mancante, invalido o scaduto."],SH)
add("D3-09",["Protocol error: tool sconosciuto, richiesta malformata, errore del server; tool execution error: errori di API, validazione dell'input, logica di business.",
 "Il client SHOULD passare i tool execution error al modello per l'autocorrezione; MAY passare anche i protocol error, ma è meno probabile che il modello si riprenda."])
# ---------- D4
rs=comp("D4","Risk & Safety Controls")['topics']
rs.append(t("D4-16","Tool poisoning, rug pull e lethal trifecta","notes/04-security-governance.md#68-tool-poisoning-rug-pull-lethal-trifecta-e-limiti-delle-annotations",[LS,TA],[
 "Tool poisoning: nomi e descrizioni dei tool sono istruzioni lette dal modello e possono contenere direttive nascoste.",
 "Un tool avvelenato può influenzare l'agente anche senza essere mai invocato, e può prendere di mira i tool di altri server (tool shadowing).",
 "Rug pull: il server cambia le definizioni dei tool dopo l'approvazione; consenso una tantum e pin del pacchetto non bastano.",
 "Lethal trifecta: accesso a dati privati + contenuti non fidati + capacità di comunicare all'esterno = rischio di esfiltrazione via prompt injection.",
 "Il rischio è una proprietà della sessione (combinazione di tool di più server), non del singolo server.",
 "Trattare l'output dei tool open-world come contenuto non fidato."],prio="alta"))
rs.append(t("D4-17","Tool annotations: cosa possono e non possono fare","notes/04-security-governance.md#68-tool-poisoning-rug-pull-lethal-trifecta-e-limiti-delle-annotations",[TA,TL],[
 "Default pessimisti: readOnlyHint false, destructiveHint true, idempotentHint false, openWorldHint true.",
 "destructiveHint e idempotentHint sono significativi solo se readOnlyHint è false.",
 "Le annotations possono guidare le conferme, la fiducia graduata, la UX e i policy engine.",
 "Le annotations non fanno enforcement e non proteggono dalla prompt injection; per garanzie servono sandbox o controlli di rete.",
 "Un server non fidato può mentire nelle annotations: i client devono trattarle come non fidate, salvo server fidati."],prio="alta"))
tb=comp("D4","Trust Boundaries")['topics']
tb.append(t("D4-18","Threat model dei server locali e provenienza","notes/04-security-governance.md#65b-modello-di-minaccia-dei-server-locali",[LS],[
 "Tra client e server stdio non c'è un confine di sicurezza: il transport stdio non è una sandbox e gli SDK assumono piena fiducia tra i peer.",
 "Le decisioni di sicurezza per i server locali avvengono prima del lancio: provenienza (cosa installi) e isolamento (come lo esegui).",
 "Il trust domain è cumulativo: ogni server condivide il contesto del modello e può influenzare l'uso dei tool degli altri.",
 "Minacce: server malevolo (typosquatting), server che raccoglie troppo, dipendenza compromessa, catalogo di tool avvelenato, bridge vulnerabile.",
 "Nessun controllo prova cosa farà un server: firme, SBOM e listing curati dicono di chi ti fidi, non che la fiducia sia meritata.",
 "Il pin con npx/uvx copre solo il pacchetto top-level; un'immagine container pinnata per digest congela tutto l'albero delle dipendenze.",
 "Se il server non ha bisogno della macchina locale, preferire la versione remota (Streamable HTTP + OAuth)."],prio="alta"))
add("D4-13",["Il client SHOULD registrare l'uso dei tool per audit; il host dovrebbe offrire un activity log delle esecuzioni.",
 "Per l'audit bisogna poter dire quale agente ha agito e per conto di quale utente; il token dovrebbe essere legato al server (audience).",
 "Trace context W3C (traceparent, tracestate, baggage) in _meta per correlare host, client, server e sistemi a valle."],TL)
# ---------- D5
oc=comp("D5","Operational Use Cases")['topics']
oc.append(t("D5-10","Quale estensione per quale caso d'uso","notes/05-use-cases-ecosystem.md#23b-quando-usare-quale-estensione",[src("sources/extensions/apps/overview.md","https://modelcontextprotocol.io/extensions/apps/overview"),src("sources/extensions/auth/oauth-client-credentials.md","https://modelcontextprotocol.io/extensions/auth/oauth-client-credentials"),src("sources/extensions/auth/enterprise-managed-authorization.md","https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization"),src("sources/extensions/events/overview.md","https://modelcontextprotocol.io/extensions/events/overview")],[
 "MCP Apps: dati complessi da esplorare, configurazioni con molte opzioni, media ricchi, monitoraggio in tempo reale, workflow a più passi.",
 "Le MCP Apps girano in un iframe sandbox senza accesso a DOM, cookie o storage del host; comunicano solo via postMessage e il host limita le capability.",
 "OAuth Client Credentials: servizi in background, CI/CD, integrazioni server-to-server, daemon; JWT bearer assertion raccomandata rispetto al client secret.",
 "Se c'è un utente che deve autorizzare l'accesso si usa il flusso di autorizzazione standard, non client credentials.",
 "Enterprise-Managed Authorization: IT che gestisce gli accessi, policy organizzative, revoca centralizzata, compliance, SSO aziendale.",
 "Events per reagire ad attività upstream o svegliare agenti non presidiati; Tasks per il risultato di un'operazione lunga avviata dal client."]))
oc.append(t("D5-11","Events: modalità di consegna e garanzie","notes/05-use-cases-ecosystem.md#23b-quando-usare-quale-estensione",[src("sources/extensions/events/overview.md","https://modelcontextprotocol.io/extensions/events/overview")],[
 "Le notifiche esistenti non bastano: niente parametri né payload, serve una connessione aperta, nessuna ripresa dopo una disconnessione.",
 "Tre modalità di consegna, nessuna obbligatoria: poll (events/poll), push (events/stream), webhook (events/subscribe con callback https firmata e TTL).",
 "Poll è adatto a server serverless, push a server stdio, webhook a server remoti con client che non mantengono una connessione.",
 "I cursori opachi danno una consegna at-least-once; eventId stabile per la deduplicazione; maxAgeMs limita il replay.",
 "Ordine garantito per poll e push all'interno di una subscription; best-effort per webhook. Le subscription appartengono al client."]))
add("D5-07",["Verifica di proprietà dei pacchetti: npm con mcpName in package.json, PyPI con 'mcp-name:' nel README, OCI con la label io.modelcontextprotocol.server.name.",
 "Per i server remoti il registry verifica il namespace del nome, non il controllo dell'URL remoto; più nomi possono puntare allo stesso URL.",
 "I consumatori identificano i record per nome e versione, non per URL.",
 "Remotes: type streamable-http (raccomandato) o sse (deprecato, solo per client esistenti).",
 "I metadata sono immutabili tranne status (deprecated, deleted); deleted indica di solito una violazione della moderation policy.",
 "Moderation permissiva: rimuove illegale, malware, spam e server non funzionanti; non rimuove server buggy o con vulnerabilità.",
 "Un subregistry implementa l'OpenAPI del registry e può aggiungere metadata in _meta (rating, download, scansioni di sicurezza)."],src("sources/registry/package-types.md","https://modelcontextprotocol.io/registry/package-types"))
ep=comp("D5","Ecosystem & Portability")['topics']
ep.append(t("D5-12","MCP Bundles (MCPB)","notes/05-use-cases-ecosystem.md#36-mcp-bundles-mcpb",[src("sources/blog/2025-11-20-adopting-mcpb.md","https://blog.modelcontextprotocol.io/posts/2025-11-20-adopting-mcpb/")],[
 "Un MCPB è un archivio ZIP (.mcpb) con un server MCP locale e un manifest.json obbligatorio, per l'installazione one-click.",
 "Nato da Anthropic come DXT per Claude Desktop, poi spostato nel progetto MCP per la portabilità cross-client.",
 "Supporta server Node.js, Python e binari; pubblicabile sul registry con registryType mcpb."]))
ep.append(t("D5-13","Skills over MCP","notes/05-use-cases-ecosystem.md#23b-quando-usare-quale-estensione",[src("sources/extensions/skills/overview.md","https://modelcontextprotocol.io/extensions/skills/overview")],[
 "Una skill è una directory con SKILL.md e file di supporto, esposta tramite il primitive Resources.",
 "Il server MUST dichiarare la capability resources e l'estensione io.modelcontextprotocol/skills in server/discover.",
 "skills/list fornisce per ogni file URI (schema skill:// raccomandato), digest SHA-256 e dimensione, per verificarne l'integrità.",
 "Leggere SKILL.md con resources/read non attiva la skill: il host la carica dopo verifica ed eventuale approvazione."],new=False))
oc.append(t("D5-14","Pattern enterprise: scala, gateway, audit, settori regolati","notes/05-use-cases-ecosystem.md#23c-pattern-enterprise-e-responsabilità",[src("sources/blog/aaif/README.md","https://aaif.io/projects/model-context-protocol/"),src("sources/community/interest-groups/enterprise (online)","https://modelcontextprotocol.io/community/interest-groups/enterprise")],[
 "In azienda il problema di scala è operativo: ownership, governance, deploy e osservabilità di molti server.",
 "Server con cataloghi di tool molto ampi aumentano consumo di token, latenza e superficie d'attacco; meglio tool stretti e contestuali.",
 "Il gateway che filtra su Mcp-Method e Mcp-Name è un controllo grossolano; l'autorizzazione fine resta nel server, a ogni chiamata.",
 "Gli handle di stato sono capability: vanno autorizzati a ogni chiamata e devono avere scope e scadenza.",
 "Il trace context W3C correla i passaggi ma non è un audit trail: serve un record durevole per richiesta (utente, agente, tool, autorizzazione).",
 "Nei settori regolati i dati sensibili vanno tenuti fuori dal contesto del modello quando possibile, con correlation ID end-to-end e policy nei servizi interni.",
 "Con la 2026-07-28 i server possono stare dietro load balancer standard senza sticky session.",
 "L'Enterprise Interest Group raccoglie requisiti aziendali e li passa ai Working Group; non scrive SEP."]))
add("D5-01",["Il server author implementa PRM e la validazione dei token (ruolo di resource server); il host gestisce consenso, contesto e approvazioni.",
 "L'utente finale approva tool e accessi; l'operatore o il security team si occupa di sandbox, gateway, egress e IdP aziendale.",
 "Il publisher sul registry possiede server.json (nome, versione, pacchetti); gli aggregatori fanno curation e scansioni di sicurezza."])
SCORES={"D1":(9,0.8,12,"concettuale, poco cambiato; buona copertura"),"D2":(9,1.1,15,"molte novità 2026-07-28 (header, discover, x-mcp-header)"),"D3":(9.5,1.2,29,"il dominio più pesante e più nuovo (MRTR, subscriptions, errori, caching)"),"D4":(9,1.2,27,"denso di dettagli OAuth, MUST vs SHOULD, attacchi"),"D5":(8,0.9,17,"meno materiale normativo: domande di scenario; integrato con blog AAIF")}
for d in m['domains']:
    c,mult,sw,why=SCORES[d['id']]
    d['coverage_score_10']=c; d['difficulty_multiplier']=mult; d['study_weight_pct']=sw; d['study_note']=why
n=sum(len(c["topics"]) for d in m['domains'] for c in d["competencies"]); f=sum(len(tp["key_facts"]) for d in m['domains'] for c in d["competencies"] for tp in c["topics"])
m["stats"]={"topics":n,"key_facts":f}; m["kb_revision"]="fase1.2 (2026-11-22)"
m["coverage_check"]={"date":"2026-11-22","target_question_bank":400,"note":"Verifica di completezza per dominio: vedi notes/14-copertura-domini.md"}
json.dump(m,open(M,'w'),ensure_ascii=False,indent=2)
for d in m['domains']:
    T=sum(len(c['topics']) for c in d['competencies']); F=sum(len(tp['key_facts']) for c in d['competencies'] for tp in c['topics'])
    print(d['id'],T,F)
print(n,f)
