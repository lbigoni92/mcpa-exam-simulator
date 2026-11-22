# Domande personali (cartella esclusa da git)

Metti qui le tue domande in file `questions-*.json`. Git le ignora, quindi restano solo sul tuo computer e non finiscono nel repository pubblico.

- Formato: lo stesso di `site/content/questions-D*.json` (campi `id`, `t`, `type`, `q`, `o`, `c`, `x`, con testi `it` ed `en`). Usa id che iniziano con `o-U-`.
- Il server le importa all'avvio insieme a `bank.json` e le rilegge quando un file cambia. Nel simulatore compaiono con l'etichetta "Domanda personale" e fanno parte del set "Originali".
- Con Docker la cartella è montata in sola lettura (`docker-compose.yml`): basta riavviare il container con `docker compose restart`.
- Se togli un file, al riavvio successivo le sue domande vengono disattivate; risposte e progressi già salvati restano nel database.

---

**EN.** Put your own questions here as `questions-*.json` files (same format as `site/content/questions-D*.json`). This folder is ignored by git, so they stay on your machine. The server imports them at startup together with `bank.json`.
