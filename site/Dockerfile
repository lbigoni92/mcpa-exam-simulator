# Simulatore MCPA in un container: Python standard library + SQLite, nessuna dipendenza esterna.
# Uso rapido:  docker compose up -d   poi apri http://localhost:8765/
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MCPA_BIND=0.0.0.0 \
    MCPA_PORT=8765 \
    MCPA_DB=/data/mcpa.db \
    MCPA_NO_BROWSER=1

WORKDIR /app
COPY server.py entrypoint.py bank.json index.html app.js app.css ./
COPY migrations ./migrations
# domande personali (site/local, esclusa da git): entrano nell'immagine solo se presenti nella cartella da cui fai la build
COPY local ./local

# utente non privilegiato; /data contiene il database (montato come volume per non perdere le sessioni).
# Il container parte da root solo per rendere /data scrivibile (volumi Fly.io e dischi Render sono di root),
# poi entrypoint.py passa all'utente mcpa prima di avviare il server.
RUN groupadd --system --gid 10001 mcpa && useradd --system --uid 10001 --gid 10001 mcpa && mkdir /data && chown mcpa:mcpa /data
VOLUME ["/data"]

EXPOSE 8765
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import os,urllib.request,sys; p=os.environ.get('MCPA_PORT') or os.environ.get('PORT') or '8765'; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:'+p+'/healthz', timeout=2).status==200 else 1)"

CMD ["python", "entrypoint.py"]
