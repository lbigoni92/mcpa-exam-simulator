# Simulatore online, solo per te (opzionale)

In locale non cambia nulla: `avvia.bat`, `python site/server.py` e `docker compose up` restano senza password e raggiungibili solo da `127.0.0.1`.

Online il server si attiva in modalità protetta quando trova la variabile d'ambiente **`MCPA_PASSWORD`** (almeno 12 caratteri):

- tutte le pagine e le API chiedono il login (pagina con una sola password, cookie `HttpOnly`/`Secure`/`SameSite=Strict` valido 30 giorni, "Esci" nelle Impostazioni);
- dopo 5 password sbagliate lo stesso IP aspetta 5 minuti;
- accetta solo l'host pubblico del servizio (`MCPA_PUBLIC_HOST`, oppure quello che Fly.io e Render impostano da soli) e richieste `https` da quell'origine;
- se c'è un host pubblico ma manca la password, il server **non parte**;
- `noindex` per i motori di ricerca; `/healthz` è l'unica pagina senza login (risponde solo `ok`).

Cambiare la password invalida subito tutti i login esistenti.

## Dove pubblicarlo

Il database SQLite deve stare su un disco che sopravvive a riavvii e deploy.

| Opzione | Costo indicativo | Note |
|---|---|---|
| **Fly.io** con volume da 1 GB (consigliata) | circa **1–3 $/mese**: macchina 256 MB a 2,19 $/mese se sempre accesa, meno con lo spegnimento automatico; volume 0,15 $/GB/mese | Si spegne quando non lo usi e si riaccende in pochi secondi alla prima visita. Serve una carta di credito; nessun piano gratuito per i nuovi account (prova di 7 giorni o 2 ore di macchina). |
| Render, istanza Starter + disco 1 GB | circa **7,25 $/mese** (7 $ + 0,25 $/GB) | Più semplice da dashboard. Il piano free **non** può avere dischi: il database si perde a ogni riavvio, deploy o dopo 15 minuti di inattività. |

Prezzi letti il 2026-11-22 su [fly.io/docs/about/pricing](https://fly.io/docs/about/pricing/) e [render.com/pricing](https://render.com/pricing): controllali prima di attivare.

## Fly.io (consigliata)

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

## Render (alternativa)

1. Crea l'account su [render.com](https://render.com) e collega GitHub (lo fai tu).
2. **New → Blueprint**, scegli il repository: Render legge `render.yaml` (istanza Starter, disco da 1 GB su `/data`, regione Frankfurt).
3. Quando lo chiede, inserisci `MCPA_PASSWORD`.
4. Apri l'indirizzo `https://<nome>.onrender.com` e accedi.

Con Render la build parte da GitHub, quindi le domande personali di `site/local` non ci sono.

## Portare i progressi online

Locale: **Impostazioni → Esporta i progressi**. Online: **Impostazioni → Importa da file**. Lo stesso file serve anche per tornare indietro.
