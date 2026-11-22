# practice-questions/ — Domande di allenamento gratuite (NON ufficiali)

> **A cosa serve questa sezione:** calibrare **stile, formato e difficoltà** delle domande che genereremo in Fase 2 e fornire un primo banco per il simulatore.
> **Non è una fonte di fatti.** Ogni fatto si verifica sulla spec 2026-07-28 (`../sources/spec-2026-07-28/`) e sulle dispense (`../notes/`).
> Nessuna di queste fonti contiene domande d'esame reali: sono tutte scritte da terzi. Siti di "domande reali" o dump **esclusi** (vedi in fondo).

Raccolta: 2026-11-22.

## Riepilogo

| Fonte | Domande gratuite | Formato | Allineata alla 2026-07-28? | Licenza | Cosa c'è qui |
|---|---|---|---|---|---|
| **rohitg00 / ai-engineering-from-scratch** (`certifications/mcpa`) | **414**: diagnostic 30 + 3 mock da 60 + 34 quiz di lezione da 6 | MC 4 opzioni, single (88%) e multiple "select 2/3", spiegazione per ogni domanda | **Sì, ottima** (scan + verifiche a campione sulla spec: 3 imprecisioni minori, 0 risposte sbagliate trovate) | **MIT** | **copia integrale** + versione normalizzata |
| **Hugging Face MCP Course** (quiz unit 1 e 3.1) | **23** (unit1: 10, unit3_1: 13) | MC 4 opzioni, single, spiegazione per opzione | Generiche, nessuna versione; 2 risposte non valide per MCP in generale | **Apache-2.0** | **copia integrale** + versione normalizzata |
| **CertSafari** | 35 (su banca da 350+) | MC single + multi-select, spiegazioni | **No**: molte domande da spec vecchia (initialize, sessioni, GET SSE, roots); landing page dice 120 min | proprietaria | catalogo argomenti + errori ([scheda](catalogo-fonti/certsafari.md)) |
| **eSEOspace — The MCP Guide** | 18 | MC 4 opzioni, single, spiegazione + link alla spec | **Sì** | proprietaria | catalogo argomenti ([scheda](catalogo-fonti/eseospace.md)) |
| **aguidetocloud** | 20 dichiarate (banca 250 a $9) | MC, modalità esame/studio | Non verificabile: domande caricate via JavaScript, non lette | proprietaria | solo scheda ([scheda](catalogo-fonti/aguidetocloud.md)) |
| **Cloud Soft Solutions** (exam guide) | 15 + 55 domande da colloquio | domande aperte con risposta breve, **non MC** | Exam guide **no** (initialize, sampling/roots come richieste server); interview guide in gran parte sì | proprietaria | catalogo + errori ([scheda](catalogo-fonti/cloudsoftsol.md)) |
| Altre risorse (WorkOS, eSEOspace study guide, howtoai, corsi gratuiti) | 0 domande MC MCPA | articoli / corsi | vario | — | [scheda](catalogo-fonti/altre-risorse.md) |

**Totale scaricato in locale:** 437 domande con licenza aperta (414 + 23). Delle altre fonti (circa 90 domande) ci sono solo cataloghi.

## Perché alcune fonti sono copiate e altre no
Le domande di CertSafari, eSEOspace, aguidetocloud e Cloud Soft Solutions sono **gratuite da consultare ma protette da copyright** (nessuna licenza di riuso). Copiarle integralmente in locale sarebbe una riproduzione non autorizzata. Per queste fonti ci sono:
- URL;
- numero di domande e distribuzione per dominio;
- **argomenti parafrasati**;
- **dove contraddicono la spec 2026-07-28**.

Per esercitarti su quelle domande apri il link (sono tutte senza login).

Le due fonti con **licenza aperta** (MIT, Apache-2.0) sono invece copiate integralmente, con licenza e attribuzione, e sono usabili nel simulatore.

## Struttura
```
practice-questions/
├── README.md                      ← questo file
├── open-licensed/
│   ├── rohitg00-mcpa/             (MIT, commit 9712e32)
│   │   ├── LICENSE  ATTRIBUTION.md
│   │   ├── assessments/           diagnostic.json, mock-01..03.json  (originali)
│   │   ├── lesson-quizzes/        00..33-*.json                       (originali)
│   │   ├── normalizzate.json      ← tutte le 414 in un formato unico (dominio D1-D5, opzioni A-D, review)
│   │   ├── source-verification-ledger.md, mcp-2026-07-28-brief.md
│   │   └── REVISIONE.md           ← verifica sulla spec: errori/imprecisioni trovati
│   └── huggingface-mcp-course/    (Apache-2.0, commit dbfa79b)
│       ├── LICENSE  ATTRIBUTION.md
│       ├── originali/*.mdx
│       ├── normalizzate.json
│       └── REVISIONE.md
└── catalogo-fonti/                schede delle fonti non copiabili
    ├── certsafari.md  eseospace.md  aguidetocloud.md  cloudsoftsol.md  altre-risorse.md
```

## Come usarle
- **Simulatore (Fase 3):** `rohitg00-mcpa/normalizzate.json` contiene già 3 mock da 60 domande pesati sui domini (D1 10, D2 8, D3 16, D4 14, D5 12) e 90 minuti. Le domande con `review.status` = `imprecisa` vanno mostrate con la nota.
- **Generazione (Fase 2):** usare queste domande come **riferimento di difficoltà e stile**, non come fonte. Le nostre domande devono essere originali, non parafrasi di queste.
- **Calibrazione:** l'esame è "Beginner", ma le domande migliori (rohitg00, eSEOspace) sono **scenari brevi** che richiedono di applicare una regola della spec. Le domande di pura definizione (HF, Cloud Soft) sono più facili dell'esame atteso.

## Distrattori ricorrenti nelle fonti datate
Utili per `../notes/13-trappole-e-ambiguita.md`. Nelle fonti non aggiornate tornano sempre gli stessi errori:
1. handshake `initialize` / `notifications/initialized` come primo passo;
2. sessione stateful / `Mcp-Session-Id`;
3. stream GET SSE standalone su cui il server invia richieste;
4. sampling, roots ed elicitation come richieste server→client, invece che via MRTR;
5. logging con livelli impostati per sessione;
6. durata d'esame di 120 minuti.

## Da evitare (non cercate né scaricate)
- **PassQuestion, CertEmpire, vmexam** e qualsiasi sito che promette "domande reali", "real exam questions", PDF o "dumps": violano il LF Certification & Confidentiality Agreement (s. 2.1 e 4.4: è misconduct anche la diffusione di "braindump" e la ricostruzione a memoria).
- **Udemy**, pacchetto da circa 400 domande: a pagamento, con una sola valutazione.
- Siti di software crackato o piratato emersi nelle ricerche: esclusi.
- Banche a pagamento (CertSafari 350, aguidetocloud 250): non acquistate né lette.
