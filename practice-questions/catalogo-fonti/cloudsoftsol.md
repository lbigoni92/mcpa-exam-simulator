# Cloud Soft Solutions (cloudsoftsol.com)

Istituto di formazione (Hyderabad) che vende corsi. Licenza proprietaria ("All rights reserved") → nessuna copia.

## 1. MCPA exam guide: 15 domande
- URL: https://cloudsoftsol.com/blog/mcpa-model-context-protocol-associate-exam-guide/ (aggiornato 2026-11-17)
- Formato: 15 domande **aperte** con risposta di una riga, **non MC**, senza link alla spec. Livello base.
- Dati d'esame: 90 min, $250, validità 2 anni, una retake (corretti).
- Argomenti: problema risolto da MCP; host; un server per client; JSON-RPC 2.0; inizializzazione; tool; resource; prompt; sampling; elicitation; stdio per server locali; timeout API come `isError`; argomenti da `inputSchema`; perché i risultati dei tool non sono fidati; OAuth 2.1 per server HTTP.

### ⚠️ Contraddizioni con la 2026-07-28
- Tabella dei concetti, riga "Lifecycle", e risposta Q5: descrivono l'handshake **`initialize` + `notifications/initialized`**. Rimosso.
- "Client primitives" e risposte Q9/Q10: sampling, roots ed elicitation come **richieste del server al client**. Ora solo via MRTR; sampling e roots sono **deprecati**.
- Piano di studio, settimana 2, e sezione security: roots come argomento attuale. Deprecati.
- Esempio JSON di `tools/call` **senza `_meta`** (`protocolVersion`, `clientCapabilities` obbligatori).
- Streamable HTTP descritto senza dire che sessioni e GET stream sono stati rimossi.

## 2. MCP interview questions: 55 domande
- URL: https://cloudsoftsol.com/blog/mcp-interview-questions/ (2026-10-06)
- Formato: domande **aperte** da colloquio con risposte estese, non MC. Le Q26-55 sono state lette solo in sintesi.
- Copre sia le versioni legacy sia la 2026-07-28, dichiarando quest'ultima come riferimento.
- Sezioni: Fundamentals (Q1-5), Architecture (6-9), Primitives (10-15), Transports (16-19), Building servers (20-24), Clients/hosts (25-27), Security (28-33), Authorization (34-37), Confronti MCP vs function calling / A2A / REST (38-40), Enterprise: gateway, registry, monitoring (41-43), Testing (44-45), Scenari (46-55).
- **In linea** con la 2026-07-28 su: stateless, assenza di initialize, `server/discover`, assenza di `Mcp-Session-Id`, MRTR, `subscriptions/listen`, sampling e roots deprecati, Tasks come estensione, DCR deprecata, stream non riprendibili.
- Da verificare: rinomina di FastMCP in `MCPServer` nell'SDK Python v2 (dettaglio di SDK, fuori dal perimetro dell'esame).
- **Uso:** buona per ripassare a voce e per idee di scenari (D4/D5). Non è in formato d'esame.
