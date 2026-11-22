# Revisione sulla spec 2026-07-28: rohitg00 MCPA (414 domande)

**Giudizio: la migliore fonte gratuita trovata.** Allineata alla 2026-07-28, scenari realistici, distrattori basati proprio sulle "trappole da versione vecchia". Ogni domanda ha una spiegazione.

## Numeri
| Set | Domande | Note |
|---|---|---|
| `mcpa-f-diagnostic` | 30 | D1 5 · D2 4 · D3 8 · D4 7 · D5 6 |
| `mcpa-f-mock-01` "Operational Scenarios" | 60 | D1 10 · D2 8 · D3 16 · D4 14 · D5 12, 90 min |
| `mcpa-f-mock-02` | 60 | stessa distribuzione |
| `mcpa-f-mock-03` | 60 | stessa distribuzione |
| quiz di lezione (34 × 6) | 204 | `stage` pre / check / post; dominio dedotto dalla lezione |
| **Totale** | **414** | D1 77 · D2 58 · D3 122 · D4 85 · D5 72 |

- Tipi: 378 single, 36 multiple (27 "select two", 9 "select three"). Sempre 4 opzioni.
- Risposte corrette ben bilanciate (A 92, B 96, C 97, D 93).
- La distribuzione dei mock coincide con quella del nostro `knowledge/manifest.json` (`distribution_example`, 60 domande).

## Metodo
1. **Scan automatico** di tutte le 414 risposte corrette e spiegazioni, cercando termini legacy (`initialize`, `Mcp-Session-Id`, `ping`, `setLevel`, `Last-Event-ID`, `-32002`, `resources/subscribe`, `120 min`...). Tutte le occorrenze compaiono come **distrattori o come "cosa è stato rimosso"**, mai come risposta corretta da spec vecchia.
2. **Verifica manuale** sulla spec locale delle domande con fatti "rischiosi": header HTTP, codici d'errore, cancellazione, caching (`ttlMs`/`cacheScope`, chiave di cache), SDK tiers, registry, fallback dual-era, deprecazioni. Circa 165 domande lette.

## Esito
| Stato (`review.status`) | N | Significato |
|---|---|---|
| `scan-ok` | 405 | nessun termine legacy nella risposta; non verificata riga per riga |
| `verificata` | 5 | controllata puntualmente sulla spec |
| `imprecisa` | 3 | risposta corretta, ma stem o spiegazione contengono un dettaglio impreciso |
| `datata` | 1 | domanda sulla durata 90 vs 120 (ora risolta: 90) |

### Imprecisioni trovate
- **mcpa-f-m2-003**: lo stem attribuisce la deprecazione di DCR a SEP-2577. Nella 2026-07-28 SEP-2577 depreca roots, sampling e logging, mentre DCR è deprecata dalla PR #2858. La risposta (finestra minima di 12 mesi) è corretta.
- **quiz 18-01 e 18-03**: la spiegazione dice che `-32002` è stato ritirato "prima" della 2026-07-28. In realtà la sostituzione con `-32602` avviene **nella** 2026-07-28 (SEP-2164). Le risposte sono corrette.
- **quiz 00-03**: registra la discrepanza 90/120. Ora le pagine LF confermano **90 minuti**.

### Verifiche puntuali (corrette)
- m1-033: `MCP-Protocol-Version` e `Mcp-Method` obbligatori su ogni POST (`basic/transports/streamable-http.md`). Ci ha fatto anche correggere `notes/10`, che diceva "Mcp-Name obbligatorio su POST": è obbligatorio solo su `tools/call`, `resources/read`, `prompts/get`.
- m1-032: fallback dual-era su stdio (`stdio.md`, `versioning.md`).
- quiz 32-06: relegation degli SDK dopo 4 settimane di fallimenti (`community/sdk-tiers.md`).
- quiz 20-04: risultati di retry MRTR (`inputResponses`/`requestState`) MUST NOT essere cachati (`server/utilities/caching.md`).
- m1-058: registry in preview (`registry/about.md`).

## Attenzione
- Nota sul curriculum: considera **60 domande** come dimensione di pratica, non come dato ufficiale. Le regole LF generiche per gli esami MC dicono 60 domande e 75% di soglia (vedi `../../../sources/exam/lf-exam-page.md`).
- Le domande sono in inglese, come l'esame.
- Se usi queste domande per studiare, **non** considerarle fonte normativa: in caso di dubbio vale la spec.
