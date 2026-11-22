"""Avvio nel container. I volumi di Fly.io e i dischi di Render vengono montati come root:
se il processo parte da root, rende /data scrivibile dall'utente mcpa e poi rinuncia ai privilegi.
Con Docker in locale (volume già dell'utente mcpa) il risultato è lo stesso."""
import os
import sys

UID = GID = 10001
DATA = os.path.dirname(os.environ.get("MCPA_DB", "/data/mcpa.db"))

if os.getuid() == 0:
    os.makedirs(DATA, exist_ok=True)
    for root, dirs, files in os.walk(DATA):
        for name in [root] + [os.path.join(root, f) for f in files]:
            try:
                os.chown(name, UID, GID)
            except OSError:
                pass
    os.setgroups([])
    os.setgid(GID)
    os.setuid(UID)
    os.environ["HOME"] = "/tmp"

here = os.path.dirname(os.path.abspath(__file__))
os.execv(sys.executable, [sys.executable, os.path.join(here, "server.py"), "--no-browser"])
