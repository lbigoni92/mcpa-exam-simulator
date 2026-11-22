-- Livello di fonte (spec / docs / blog) e citazione ufficiale per ogni domanda
ALTER TABLE questions ADD COLUMN source_level TEXT;
ALTER TABLE questions ADD COLUMN cite_json TEXT;
