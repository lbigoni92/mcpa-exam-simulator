-- Confidenza sulla risposta, ripasso dilazionato, flashcard e impostazioni
ALTER TABLE answers ADD COLUMN confidence TEXT;
ALTER TABLE review_queue ADD COLUMN box INTEGER DEFAULT 0;
ALTER TABLE review_queue ADD COLUMN due_at TEXT;
ALTER TABLE review_queue ADD COLUMN reason TEXT;
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS flashcards (
  card_id TEXT PRIMARY KEY, box INTEGER DEFAULT 0, due_at TEXT, seen INTEGER DEFAULT 0, known INTEGER DEFAULT 0, last_at TEXT);
