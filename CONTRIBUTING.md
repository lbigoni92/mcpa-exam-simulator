# Contributing / Contribuire

**EN.** Thanks for helping improve the MCPA simulator.

- **Wrong or outdated question:** open an issue with the "Wrong question" template. Include the question id (shown in the session detail, e.g. `o-D3-10`) and the section of the MCP spec 2026-07-28 that proves the correct answer.
- **New questions:** add them to `site/content/questions-*.json` with both `it` and `en` text, then run:
  ```bash
  python site/build/build_data.py && python site/build/check_consistency.py
  ```
  The check must end with `ERRORI: 0`.
- **Rules:** official sources only (spec, modelcontextprotocol.io, SEPs). Never submit real exam questions or "dumps": they violate the Linux Foundation confidentiality agreement and will be removed. Do not copy copyrighted third-party questions.
- **Database changes:** add a new `site/migrations/NNNN_description.sql`; never edit a published migration.

**IT.** Grazie per l'aiuto. Per una domanda sbagliata apri una issue con l'id della domanda e la sezione della spec 2026-07-28 che lo dimostra. Le nuove domande vanno in `site/content/` in italiano e inglese, poi si lanciano `build_data.py` e `check_consistency.py`. Solo fonti ufficiali, mai domande d'esame reali o dump.
