# Revisione: Hugging Face MCP Course quiz (23 domande)

**Giudizio:** quiz introduttivi, più facili dell'esame. Utili solo per D1 (Fundamentals) e qualche concetto di D2. Nessuna versione della spec dichiarata. Le risposte corrette cadono quasi sempre su B o C (prevedibili).

| Quiz | Domande | Argomenti | Utilità MCPA |
|---|---|---|---|
| unit1-quiz1 "MCP Fundamentals" | 5 | scopo di MCP, problema M×N, standardizzazione, Host | buona per D1 |
| unit1-quiz2 "MCP SDK" | 5 | scopo degli SDK, serializzazione, JSON-RPC 2.0, comando dev server | parziale |
| unit3_1-quiz1 "MCP Server Implementation" | 6 | progetto "Pull Request Agent" su Hugging Face Hub, FastMCP | bassa (specifico del progetto) |
| unit3_1-quiz2 | 7 | webhook, FastAPI, agent client via stdio | bassa |

## Problemi rispetto alla spec 2026-07-28 e all'ecosistema attuale
- **unit1-quiz2-q3** dice che "Anthropic" mantiene l'SDK Python ufficiale. La domanda stessa dice "according to the provided text". Oggi gli SDK sono nel GitHub org `modelcontextprotocol`, sotto la governance AAIF / Linux Foundation, e sono classificati per tier (`../../../sources/community/sdk-tiers.md`). **Non usare come fatto.**
- **unit3_1-quiz1-q2**: "i tool MCP devono restituire stringhe". Vale solo per quel progetto. Nella spec un tool restituisce **content blocks** (text, image, audio, resource link, embedded resource) e opzionalmente `structuredContent` (qualsiasi valore JSON). **Falso in generale.**
- **unit1-quiz2-q4** (`mcp dev server.py`): comando del CLI dell'SDK Python, fuori dal perimetro dell'esame.
- Nessuna domanda menziona initialize o sessioni: niente errori "da versione vecchia".
