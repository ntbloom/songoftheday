BEGIN;
SET CLIENT_MIN_MESSAGES=WARNING; --ignores notices
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    has_administrator_access BOOLEAN NOT NULL, --allowed to edit entries
    email TEXT NOT NULL,
    day_of_week TEXT NOT NULL,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    UNIQUE(username),
    UNIQUE(day_of_week),
    UNIQUE(password),
    UNIQUE(salt)
);

DROP TABLE IF EXISTS prohibited_passwords;
CREATE TABLE prohibited_passwords (
    password TEXT
);
DROP INDEX IF EXISTS prohib_idx;
CREATE INDEX prohib_idx ON prohibited_passwords USING HASH (password);


DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
  entry_id SERIAL PRIMARY KEY,
  day DATE NOT NULL,
  username TEXT,
  artist TEXT NOT NULL,
  artist_lexemes TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', artist)) STORED,
  song_name TEXT NOT NULL,
  song_lexemes TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', song_name)) STORED,
  year INTEGER NOT NULL,
  hyperlink TEXT NOT NULL,
  duration INTEGER,
  entered_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE,
  updated_by TEXT,
  FOREIGN KEY(username) REFERENCES users(username),
  FOREIGN KEY(updated_by) REFERENCES users(username)
);

--index on entries
DROP INDEX IF EXISTS song_lexemes_idx;
CREATE INDEX song_lexemes_idx ON entries USING GIN (song_lexemes);

DROP INDEX IF EXISTS artist_lexemes_idx;
CREATE INDEX artist_lexemes_idx ON entries USING GIN(artist_lexemes);

COMMIT;
