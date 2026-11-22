# Revisione delle domande (2026-11-22)

Verifica delle 154 domande originali sulla spec locale 2026-07-28 (`sources/spec-2026-07-28/`, estensioni, registry, community).

## Errori di contenuto corretti
- **o-D2-09** (stream interrotto): la risposta diceva "reinviala se sicuro". La spec dice che il client MUST reinviarla come nuova richiesta con nuovo id (SEP-2575).
- **o-D2-11** (x-mcp-header su number): la spiegazione dava un motivo inventato. Ora riporta la regola: solo integer, string e boolean; integer nell'intervallo sicuro ±2^53−1.
- **o-D5-22** (versione nel registry): l'opzione "latest" non è elencata dalla pagina del registry, quindi era ambigua. Sostituita con "1.x", che è esplicitamente vietata.

## Doppioni sostituiti con un altro aspetto dello stesso argomento
- **o-D3-27**: era uguale a o-D2-08 (GET → 405). Ora chiede del metodo non implementato (404 con -32601).
- **o-D5-28**: era uguale a o-D2-05 (log su stdout). Ora chiede cosa resta uguale tra stdio e HTTP.
- **o-D4-01**: era uguale a o-D2-16 (clientInfo non verificato). Ora chiede perché le descrizioni dei tool vanno trattate con cautela.

## Indizio involontario rimosso
In 50 domande su 135 a risposta singola la risposta giusta era nettamente la più lunga. Ho riscritto le opzioni di 35 domande e ora i casi sono 17, con uno scarto minore.

## Domande rohitg00 (licenza MIT)
Correzioni applicate in `build/build_data.py` (ERRATA) e segnalate nel sito con una nota:
- **m2-003**: lo stem attribuiva la deprecazione di DCR a SEP-2577.
- **quiz 18-01**: la spiegazione diceva che -32002 era stato ritirato "prima" della 2026-07-28.
- **quiz 18-03**: stesso errore, presente sia nell'opzione D sia nella spiegazione.
- **quiz 00-03**: aggiunta una nota che la durata è 90 minuti.

## Collegamenti alla teoria
- L'abbinamento automatico ora usa anche il titolo della lezione e il testo delle domande originali di ogni argomento.
- Non è più vincolato al dominio: prima, per esempio, "tool sconosciuto → -32602" in D1 finiva su un argomento D1.
- 57 collegamenti sono stati corretti a mano in `build/topic_overrides.json`.

Rigenerare: `python3 site/build/review_fixes.py && python3 site/build/build_data.py`
