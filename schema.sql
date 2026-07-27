PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS contents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content_type TEXT DEFAULT 'article',
  title TEXT,
  url TEXT,
  author TEXT,
  source_platform TEXT,
  published_at TEXT,
  raw_text TEXT,
  summary TEXT,
  tools TEXT,
  methods TEXT,
  suggested_category TEXT,
  applicable_scenarios TEXT,
  extraction_status TEXT DEFAULT '仅保存链接',
  extraction_error TEXT,
  content_source TEXT DEFAULT 'manual',
  user_reflection TEXT,
  save_reason TEXT,
  problem_statement TEXT,
  intended_use TEXT,
  status TEXT DEFAULT '待补充',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT,
  isbn TEXT,
  publisher TEXT,
  published_at TEXT,
  description TEXT,
  category TEXT,
  problem_statement TEXT,
  relationship_status TEXT,
  reading_status TEXT DEFAULT '未开始',
  priority TEXT,
  is_read INTEGER DEFAULT 0,
  start_date TEXT,
  finish_date TEXT,
  user_note TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS reading_notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER,
  chapter_or_page TEXT,
  source_idea TEXT,
  user_understanding TEXT,
  related_experience TEXT,
  planned_action TEXT,
  convert_to_experiment INTEGER DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  deleted_at TEXT,
  FOREIGN KEY(book_id) REFERENCES books(id)
);

CREATE TABLE IF NOT EXISTS problems (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  problem_type TEXT,
  importance TEXT,
  status TEXT DEFAULT '待处理',
  current_conclusion TEXT,
  next_action TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS experiments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content_id INTEGER,
  book_id INTEGER,
  reading_note_id INTEGER,
  problem_id INTEGER,
  goal TEXT,
  current_problem TEXT,
  minimum_test TEXT,
  success_criteria TEXT,
  estimated_effort TEXT,
  started_at TEXT,
  actual_action TEXT,
  actual_result TEXT,
  issues_found TEXT,
  is_effective TEXT,
  final_decision TEXT,
  reusable_conclusion TEXT,
  next_action TEXT,
  status TEXT DEFAULT '待实践',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  deleted_at TEXT,
  FOREIGN KEY(content_id) REFERENCES contents(id),
  FOREIGN KEY(book_id) REFERENCES books(id),
  FOREIGN KEY(reading_note_id) REFERENCES reading_notes(id),
  FOREIGN KEY(problem_id) REFERENCES problems(id)
);

CREATE TABLE IF NOT EXISTS content_problem_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content_id INTEGER NOT NULL,
  problem_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(content_id, problem_id),
  FOREIGN KEY(content_id) REFERENCES contents(id),
  FOREIGN KEY(problem_id) REFERENCES problems(id)
);

CREATE TABLE IF NOT EXISTS book_problem_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER NOT NULL,
  problem_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(book_id, problem_id),
  FOREIGN KEY(book_id) REFERENCES books(id),
  FOREIGN KEY(problem_id) REFERENCES problems(id)
);

CREATE TABLE IF NOT EXISTS note_problem_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  reading_note_id INTEGER NOT NULL,
  problem_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(reading_note_id, problem_id),
  FOREIGN KEY(reading_note_id) REFERENCES reading_notes(id),
  FOREIGN KEY(problem_id) REFERENCES problems(id)
);

CREATE TABLE IF NOT EXISTS attachments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL,
  entity_id INTEGER NOT NULL,
  file_name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  mime_type TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT
);
