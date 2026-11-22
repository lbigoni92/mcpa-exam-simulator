# Pubblicare il progetto su GitHub in modo che si trovi

Il codice è già pronto (README in inglese con parole chiave, schermate, licenza, template per le segnalazioni). Su GitHub restano da fare alcune impostazioni, che si possono fare solo dal tuo account.

## 1. Crea il repository
- **Nome consigliato:** `mcpa-exam-simulator`. Contiene le parole che si cercano ("MCPA", "exam", "simulator"); il nome del repository è il fattore che pesa di più nella ricerca di GitHub.
- **Visibilità:** pubblico.
- Non aggiungere README, licenza o .gitignore da GitHub: ci sono già.

## 2. Primo push (dalla cartella del progetto)
```bash
git init
git add .
git commit -m "MCPA exam simulator: course, 641 questions, local SQLite progress"
git branch -M main
git remote add origin https://github.com/<tuo-utente>/mcpa-exam-simulator.git
git push -u origin main
```
Il database (`site/mcpa.db`) è escluso da `.gitignore`: chi clona lo ritrova creato al primo avvio.

## 3. Descrizione e topics (pannello "About", icona ⚙ a destra)
- **Description:** `MCPA (Model Context Protocol Associate) exam simulator and course: 641 practice questions, 60-question mock exams, EN/IT, progress in SQLite. MCP spec 2026-07-28.`
- **Website:** lascia vuoto (il sito gira in locale).
- **Topics** (max 20):
  `mcpa` `model-context-protocol` `mcp` `certification` `exam-simulator` `practice-exam` `mock-exam` `exam-prep` `quiz` `linux-foundation` `agentic-ai` `ai-agents` `study-guide` `sqlite` `python` `docker` `self-hosted` `italian`

In alternativa, con la GitHub CLI:
```bash
gh repo edit <tuo-utente>/mcpa-exam-simulator \
  --description "MCPA (Model Context Protocol Associate) exam simulator and course: 641 practice questions, 60-question mock exams, EN/IT, progress in SQLite. MCP spec 2026-07-28." \
  --add-topic mcpa,model-context-protocol,mcp,certification,exam-simulator,practice-exam,mock-exam,exam-prep,quiz,linux-foundation,agentic-ai,ai-agents,study-guide,sqlite,python,docker,self-hosted,italian
```

## 4. Immagine di anteprima
Settings → General → **Social preview** → carica `docs/social-preview.png` (1280×640). È l'immagine che compare quando il link viene condiviso su LinkedIn, X, Slack, Telegram.

## 5. Altre cose che aiutano
- **Release:** crea una release `v1.0.0` (Releases → Draft a new release). I repository con release compaiono meglio nei risultati.
- **Issues attive:** lascia attive le Issues; il template "Wrong or outdated question" è già pronto.
- **Condivisione:** un post su LinkedIn con l'immagine di anteprima e il link porta le prime stelle, che fanno salire il repository nella ricerca.
- **Liste "awesome":** si può proporre il repository in elenchi come `awesome-mcp` con una pull request, ma solo dopo averlo pubblicato e verificato.

## Nota sui marchi
Nome e descrizione usano "MCPA" e "Model Context Protocol" solo in modo descrittivo, e il README dice che il progetto non è ufficiale. Evita loghi Linux Foundation o AAIF nell'immagine di anteprima.
