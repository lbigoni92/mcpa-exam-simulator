(function () {
  "use strict";
  var app = document.getElementById("app");
  function api(path, body) {
    var o = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
    return fetch(path, o).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
  }
  var KEY = "mcpa-sim-lang";
  var S = { lang: "it" };
  try { var lg = localStorage.getItem(KEY); if (lg === "it" || lg === "en") S.lang = lg; } catch (e) {}
  function save() { try { localStorage.setItem(KEY, S.lang); } catch (e) {} }
  if (location.protocol === "file:") {
    app.innerHTML = '<div class="card"><h1>Avvia il simulatore</h1><p>Da questa versione domande e progressi stanno in un database locale (SQLite). Chiudi questa pagina e fai doppio clic su <b>avvia.bat</b> nella cartella <code>site</code>: si apre il browser su <code>http://127.0.0.1:8765</code>.</p><p class="muted small">From this version questions and progress live in a local SQLite database. Double-click <b>avvia.bat</b> in the <code>site</code> folder.</p></div>';
    return;
  }
  Promise.all([api("/api/data"), api("/api/stats")]).then(function (r) { main(r[0], r[1]); }).catch(function (e) {
    app.innerHTML = '<div class="card"><h1>Server non raggiungibile</h1><p>Il server locale non risponde (' + String(e.message).replace(/</g, "&lt;") + '). Riavvialo con <b>avvia.bat</b> e ricarica la pagina.</p></div>';
  });

  function main(DATA, STATS) {
  // ---------- i18n ----------
  var T = {
    it: {
      navHome: "Home", navCourse: "Corso", navQuiz: "Simulatore", navReview: "Ripasso errori", navAbout: "Fonti",
      footer: "Spec di riferimento 2026-07-28. Materiale di studio non ufficiale: in caso di dubbio vale la spec.",
      welcome: "Preparazione all'esame MCPA", intro: "Studia un dominio nel corso, poi mettiti alla prova. Ogni errore ti mostra la teoria e ti porta alla pagina del corso che spiega quel punto.",
      examCta: "Simulazione d'esame (60 domande, 90 min)", studyCta: "Allenamento con feedback immediato", reviewCta: "Ripassa gli errori",
      progress: "Il tuo andamento per dominio", answered: "risposte", accuracy: "corrette", weight: "peso esame", studyW: "peso studio",
      lastExams: "Ultime simulazioni", none: "Nessuna ancora.", course: "Corso", topics: "argomenti", keyQ: "Domande chiave",
      trap: "Trappola d'esame", source: "Fonte", backCourse: "Tutti i domini", openTheory: "Apri la teoria", theory: "Teoria",
      correct: "Corretto", wrong: "Sbagliato", rightIs: "Risposta giusta", confirm: "Conferma", next: "Avanti", prev: "Indietro",
      finish: "Termina e correggi", chooseN: "Seleziona {n} risposte", flag: "Segna", unflag: "Togli segno",
      setup: "Imposta la sessione", mode: "Modalità", modeExam: "Esame: timer 90 min, correzione alla fine", modeStudy: "Studio: feedback dopo ogni domanda",
      pool: "Domande", poolOrig: "Originali IT/EN (questo corso)", poolAll: "Tutte le fonti", poolRgMock: "rohitg00 · mock", poolRgDiag: "rohitg00 · diagnostico (30)", poolRgQuiz: "rohitg00 · quiz di lezione", poolHf: "Hugging Face MCP Course (generale, non 2026-07-28)",
      domains: "Domini", count: "Numero di domande", onlyNew: "Prima quelle mai viste o sbagliate", start: "Inizia",
      examNote: "In modalità esame vengono estratte 60 domande con la distribuzione 10/8/16/14/12 (D1…D5). Un mock rohitg00 si usa intero.",
      enOnly: "Questa domanda è disponibile solo in inglese.", timeUp: "Tempo scaduto: la prova è stata consegnata.",
      result: "Risultato", passLine: "Soglia indicativa 75%", passed: "Superato", failed: "Non superato", byDomain: "Per dominio",
      wrongList: "Domande sbagliate", noneWrong: "Nessun errore. Ottimo lavoro.", again: "Nuova sessione", toReview: "Gli errori sono stati aggiunti al ripasso.",
      reviewTitle: "Ripasso errori", reviewIntro: "Le domande sbagliate restano qui finché non rispondi correttamente due volte di fila.", reviewEmpty: "Il ripasso è vuoto.", reviewStart: "Ripassa ora ({n})",
      inReview: "da ripassare", streakNote: "corrette di fila: {n}/2", unanswered: "Senza risposta", score: "Punteggio",
      reviewNote: "Nota di revisione", origLabel: "Originale", sessionDone: "Sessione completata", reset: "Azzera statistiche", resetQ: "Azzerare statistiche, ripasso e storico?",
      approx: "collegamento automatico", of: "di", q: "Domanda", time: "Tempo",
      aboutTitle: "Fonti e licenze", resume: "Riprendi la sessione",
      navProgress: "Progressi", progressTitle: "I tuoi progressi", progressIntro: "Ogni sessione di studio o d'esame è salvata nel database locale. Qui vedi come cambia il punteggio nel tempo, in totale e per dominio.",
      sessionsN: "sessioni", trendLbl: "Andamento", chartNote: "Punteggio di ogni sessione in ordine di tempo; la linea tratteggiata è la soglia del 75%.",
      domain: "Dominio", overall: "Totale risposte", last30: "Ultime 30 risposte", trendHelp: "Andamento = media delle ultime sessioni meno media delle prime (fino a 3 per lato). Per dominio contano solo le sessioni con almeno 3 domande di quel dominio.",
      weakTitle: "Argomenti più deboli", allSessions: "Tutte le sessioni", date: "Data", answersTitle: "Domande e risposte date",
      deleteSession: "Elimina sessione", deleteQ: "Eliminare questa sessione e le sue risposte dal database?", vsPrev: "Rispetto alla sessione precedente",
      modeExamShort: "Esame", modeStudyShort: "Studio", recentNote: "Percentuale sulle ultime 30 risposte di ogni dominio.",
      poolHard: "Difficili (scenari, risposte multiple)", hardLabel: "Difficile", difficulty: "Difficoltà", diffAll: "Tutte", diffHard: "Solo difficili (livello 3 e risposte multiple)",
      objectives: "Obiettivi del dominio (curriculum rohitg00)", objectivesNote: "Riformulazione comunitaria degli obiettivi, in inglese, non ufficiale (licenza MIT). Fa fede la pagina LF dell'esame.", userLabel: "Domanda personale", noQuestions: "Nessuna domanda corrisponde ai filtri scelti.", saveError: "Errore nel salvataggio sul database.", flaggedN1: "1 segnata", finishUnans1: "Hai 1 domanda senza risposta: verrà contata come sbagliata.", finishFlag1: "Hai 1 domanda segnata da ricontrollare.", searchN1: "1 argomento trovato", secStudy: "Studia", secPractice: "Esercitati", secInfo: "Info", navDomains: "Mostra o nascondi i domini", menuMini: "Riduci o espandi il menu", menuOpen: "Apri il menu", sessionN: "Sessione #{n}", prevDom: "Dominio precedente", nextDom: "Dominio successivo", toIndex: "indice", skip: "Vai al contenuto", themeAuto: "Tema: automatico (clic per chiaro)", themeLight: "Tema: chiaro (clic per scuro)", themeDark: "Tema: scuro (clic per automatico)",
      statAnswered: "risposte date", statAccuracy: "corrette in totale", statSessions: "sessioni completate", statReview: "da ripassare", statReady: "stima esame",
      readyNote: "Media delle ultime 30 risposte di ogni dominio, pesata con i pesi ufficiali. Compare quando ogni dominio ha almeno 5 risposte.",
      resumeTitle: "Hai una sessione in corso", resumeBtn: "Riprendi", quickStart: "Avvio rapido", presetExam: "Esame completo", presetQuick: "10 domande veloci", presetSec: "Solo Security & Governance", presetHard: "Solo difficili",
      modeStudyT: "Studio", modeStudyD: "Feedback e teoria subito dopo ogni risposta", modeExamT: "Esame", modeExamD: "60 domande, timer di 90 minuti, correzione alla fine",
      answeredN: "{a} di {n} risposte", flaggedN: "{n} segnate", qmap: "Mappa domande", legAns: "risposta data", legFlag: "segnata", availN: "{n} domande disponibili con questi filtri",
      kbdHint: "Tastiera: A–D o 1–4 per rispondere · Invio per confermare o andare avanti · ← → per spostarti · F per segnare (esame)",
      finishTitle: "Consegnare la prova?", finishUnans: "Hai {n} domande senza risposta: verranno contate come sbagliate.", finishFlag: "Hai {n} domande segnate da ricontrollare.", finishOk: "Hai risposto a tutte le domande.", finishGo: "Consegna", cancel: "Annulla",
      searchPh: "Cerca un argomento (es. elicitation, OAuth, -32022)", searchNone: "Nessun argomento trovato.", searchN: "{n} argomenti trovati", selectedN: "selezionate {s} di {n}", backTop: "Torna su", deleteGo: "Elimina",
      conf_sure: "Sicuro", conf_doubt: "Dubbio", conf_guess: "Tirata a indovinare",
      confAsk: "Quanto sei sicuro? La scelta conferma la risposta.", confAskExam: "Quanto sei sicuro? (facoltativo)",
      confLucky: "Giusta, ma tirata a indovinare: la domanda va comunque nel ripasso.", confDoubtOk: "Giusta ma con un dubbio: rileggi la teoria qui sotto per fissarla.", confSureWrong: "Eri sicuro ma è sbagliata: è il tipo di errore più importante da correggere.",
      navSettings: "Impostazioni", navFlash: "Flashcard",
      setTitle: "Impostazioni", setIntro: "Le opzioni sono salvate nel database locale e valgono subito.",
      setSrs: "Ripasso dilazionato degli errori", setSrsD: "Una domanda sbagliata o tirata a indovinare torna subito, poi dopo 1, 3 e 7 giorni; esce dal ripasso dopo quattro risposte giuste di fila. Se lo disattivi resta nel ripasso finché non rispondi giusto due volte di fila, senza attese.",
      setConf: "Confidenza sulla risposta", setConfD: "Dopo aver scelto indichi se eri sicuro, in dubbio o se hai tirato a indovinare. Le risposte giuste tirate a indovinare finiscono nel ripasso e la pagina Progressi mostra quanto sei preciso per ogni livello.",
      setPace: "Analisi dei tempi e ritmo d'esame", setPaceD: "Durante l'esame un indicatore dice se sei in anticipo o in ritardo rispetto a 90 secondi per domanda. La pagina Progressi mostra il tempo medio per dominio e gli argomenti più lenti.",
      dataTitle: "Esporta e importa i progressi", dataIntro: "Il file contiene sessioni, risposte, ripasso, flashcard e impostazioni. Serve come backup e per spostare i progressi tra la versione Docker e quella Python.",
      exportBtn: "Esporta i progressi", importBtn: "Importa da file", importTitle: "Importare i progressi?", importQ: "I progressi attuali verranno sostituiti con quelli del file (esportato il {d}, {n} risposte). Se ti servono, esportali prima.", importGo: "Importa e sostituisci",
      importOk: "Progressi importati: {n} risposte.", importSkipped: "{n} righe saltate perché riferite a domande che qui non ci sono.", importBad: "Il file non è un export valido del simulatore.", exportOk: "File scaricato: {f}", saved: "Impostazione salvata.",
      reviewIntroSrs: "Le domande sbagliate o tirate a indovinare tornano oggi, poi dopo 1, 3 e 7 giorni. Escono dal ripasso dopo quattro risposte giuste di fila.",
      reviewDue: "Da ripassare oggi", reviewLater: "Prossimi ripassi", reviewNone: "Niente da ripassare oggi. Prossimo ripasso: {d}.", reasonGuess: "indovinata", reasonWrong: "sbagliata", boxN: "livello {n}/4", dueOn: "dal {d}",
      paceAhead: "in anticipo di {m}", paceBehind: "in ritardo di {m}", paceOk: "ritmo giusto", paceTitle: "Ritmo rispetto a 90 secondi per domanda",
      confTitle: "Confidenza e precisione", confIntro: "Quanto sei preciso quando sei sicuro, in dubbio o tiri a indovinare. Il segnale che sei pronto: quasi 100% sulle risposte date come sicure.", confNone: "Ancora nessuna risposta con la confidenza.",
      luckyN: "{n} risposte giuste tirate a indovinare: sono finite nel ripasso.", sureWrongN: "{n} errori su risposte date come sicure: sono i punti da rivedere per primi.", answersN: "{n} risposte",
      timeTitle: "Tempi di risposta", timeIntro: "Tempo medio per domanda nelle sessioni di studio e d'esame, rispetto ai 90 secondi disponibili in media all'esame.", avgTime: "Tempo medio", slowTitle: "Argomenti più lenti", timeNone: "Ancora nessun tempo registrato.",
      presetAdaptive: "Esame adattivo", adaptiveCta: "Esame adattivo sui punti deboli", poolAdaptive: "Adattivo (punti deboli)",
      adaptiveNote: "L'esame adattivo usa la distribuzione ufficiale per dominio e sceglie le domande da ripassare, quelle sbagliate di recente, quelle mai viste e quelle degli argomenti con la percentuale più bassa.",
      flashTitle: "Flashcard", flashIntro: "Carte generate dai punti del corso: codici di errore, header, metodi, campi, RFC e parole chiave normative. Si parte dagli argomenti dove sbagli di più e le carte che non sapevi tornano prima.",
      flashScopeWeak: "Punti deboli", flashScopeAll: "Tutto il corso", flashAllDoms: "Tutti i domini", flashDue: "da ripetere", flashNew: "nuove", flashStart: "Inizia ({n} carte)", flashShow: "Mostra la risposta", flashKnew: "Lo sapevo", flashNot: "Non lo sapevo",
      flashDone: "Mazzo finito", flashResult: "Sapevi {k} carte su {n}.", flashAgain: "Altro giro", flashEmpty: "Nessuna carta da fare con questi filtri: torna domani per quelle da ripetere oppure scegli «Tutto il corso».", flashMiss: "Da rivedere",
      flashWeakNote: "Punti deboli: argomenti sotto il 75%, con domande nel ripasso o con carte che non sapevi. Senza risposte date si parte dai domini con più peso all'esame.", flashKbd: "Tastiera: Spazio o Invio per girare la carta · 1 non lo sapevo · 2 lo sapevo", flashCardN: "Carta {i} di {n}", flashFill: "Completa il punto", flashTotal: "{n} carte nel corso",
      kbdHintConf: "Tastiera: A–D o 1–4 per scegliere · Invio per confermare come «sicuro» · ← → per spostarti · F per segnare (esame)"
    },
    en: {
      navHome: "Home", navCourse: "Course", navQuiz: "Simulator", navReview: "Error review", navAbout: "Sources",
      footer: "Reference spec 2026-07-28. Unofficial study material: when in doubt, the spec wins.",
      welcome: "MCPA exam preparation", intro: "Study a domain in the course, then test yourself. Every mistake shows you the theory and links to the course page explaining that point.",
      examCta: "Exam simulation (60 questions, 90 min)", studyCta: "Practice with instant feedback", reviewCta: "Review mistakes",
      progress: "Your progress by domain", answered: "answered", accuracy: "correct", weight: "exam weight", studyW: "study weight",
      lastExams: "Recent simulations", none: "None yet.", course: "Course", topics: "topics", keyQ: "Key questions",
      trap: "Exam trap", source: "Source", backCourse: "All domains", openTheory: "Open the theory", theory: "Theory",
      correct: "Correct", wrong: "Wrong", rightIs: "Correct answer", confirm: "Confirm", next: "Next", prev: "Back",
      finish: "Finish and score", chooseN: "Select {n} answers", flag: "Flag", unflag: "Unflag",
      setup: "Set up the session", mode: "Mode", modeExam: "Exam: 90-minute timer, scored at the end", modeStudy: "Study: feedback after each question",
      pool: "Questions", poolOrig: "Original IT/EN (this course)", poolAll: "All sources", poolRgMock: "rohitg00 · mock", poolRgDiag: "rohitg00 · diagnostic (30)", poolRgQuiz: "rohitg00 · lesson quizzes", poolHf: "Hugging Face MCP Course (general, not 2026-07-28)",
      domains: "Domains", count: "Number of questions", onlyNew: "Unseen or missed questions first", start: "Start",
      examNote: "Exam mode draws 60 questions with the 10/8/16/14/12 distribution (D1…D5). A rohitg00 mock is used in full.",
      enOnly: "", timeUp: "Time is up: the exam has been submitted.",
      result: "Result", passLine: "Indicative pass mark 75%", passed: "Passed", failed: "Not passed", byDomain: "By domain",
      wrongList: "Missed questions", noneWrong: "No mistakes. Well done.", again: "New session", toReview: "Mistakes were added to the review queue.",
      reviewTitle: "Error review", reviewIntro: "Missed questions stay here until you answer them correctly twice in a row.", reviewEmpty: "The review queue is empty.", reviewStart: "Review now ({n})",
      inReview: "to review", streakNote: "correct in a row: {n}/2", unanswered: "Unanswered", score: "Score",
      reviewNote: "Review note", origLabel: "Original", sessionDone: "Session complete", reset: "Reset statistics", resetQ: "Reset statistics, review queue and history?",
      approx: "automatic link", of: "of", q: "Question", time: "Time",
      aboutTitle: "Sources and licenses", resume: "Resume session",
      navProgress: "Progress", progressTitle: "Your progress", progressIntro: "Every study or exam session is saved in the local database. Here you can see how your score changes over time, overall and per domain.",
      sessionsN: "sessions", trendLbl: "Trend", chartNote: "Score of each session in time order; the dashed line is the 75% pass mark.",
      domain: "Domain", overall: "All answers", last30: "Last 30 answers", trendHelp: "Trend = average of the latest sessions minus average of the first ones (up to 3 each). Per domain, only sessions with at least 3 questions from that domain count.",
      weakTitle: "Weakest topics", allSessions: "All sessions", date: "Date", answersTitle: "Questions and answers given",
      deleteSession: "Delete session", deleteQ: "Delete this session and its answers from the database?", vsPrev: "Compared with the previous session",
      modeExamShort: "Exam", modeStudyShort: "Study", recentNote: "Percentage over the last 30 answers in each domain.",
      poolHard: "Hard (scenarios, multiple answers)", hardLabel: "Hard", difficulty: "Difficulty", diffAll: "All", diffHard: "Hard only (level 3 and multiple answers)",
      objectives: "Domain objectives (rohitg00 curriculum)", objectivesNote: "Community rewording of the objectives, unofficial (MIT license). The LF exam page is authoritative.", userLabel: "Personal question", noQuestions: "No question matches the chosen filters.", saveError: "Error saving to the database.", flaggedN1: "1 flagged", finishUnans1: "You have 1 unanswered question: it will count as wrong.", finishFlag1: "You have 1 flagged question to double-check.", searchN1: "1 topic found", secStudy: "Study", secPractice: "Practice", secInfo: "Info", navDomains: "Show or hide the domains", menuMini: "Collapse or expand the menu", menuOpen: "Open the menu", sessionN: "Session #{n}", prevDom: "Previous domain", nextDom: "Next domain", toIndex: "index", skip: "Skip to content", themeAuto: "Theme: automatic (click for light)", themeLight: "Theme: light (click for dark)", themeDark: "Theme: dark (click for automatic)",
      statAnswered: "answers given", statAccuracy: "correct overall", statSessions: "sessions completed", statReview: "to review", statReady: "exam estimate",
      readyNote: "Average of the last 30 answers in each domain, weighted by the official weights. Shown once every domain has at least 5 answers.",
      resumeTitle: "You have a session in progress", resumeBtn: "Resume", quickStart: "Quick start", presetExam: "Full exam", presetQuick: "10 quick questions", presetSec: "Security & Governance only", presetHard: "Hard only",
      modeStudyT: "Study", modeStudyD: "Feedback and theory right after each answer", modeExamT: "Exam", modeExamD: "60 questions, 90-minute timer, scored at the end",
      answeredN: "{a} of {n} answered", flaggedN: "{n} flagged", qmap: "Question map", legAns: "answered", legFlag: "flagged", availN: "{n} questions available with these filters",
      kbdHint: "Keyboard: A–D or 1–4 to answer · Enter to confirm or move on · ← → to navigate · F to flag (exam)",
      finishTitle: "Submit the exam?", finishUnans: "You have {n} unanswered questions: they will count as wrong.", finishFlag: "You have {n} flagged questions to double-check.", finishOk: "You answered every question.", finishGo: "Submit", cancel: "Cancel",
      searchPh: "Search a topic (e.g. elicitation, OAuth, -32022)", searchNone: "No topic found.", searchN: "{n} topics found", selectedN: "{s} of {n} selected", backTop: "Back to top", deleteGo: "Delete",
      conf_sure: "Sure", conf_doubt: "Unsure", conf_guess: "Guessed",
      confAsk: "How sure are you? Your choice confirms the answer.", confAskExam: "How sure are you? (optional)",
      confLucky: "Correct, but guessed: the question still goes to the review queue.", confDoubtOk: "Correct but unsure: reread the theory below to lock it in.", confSureWrong: "You were sure but it is wrong: this is the most important kind of mistake to fix.",
      navSettings: "Settings", navFlash: "Flashcards",
      setTitle: "Settings", setIntro: "Options are saved in the local database and apply right away.",
      setSrs: "Spaced review of mistakes", setSrsD: "A missed or guessed question comes back right away, then after 1, 3 and 7 days; it leaves the queue after four correct answers in a row. When off, it stays until you answer correctly twice in a row, with no waiting.",
      setConf: "Answer confidence", setConfD: "After choosing, you say whether you were sure, unsure or guessing. Correct guesses go to the review queue and the Progress page shows your accuracy at each level.",
      setPace: "Timing analysis and exam pace", setPaceD: "During the exam an indicator tells you whether you are ahead of or behind 90 seconds per question. The Progress page shows the average time per domain and the slowest topics.",
      dataTitle: "Export and import progress", dataIntro: "The file holds sessions, answers, review queue, flashcards and settings. Use it as a backup and to move progress between the Docker and the Python version.",
      exportBtn: "Export progress", importBtn: "Import from file", importTitle: "Import progress?", importQ: "Your current progress will be replaced by the file's (exported {d}, {n} answers). Export it first if you need it.", importGo: "Import and replace",
      importOk: "Progress imported: {n} answers.", importSkipped: "{n} rows skipped because they refer to questions that are not here.", importBad: "The file is not a valid simulator export.", exportOk: "File downloaded: {f}", saved: "Setting saved.",
      reviewIntroSrs: "Missed or guessed questions come back today, then after 1, 3 and 7 days. They leave the queue after four correct answers in a row.",
      reviewDue: "Due today", reviewLater: "Coming up", reviewNone: "Nothing due today. Next review: {d}.", reasonGuess: "guessed", reasonWrong: "missed", boxN: "level {n}/4", dueOn: "from {d}",
      paceAhead: "{m} ahead", paceBehind: "{m} behind", paceOk: "on pace", paceTitle: "Pace against 90 seconds per question",
      confTitle: "Confidence and accuracy", confIntro: "How accurate you are when sure, unsure or guessing. The sign you are ready: close to 100% on answers given as sure.", confNone: "No answers with confidence yet.",
      luckyN: "{n} correct answers were guesses: they went to the review queue.", sureWrongN: "{n} mistakes on answers given as sure: review these first.", answersN: "{n} answers",
      timeTitle: "Answer times", timeIntro: "Average time per question in study and exam sessions, against the 90 seconds available on average in the exam.", avgTime: "Average time", slowTitle: "Slowest topics", timeNone: "No times recorded yet.",
      presetAdaptive: "Adaptive exam", adaptiveCta: "Adaptive exam on weak points", poolAdaptive: "Adaptive (weak points)",
      adaptiveNote: "The adaptive exam uses the official domain distribution and picks questions due for review, recently missed, never seen and from the topics with the lowest score.",
      flashTitle: "Flashcards", flashIntro: "Cards generated from the course points: error codes, headers, methods, fields, RFCs and normative keywords. They start from the topics where you miss most, and cards you did not know come back sooner.",
      flashScopeWeak: "Weak points", flashScopeAll: "Whole course", flashAllDoms: "All domains", flashDue: "due", flashNew: "new", flashStart: "Start ({n} cards)", flashShow: "Show the answer", flashKnew: "I knew it", flashNot: "I didn't know",
      flashDone: "Deck finished", flashResult: "You knew {k} of {n} cards.", flashAgain: "Another round", flashEmpty: "No cards to do with these filters: come back tomorrow for due cards or choose “Whole course”.", flashMiss: "To review",
      flashWeakNote: "Weak points: topics below 75%, with questions in the review queue or cards you did not know. With no answers yet, it starts from the domains with the highest exam weight.", flashKbd: "Keyboard: Space or Enter to flip the card · 1 didn't know · 2 knew it", flashCardN: "Card {i} of {n}", flashFill: "Complete the point", flashTotal: "{n} cards in the course",
      kbdHintConf: "Keyboard: A–D or 1–4 to choose · Enter to confirm as “sure” · ← → to navigate · F to flag (exam)"
    }
  };
  function tn(k, n, vars) { vars = vars || {}; vars.n = n; return t(n === 1 && T[S.lang][k + "1"] ? k + "1" : k, vars); }
  function t(k, vars) { var s = (T[S.lang] && T[S.lang][k]) || T.it[k] || k; if (vars) for (var v in vars) s = s.replace("{" + v + "}", vars[v]); return s; }
  function L(o) { if (!o) return ""; if (typeof o === "string") return o; return o[S.lang] || o.en || o.it || ""; }
  function hasLang(o) { return o && typeof o === "object" && !!o[S.lang]; }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function fmt(s) { return esc(s).replace(/`([^`]+)`/g, "<code>$1</code>"); }

  // ---------- indexes ----------
  var TOPIC = {}, DOMAIN = {}, QBYID = {}, QBYTOPIC = {};
  DATA.course.forEach(function (d) { DOMAIN[d.id] = d; d.topics.forEach(function (tp) { tp.dom = d.id; TOPIC[tp.id] = tp; }); });
  DATA.questions.forEach(function (q) { QBYID[q.id] = q; if (q.src === "original") (QBYTOPIC[q.t] = QBYTOPIC[q.t] || []).push(q); });
  var DOMS = ["D1", "D2", "D3", "D4", "D5"];
  var EXAM_DIST = { D1: 10, D2: 8, D3: 16, D4: 14, D5: 12 };

  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var x = a[i]; a[i] = a[j]; a[j] = x; } return a; }
  function domTag(d) { return '<span class="dom ' + d + '">' + d + "</span>"; }

  // ---------- stats ----------
  function setting(k) { return !STATS.settings || STATS.settings[k] !== false; }
  function inReview(id) { return STATS.review.hasOwnProperty(id); }
  function dueIds() { return Object.keys(STATS.review).filter(function (id) { return QBYID[id] && (STATS.review[id].due || !setting("srs")); }); }
  function record(q, ok, conf) {
    var s = STATS.qstats[q.id] || { n: 0, ok: 0, last: 0 };
    s.n++; if (ok) s.ok++; s.last = ok ? 1 : 0; STATS.qstats[q.id] = s;
    if (!ok || conf === "guess") STATS.review[q.id] = { streak: 0, box: 0, due: true, reason: ok ? "guess" : "wrong" };
    [STATS.totals, STATS.recent].forEach(function (b) { var x = b[q.dom] || (b[q.dom] = { n: 0, ok: 0 }); x.n++; if (ok) x.ok++; });
    var ts = STATS.topicStats[q.t] || (STATS.topicStats[q.t] = { n: 0, ok: 0 }); ts.n++; if (ok) ts.ok++;
  }
  function refreshStats() { return api("/api/stats").then(function (x) { STATS = x; updateBadge(); }).catch(function () {}); }
  // domande chiave del corso: una sessione "course" per visita, creata alla prima risposta
  var courseSid = null;
  function persistCourse(st) {
    var send = function () { return api("/api/answers", { session_id: courseSid, question_id: st.q.id, selected: st.sel, time_ms: 0, confidence: st.conf || null }).then(refreshStats); };
    if (courseSid) return send().catch(function () {});
    api("/api/sessions", { mode: "course", pool: "course", questions: [st.q.id] }).then(function (r) { courseSid = r.id; return send(); }).catch(function () {});
  }

  // ---------- question widget ----------
  // opts: {mode:'instant'|'exam', onAnswer(ok), persist(st, ok)}
  var CONF = ["sure", "doubt", "guess"], CONF_ICON = { sure: "✓", doubt: "?", guess: "~" };
  function prepare(q) { return { q: q, order: shuffle(q.o.map(function (_, i) { return i; })), sel: [], done: false, conf: null }; }
  function isCorrect(st) { var c = st.q.c.slice().sort().join(","); return st.sel.slice().sort().join(",") === c; }
  function complete(st) { return st.sel.length === st.q.c.length; }
  function confLabel(k) { return t("conf_" + k); }

  function theoryHtml(q) {
    var tp = TOPIC[q.t]; if (!tp) return "";
    var pts = (tp.points[S.lang] || tp.points.en || []).map(function (p) { return "<li>" + fmt(p) + "</li>"; }).join("");
    return '<div class="theory"><div class="spread"><h3>' + t("theory") + ": " + esc(L(tp.title)) + "</h3>" + domTag(tp.dom) + "</div>" +
      "<p>" + fmt(L(tp.summary)) + "</p><ul>" + pts + "</ul>" +
      (tp.trap ? '<div class="trap"><b>' + t("trap") + ":</b> " + fmt(L(tp.trap)) + "</div>" : "") +
      '<a class="btn ghost" href="#t/' + tp.id + '"' + (location.hash === "#run" ? ' target="_blank" rel="noopener"' : "") + ">" + t("openTheory") + " →</a>" +
      (q.src !== "original" ? ' <span class="chip">' + t("approx") + "</span>" : "") + "</div>";
  }

  function qHtml(st, opt) {
    var q = st.q, multi = q.c.length > 1, show = st.done && opt.mode !== "exam", useConf = setting("confidence") && !opt.readonly;
    var h = '<div class="q">';
    h += '<div class="row small muted">' + domTag(q.dom) + (q.src === "original" ? ' <span class="chip">' + (q.set === "hard" ? t("hardLabel") : q.set === "utente" ? t("userLabel") : t("origLabel")) + "</span>" : ' <span class="chip">' + esc(q.src) + " · " + esc(q.set) + "</span>") +
      (inReview(q.id) ? ' <span class="chip">' + t("inReview") + "</span>" : "") + (show ? ' <span class="small muted" style="margin-left:auto" title="id">' + esc(q.id) + "</span>" : "") + "</div>";
    if (!hasLang(q.q) && S.lang === "it") h += '<div class="note">' + t("enOnly") + "</div>";
    h += '<div class="stem">' + fmt(L(q.q)) + "</div>";
    if (multi) h += '<div class="hint"><b>' + t("chooseN", { n: q.c.length }) + "</b>" + (show ? "" : " · " + t("selectedN", { s: st.sel.length, n: q.c.length })) + "</div>";
    st.order.forEach(function (oi, pos) {
      var cls = "opt";
      if (st.sel.indexOf(oi) >= 0) cls += " sel";
      if (show) { if (q.c.indexOf(oi) >= 0) cls += " right"; else if (st.sel.indexOf(oi) >= 0) cls += " wrong"; }
      if (multi) cls += " multi";
      h += '<button type="button" class="' + cls + '" data-oi="' + oi + '"' + (show ? " disabled" : "") + '><span class="k">' + "ABCDEFG"[pos] + "</span><span>" + fmt(L(q.o[oi])) + "</span></button>";
    });
    if (!show && opt.mode !== "exam" && useConf) {
      // studio: la scelta della confidenza conferma la risposta
      h += '<div class="conf"><span class="hint">' + t("confAsk") + '</span><div class="conf-btns">' + CONF.map(function (k) {
        return '<button type="button" class="btn ghost conf-' + k + '" data-conf="' + k + '"' + (complete(st) ? "" : " disabled") + ">" + CONF_ICON[k] + " " + confLabel(k) + "</button>"; }).join("") + "</div></div>";
    } else if (!show && opt.mode === "exam" && useConf) {
      h += '<div class="conf"><span class="hint">' + t("confAskExam") + '</span><div class="conf-btns">' + CONF.map(function (k) {
        return '<button type="button" class="btn ghost conf-' + k + (st.conf === k ? " on" : "") + '" data-conf="' + k + '" aria-pressed="' + (st.conf === k) + '">' + CONF_ICON[k] + " " + confLabel(k) + "</button>"; }).join("") + "</div></div>";
    } else if (multi && !st.done && opt.mode !== "exam") h += '<button type="button" class="btn" data-act="confirm"' + (complete(st) ? "" : " disabled") + ">" + t("confirm") + "</button>";
    if (show) h += feedbackHtml(st);
    return h + "</div>";
  }
  function feedbackHtml(st) {
    var q = st.q, ok = isCorrect(st);
    var right = st.order.filter(function (oi) { return q.c.indexOf(oi) >= 0; }).map(function (oi) { return "ABCDEFG"[st.order.indexOf(oi)]; }).join(", ");
    var h = '<div class="fb ' + (ok ? "ok" : "bad") + '"><h4>' + (ok ? "✓ " + t("correct") : "✗ " + t("wrong") + " · " + t("rightIs") + ": " + right) +
      (st.conf ? ' <span class="chip conf-chip conf-' + st.conf + '">' + CONF_ICON[st.conf] + " " + confLabel(st.conf) + "</span>" : "") +
      (st.ms >= 1000 && setting("pacing") ? ' <span class="chip">⏱ ' + Math.round(st.ms / 1000) + " s</span>" : "") + "</h4>";
    if (st.conf && ok && st.conf === "guess") h += '<div class="note">' + t("confLucky") + "</div>";
    else if (st.conf && ok && st.conf === "doubt") h += '<div class="note">' + t("confDoubtOk") + "</div>";
    else if (st.conf && !ok && st.conf === "sure") h += '<div class="note">' + t("confSureWrong") + "</div>";
    h += "<div>" + fmt(L(q.x)) + "</div>";
    if (q.review) h += '<div class="note"><b>' + t("reviewNote") + ":</b> " + esc(q.review.note || q.review.status) + "</div>";
    if (!ok || st.conf === "guess" || st.conf === "doubt") h += theoryHtml(q);
    else if (TOPIC[q.t]) h += '<div class="small" style="margin-top:.4rem"><a href="#t/' + q.t + '">' + t("theory") + ": " + esc(L(TOPIC[q.t].title)) + " →</a></div>";
    return h + "</div>";
  }
  // wire clicks inside container for one question state
  function bindQ(el, st, opt, rerender) {
    el.onclick = function (ev) {
      var b = ev.target.closest("button"); if (!b || b.disabled) return;
      if (b.dataset.act === "confirm") { finishQ(st, opt); rerender(); return; }
      if (b.dataset.conf) {
        if (opt.mode === "exam") st.conf = st.conf === b.dataset.conf ? null : b.dataset.conf;
        else { st.conf = b.dataset.conf; finishQ(st, opt); }
        rerender(); return;
      }
      if (b.dataset.oi === undefined || (st.done && opt.mode !== "exam")) return;
      var oi = +b.dataset.oi, multi = st.q.c.length > 1, useConf = setting("confidence");
      if (multi) { var i = st.sel.indexOf(oi); if (i >= 0) st.sel.splice(i, 1); else if (st.sel.length < st.q.c.length || opt.mode === "exam") st.sel.push(oi); }
      else { st.sel = [oi]; if (opt.mode !== "exam" && !useConf) finishQ(st, opt); }
      rerender();
    };
  }
  function finishQ(st, opt) { if (st.done) return; st.done = true; var ok = isCorrect(st); record(st.q, ok, st.conf); if (opt.persist) opt.persist(st, ok); if (opt.onAnswer) opt.onAnswer(ok); }

  // ---------- pages ----------
  function pct(x) { return x && x.n ? Math.round(100 * x.ok / x.n) : null; }
  function fmtDur(sec) { sec = sec || 0; var m = Math.floor(sec / 60), s = sec % 60; return m + " min " + (s < 10 ? "0" : "") + s + " s"; }
  function fmtDate(iso) { return iso ? iso.replace("T", " ").slice(0, 16) : ""; }
  function modeLabel(m) { return m === "exam" ? t("modeExamShort") : t("modeStudyShort"); }
  function poolLabel(p) {
    var m = { orig: t("poolOrig"), hard: t("poolHard"), all: t("poolAll"), "rg-quiz": t("poolRgQuiz"), hf: "Hugging Face", review: t("navReview"), adaptive: t("poolAdaptive"), "mcpa-f-diagnostic": t("poolRgDiag") };
    return m[p] || (/^mcpa-f-mock/.test(p) ? t("poolRgMock") + " " + p.slice(-2) : p);
  }
  function sessionsOf(mode) { return STATS.sessions.filter(function (x) { return x.mode === mode; }); }
  // confronto tra la media delle prime 3 e delle ultime 3 sessioni della stessa modalità
  function trend(list, d) {
    var v = list.map(function (x) { return d ? pct(x.byDom[d]) : x.score_pct; }).filter(function (x) { return x !== null && x !== undefined; });
    if (v.length < 2) return null;
    var k = Math.min(3, Math.floor(v.length / 2)), avg = function (a) { return a.reduce(function (s, x) { return s + x; }, 0) / a.length; };
    return { first: Math.round(avg(v.slice(0, k))), last: Math.round(avg(v.slice(-k))), n: v.length };
  }
  function deltaTxt(tr) { if (!tr) return "–"; var d = tr.last - tr.first; return (d > 0 ? "+" : "") + d + " pt"; }
  function deltaHtml(mode) {
    var list = sessionsOf(mode); if (list.length < 2) return "";
    var prev = list[list.length - 2], cur = list[list.length - 1], d = Math.round(cur.score_pct - prev.score_pct);
    return '<div class="small" style="margin-top:.3rem">' + t("vsPrev") + ": <b class=\"" + (d >= 0 ? "pass" : "fail") + '">' + (d > 0 ? "+" : "") + d + " pt</b></div>";
  }

  function pageHome() {
    var rv = dueIds().length;
    var totN = 0, totOk = 0; DOMS.forEach(function (d) { var x = STATS.totals[d]; if (x) { totN += x.n; totOk += x.ok; } });
    var done = STATS.sessions.filter(function (x) { return x.mode === "exam" || x.mode === "study"; }).length;
    // stima esame: % delle ultime 30 risposte per dominio pesata con i pesi ufficiali, solo se ogni dominio ha almeno 5 risposte
    var ready = null, wsum = 0, acc = 0, okAll = true;
    DATA.course.forEach(function (d) { var r = STATS.recent[d.id]; if (!r || r.n < 5) okAll = false; else { acc += d.weight * r.ok / r.n; wsum += d.weight; } });
    if (okAll && wsum) ready = Math.round(100 * acc / wsum);
    var h = "";
    if (session && !session.over) h += resumeHtml();
    h += '<section class="hero"><h1>' + t("welcome") + '</h1><p class="lead">' + t("intro") + "</p>" +
      '<div class="row"><a class="btn lg" href="#quiz/exam">' + t("examCta") + '</a><a class="btn ghost lg" href="#quiz">' + t("studyCta") + "</a>" +
      (totN ? '<button type="button" class="btn ghost lg" id="adaptBtn">' + t("adaptiveCta") + "</button>" : "") +
      (rv ? '<a class="btn ghost lg" href="#review">' + t("reviewCta") + " (" + rv + ")</a>" : "") + "</div>" +
      '<div class="stats">' +
      stat(totN, t("statAnswered")) +
      stat(totN ? Math.round(100 * totOk / totN) + "%" : "–", t("statAccuracy")) +
      stat(done, t("statSessions")) +
      stat(rv, t("statReview")) +
      stat(ready === null ? "–" : ready + "%", t("statReady"), ready === null ? "" : ready >= 75 ? "pass" : "fail", t("readyNote")) +
      "</div></section>";
    h += "<h2>" + t("progress") + '</h2><p class="small muted">' + t("recentNote") + '</p><div class="grid">';
    DATA.course.forEach(function (d) {
      var r = STATS.recent[d.id] || { n: 0, ok: 0 }, tot = STATS.totals[d.id] || { n: 0, ok: 0 }, p = pct(r);
      h += '<a class="card domcard" href="#course/' + d.id + '"><div class="spread">' + domTag(d.id) + '<span class="small muted">' + t("weight") + " " + d.weight + "%</span></div>" +
        "<h3>" + esc(L(d.title)) + "</h3>" +
        '<div class="spread"><span class="pct ' + (p === null ? "muted" : p >= 75 ? "pass" : "fail") + '">' + (p === null ? "–" : p + "%") + '</span><span class="small muted">' + tot.n + " " + t("answered") + " · " + d.topics.length + " " + t("topics") + "</span></div>" +
        '<div class="bar ' + (r.n ? (p >= 75 ? "ok" : "bad") : "") + '"><i style="width:' + (p || 0) + '%"></i></div></a>';
    });
    h += "</div><h2>" + t("lastExams") + "</h2>" + sessionsTable(STATS.sessions.slice(-8).reverse());
    app.innerHTML = h;
    var ab = document.getElementById("adaptBtn"); if (ab) ab.onclick = startAdaptive;
  }
  function stat(v, l, cls, title) { return '<div class="stat"' + (title ? ' title="' + esc(title) + '"' : "") + '><div class="v ' + (cls || "") + '">' + v + '</div><div class="l">' + esc(l) + (title ? " ⓘ" : "") + "</div></div>"; }
  function resumeHtml() {
    var s = session, a = s.items.filter(function (x) { return x.sel.length; }).length;
    return '<div class="resume"><div><b>' + t("resumeTitle") + '</b><div class="small muted">' + esc(modeLabel(s.mode)) + " · " + t("answeredN", { a: a, n: s.items.length }) +
      (s.mode === "exam" ? " · " + fmtTime(s.end - Date.now()) : "") + '</div></div><a class="btn" href="#run">' + t("resumeBtn") + " →</a></div>";
  }

  function sessionsTable(list) {
    if (!list.length) return '<p class="muted">' + t("none") + "</p>";
    var h = '<div class="card" style="overflow-x:auto"><table><tr><th>' + t("date") + "</th><th>" + t("mode") + "</th><th>" + t("score") + "</th><th>" + t("time") + "</th>" + DOMS.map(function (d) { return "<th>" + d + "</th>"; }).join("") + "</tr>";
    list.forEach(function (r) {
      h += '<tr><td><a href="#session/' + r.id + '">' + esc(fmtDate(r.started_at)) + "</a></td><td>" + esc(modeLabel(r.mode)) + '<div class="small muted">' + esc(poolLabel(r.pool)) + "</div></td><td><b class=\"" + (r.score_pct >= 75 ? "pass" : "fail") + "\">" + Math.round(r.score_pct) + "%</b> <span class=\"small muted\">" + r.n_correct + "/" + r.n_questions + "</span></td><td class=\"small\">" + fmtDur(r.duration_s) + "</td>" +
        DOMS.map(function (d) { var p = pct(r.byDom[d]); return "<td>" + (p === null ? "–" : p + "%") + "</td>"; }).join("") + "</tr>";
    });
    return h + "</table></div>";
  }

  // grafico a linee SVG: una serie, soglia 75%, tooltip nativo + etichetta all'ultimo punto
  function lineChart(vals, labels, color, h, w) {
    h = h || 160; w = w || 600; var padL = 34, padR = 44, padT = 10, padB = 22;
    if (!vals.length) return "";
    var n = vals.length, x = function (i) { return padL + (n === 1 ? (w - padL - padR) / 2 : i * (w - padL - padR) / (n - 1)); }, y = function (v) { return padT + (100 - v) * (h - padT - padB) / 100; };
    var g = "";
    [0, 25, 50, 75, 100].forEach(function (v) { g += '<line x1="' + padL + '" x2="' + (w - padR) + '" y1="' + y(v) + '" y2="' + y(v) + '" class="grid' + (v === 75 ? " pass-line" : "") + '"/><text x="' + (padL - 6) + '" y="' + (y(v) + 4) + '" class="ax" text-anchor="end">' + v + "</text>"; });
    var path = vals.map(function (v, i) { return (i ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1); }).join(" ");
    var dots = vals.map(function (v, i) { return '<g class="pt"><circle cx="' + x(i) + '" cy="' + y(v) + '" r="10" fill="transparent"/><circle cx="' + x(i) + '" cy="' + y(v) + '" r="4" fill="' + color + '" stroke="var(--panel)" stroke-width="2"/><title>' + esc(labels[i]) + ": " + v + "%</title></g>"; }).join("");
    var last = vals[n - 1];
    return '<svg viewBox="0 0 ' + w + " " + h + '" class="chart" role="img" aria-label="' + esc(labels.join(", ")) + '">' + g +
      '<path d="' + path + '" fill="none" stroke="' + color + '" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>' + dots +
      '<text x="' + (x(n - 1) + 8) + '" y="' + (y(last) + 4) + '" class="lbl">' + last + "%</text></svg>";
  }

  function pageProgress() {
    var h = "<h1>" + t("progressTitle") + '</h1><p class="muted">' + t("progressIntro") + "</p>";
    var modes = [["exam", t("modeExamShort")], ["study", t("modeStudyShort")]], any = false;
    modes.forEach(function (m) {
      var list = sessionsOf(m[0]); if (!list.length) return; any = true;
      var tr = trend(list);
      h += '<div class="card"><div class="spread"><h2 style="margin:0">' + esc(m[1]) + ' <span class="chip">' + list.length + " " + t("sessionsN") + '</span></h2><div class="small">' + t("trendLbl") + ": <b>" + deltaTxt(tr) + "</b>" + (tr ? ' <span class="muted">(' + tr.first + "% → " + tr.last + "%)</span>" : "") + "</div></div>" +
        '<p class="small muted">' + t("chartNote") + "</p>" +
        lineChart(list.map(function (x) { return Math.round(x.score_pct); }), list.map(function (x) { return fmtDate(x.started_at); }), "var(--accent)") + "</div>";
    });
    if (!any) { app.innerHTML = h + '<p class="muted">' + t("none") + "</p>"; return; }
    // per dominio: tutte le sessioni (esame + studio), piccoli multipli
    var all = STATS.sessions;
    h += "<h2>" + t("byDomain") + '</h2><div class="card" style="overflow-x:auto"><table><tr><th>' + t("domain") + "</th><th>" + t("overall") + "</th><th>" + t("last30") + "</th><th>" + t("trendLbl") + "</th></tr>";
    DOMS.forEach(function (d) {
      var tr = trend(all.filter(function (x) { return x.byDom[d] && x.byDom[d].n >= 3; }), d), r = STATS.recent[d], tot = STATS.totals[d];
      h += "<tr><td>" + domTag(d) + " " + esc(L(DOMAIN[d].title)) + "</td><td>" + (pct(tot) === null ? "–" : pct(tot) + "% <span class=\"small muted\">(" + tot.n + ")</span>") + "</td><td>" + (pct(r) === null ? "–" : pct(r) + "%") + "</td><td><b>" + deltaTxt(tr) + "</b>" + (tr ? ' <span class="small muted">' + tr.first + "% → " + tr.last + "%</span>" : "") + "</td></tr>";
    });
    h += '</table><p class="small muted">' + t("trendHelp") + '</p></div><div class="grid">';
    DOMS.forEach(function (d) {
      var list = all.filter(function (x) { return x.byDom[d] && x.byDom[d].n >= 3; });
      if (list.length < 2) return;
      h += '<div class="card"><h3>' + domTag(d) + " " + esc(L(DOMAIN[d].title)) + "</h3>" + lineChart(list.map(function (x) { return pct(x.byDom[d]); }), list.map(function (x) { return fmtDate(x.started_at); }), "var(--" + d.toLowerCase() + ")", 150, 260) + "</div>";
    });
    h += "</div>";
    if (STATS.weakTopics.length) {
      h += "<h2>" + t("weakTitle") + '</h2><div class="card"><ul>' + STATS.weakTopics.map(function (w) {
        return '<li>' + domTag(w.domain_id) + ' <a href="#t/' + w.id + '">' + esc(S.lang === "it" ? w.title_it : w.title_en) + "</a> · " + Math.round(100 * w.ok / w.n) + "% (" + w.ok + "/" + w.n + ")</li>";
      }).join("") + "</ul></div>";
    }
    h += confSection() + timeSection();
    h += "<h2>" + t("allSessions") + "</h2>" + sessionsTable(all.slice().reverse());
    app.innerHTML = h;
  }

  function pageSession(id) {
    app.innerHTML = '<p class="muted">…</p>';
    api("/api/sessions/" + id).then(function (s) {
      var h = "<h1>" + esc(modeLabel(s.mode)) + " · " + esc(fmtDate(s.started_at)) + "</h1>";
      h += '<div class="card"><div class="spread"><div><div class="big ' + (s.score_pct >= 75 ? "pass" : "fail") + '">' + Math.round(s.score_pct || 0) + '%</div><div class="muted">' + s.n_correct + " / " + s.n_questions + " · " + fmtDur(s.duration_s) + " · " + esc(poolLabel(s.pool)) + "</div></div>" +
        '<button type="button" class="btn danger" id="del">' + t("deleteSession") + "</button></div><table style=\"margin-top:.8rem\">";
      DOMS.forEach(function (d) { var x = s.byDom[d]; if (!x) return; var p = pct(x); h += "<tr><td>" + domTag(d) + " " + esc(L(DOMAIN[d].title)) + "</td><td>" + x.ok + "/" + x.n + " (" + p + "%)</td></tr>"; });
      h += "</table></div><h2>" + t("answersTitle") + "</h2>";
      s.items.forEach(function (it, i) { h += '<div class="card" data-i="' + i + '"></div>'; });
      app.innerHTML = h;
      s.items.forEach(function (it, i) {
        var q = QBYID[it.question_id], el = app.querySelector('[data-i="' + i + '"]'); if (!q) { el.textContent = it.question_id; return; }
        var st = { q: q, order: q.o.map(function (_, k) { return k; }), sel: it.selected_json ? JSON.parse(it.selected_json) : [], done: true, conf: it.confidence, ms: it.time_ms };
        el.innerHTML = (it.selected_json === null || !st.sel.length ? '<div class="note">' + t("unanswered") + "</div>" : "") + qHtml(st, { mode: "instant" });
      });
      document.getElementById("del").onclick = function () {
        modal(t("deleteSession"), "<p>" + t("deleteQ") + "</p>", t("deleteGo"), function () {
          api("/api/sessions/" + id + "/delete", {}).then(refreshStats).then(function () { updateBadge(); location.hash = "#progress"; });
        }, true);
      };
    }).catch(function () { app.innerHTML = '<p class="muted">' + t("none") + "</p>"; });
  }

  function pageCourse() {
    var h = "<h1>" + t("course") + '</h1><div class="card"><input type="search" id="tsearch" placeholder="' + esc(t("searchPh")) + '" aria-label="' + esc(t("searchPh")) + '" autocomplete="off"><div id="tres" aria-live="polite"></div></div><div class="grid" id="dgrid">';
    DATA.course.forEach(function (d) {
      h += '<div class="card"><div class="spread">' + domTag(d.id) + '<span class="small muted">' + d.topics.length + " " + t("topics") + " · " + t("weight") + " " + d.weight + "%</span></div>" +
        '<h3 style="margin-top:.5rem"><a href="#course/' + d.id + '">' + esc(L(d.title)) + '</a></h3><ul class="small" style="padding-left:1.1rem;margin:.3rem 0">' +
        d.topics.slice(0, 5).map(function (tp) { return '<li><a href="#t/' + tp.id + '">' + esc(L(tp.title)) + "</a></li>"; }).join("") +
        (d.topics.length > 5 ? '<li><a class="muted" href="#course/' + d.id + '">+' + (d.topics.length - 5) + "…</a></li>" : "") + "</ul></div>";
    });
    app.innerHTML = h + "</div>";
    var inp = document.getElementById("tsearch"), res = document.getElementById("tres"), grid = document.getElementById("dgrid");
    function hl(s, q) { var i = s.toLowerCase().indexOf(q); return i < 0 ? esc(s) : esc(s.slice(0, i)) + "<mark>" + esc(s.slice(i, i + q.length)) + "</mark>" + esc(s.slice(i + q.length)); }
    inp.oninput = function () {
      var q = inp.value.trim().toLowerCase();
      grid.style.display = q.length >= 2 ? "none" : "";
      if (q.length < 2) { res.innerHTML = ""; return; }
      var out = [];
      DATA.course.forEach(function (d) { d.topics.forEach(function (tp) {
        var pts = tp.points[S.lang] || tp.points.en || [], title = L(tp.title), summ = L(tp.summary);
        var hit = title.toLowerCase().indexOf(q) >= 0 ? title : summ.toLowerCase().indexOf(q) >= 0 ? summ : (pts.filter(function (p) { return p.toLowerCase().indexOf(q) >= 0; })[0] || (tp.trap && L(tp.trap).toLowerCase().indexOf(q) >= 0 ? L(tp.trap) : null));
        if (hit !== null && hit !== undefined) out.push({ tp: tp, d: d.id, title: title, hit: hit, score: title.toLowerCase().indexOf(q) >= 0 ? 0 : 1 });
      }); });
      out.sort(function (a, b) { return a.score - b.score; });
      res.innerHTML = '<p class="small muted" style="margin:.6rem 0 0">' + (out.length ? tn("searchN", out.length) : t("searchNone")) + '</p><ul class="search-results">' + out.slice(0, 40).map(function (o) {
        var snip = o.hit === o.title ? L(o.tp.summary) : o.hit; if (snip.length > 220) { var i = Math.max(0, snip.toLowerCase().indexOf(q) - 80); snip = (i ? "…" : "") + snip.slice(i, i + 220) + "…"; }
        return "<li>" + domTag(o.d) + ' <a href="#t/' + o.tp.id + '"><b>' + hl(o.title, q) + '</b></a><div class="small muted">' + hl(snip, q) + "</div></li>";
      }).join("") + "</ul>";
    };
    if (window.innerWidth > 720) inp.focus();
  }

  var keyStates = {};
  function pageDomain(did, focus) {
    var d = DOMAIN[did]; if (!d) return pageCourse();
    var h = "<h1>" + domTag(d.id) + " " + esc(L(d.title)) + '</h1><p class="muted">' + d.topics.length + " " + t("topics") + " · " + t("weight") + " " + d.weight + "%</p>";
    if (d.objectives && d.objectives.en) h += '<div class="card"><details><summary>' + t("objectives") + '</summary><ul class="small">' + d.objectives.en.map(function (o) { return "<li>" + esc(o) + "</li>"; }).join("") + '</ul><div class="small muted">' + t("objectivesNote") + "</div></details></div>";
    h += '<div class="card" id="toc"><ol class="toc">' + d.topics.map(function (tp) { return '<li><a href="#t/' + tp.id + '">' + esc(L(tp.title)) + "</a></li>"; }).join("") + "</ol></div>";
    d.topics.forEach(function (tp) {
      var pts = (tp.points[S.lang] || tp.points.en || []).map(function (p) { return "<li>" + fmt(p) + "</li>"; }).join("");
      h += '<section class="card topic" id="topic-' + tp.id + '"><div class="spread"><h2 style="margin:0">' + esc(L(tp.title)) + '</h2><span class="row"><span class="chip">' + tp.id + '</span><a class="topic-up" href="#course/' + d.id + '" title="' + t("toIndex") + '">↑ ' + t("toIndex") + "</a></span></div>" +
        "<p>" + fmt(L(tp.summary)) + "</p><ul>" + pts + "</ul>" +
        (tp.trap ? '<div class="trap"><b>' + t("trap") + ":</b> " + fmt(L(tp.trap)) + "</div>" : "") +
        (tp.source ? '<div class="small muted">' + t("source") + ': <a href="' + esc(tp.source.url) + '" target="_blank" rel="noopener">' + esc(tp.source.label) + "</a></div>" : "");
      var kq = QBYTOPIC[tp.id] || [];
      if (kq.length) {
        h += '<div class="keyq"><details' + (focus === tp.id ? " open" : "") + "><summary>" + t("keyQ") + " (" + kq.length + ")</summary>" +
          kq.map(function (q) { return '<div class="kq" data-q="' + q.id + '"></div>'; }).join("") + "</details></div>";
      }
      h += "</section>";
    });
    var di = DOMS.indexOf(d.id), pv = DOMAIN[DOMS[di - 1]], nx = DOMAIN[DOMS[di + 1]];
    h += '<nav class="pager">' + (pv ? '<a href="#course/' + pv.id + '"><span class="k">← ' + t("prevDom") + "</span>" + domTag(pv.id) + " " + esc(L(pv.title)) + "</a>" : "") +
      (nx ? '<a class="next" href="#course/' + nx.id + '"><span class="k">' + t("nextDom") + " →</span>" + domTag(nx.id) + " " + esc(L(nx.title)) + "</a>" : "") + "</nav>";
    h += '<button type="button" class="icon-btn backtop" id="backtop" title="' + t("backTop") + '" aria-label="' + t("backTop") + '">↑</button>';
    app.innerHTML = h;
    document.getElementById("backtop").onclick = function () { window.scrollTo(0, 0); };
    app.querySelectorAll(".topic-up").forEach(function (x) { x.onclick = function (e) { e.preventDefault(); document.getElementById("toc").scrollIntoView(); }; });
    app.querySelectorAll(".kq").forEach(function (el) {
      var q = QBYID[el.dataset.q]; var st = keyStates[q.id] || (keyStates[q.id] = prepare(q));
      var opt = { mode: "instant", persist: persistCourse };
      var rr = function () { el.innerHTML = qHtml(st, opt); };
      bindQ(el, st, opt, rr); rr();
    });
    if (focus) {
      var el = document.getElementById("topic-" + focus);
      if (el) { el.scrollIntoView({ behavior: "instant", block: "start" }); el.classList.add("flash"); setTimeout(function () { el.classList.remove("flash"); }, 1600); }
    } else window.scrollTo(0, 0);
  }

  // ---------- simulator ----------
  var session = null, timerId = null;
  function poolOf(key) {
    var all = DATA.questions;
    if (key === "orig") return all.filter(function (q) { return q.src === "original"; });
    if (key === "all") return all.filter(function (q) { return q.src !== "huggingface"; });
    if (key === "rg-quiz") return all.filter(function (q) { return q.src === "rohitg00" && q.set.indexOf("lesson-quiz/") === 0; });
    if (key === "hf") return all.filter(function (q) { return q.src === "huggingface"; });
    if (key === "hard") return all.filter(function (q) { return q.set === "hard"; });
    return all.filter(function (q) { return q.set === key; });
  }
  function priority(q) { var s = STATS.qstats[q.id], r = STATS.review[q.id]; if (r && (r.due || !setting("srs"))) return 0; if (!s) return 1; if (!s.last) return 0; return 2; }
  function pick(pool, n, doms, onlyNew) {
    pool = shuffle(pool.filter(function (q) { return doms.indexOf(q.dom) >= 0; }));
    if (onlyNew) pool.sort(function (a, b) { return priority(a) - priority(b); });
    return pool.slice(0, n);
  }
  function pickExam(pool) {
    var out = [];
    DOMS.forEach(function (d) { out = out.concat(pick(pool, EXAM_DIST[d], [d], true)); });
    var need = 60 - out.length;
    if (need > 0) { var ids = {}; out.forEach(function (q) { ids[q.id] = 1; }); out = out.concat(shuffle(pool.filter(function (q) { return !ids[q.id]; })).slice(0, need)); }
    return shuffle(out);
  }

  function pageSetup(presetExam) {
    stopTimer();
    var sets = {}; DATA.questions.forEach(function (q) { if (q.src === "rohitg00" && /^mcpa-f-mock/.test(q.set)) sets[q.set] = q.setTitle; });
    var h = "<h1>" + t("setup") + "</h1>";
    if (session && !session.over) h += resumeHtml();
    h += '<div class="presets" aria-label="' + esc(t("quickStart")) + '"><span class="small muted" style="align-self:center">' + t("quickStart") + ':</span>' +
      '<button type="button" data-preset="exam">' + t("presetExam") + '</button><button type="button" data-preset="quick">' + t("presetQuick") + '</button>' +
      '<button type="button" data-preset="sec">' + t("presetSec") + '</button><button type="button" data-preset="hard">' + t("presetHard") + '</button><button type="button" data-preset="adaptive" title="' + esc(t("adaptiveNote")) + '">' + t("presetAdaptive") + "</button></div>";
    h += '<div class="card"><form id="setup">';
    h += '<label class="f">' + t("mode") + '</label><div class="choice">' +
      '<label><input type="radio" name="mode" value="study"' + (presetExam ? "" : " checked") + "><span><b>" + t("modeStudyT") + '</b><span class="small muted">' + t("modeStudyD") + "</span></span></label>" +
      '<label><input type="radio" name="mode" value="exam"' + (presetExam ? " checked" : "") + "><span><b>" + t("modeExamT") + '</b><span class="small muted">' + t("modeExamD") + "</span></span></label></div>";
    h += '<label class="f" for="pool">' + t("pool") + '</label><select id="pool" name="pool"><option value="orig">' + t("poolOrig") + '</option><option value="hard">' + t("poolHard") + '</option><option value="all">' + t("poolAll") + "</option>" +
      Object.keys(sets).sort().map(function (k) { return '<option value="' + k + '">' + t("poolRgMock") + " " + k.slice(-2) + " · " + esc(sets[k]) + "</option>"; }).join("") +
      '<option value="mcpa-f-diagnostic">' + t("poolRgDiag") + '</option><option value="rg-quiz">' + t("poolRgQuiz") + '</option><option value="hf">' + t("poolHf") + "</option></select>";
    h += '<div id="studyOpts"><label class="f">' + t("domains") + '</label><div class="checks">' + DOMS.map(function (d) { return '<label><input type="checkbox" name="dom" value="' + d + '" checked> ' + domTag(d) + " " + esc(L(DOMAIN[d].title)) + "</label>"; }).join("") + "</div>";
    h += '<label class="f" for="n">' + t("count") + '</label><div class="row"><input type="number" id="n" name="n" min="1" max="200" value="20" style="width:7rem"><span class="small muted" id="avail"></span></div>';
    h += '<div class="checks" style="margin-top:.7rem"><label><input type="checkbox" name="onlyNew" checked> ' + t("onlyNew") + "</label></div></div>";
    h += '<label class="f" for="diff">' + t("difficulty") + '</label><select id="diff" name="diff"><option value="all">' + t("diffAll") + '</option><option value="hard">' + t("diffHard") + "</option></select>";
    h += '<p class="small muted" id="examNote" style="margin:.9rem 0 0">' + t("examNote") + " " + t("adaptiveNote") + '</p><div class="form-actions"><button class="btn lg" type="submit">' + t("start") + ' →</button></div></form></div>';
    app.innerHTML = h;
    var f = document.getElementById("setup");
    function filtered() {
      var pool = poolOf(f.pool.value);
      if (f.diff.value === "hard") pool = pool.filter(function (q) { return q.set === "hard" || (q.d || 2) >= 3 || q.type === "multi"; });
      return pool;
    }
    function sync() {
      var ex = f.mode.value === "exam"; document.getElementById("studyOpts").style.display = ex ? "none" : ""; document.getElementById("examNote").style.display = ex ? "" : "none";
      var doms = [].slice.call(f.querySelectorAll("input[name=dom]:checked")).map(function (x) { return x.value; });
      var n = filtered().filter(function (q) { return doms.indexOf(q.dom) >= 0; }).length;
      document.getElementById("avail").textContent = t("availN", { n: n });
    }
    f.onchange = sync; sync();
    app.querySelectorAll("[data-preset]").forEach(function (b) {
      b.onclick = function () {
        var p = b.dataset.preset;
        if (p === "adaptive") return startAdaptive();
        f.pool.value = p === "hard" ? "hard" : "orig"; f.diff.value = "all";
        f.mode.value = p === "exam" ? "exam" : "study";
        f.querySelectorAll("input[name=dom]").forEach(function (x) { x.checked = p !== "sec" || x.value === "D4"; });
        f.n.value = p === "quick" ? 10 : 20; f.onlyNew.checked = true;
        sync(); f.requestSubmit ? f.requestSubmit() : f.onsubmit(new Event("submit"));
      };
    });
    f.onsubmit = function (e) {
      e.preventDefault();
      var mode = f.mode.value, poolKey = f.pool.value, pool = filtered(), list;
      if (mode === "exam") list = /^mcpa-f-mock/.test(poolKey) ? pool.slice() : pickExam(pool);
      else {
        var doms = [].slice.call(f.querySelectorAll("input[name=dom]:checked")).map(function (x) { return x.value; });
        list = pick(pool, Math.max(1, +f.n.value || 20), doms.length ? doms : DOMS, f.onlyNew.checked);
      }
      if (!list.length) { alertBox(t("noQuestions")); return; }
      startSession(mode, list, poolKey);
    };
  }

  function alertBox(msg) {
    var old = document.querySelector(".toast"); if (old) old.remove();
    var n = document.createElement("div"); n.className = "toast"; n.setAttribute("role", "status"); n.textContent = msg; document.body.appendChild(n);
    setTimeout(function () { n.remove(); }, 4000);
  }
  function modal(title, body, okLabel, onOk, danger) {
    var bg = document.createElement("div"); bg.className = "modal-bg";
    bg.innerHTML = '<div class="modal" role="dialog" aria-modal="true" aria-labelledby="mdlT"><h3 id="mdlT">' + esc(title) + "</h3><div>" + body + '</div><div class="row"><button type="button" class="btn ghost" data-m="0">' + t("cancel") + '</button><button type="button" class="btn' + (danger ? " danger" : "") + '" data-m="1">' + esc(okLabel) + "</button></div></div>";
    function close() { bg.remove(); document.removeEventListener("keydown", onKey, true); modalOpen = false; }
    function onKey(e) { if (e.key === "Escape") { e.stopPropagation(); close(); } }
    bg.onclick = function (e) { var b = e.target.closest("[data-m]"); if (e.target === bg || (b && b.dataset.m === "0")) close(); else if (b) { close(); onOk(); } };
    document.addEventListener("keydown", onKey, true);
    document.body.appendChild(bg); modalOpen = true; bg.querySelector('[data-m="1"]').focus();
  }
  var modalOpen = false;

  // ---------- sessione in corso salvata nel browser (sopravvive al ricaricamento della pagina) ----------
  var SESS_KEY = "mcpa-sim-session";
  function saveSession() {
    try {
      if (!session || session.over) { localStorage.removeItem(SESS_KEY); return; }
      var s = session;
      localStorage.setItem(SESS_KEY, JSON.stringify({ id: s.id, mode: s.mode, label: s.label, i: s.i, flags: s.flags, start: s.start, end: s.end,
        items: s.items.map(function (x) { return { q: x.q.id, o: x.order, s: x.sel, d: x.done, ms: x.ms, c: x.conf || null }; }) }));
    } catch (e) {}
  }
  function restoreSession() {
    try {
      var o = JSON.parse(localStorage.getItem(SESS_KEY) || "null"); if (!o || !o.items) return;
      if (o.items.some(function (x) { return !QBYID[x.q]; })) { localStorage.removeItem(SESS_KEY); return; }
      session = { id: o.id, mode: o.mode, label: o.label, i: o.i || 0, flags: o.flags || {}, start: o.start, end: o.end, over: false, viewAt: Date.now(),
        items: o.items.map(function (x) { return { q: QBYID[x.q], order: x.o, sel: x.s || [], done: !!x.d, ms: x.ms || 0, conf: x.c || null }; }) };
    } catch (e) {}
  }

  function startSession(mode, list, label) {
    api("/api/sessions", { mode: mode, pool: label, questions: list.map(function (q) { return q.id; }) }).then(function (r) {
      session = { id: r.id, mode: mode, label: label, items: list.map(prepare), i: 0, flags: {}, start: Date.now(), end: mode === "exam" ? Date.now() + 90 * 60000 : 0, over: false, viewAt: Date.now() };
      session.items.forEach(function (st) { st.ms = 0; });
      saveSession();
      location.hash = "#run";
      if (location.hash === "#run") render();
    }).catch(function (e) { alertBox(t("saveError") + " " + e.message); });
  }

  function tick() { if (session && !session.over) { var st = session.items[session.i]; st.ms += Date.now() - session.viewAt; session.viewAt = Date.now(); } }
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } }
  function fmtTime(ms) { ms = Math.max(0, ms); var m = Math.floor(ms / 60000), s = Math.floor(ms / 1000) % 60; return m + ":" + (s < 10 ? "0" : "") + s; }

  var keyCtx = null;
  function pageRun() {
    if (!session) { location.hash = "#quiz"; return; }
    if (session.over) return pageResult();
    var s = session, st = s.items[s.i], exam = s.mode === "exam", last = s.i === s.items.length - 1;
    var nAns = s.items.filter(function (x) { return exam ? x.sel.length : x.done; }).length, nFlag = Object.keys(s.flags).filter(function (k) { return s.flags[k]; }).length;
    var h = '<div class="runbar"><span class="count">' + t("q") + " <b>" + (s.i + 1) + "</b> " + t("of") + " " + s.items.length + '</span><div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="' + s.items.length + '" aria-valuenow="' + nAns + '"><i style="width:' + (100 * nAns / s.items.length) + '%"></i></div>' +
      (exam ? paceHtml(s) + '<span class="timer" id="timer" aria-label="' + t("time") + '">' + fmtTime(s.end - Date.now()) + "</span>" : '<span class="chip">' + esc(modeLabel(s.mode)) + "</span>") + "</div>";
    if (exam) {
      h += '<details class="qmap"' + (window.innerWidth > 720 && s.items.length <= 60 ? " open" : "") + "><summary><b>" + t("qmap") + '</b><span class="small muted" id="mapAns">' + t("answeredN", { a: nAns, n: s.items.length }) + "</span>" +
        (nFlag ? '<span class="chip warn">' + tn("flaggedN", nFlag) + "</span>" : "") + '</summary><div class="qnav">' +
        s.items.map(function (x, i) { return '<button type="button" data-go="' + i + '" aria-label="' + t("q") + " " + (i + 1) + '" class="' + (x.sel.length ? "ans " : "") + (i === s.i ? "cur " : "") + (s.flags[i] ? "flag" : "") + '">' + (i + 1) + "</button>"; }).join("") +
        '</div><div class="legend"><span><i class="ans"></i>' + t("legAns") + '</span><span><i class="flag"></i>' + t("legFlag") + "</span></div></details>";
    }
    h += '<div class="card" id="qbox" aria-live="polite"></div><div class="actions">' +
      '<div class="row"><button type="button" class="btn ghost" data-nav="-1"' + (s.i === 0 ? " disabled" : "") + ' aria-label="' + t("prev") + '">←<span class="hide-sm"> ' + t("prev") + "</span></button>" +
      (exam ? '<button type="button" class="btn ghost" data-flag="1" aria-pressed="' + !!s.flags[s.i] + '" aria-label="' + (s.flags[s.i] ? t("unflag") : t("flag")) + '">' + (s.flags[s.i] ? "★" : "☆") + '<span class="hide-sm"> ' + (s.flags[s.i] ? t("unflag") : t("flag")) + "</span></button>" : "") + "</div>" +
      '<div class="row">' + (!last ? '<button type="button" class="btn" data-nav="1">' + t("next") + " →</button>" : "") +
      ((exam || last) ? '<button type="button" class="btn' + (!last ? " ghost" : "") + '" data-finish="1"><span class="hide-sm">' + t("finish") + '</span><span class="show-sm">' + t("finishGo") + "</span></button>" : "") + "</div></div>" +
      '<p class="small muted kbd-hint" style="margin-top:1rem">' + t(setting("confidence") ? "kbdHintConf" : "kbdHint") + "</p>";
    app.innerHTML = h;
    var box = document.getElementById("qbox"), opt = { mode: exam ? "exam" : "instant", persist: exam ? null : function (st2) {
      tick(); api("/api/answers", { session_id: s.id, question_id: st2.q.id, selected: st2.sel, time_ms: st2.ms, confidence: st2.conf || null }).then(updateBadgeLater).catch(function () { alertBox(t("saveError")); });
    } };
    var rr = function () {
      box.innerHTML = qHtml(st, opt);
      if (!exam) app.querySelectorAll("[data-nav='1'],[data-finish]").forEach(function (b) { b.disabled = !st.done; });
      else {
        var g = app.querySelector('[data-go="' + s.i + '"]'); if (g) g.classList.toggle("ans", st.sel.length > 0);
        var a = s.items.filter(function (x) { return x.sel.length; }).length, m = document.getElementById("mapAns"); if (m) m.textContent = t("answeredN", { a: a, n: s.items.length });
        var bar = app.querySelector(".runbar .bar i"); if (bar) bar.style.width = (100 * a / s.items.length) + "%";
      }
      saveSession();
    };
    bindQ(box, st, opt, rr); rr();
    function go(fn) { tick(); fn(); saveSession(); pageRun(); window.scrollTo(0, 0); }
    function askFinish() {
      if (!exam) return finishSession();
      var un = s.items.filter(function (x) { return !x.sel.length; }).length, fl = Object.keys(s.flags).filter(function (k) { return s.flags[k]; }).length;
      modal(t("finishTitle"), "<p>" + (un ? tn("finishUnans", un) : t("finishOk")) + (fl ? "<br>" + tn("finishFlag", fl) : "") + "</p>", t("finishGo"), finishSession);
    }
    app.querySelectorAll("[data-nav],[data-go],[data-flag],[data-finish]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (b.dataset.finish) { tick(); return askFinish(); }
        go(function () {
          if (b.dataset.nav) s.i = Math.min(s.items.length - 1, Math.max(0, s.i + +b.dataset.nav));
          else if (b.dataset.go) s.i = +b.dataset.go;
          else if (b.dataset.flag) s.flags[s.i] = !s.flags[s.i];
        });
      });
    });
    keyCtx = function (e) {
      var k = e.key, multi = st.q.c.length > 1;
      var pos = /^[1-7]$/.test(k) ? +k - 1 : /^[a-gA-G]$/.test(k) && !(k === "f" || k === "F") ? k.toUpperCase().charCodeAt(0) - 65 : -1;
      if (pos >= 0 && pos < st.order.length) { var b = box.querySelector('[data-oi="' + st.order[pos] + '"]'); if (b && !b.disabled) b.click(); return true; }
      if (k === "Enter") {
        if (!exam && !st.done) { var c = box.querySelector(setting("confidence") ? "[data-conf=sure]" : "[data-act=confirm]"); if (c && !c.disabled) c.click(); return true; }
        if (exam || st.done) { if (!last) go(function () { s.i++; }); else askFinish(); return true; }
      }
      if (k === "ArrowRight" && !last && (exam || st.done)) { go(function () { s.i++; }); return true; }
      if (k === "ArrowLeft" && s.i > 0) { go(function () { s.i--; }); return true; }
      if ((k === "f" || k === "F") && exam) { go(function () { s.flags[s.i] = !s.flags[s.i]; }); return true; }
      return false;
    };
    stopTimer();
    if (exam) timerId = setInterval(function () {
      var el = document.getElementById("timer"), left = s.end - Date.now();
      if (left <= 0) { s.timeUp = true; finishSession(); return; }
      if (el) { el.textContent = fmtTime(left); el.classList.toggle("low", left < 5 * 60000); }
      var pc = document.getElementById("pace"); if (pc && Math.floor(left / 1000) % 15 === 0) pc.outerHTML = paceHtml(s);
    }, 1000);
  }

  function finishSession() {
    var s = session; stopTimer(); if (!s || s.over || s.finishing) return;
    s.finishing = true; tick();
    var answers = [];
    if (s.mode === "exam") s.items.forEach(function (st) { st.done = true; record(st.q, isCorrect(st), st.conf); if (st.sel.length) answers.push({ question_id: st.q.id, selected: st.sel, time_ms: st.ms, confidence: st.conf || null }); });
    api("/api/sessions/" + s.id + "/finish", { answers: answers, time_up: !!s.timeUp }).then(function (r) {
      s.over = true; saveSession();
      s.score = { ok: r.n_correct, n: r.n_questions, pct: Math.round(r.score_pct), byDom: r.byDom, dur: r.duration_s };
      return refreshStats();
    }).then(function () { if (location.hash !== "#run") location.hash = "#run"; else pageResult(); updateBadge(); window.scrollTo(0, 0); }).catch(function (e) { s.finishing = false; alertBox(t("saveError") + " " + e.message); });
  }

  function pageResult() {
    keyCtx = null;
    var s = session, sc = s.score, pass = sc.pct >= 75;
    var h = "<h1>" + t("result") + "</h1>" + (s.timeUp ? '<div class="note">' + t("timeUp") + "</div>" : "");
    h += '<div class="card"><div class="spread"><div><div class="big ' + (pass ? "pass" : "fail") + '">' + sc.pct + '%</div><div class="muted" style="margin-top:.35rem">' + sc.ok + " / " + sc.n + " · " + fmtDur(sc.dur) + " · " + t("passLine") + "</div>" + deltaHtml(s.mode) + "</div>" +
      '<span class="verdict ' + (pass ? "pass" : "fail") + '">' + (pass ? "✓ " + t("passed") : "✗ " + t("failed")) + "</span></div>";
    h += "<h3 style=\"margin-top:1.2rem\">" + t("byDomain") + "</h3><table>";
    DOMS.forEach(function (d) {
      var x = sc.byDom[d]; if (!x) return; var p = Math.round(100 * x.ok / x.n);
      h += "<tr><td>" + domTag(d) + " " + esc(L(DOMAIN[d].title)) + '</td><td class="barcol" style="width:35%;vertical-align:middle"><div class="bar ' + (p >= 75 ? "ok" : "bad") + '"><i style="width:' + p + '%"></i></div></td><td style="white-space:nowrap">' + x.ok + "/" + x.n + " (" + p + "%)</td></tr>";
    });
    h += "</table></div>";
    var wrong = s.items.filter(function (st) { return !isCorrect(st); });
    h += '<div class="row" style="margin:0 0 1rem"><a class="btn" href="#quiz">' + t("again") + '</a><a class="btn ghost" href="#review">' + t("navReview") + '</a><a class="btn ghost" href="#progress">' + t("navProgress") + "</a></div>";
    h += "<h2>" + t("wrongList") + " (" + wrong.length + ")</h2>";
    if (!wrong.length) h += "<p>" + t("noneWrong") + "</p>";
    else {
      h += '<p class="small muted">' + t("toReview") + "</p>";
      wrong.forEach(function (st, i) { h += '<div class="card" data-w="' + i + '"></div>'; });
    }
    app.innerHTML = h;
    wrong.forEach(function (st, i) {
      var el = app.querySelector('[data-w="' + i + '"]');
      el.innerHTML = (st.sel.length ? "" : '<div class="note">' + t("unanswered") + "</div>") + qHtml(st, { mode: "instant" });
    });
  }

  function pageReview() {
    stopTimer();
    var srs = setting("srs"), all = Object.keys(STATS.review).filter(function (id) { return QBYID[id]; }), due = dueIds();
    var later = all.filter(function (id) { return due.indexOf(id) < 0; }).sort(function (a, b) { return (STATS.review[a].dueAt || "").localeCompare(STATS.review[b].dueAt || ""); });
    var h = "<h1>" + t("reviewTitle") + '</h1><p class="muted">' + t(srs ? "reviewIntroSrs" : "reviewIntro") + "</p>";
    if (!all.length) { app.innerHTML = h + "<p>" + t("reviewEmpty") + "</p>"; return; }
    if (due.length) h += '<p><button type="button" class="btn" id="go">' + t("reviewStart", { n: due.length }) + "</button></p>";
    else h += '<p class="note">' + t("reviewNone", { d: fmtDate(STATS.review[later[0]].dueAt).slice(0, 10) }) + "</p>";
    function item(q, showDate) {
      var r = STATS.review[q.id], tp = TOPIC[q.t];
      return "<li>" + fmt(L(q.q)).slice(0, 400) + ' <span class="muted">· ' + t(r.reason === "guess" ? "reasonGuess" : "reasonWrong") + " · " + (srs ? t("boxN", { n: r.box }) : t("streakNote", { n: r.streak })) +
        (showDate ? " · " + t("dueOn", { d: fmtDate(r.dueAt).slice(0, 10) }) : "") + "</span>" + (tp ? ' · <a href="#t/' + tp.id + '">' + esc(L(tp.title)) + "</a>" : "") + "</li>";
    }
    if (due.length) {
      h += "<h2>" + t("reviewDue") + "</h2>";
      var byDom = {}; due.forEach(function (id) { var q = QBYID[id]; (byDom[q.dom] = byDom[q.dom] || []).push(q); });
      DOMS.forEach(function (d) {
        if (!byDom[d]) return;
        h += '<div class="card"><h3>' + domTag(d) + " " + esc(L(DOMAIN[d].title)) + ' <span class="chip">' + byDom[d].length + '</span></h3><ul class="small" style="padding-left:1.1rem">' +
          byDom[d].map(function (q) { return item(q, false); }).join("") + "</ul></div>";
      });
    }
    if (later.length) h += "<h2>" + t("reviewLater") + ' <span class="chip">' + later.length + '</span></h2><div class="card"><ul class="small" style="padding-left:1.1rem">' + later.map(function (id) { return item(QBYID[id], true); }).join("") + "</ul></div>";
    app.innerHTML = h;
    var go = document.getElementById("go"); if (go) go.onclick = function () { startSession("study", shuffle(due.map(function (id) { return QBYID[id]; })), "review"); };
  }

  // ---------- impostazioni ed esportazione ----------
  function pageSettings() {
    var opts = [["srs", "setSrs", "setSrsD"], ["confidence", "setConf", "setConfD"], ["pacing", "setPace", "setPaceD"]];
    var h = "<h1>" + t("setTitle") + '</h1><p class="muted">' + t("setIntro") + '</p><div class="card settings">' +
      opts.map(function (o) {
        return '<label class="switch-row"><span><b>' + t(o[1]) + '</b><span class="small muted">' + t(o[2]) + '</span></span><input type="checkbox" class="switch" data-set="' + o[0] + '"' + (setting(o[0]) ? " checked" : "") + "></label>";
      }).join("") + "</div>";
    h += "<h2>" + t("dataTitle") + '</h2><div class="card"><p class="muted" style="margin-top:0">' + t("dataIntro") + '</p><div class="row">' +
      '<button type="button" class="btn" id="expBtn">' + t("exportBtn") + '</button><label class="btn ghost" for="impFile">' + t("importBtn") + '</label><input type="file" id="impFile" accept=".json,application/json" hidden></div></div>';
    app.innerHTML = h;
    app.querySelectorAll("[data-set]").forEach(function (el) {
      el.onchange = function () {
        var body = {}; body[el.dataset.set] = el.checked;
        api("/api/settings", body).then(function (s) { STATS.settings = s; return refreshStats(); }).then(function () { alertBox(t("saved")); })
          .catch(function (e) { el.checked = !el.checked; alertBox(t("saveError") + " " + e.message); });
      };
    });
    document.getElementById("expBtn").onclick = function () {
      api("/api/export").then(function (data) {
        var f = "mcpa-progressi-" + new Date().toISOString().slice(0, 10) + ".json";
        var url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: "application/json" }));
        var a = document.createElement("a"); a.href = url; a.download = f; document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
        alertBox(t("exportOk", { f: f }));
      }).catch(function (e) { alertBox(t("saveError") + " " + e.message); });
    };
    var inp = document.getElementById("impFile");
    inp.onchange = function () {
      var file = inp.files[0]; inp.value = ""; if (!file) return;
      file.text().then(function (txt) {
        var data; try { data = JSON.parse(txt); } catch (e) { data = null; }
        if (!data || data.format !== "mcpa-sim-progress" || !data.tables) { alertBox(t("importBad")); return; }
        var n = (data.tables.answers || []).length;
        modal(t("importTitle"), "<p>" + esc(t("importQ", { d: fmtDate(data.exported_at || ""), n: n })) + "</p>", t("importGo"), function () {
          api("/api/import", { data: data }).then(function (r) {
            var im = r.imported || {}; alertBox(t("importOk", { n: im.answers || 0 }) + (im.skipped ? " " + t("importSkipped", { n: im.skipped }) : ""));
            return refreshStats();
          }).then(function () { render(); }).catch(function (e) { alertBox(t("importBad") + " (" + e.message + ")"); });
        }, true);
      });
    };
  }

  // ---------- esame adattivo ----------
  function weakness(q) {
    var s = STATS.qstats[q.id], r = STATS.review[q.id], ts = STATS.topicStats[q.t], w = Math.random();
    if (r) w += r.due ? 4 : 1.5;
    if (!s) w += 1.5; else if (!s.last) w += 2.5; else if (s.n >= 2 && s.ok === s.n) w -= 1;
    w += ts && ts.n ? 3 * (1 - ts.ok / ts.n) : 1;
    return w;
  }
  function pickAdaptive(pool) {
    var out = [];
    DOMS.forEach(function (d) {
      out = out.concat(pool.filter(function (q) { return q.dom === d; }).map(function (q) { return { q: q, w: weakness(q) }; })
        .sort(function (a, b) { return b.w - a.w; }).slice(0, EXAM_DIST[d]).map(function (x) { return x.q; }));
    });
    return shuffle(out);
  }
  function startAdaptive() { startSession("exam", pickAdaptive(poolOf("all")), "adaptive"); }

  // ---------- flashcard ----------
  // il termine nascosto è il primo token "da ricordare" del punto in inglese, presente anche nel punto in italiano
  var CARD_RX = [
    /(?<![\w-])-32\d{3}\b/,
    /\b(?:MCP|Mcp)-[A-Z][A-Za-z-]+\b|\bWWW-Authenticate\b|\bLast-Event-ID\b/,
    /(?<![\w.\/-])[a-z]+(?:\/[a-zA-Z_]+)+\b/,
    /\b_meta\b|\b[a-z]+[A-Z][A-Za-z]+\b/,
    /\bRFC ?\d{3,4}\b|\bSEP-\d+\b/,
    /\b[45]\d\d\b/,
    /MUST NOT|SHOULD NOT|\bMUST\b|\bSHOULD\b|\bMAY\b/
  ];
  function cardToken(en, it) {
    for (var i = 0; i < CARD_RX.length; i++) {
      var re = new RegExp(CARD_RX[i].source, "g"), m;
      while ((m = re.exec(en))) { var tk = m[0]; if (/^(and\/or|e\/o)$/i.test(tk)) continue; if (!it || it.indexOf(tk) >= 0) return tk; }
    }
    return null;
  }
  var CARDS = null;
  function allCards() {
    if (CARDS) return CARDS;
    CARDS = [];
    DATA.course.forEach(function (d) { d.topics.forEach(function (tp) {
      var en = tp.points.en || [], it = tp.points.it || [];
      en.forEach(function (p, i) { var tk = cardToken(p, it[i]); if (tk) CARDS.push({ id: tp.id + ":" + i, tp: tp, i: i, tok: tk }); });
    }); });
    return CARDS;
  }
  // debolezza di un argomento: 0 = forte, valori alti = da studiare; null = nessun dato
  function topicWeak() {
    var w = {};
    function add(id, v) { w[id] = (w[id] || 0) + v; }
    Object.keys(STATS.topicStats).forEach(function (id) { var s = STATS.topicStats[id]; if (s.n && s.ok / s.n < 0.75) add(id, 1 + 2 * (1 - s.ok / s.n)); });
    Object.keys(STATS.review).forEach(function (id) { var q = QBYID[id]; if (q) add(q.t, 1); });
    Object.keys(STATS.cards || {}).forEach(function (cid) { var c = STATS.cards[cid]; if (c.seen > c.known) add(cid.split(":")[0], 0.5); });
    return w;
  }
  var FL = { scope: "weak", dom: "", deck: null };
  function buildDeck() {
    var cards = allCards().filter(function (c) { return !FL.dom || c.tp.dom === FL.dom; }), w = topicWeak(), noData = !Object.keys(w).length;
    var wt = {}; DATA.course.forEach(function (d) { wt[d.id] = d.weight; });
    var due = [], fresh = [];
    cards.forEach(function (c) {
      var s = (STATS.cards || {})[c.id];
      if (s) { if (s.due) due.push(c); return; }
      if (FL.scope === "all" || noData || w[c.tp.id]) fresh.push(c);
    });
    due.sort(function (a, b) { return STATS.cards[a.id].box - STATS.cards[b.id].box; });
    fresh = shuffle(fresh).sort(function (a, b) { return noData ? wt[b.tp.dom] - wt[a.tp.dom] : (w[b.tp.id] || 0) - (w[a.tp.id] || 0); });
    return { due: due, fresh: fresh, list: due.concat(fresh).slice(0, 20) };
  }
  function cardText(c, reveal) {
    var p = (c.tp.points[S.lang] || [])[c.i] || c.tp.points.en[c.i], h = fmt(p), tk = esc(c.tok), i = h.indexOf(tk);
    if (i < 0) return h;
    return h.slice(0, i) + (reveal ? "<mark>" + tk + "</mark>" : '<span class="blank" aria-label="?">' + " ".repeat(Math.min(12, Math.max(4, c.tok.length))) + "</span>") + h.slice(i + tk.length);
  }
  var flashKey = null;
  function pageFlash() {
    var dk = buildDeck(), nAll = allCards().length;
    var h = "<h1>" + t("flashTitle") + '</h1><p class="muted">' + t("flashIntro") + "</p>";
    h += '<div class="card"><div class="seg-row"><div class="seg" role="group">' +
      ["weak", "all"].map(function (k) { return '<button type="button" data-scope="' + k + '" class="' + (FL.scope === k ? "on" : "") + '" aria-pressed="' + (FL.scope === k) + '">' + t(k === "weak" ? "flashScopeWeak" : "flashScopeAll") + "</button>"; }).join("") +
      '</div><select id="flDom" aria-label="' + esc(t("domains")) + '"><option value="">' + t("flashAllDoms") + "</option>" +
      DOMS.map(function (d) { return '<option value="' + d + '"' + (FL.dom === d ? " selected" : "") + ">" + d + " · " + esc(L(DOMAIN[d].title)) + "</option>"; }).join("") + "</select></div>" +
      '<p class="small muted">' + tn("flashTotal", nAll) + " · <b>" + dk.due.length + "</b> " + t("flashDue") + " · <b>" + dk.fresh.length + "</b> " + t("flashNew") + "</p>" +
      (FL.scope === "weak" ? '<p class="small muted" style="margin-bottom:0">' + t("flashWeakNote") + "</p>" : "") +
      '<div class="form-actions"><button type="button" class="btn lg" id="flGo"' + (dk.list.length ? "" : " disabled") + ">" + t("flashStart", { n: dk.list.length }) + " →</button></div>" +
      (dk.list.length ? "" : '<p class="note">' + t("flashEmpty") + "</p>") + "</div>";
    app.innerHTML = h;
    app.querySelectorAll("[data-scope]").forEach(function (b) { b.onclick = function () { FL.scope = b.dataset.scope; pageFlash(); }; });
    document.getElementById("flDom").onchange = function () { FL.dom = this.value; pageFlash(); };
    document.getElementById("flGo").onclick = function () { FL.deck = { list: dk.list, i: 0, shown: false, known: 0, miss: [] }; flashRun(); };
  }
  function flashRun() {
    var d = FL.deck, c = d.list[d.i];
    if (!c) return flashDone();
    var h = '<div class="runbar"><span class="count">' + t("flashCardN", { i: d.i + 1, n: d.list.length }) + '</span><div class="bar"><i style="width:' + (100 * d.i / d.list.length) + '%"></i></div><button type="button" class="btn ghost" id="flQuit">✕</button></div>';
    h += '<div class="card flashcard' + (d.shown ? " shown" : "") + '"><div class="spread small muted"><span>' + domTag(c.tp.dom) + " " + esc(L(c.tp.title)) + "</span><span>" + t("flashFill") + "</span></div>" +
      '<p class="fc-text">' + cardText(c, d.shown) + "</p>" +
      (d.shown ? '<div class="small"><a href="#t/' + c.tp.id + '" target="_blank" rel="noopener">' + t("openTheory") + " →</a></div>" : "") + "</div>";
    h += '<div class="actions">' + (d.shown ?
      '<div class="row"><button type="button" class="btn ghost" data-known="0">1 · ' + t("flashNot") + '</button></div><div class="row"><button type="button" class="btn" data-known="1">2 · ' + t("flashKnew") + "</button></div>" :
      '<div></div><div class="row"><button type="button" class="btn" id="flShow">' + t("flashShow") + "</button></div>") + "</div>";
    h += '<p class="small muted kbd-hint" style="margin-top:1rem">' + t("flashKbd") + "</p>";
    app.innerHTML = h;
    document.getElementById("flQuit").onclick = function () { FL.deck = null; flashKey = null; pageFlash(); };
    var show = document.getElementById("flShow"); if (show) { show.onclick = function () { d.shown = true; flashRun(); }; show.focus(); }
    app.querySelectorAll("[data-known]").forEach(function (b) {
      b.onclick = function () {
        var k = b.dataset.known === "1"; if (k) d.known++; else d.miss.push(c);
        api("/api/flashcards", { card_id: c.id, known: k }).then(function (r) { STATS.cards = STATS.cards || {}; var o = STATS.cards[c.id] || { seen: 0, known: 0 }; STATS.cards[c.id] = { box: r.box, due: r.box === 0, seen: o.seen + 1, known: o.known + (k ? 1 : 0) }; }).catch(function () { alertBox(t("saveError")); });
        d.i++; d.shown = false; flashRun(); window.scrollTo(0, 0);
      };
    });
    flashKey = function (e) {
      if (!d.shown && (e.key === " " || e.key === "Enter")) { d.shown = true; flashRun(); return true; }
      if (d.shown && (e.key === "1" || e.key === "2")) { var b = app.querySelector('[data-known="' + (e.key === "2" ? 1 : 0) + '"]'); if (b) b.click(); return true; }
      return false;
    };
  }
  function flashDone() {
    var d = FL.deck; flashKey = null; FL.deck = null;
    var h = "<h1>" + t("flashDone") + '</h1><div class="card"><div class="big ' + (d.known / d.list.length >= 0.75 ? "pass" : "fail") + '">' + d.known + " / " + d.list.length + '</div><p class="muted">' + t("flashResult", { k: d.known, n: d.list.length }) + "</p>" +
      '<div class="row"><button type="button" class="btn" id="flAgain">' + t("flashAgain") + "</button></div></div>";
    if (d.miss.length) h += "<h2>" + t("flashMiss") + '</h2><div class="card"><ul class="fc-miss">' + d.miss.map(function (c) { return "<li>" + domTag(c.tp.dom) + " " + cardText(c, true) + ' <a href="#t/' + c.tp.id + '">' + esc(L(c.tp.title)) + " →</a></li>"; }).join("") + "</ul></div>";
    app.innerHTML = h;
    document.getElementById("flAgain").onclick = function () { pageFlash(); };
  }
  document.addEventListener("keydown", function (e) {
    if (!flashKey || modalOpen || e.ctrlKey || e.metaKey || e.altKey || location.hash.indexOf("#flash") !== 0) return;
    var tg = e.target; if (tg && (tg.tagName === "INPUT" || tg.tagName === "SELECT" || tg.tagName === "TEXTAREA")) return;
    if (e.key === "Enter" && tg && tg.tagName === "BUTTON" && tg.id !== "flShow") return;
    if (flashKey(e)) e.preventDefault();
  });

  // ---------- analisi su confidenza e tempi (pagina Progressi) ----------
  function confSection() {
    if (!setting("confidence")) return "";
    var c = STATS.confidence || {}, tot = CONF.reduce(function (s, k) { return s + ((c[k] || {}).n || 0); }, 0);
    var h = "<h2>" + t("confTitle") + '</h2><div class="card"><p class="small muted" style="margin-top:0">' + t("confIntro") + "</p>";
    if (!tot) return h + '<p class="muted">' + t("confNone") + "</p></div>";
    h += "<table>" + CONF.map(function (k) {
      var x = c[k] || { n: 0, ok: 0 }, p = pct(x);
      return '<tr><td style="white-space:nowrap"><span class="chip conf-chip conf-' + k + '">' + CONF_ICON[k] + " " + confLabel(k) + '</span></td><td class="barcol" style="width:45%;vertical-align:middle"><div class="bar ' + (p === null ? "" : p >= 75 ? "ok" : "bad") + '"><i style="width:' + (p || 0) + '%"></i></div></td><td style="white-space:nowrap">' + (p === null ? "–" : p + "%") + ' <span class="small muted">' + t("answersN", { n: x.n }) + "</span></td></tr>";
    }).join("") + "</table>";
    var lucky = (c.guess || {}).ok || 0, sw = ((c.sure || {}).n || 0) - ((c.sure || {}).ok || 0);
    if (lucky) h += '<p class="small" style="margin-bottom:0">' + t("luckyN", { n: lucky }) + "</p>";
    if (sw) h += '<p class="small fail" style="margin-bottom:0">' + t("sureWrongN", { n: sw }) + "</p>";
    return h + "</div>";
  }
  function timeSection() {
    if (!setting("pacing")) return "";
    var tm = STATS.timing || { byDom: {}, slowTopics: [] }, any = Object.keys(tm.byDom).length;
    var h = "<h2>" + t("timeTitle") + '</h2><div class="card"><p class="small muted" style="margin-top:0">' + t("timeIntro") + "</p>";
    if (!any) return h + '<p class="muted">' + t("timeNone") + "</p></div>";
    h += "<table><tr><th>" + t("domain") + "</th><th class=\"barcol\"></th><th>" + t("avgTime") + "</th></tr>" + DOMS.map(function (d) {
      var x = tm.byDom[d]; if (!x) return "";
      var s = Math.round(x.avg / 1000);
      return "<tr><td>" + domTag(d) + " " + esc(L(DOMAIN[d].title)) + '</td><td class="barcol" style="width:35%;vertical-align:middle"><div class="bar tbar ' + (s > 90 ? "bad" : "ok") + '"><i style="width:' + Math.min(100, s / 1.8) + '%"></i><b></b></div></td><td style="white-space:nowrap">' + s + ' s <span class="small muted">(' + x.n + ")</span></td></tr>";
    }).join("") + "</table>";
    if (tm.slowTopics.length) h += "<h3 style=\"margin-top:1rem\">" + t("slowTitle") + '</h3><ul class="small">' + tm.slowTopics.map(function (w) {
      return "<li>" + domTag(w.domain_id) + ' <a href="#t/' + w.id + '">' + esc(S.lang === "it" ? w.title_it : w.title_en) + "</a> · " + Math.round(w.avg / 1000) + " s (" + w.n + ")</li>";
    }).join("") + "</ul>";
    return h + "</div>";
  }
  // ritmo d'esame: differenza tra il tempo "guadagnato" (domande risposte × tempo medio disponibile) e quello trascorso
  function paceHtml(s) {
    if (!setting("pacing") || s.mode !== "exam" || !s.end) return "";
    var per = (s.end - s.start) / s.items.length, el = Date.now() - s.start;
    if (el < 60000) return '<span class="chip pace" id="pace" title="' + esc(t("paceTitle")) + '">⏱ ' + t("paceOk") + "</span>";
    var a = s.items.filter(function (x) { return x.sel.length; }).length, delta = a * per - el, m = Math.round(Math.abs(delta) / 60000) + " min";
    var cls = Math.abs(delta) < 60000 ? "" : delta > 0 ? " ok" : delta < -180000 ? " warn" : "";
    var txt = Math.abs(delta) < 60000 ? t("paceOk") : delta > 0 ? t("paceAhead", { m: m }) : t("paceBehind", { m: m });
    return '<span class="chip pace' + cls + '" id="pace" title="' + esc(t("paceTitle")) + '">⏱ ' + txt + "</span>";
  }

  function pageAbout() {
    var n = { o: 0, r: 0, h: 0 }; DATA.questions.forEach(function (q) { if (q.src === "original") n.o++; else if (q.src === "rohitg00") n.r++; else n.h++; });
    var it = S.lang === "it";
    app.innerHTML = "<h1>" + t("aboutTitle") + "</h1>" +
      '<div class="card"><h3>' + (it ? "Corso e domande originali" : "Course and original questions") + "</h3><p>" +
      (it ? "Il corso (74 argomenti) e le " + n.o + " domande originali sono stati scritti per questo progetto a partire dalla specifica MCP 2026-07-28 e dalla documentazione ufficiale (modelcontextprotocol.io, blog AAIF). Ogni argomento indica la sua fonte. Non contengono domande d'esame reali." :
        "The course (74 topics) and the " + n.o + " original questions were written for this project from the MCP 2026-07-28 specification and official documentation (modelcontextprotocol.io, AAIF blog). Each topic names its source. They contain no real exam questions.") + "</p></div>" +
      '<div class="card"><h3>rohitg00 · MCPA practice (' + n.r + ")</h3><p>" +
      (it ? "Domande in inglese con licenza MIT, testo invariato tranne 3 correzioni segnalate nella domanda stessa (imprecisioni rispetto alla spec). Copyright dei rispettivi autori; licenza e attribuzione in practice-questions/open-licensed/rohitg00-mcpa/. Il collegamento alla teoria è automatico (per parole chiave), rivisto a mano dove era sbagliato. Le note di revisione segnalano le imprecisioni trovate rispetto alla spec." :
        "English questions under the MIT license, text unchanged except for 3 corrections flagged on the question itself (inaccuracies against the spec). Copyright their respective authors; license and attribution in practice-questions/open-licensed/rohitg00-mcpa/. The theory link is automatic (keyword-based), hand-corrected where it was wrong. Review notes flag inaccuracies found against the spec.") + "</p></div>" +
      '<div class="card"><h3>Hugging Face MCP Course (' + n.h + ")</h3><p>" +
      (it ? "Quiz del corso MCP di Hugging Face, licenza Apache 2.0 (practice-questions/open-licensed/huggingface-mcp-course/). Precedono la 2026-07-28: usali solo come ripasso generale, sono esclusi dalla simulazione d'esame." :
        "Quizzes from the Hugging Face MCP course, Apache 2.0 license (practice-questions/open-licensed/huggingface-mcp-course/). They predate 2026-07-28: use them only for general review; they are excluded from the exam simulation.") + "</p></div>" +
      '<div class="card"><h3>' + (it ? "Esame" : "Exam") + "</h3><p>" +
      (it ? "90 minuti, a libro chiuso. Pesi ufficiali dei domini 16/14/26/24/20. Numero di domande (60) e soglia (75%) sono valori indicativi presi dalle regole generali LF, non confermati per MCPA." :
        "90 minutes, closed book. Official domain weights 16/14/26/24/20. Question count (60) and pass mark (75%) are indicative values from general LF rules, not confirmed for MCPA.") + "</p></div>";
  }

  // ---------- tema e badge ----------
  var THEME_KEY = "mcpa-sim-theme";
  var ICON = {
    auto: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor"/></svg>',
    light: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    dark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>'
  };
  function getTheme() { try { var v = localStorage.getItem(THEME_KEY); return v === "light" || v === "dark" ? v : "auto"; } catch (e) { return "auto"; } }
  function applyTheme(v) {
    if (v === "auto") delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = v;
    try { if (v === "auto") localStorage.removeItem(THEME_KEY); else localStorage.setItem(THEME_KEY, v); } catch (e) {}
    var b = document.getElementById("themeBtn"); if (!b) return;
    var lbl = t("theme" + v.charAt(0).toUpperCase() + v.slice(1)); b.innerHTML = ICON[v]; b.title = lbl; b.setAttribute("aria-label", lbl);
  }
  var themeBtn = document.getElementById("themeBtn");
  if (themeBtn) themeBtn.onclick = function () { var v = getTheme(); applyTheme(v === "auto" ? "light" : v === "light" ? "dark" : "auto"); };
  var badgeT = null; function updateBadgeLater() { clearTimeout(badgeT); badgeT = setTimeout(refreshStats, 300); }
  function updateBadge() { var b = document.getElementById("rvBadge"), d = document.getElementById("rvDot"); if (!b) return; var n = dueIds().length; b.style.display = n ? "" : "none"; b.textContent = n; if (d) d.style.display = n ? "" : "none"; }
  document.addEventListener("keydown", function (e) {
    if (!keyCtx || modalOpen || e.ctrlKey || e.metaKey || e.altKey || location.hash !== "#run") return;
    var tg = e.target; if (tg && (tg.tagName === "INPUT" || tg.tagName === "SELECT" || tg.tagName === "TEXTAREA")) return;
    if (e.key === "Enter" && tg && tg.tagName === "BUTTON" && !tg.classList.contains("opt")) return;
    if (keyCtx(e)) e.preventDefault();
  });
  window.addEventListener("beforeunload", function (e) { if (session && !session.over && session.mode === "exam") { saveSession(); } });

  // ---------- menu laterale e percorso ----------
  var SVG = function (d) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + "</svg>"; };
  var NAVICON = {
    home: SVG('<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>'),
    course: SVG('<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 19.5V4.5"/><path d="M8 7h8M8 11h6"/>'),
    quiz: SVG('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8l1.5 1.5L12 7M8 14l1.5 1.5L12 13M14 8.5h2M14 14.5h2"/>'),
    review: SVG('<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/><path d="M12 8v4l3 2"/>'),
    progress: SVG('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
    about: SVG('<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/>'),
    flash: SVG('<rect x="3" y="6" width="14" height="14" rx="2"/><path d="M7 3h12a2 2 0 0 1 2 2v12"/><path d="M7 13h6"/>'),
    settings: SVG('<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>'),
    resume: SVG('<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l6-3.5z" fill="currentColor"/>')
  };
  var CARET = SVG('<path d="M9 6l6 6-6 6"/>');
  var courseOpen = null;
  function navItem(key, href, label, extra) { return '<a class="nav-item" href="' + href + '" data-nav="' + key + '" title="' + esc(label) + '">' + NAVICON[key] + '<span class="lbl">' + esc(label) + "</span>" + (extra || "") + "</a>"; }
  function buildSide(sec, dom) {
    var nav = document.getElementById("sideNav"); if (!nav) return;
    var h = "";
    if (session && !session.over && sec !== "run") {
      var a = session.items.filter(function (x) { return x.sel.length; }).length;
      h += '<a class="nav-item nav-resume" href="#run" title="' + esc(t("resumeBtn")) + '">' + NAVICON.resume + '<span class="lbl">' + t("resumeBtn") + " · " + a + "/" + session.items.length + "</span></a>";
    }
    var open = courseOpen === null ? (sec === "course" || sec === "t") : courseOpen;
    h += '<div class="side-sec">' + t("secStudy") + "</div>" + navItem("home", "#home", t("navHome"));
    h += '<div class="nav-group' + (open ? " open" : "") + '" id="grpCourse"><div class="nav-row">' + navItem("course", "#course", t("navCourse")) +
      '<button type="button" class="exp" id="expCourse" aria-expanded="' + open + '" aria-label="' + esc(t("navDomains")) + '">' + CARET.replace("<svg", '<svg class="caret"') + '</button></div><div class="nav-sub">' +
      DATA.course.map(function (d) { return '<a href="#course/' + d.id + '" data-dom="' + d.id + '" title="' + esc(L(d.title)) + '"' + (d.id === dom ? ' class="on" aria-current="page"' : "") + '><span class="dot" style="background:var(--' + d.id.toLowerCase() + ')"></span><span class="t">' + d.id + " · " + esc(L(d.title)) + "</span></a>"; }).join("") + "</div></div>";
    h += '<div class="side-sec">' + t("secPractice") + "</div>" + navItem("quiz", "#quiz", t("navQuiz")) +
      navItem("review", "#review", t("navReview"), '<span class="badge" id="rvBadge"></span><span class="dotbadge" id="rvDot"></span>') + navItem("flash", "#flash", t("navFlash")) + navItem("progress", "#progress", t("navProgress"));
    h += '<div class="side-sec">' + t("secInfo") + "</div>" + navItem("settings", "#settings", t("navSettings")) + navItem("about", "#about", t("navAbout"));
    nav.innerHTML = h;
    nav.querySelectorAll(".nav-item[data-nav]").forEach(function (el) {
      var n = el.dataset.nav, on = n === sec || (n === "course" && sec === "t" && !dom) || (n === "course" && sec === "course" && !dom) || (n === "quiz" && sec === "run") || (n === "progress" && sec === "session");
      if (n === "course" && (sec === "course" || sec === "t")) on = true;
      el.classList.toggle("on", on); if (on) el.setAttribute("aria-current", "page");
    });
    document.getElementById("expCourse").onclick = function () {
      var g = document.getElementById("grpCourse"); courseOpen = !g.classList.contains("open"); g.classList.toggle("open", courseOpen); this.setAttribute("aria-expanded", courseOpen);
    };
    var mini = document.getElementById("sideMini"); if (mini) { var lbl = t("menuMini"); mini.title = lbl; mini.setAttribute("aria-label", lbl); }
    var bg = document.getElementById("burger"); if (bg) bg.setAttribute("aria-label", t("menuOpen"));
  }
  function crumbs(parts) {
    var el = document.getElementById("crumbs"); if (!el) return;
    el.innerHTML = parts.map(function (p, i) {
      var last = i === parts.length - 1;
      return (i ? '<span class="sep" aria-hidden="true">›</span>' : "") + (last || !p[1] ? '<span class="cur"' + (last ? ' aria-current="page"' : "") + ">" + p[0] + "</span>" : '<a href="' + p[1] + '">' + p[0] + "</a>");
    }).join("");
  }
  function crumbsFor(sec, parts) {
    var H = [t("navHome"), "#home"], C = [t("navCourse"), "#course"], Q = [t("navQuiz"), "#quiz"], P = [t("navProgress"), "#progress"];
    if (sec === "course" && DOMAIN[parts[1]]) return [H, C, [esc(parts[1] + " · " + L(DOMAIN[parts[1]].title))]];
    if (sec === "course") return [H, [t("navCourse")]];
    if (sec === "t" && TOPIC[parts[1]]) { var tp = TOPIC[parts[1]]; return [H, C, [esc(tp.dom + " · " + L(DOMAIN[tp.dom].title)), "#course/" + tp.dom], [esc(L(tp.title))]]; }
    if (sec === "quiz") return [H, [t("navQuiz")]];
    if (sec === "run") return [H, Q, [session ? esc(modeLabel(session.mode)) : t("navQuiz")]];
    if (sec === "review") return [H, [t("navReview")]];
    if (sec === "progress") return [H, [t("navProgress")]];
    if (sec === "session") return [H, P, [t("sessionN", { n: parts[1] })]];
    if (sec === "about") return [H, [t("navAbout")]];
    if (sec === "settings") return [H, [t("navSettings")]];
    if (sec === "flash") return [H, [t("navFlash")]];
    return [[t("navHome")]];
  }
  function setSide(open) {
    document.documentElement.classList.toggle("side-open", open);
    var s = document.getElementById("scrim"); if (s) s.hidden = !open;
    var b = document.getElementById("burger"); if (b) b.setAttribute("aria-expanded", open);
  }
  (function wireSide() {
    var b = document.getElementById("burger"), s = document.getElementById("scrim"), m = document.getElementById("sideMini");
    if (b) b.onclick = function () { setSide(!document.documentElement.classList.contains("side-open")); };
    if (s) s.onclick = function () { setSide(false); };
    if (m) m.onclick = function () {
      var mini = !document.documentElement.classList.contains("side-mini");
      document.documentElement.classList.toggle("side-mini", mini);
      try { if (mini) localStorage.setItem("mcpa-sim-side", "mini"); else localStorage.removeItem("mcpa-sim-side"); } catch (e) {}
    };
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && document.documentElement.classList.contains("side-open")) setSide(false); });
  })();

  // ---------- router ----------
  function render() {
    document.documentElement.lang = S.lang;
    document.querySelectorAll("[data-i18n]").forEach(function (el) { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll("[data-lang]").forEach(function (b) { b.classList.toggle("on", b.dataset.lang === S.lang); });
    var h = (location.hash || "#home").slice(1), parts = h.split("/"), sec = parts[0];
    var dom = sec === "course" && DOMAIN[parts[1]] ? parts[1] : sec === "t" && TOPIC[parts[1]] ? TOPIC[parts[1]].dom : null;
    buildSide(sec, dom); crumbs(crumbsFor(sec, parts)); setSide(false);
    if (sec !== "run") { stopTimer(); keyCtx = null; }
    if (sec !== "flash") { flashKey = null; FL.deck = null; }
    applyTheme(getTheme()); updateBadge();
    if (sec === "course" && parts[1]) pageDomain(parts[1]);
    else if (sec === "course") pageCourse();
    else if (sec === "t" && TOPIC[parts[1]]) pageDomain(TOPIC[parts[1]].dom, parts[1]);
    else if (sec === "quiz") pageSetup(parts[1] === "exam");
    else if (sec === "run") pageRun();
    else if (sec === "review") pageReview();
    else if (sec === "about") pageAbout();
    else if (sec === "settings") pageSettings();
    else if (sec === "flash") pageFlash();
    else if (sec === "progress") pageProgress();
    else if (sec === "session" && parts[1]) pageSession(+parts[1]);
    else pageHome();
  }
  document.querySelectorAll("[data-lang]").forEach(function (b) {
    b.onclick = function () { S.lang = b.dataset.lang; save(); if (location.hash === "#run" && session) { render(); } else render(); };
  });
  window.addEventListener("hashchange", function () {
    if (session && !session.over && session.mode === "exam" && location.hash !== "#run") {
      // leaving an exam in progress keeps it; coming back resumes it
    }
    render();
  });
  restoreSession();
  render();
  }
})();
