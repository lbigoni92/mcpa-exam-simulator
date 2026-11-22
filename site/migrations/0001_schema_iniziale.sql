-- Schema iniziale: corso, domande, sessioni, risposte, ripasso.
-- IF NOT EXISTS: sicura anche sui database creati prima delle migrazioni.
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS domains (
  id TEXT PRIMARY KEY, name_it TEXT, name_en TEXT, weight INTEGER, study_weight INTEGER, ord INTEGER);
CREATE TABLE IF NOT EXISTS topics (
  id TEXT PRIMARY KEY, domain_id TEXT REFERENCES domains(id), ord INTEGER,
  title_it TEXT, title_en TEXT, data_json TEXT);
CREATE TABLE IF NOT EXISTS questions (
  id TEXT PRIMARY KEY, topic_id TEXT, domain_id TEXT, source TEXT, set_name TEXT, set_title TEXT,
  difficulty INTEGER, type TEXT, stem_it TEXT, stem_en TEXT, explanation_it TEXT, explanation_en TEXT,
  review_json TEXT, active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS options (
  question_id TEXT REFERENCES questions(id), idx INTEGER, text_it TEXT, text_en TEXT, is_correct INTEGER,
  PRIMARY KEY (question_id, idx));
CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, mode TEXT, pool TEXT, started_at TEXT, ended_at TEXT,
  duration_s INTEGER, n_questions INTEGER, n_correct INTEGER, score_pct REAL, passed INTEGER, time_up INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS session_questions (
  session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE, position INTEGER, question_id TEXT,
  PRIMARY KEY (session_id, position));
CREATE TABLE IF NOT EXISTS answers (
  id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE,
  question_id TEXT, domain_id TEXT, selected_json TEXT, correct INTEGER, time_ms INTEGER, answered_at TEXT,
  UNIQUE (session_id, question_id));
CREATE TABLE IF NOT EXISTS review_queue (question_id TEXT PRIMARY KEY, streak INTEGER DEFAULT 0, added_at TEXT);
CREATE INDEX IF NOT EXISTS idx_answers_q ON answers(question_id);
CREATE INDEX IF NOT EXISTS idx_q_domain ON questions(domain_id);
