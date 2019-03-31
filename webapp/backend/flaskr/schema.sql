-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;

CREATE TABLE user (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username TEXT UNIQUE NOT NULL,
 password TEXT NOT NULL
);

-- CREATE TABLE post (
  -- id INTEGER PRIMARY KEY AUTOINCREMENT,
  -- author_id INTEGER NOT NULL,
  -- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- title TEXT NOT NULL,
  -- body TEXT NOT NULL,
  -- FOREIGN KEY (author_id) REFERENCES user (id)
-- );

CREATE TABLE books (
 id INTEGER PRIMARY KEY,
 title TEXT NOT NULL,
 author TEXT NOT NULL,
 isbn TEXT NOT NULL,
 cover TEXT NOT NULL,
 description TEXT NOT NULL,
 average_review FLOAT NOT NULL,
 purchase_link TEXT NOT NULL,
 date_published DATE,
 isbn13 TEXT,
 ratings_count FLOAT,
 work_ratings_count FLOAT, 
 work_text_reviews_count FLOAT,
 ratings_1 FLOAT,
 ratings_2 FLOAT,
 ratings_3 FLOAT,
 ratings_4 FLOAT,
 ratings_5 FLOAT,
 details TEXT
);
