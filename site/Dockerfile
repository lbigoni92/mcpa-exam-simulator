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
COPY server.py bank.json index.html app.js app.css ./
COPY migrations ./migrations

# utente non privilegiato; /data contiene il database (montato come volume per non perdere le sessioni)
RUN useradd --system --uid 10001 mcpa && mkdir /data && chown mcpa /data
USER mcpa
VOLUME ["/data"]

EXPOSE 8765
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8765/', timeout=2).status==200 else 1)"

CMD ["python", "server.py", "--no-browser"]
