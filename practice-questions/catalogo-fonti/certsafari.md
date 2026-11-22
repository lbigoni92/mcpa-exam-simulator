# CertSafari: MCPA practice questions

- Domande gratuite: https://www.certsafari.com/linux/model-context-protocol-associate/practice-questions
- Landing: https://www.certsafari.com/linux/model-context-protocol-associate
- Gratuite: **35** (banca dichiarata 350+, il resto a pagamento, non letto). Nessun login.
- Date: banca creata 2026-09-08, aggiornata 2026-09-09, guida ricontrollata 2026-11-20. "Exam guide version": **vuoto**, nessuna versione della spec dichiarata.
- Formato: MC a 4 opzioni, per lo più single. Alcune multi-select ("select 3/4"). Risposta e spiegazione per ogni opzione, senza link alla spec.
- Distribuzione: D1 7 · D2 6 · D3 8 · D4 8 · D5 6.
- Difficoltà: soprattutto richiamo e definizioni, con circa 5 scenari.
- Licenza: proprietaria → **non copiata**, solo catalogo.

## Argomenti (parafrasati)
- **D1**: formato JSON-RPC 2.0; statefulness tra chiamate; request e notification; ruolo Host; open standard; "tre pilastri" del design; un server condiviso tra più app.
- **D2**: flusso host→client→server; aggiunta progressiva di feature e retrocompatibilità; campi opzionali di una Resource; resource template; come il modello riceve il contenuto di una resource; flusso `tools/call`.
- **D3**: quali errori vanno in `isError: true`; errore di file mancante come tool error; `nextCursor` assente = fine; scopo del GET SSE standalone; `structuredContent`; tool sconosciuto = protocol error; method che "avvia la sessione"; protocol error vs isError (select 3).
- **D4**: session ID usato come autenticazione; controlli per l'installazione one-click di server locali (select 3); elicitation e dati sensibili; consenso prima di esporre roots; token passthrough in un proxy; URL OAuth aperti da shell; trust boundaries; livelli di logging.
- **D5**: deploy locale vs remoto; wiki interno; consenso nei rollout; workflow multi-tool; Agentic AI Foundation; ruolo dell'utente finale.
- Le domande 26-35 sono state lette solo in sintesi.

## ⚠️ Contraddizioni con la spec 2026-07-28 (molte)
| Domanda | Problema |
|---|---|
| Q2, Q4, Q6 | presentano la **statefulness** e la "sessione stateful" come principio core. Nella 2026-07-28 il protocollo è **stateless**. |
| Q8 | il server invia richieste stile sampling. **Falso**: nessuna richiesta server→client, si usa MRTR. |
| Q9 | capability negoziate nell'handshake **`initialize`**. Rimosso. |
| Q10 | dice che solo `uri` è obbligatorio e `name` no. Nella spec `name` è **obbligatorio** (`Resource` estende `BaseMetadata`). |
| Q17 | GET SSE standalone, richieste del server su quello stream, initialize obbligatorio. Tutto rimosso. |
| Q20 | "`initialize` deve essere il primo messaggio". Rimosso. |
| Q22 | session ID come autenticazione: la regola (non usarlo come auth) è giusta, ma `Mcp-Session-Id` non esiste più. |
| Q25 | consenso per i **roots**: deprecati. |
| Q26 | livelli di logging: logging deprecato, `logging/setLevel` rimosso. |
| Landing | **durata 120 minuti**: errato, la durata ufficiale è 90. |

**Uso consigliato:** esercizio "trova l'errore". Utile per riconoscere i distrattori da versione vecchia, non per studiare.
