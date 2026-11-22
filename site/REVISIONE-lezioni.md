# Confronto con le 34 lezioni rohitg00 (2026-11-22)

Fonte: `certifications/mcpa/lessons/` di rohitg00/ai-engineering-from-scratch, commit `9712e323` (licenza MIT, curriculum comunitario non ufficiale).
Ogni cartella contiene `quiz.json`, `docs/en.md` (la lezione), `outputs/*.md` (il riassunto) e `code/` (lab Python e test).

## Domande
I `quiz.json` di tutte le 34 cartelle sono identici, byte per byte, ai file in `practice-questions/open-licensed/rohitg00-mcpa/lesson-quizzes/`, che erano già nel simulatore.

## Teoria
Ho confrontato i riassunti di ogni lezione, e le lezioni quando serviva, con i 74 topic del corso. Ho tenuto solo i fatti che mancavano e che ho ritrovato nelle fonti ufficiali (spec 2026-07-28, SEP, pagine su estensioni, registry e community, spec MCP Apps 2026-01-26).

- **110 punti nuovi** (IT/EN) in 41 topic esistenti, più il topic nuovo **D5-15 "MCP Apps nel dettaglio"** (7 punti).
- Script ripetibile: `site/build/lesson_points.py`. I punti nuovi non entrano nel collegamento automatico domanda → topic, così i link revisionati restano stabili. Fanno eccezione le domande su MCP Apps, che ora puntano a D5-15.

| Lezioni | Dove ho aggiunto | Cosa |
|---|---|---|
| 00-02 | D1-01 | equivalenze MUST/SHALL/REQUIRED ecc. |
| 01, 05, 15 | D1-06, D1-08, D3-19 | finestra di deprecazione (da quando decorre, rimozione dal 2027-07-28, ripristino), dettagli della cronologia delle revisioni, elenco completo di ciò che è stato rimosso |
| 03 | D2-07, D3-01 | grammatica e chiavi riservate di `_meta`, resultType non riconosciuto = invalido, id assente solo con -32700 |
| 04 | D3-02 | liste che non variano per connessione, cosa ha rimosso la 2026-07-28 |
| 05, 07 | D2-02, D3-03 | probe HTTP, matrice di compatibilità, `data` di -32021/-32022 e regole di retry |
| 08, 09 | D2-05, D2-06, D2-07 | outputSchema con qualsiasi JSON Schema, `$ref` non risolti, regole di x-mcp-header, icone (stessa origine, niente credenziali, SVG) |
| 10, 17 | D2-09, D3-06, D3-09 | cosa vede il modello, ordine stabile dei tool, validazione o esecuzione, race di cancellazione |
| 11-13 | D3-11, D3-15, D3-16, D3-17 | content block, schemi URI e errori delle risorse, cosa non è cacheable |
| 14 | D3-04, D3-18, D4-12 | tipi di inputRequests, comportamento di client e server nel retry, URL mode senza elicitationId, legami di requestState |
| 16 | D3-05 | chiusura gradevole o brusca delle subscription, subscription multiple |
| 18 | D3-08 | -32700, regole dei range, codici applicativi, errori locali |
| 19 | D2-03, D2-05 | maiuscole/minuscole negli header, regole base64, stderr |
| 20 | D3-07 | chiave di cache, input_required, copia scaduta, cacheScope uguale su tutte le pagine |
| 21 | D3-14 | Tasks in dettaglio: solo tools/call, campi di CreateTaskResult, creazione durevole, completed/failed, tasks/update, tasks/cancel |
| 22, 25 | D4-01, D4-05 | contenuti non fidati, limite ai tentativi di step-up |
| 23, 24 | D4-04, D4-06, D4-08, D4-09, D4-14 | ordine di discovery dell'AS con e senza path, iss anche sugli errori, URI canonico, CIMD, application_type, flusso EMA |
| 27 | D4-13 | formato traceparent, trace id come chiave tra servizi, campi di un record di audit |
| 28 | D4-15, D5-01 | tipi e stati dei SEP, responsabile che cambia con il deployment |
| 30 | D2-10 | prefisso obbligatorio, versionamento, Beta/Stable, experimental-ext-, stringa revision |
| 31 | D5-15 (nuovo) | mimeType, visibility, CSP, permessi, sandbox proxy, fallback testuale |
| 32 | D5-04, D5-06, D5-07 | ordine dei controlli in un gateway, requisiti Tier 2 e retrocessione, tipi di pacchetti, $schema del registry, scansione delegata |
| 06, 26, 29, 33 | nessuna aggiunta | già coperte dal corso |

## Non importato
- Suggerimenti di metodo senza base normativa: ore di studio, punteggio di prontezza, hash chain dei log, "pin dell'intero descrittore". Sono buone pratiche, ma non sono nella spec.
- I lab in `code/`: sono codice Python, non teoria d'esame.

## Errore trovato nelle lezioni
La lezione 30 e la domanda `quiz-30-06` dicono che **ogni** modifica incompatibile a un'estensione richiede un nuovo identificatore. La pagina ufficiale sulle estensioni (sezione Evolution) dice invece che l'identificatore resta lo stesso. Ne serve uno nuovo (es. `-v2`) solo quando vecchio e nuovo comportamento devono coesistere nella stessa revisione. Ho riformulato la domanda (errata in `build_data.py`, stato "corretta"). La domanda `m1-051` è coerente con la spec, perché descrive proprio il caso di coesistenza.
