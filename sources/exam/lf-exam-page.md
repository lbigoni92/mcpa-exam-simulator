# MCPA – informazioni pubbliche sull'esame (fonti ufficiali LF / AAIF)

Raccolto il 2026-11-22. Il portale trainingportal.linuxfoundation.org richiede login e non è stato letto.
Nessuna domanda d'esame reale è stata cercata o usata (LF Certification & Confidentiality Agreement).

## Fonte primaria
https://training.linuxfoundation.org/certification/model-context-protocol-associate-mcpa/ (modificata 2026-09-16)

### Domini e competenze (testuali dalla pagina)
| Dominio | Peso | Competenze |
|---|---|---|
| MCP Fundamentals | 16% | MCP Purpose & Scope · Core MCP Concepts · Interoperability & Value |
| Architecture & Components | 14% | Schemas & Structured Data · MCP Hosts, Clients and Servers · Model Interaction Flow |
| Interactions & Execution | 26% | Interaction Patterns & Response Handling · Error Handling · Tool Invocation Lifecycle · Protocol Primitives |
| Security & Governance | 24% | Trust Boundaries · Permissions & Consent · Risk & Safety Controls · Auditability & Observability |
| Use Cases & Ecosystem | 20% | Roles, Responsibilities & Adoption · Operational Use Cases · Ecosystem & Portability |

### "About" (parafrasi)
L'esame copre gli interni di MCP: architettura, message flow, interazioni client-server, capabilities, tools,
resources, prompts, transports e security considerations. Il candidato deve saper ragionare su come funziona il
protocollo e su come comunicano i componenti.

### Formato e policy
- Online, proctored (PSI), multiple-choice. La pagina MCPA non dichiara numero di domande né passing score.
- **Durata: 90 minuti** (pagina ufficiale MCPA, FAQ e Important Instructions LF per gli esami multiple-choice). I 120 minuti del press release LF e del blog AAIF sono **precedenti al lancio** e non valgono più; nelle pagine LF attuali 120 minuti è la durata del **CNPA**, non dell'MCPA. Guide e siti di pratica che dicono 120 (es. CertSafari) sono da considerare non aggiornati.
- **Regole generiche LF per gli esami multiple-choice** (non confermate esplicitamente per MCPA, ma sono il riferimento migliore):
  - **60 domande** in 90 minuti (Important Instructions MC; il CNPA ne ha 85).
  - **Passing score 75%** (FAQ MC).
  - Correzione automatica, score report via email entro 24 ore; solo esito pass/fail, nessun dettaglio per domanda (Agreement s. 3.1).
- Validità certificazione: 2 anni. Eligibility: 12 mesi. One retake.
- Livello: Beginner / Associate. Nessun prerequisito formale.
- Prezzo: $250 exam only; $495 con THRIVE-ONE.
- Spec di riferimento: "latest release 2026-07-28" → https://modelcontextprotocol.io/specification/2026-07-28

### Regole d'esame (FAQ MC, Important Instructions MC, Certification Agreement — riletti il 2026-11-22)
- **Closed book**: nessuna risorsa consentita (MCPA non è tra gli esami con risorse ammesse); appunti solo nel notepad del browser d'esame.
- PSI Secure Browser, un solo monitor, webcam mobile e microfono, **niente macchine virtuali**, admin rights sulla macchina, meglio senza firewall aziendale.
- Stanza privata, scrivania sgombra, nessun altro presente, niente lettura ad alta voce delle domande, solo liquidi trasparenti.
- Documento d'identità governativo originale con nome identico a quello verificato; età minima 16 anni (16-18 con modulo del genitore).
- Inizio entro 30 minuti dall'orario prenotato, altrimenti no-show senza rimborso.
- Vietato l'uso di AI durante l'esame; diffondere o ricostruire a memoria contenuti d'esame ("braindump", "study guides" con domande reali) è Exam Misconduct (Agreement s. 2.1, 4.4). La riservatezza copre anche **numero e lunghezza delle domande**.
- Registrazioni conservate al massimo 90 giorni; ricorsi entro 30 giorni; richieste di accomodamenti 2 settimane prima.
- Rinnovo: ripetere e superare l'esame prima della scadenza dei 2 anni.

### Esperienza raccomandata (dalla pagina)
- JSON-RPC o protocolli message-based simili
- Uso di LLM API (OpenAI, Anthropic, modelli locali via Ollama)
- Concetti di Agentic AI (ReAct, tool-use, chain-of-thought)
- Basi di sicurezza: API keys, OAuth 2.1 e token handling, authentication headers
- Saper leggere manifest di server MCP e capability definitions

### Risorse di preparazione elencate
- https://modelcontextprotocol.io/docs/getting-started/intro
- https://modelcontextprotocol.io/specification/2026-07-28
- https://aaif.io/projects/model-context-protocol/
- https://aaif.io/

### Link utili
- Candidate Handbook: https://docs.linuxfoundation.org/tc-docs/certification/lf-handbook2
- FAQ: https://docs.linuxfoundation.org/tc-docs/certification/faq-mc
- Important Instructions: https://docs.linuxfoundation.org/tc-docs/certification/important-instructions-mc
- Confidentiality Agreement: https://docs.linuxfoundation.org/tc-docs/certification/lf-cert-agreement/

## Altre fonti ufficiali
- Press release LF: https://www.linuxfoundation.org/press/agentic-ai-foundation-launches-mcpa-certification-to-validate-mcp-expertise — prima certificazione ufficiale MCP e prima dell'Agentic AI Foundation (AAIF).
- Blog LF: https://training.linuxfoundation.org/blog/just-launched-model-context-protocol-associate-mcpa-certification/ — temi: architettura host/client/server, interaction lifecycles, permissions & trust boundaries, security & governance.
- Blog AAIF: https://aaif.io/blog/introducing-the-mcpa-the-first-official-certification-for-the-model-context-protocol — advisory council SME (Anthropic, Google, AWS, Microsoft, Block, GitHub, Hugging Face…), learning path "in arrivo".

## Fonti NON ufficiali (solo mappa)
- devopscube.com/mcpa-certification-exam-guide — stessa mappa dei domini; da verificare sempre sulla spec.
