# Simulatore online, solo per te (opzionale)

In locale non cambia nulla: `avvia.bat`, `python site/server.py` e `docker compose up` restano senza password e raggiungibili solo da `127.0.0.1`.

Online il server si attiva in modalità protetta quando trova la variabile d'ambiente **`MCPA_PASSWORD`** (almeno 12 caratteri):

- tutte le pagine e le API chiedono il login (pagina con una sola password, cookie `HttpOnly`/`Secure`/`SameSite=Strict` valido 30 giorni, "Esci" nelle Impostazioni);
- dopo 5 password sbagliate lo stesso IP aspetta 5 minuti; dopo 30 errori in un'ora da qualsiasi IP il login si blocca per tutti fino allo scadere dell'ora (chi è già entrato resta dentro);
- header di sicurezza: Content-Security-Policy senza script esterni, HSTS, `X-Frame-Options: DENY`, `nosniff`;
- l'import accetta solo file fino a 25 MB con valori semplici del tipo giusto per ogni colonna;
- accetta solo l'host pubblico del servizio (`MCPA_PUBLIC_HOST`, oppure quello che Fly.io e Render impostano da soli) e richieste `https` da quell'origine;
- se c'è un host pubblico ma manca la password, il server **non parte**;
- `noindex` per i motori di ricerca; `/healthz` è l'unica pagina senza login (risponde solo `ok`).

Cambiare la password invalida subito tutti i login esistenti.

## Dove pubblicarlo

Il database SQLite deve stare su un disco che sopravvive a riavvii e deploy.

| Opzione | Costo indicativo | Note |
|---|---|---|
| **Fly.io** con volume da 1 GB | circa **1–3 $/mese**: macchina 256 MB a 2,19 $/mese se sempre accesa, meno con lo spegnimento automatico; volume 0,15 $/GB/mese | Si spegne quando non lo usi e si riaccende in pochi secondi alla prima visita. Serve una carta di credito; nessun piano gratuito per i nuovi account (prova di 7 giorni o 2 ore di macchina). |
| **Render free + UptimeRobot** (scelta attuale) | **0 $** | Il disco si azzera a deploy e riavvii: i progressi si salvano con Esporta/Importa dalle Impostazioni. UptimeRobot ogni 5 minuti evita lo spegnimento dopo 15 minuti. |
| Render, istanza Starter + disco 1 GB | circa **7,25 $/mese** (7 $ + 0,25 $/GB) | Disco persistente, nessun backup esterno necessario. |

Prezzi letti il 2026-11-22 su [fly.io/docs/about/pricing](https://fly.io/docs/about/pricing/) e [render.com/pricing](https://render.com/pricing): controllali prima di attivare.

## Fly.io

Una volta sola, sul PC:

1. Crea l'account su [fly.io](https://fly.io) e aggiungi la carta (lo fai tu).
2. Installa `flyctl` (Windows, PowerShell): `iwr https://fly.io/install.ps1 -useb | iex`, poi `fly auth login`.
3. Nella cartella `site`, scegli un nome unico e aggiornalo in `fly.toml` (riga `app`), poi:

   ```bash
   fly launch --copy-config --no-deploy
   fly secrets set MCPA_PASSWORD="una-password-lunga-e-tua"
   fly deploy
   ```

   Il volume `mcpa_data` da 1 GB viene creato al primo `fly deploy` (sezione `[mounts]` di `fly.toml`).

4. Apri `https://<nome-app>.fly.dev`, entra con la password.

Aggiornare dopo un `git pull`: `fly deploy` dalla cartella `site`.
Le domande personali di `site/local` entrano nell'immagine perché la build parte dal tuo PC (registry privato di Fly).

## Render gratuito con UptimeRobot (scelta attuale)

Il piano free di Render spegne il servizio dopo 15 minuti senza visite e azzera il disco a ogni deploy o riavvio, quindi **i progressi online possono sparire**. Per non perderli: **Impostazioni → Esporta i progressi** ogni tanto, e **Importa da file** dopo un riavvio.

Passi (li fai tu, una volta sola):

1. **Render:** crea l'account su [render.com](https://render.com), collega GitHub, **New → Blueprint** e scegli il repository. Render legge `render.yaml` (piano free, Frankfurt).
2. Quando la chiede, inserisci `MCPA_PASSWORD` (almeno 12 caratteri).
3. Apri `https://<nome>.onrender.com` ed entra con la password.
4. **UptimeRobot** (stesso account e stesso schema dell'altro tuo sito): nuovo monitor **HTTP(s)** su `https://<nome>.onrender.com/healthz`, intervallo **5 minuti**. Ti avvisa via email se il sito non risponde e tiene sveglio il servizio. `/healthz` risponde `ok` senza password.

Un solo servizio acceso sempre sta nelle 750 ore gratuite al mese. La build parte da GitHub, quindi le domande personali di `site/local` non ci sono.

Variante a pagamento con dati persistenti (circa 7,25 $/mese): in `render.yaml` metti `plan: starter` e togli i `#` dal blocco `disk`.

## Portare i progressi online

Locale: **Impostazioni → Esporta i progressi**. Online: **Impostazioni → Importa da file**. Lo stesso file serve anche per tornare indietro.

Il file contiene tutto quello che nel database è tuo: sessioni, risposte (con tempi e confidenza), ripasso, flashcard e impostazioni. Corso e domande non servono, perché il server li ricarica da `bank.json` a ogni avvio.
