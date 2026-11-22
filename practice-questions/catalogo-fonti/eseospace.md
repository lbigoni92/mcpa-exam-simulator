# eSEOspace (The MCP Guide): 18 MCPA practice questions

- URL: https://eseospace.com/blog/mcpa-practice-questions/
- Autrice: Irina Shvaya (eSEOspace, agenzia di marketing). Pubblicato 2026-10-28, rivisto 2026-11-16. Si dichiara non ufficiale; scritto a partire dai domini LF e dalla spec 2026-07-28.
- Nessun login. Risposte e spiegazioni in pagina, ciascuna con link alla pagina della spec.
- Formato: **18** MC, 4 opzioni (A-D), single.
- Distribuzione: D1 2 · D2 2 · D3 5 · D4 6 · D5 3.
- Difficoltà: richiamo più scenari brevi (circa 6), vicina allo stile atteso.
- Licenza: proprietaria → **non copiata**.
- Pagina collegata: study guide https://eseospace.com/blog/mcpa-study-guide/ (7 domande aperte di autoverifica, nessuna MC).

## Argomenti (parafrasati)
1. formato messaggi (JSON-RPC 2.0)
2. primitiva model-controlled (tools)
3. server per client (uno)
4. dove va la versione nella 2026-07-28 (`_meta`, non `initialize`)
5. errore di validazione input → risultato con `isError`
6. tool sconosciuto → protocol error
7. versione non supportata → `UnsupportedProtocolVersionError` con l'elenco delle versioni supportate
8. `server/discover` obbligatorio (MUST) per i server
9. MRTR `input_required` al posto delle richieste del server
10. rifiutare token non emessi per il server
11. tool annotations = hint non fidati
12. state handle ≠ autenticazione
13. MUST del server sull'invocazione dei tool (validazione, access control, rate limit, sanitizzazione output)
14. segreti tramite URL elicitation, non form
15. errore di progettazione degli scope (guida di sicurezza)
16. il registry ospita metadata, non codice
17. log su stdio (stderr / OpenTelemetry); logging deprecato
18. fallback o rifiuto se il peer non supporta un'estensione

## Contraddizioni con la 2026-07-28
Nessuna trovata. È la fonte proprietaria più allineata. Nota: nella study guide l'elicitation è descritta come "client feature" richiesta dal server; nella 2026-07-28 passa via MRTR (formulazione da aggiornare, non un errore grave).
