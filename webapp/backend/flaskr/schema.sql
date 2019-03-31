-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;

CREATE TABLE user (
 id INTEGER PRIMARY KEY AUTO_INCREMENT,
 username TEXT NOT NULL,
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
 date_published TEXT,
 isbn13 TEXT NOT NULL,
 ratings_count FLOAT NOT NULL,
 work_ratings_count FLOAT NOT NULL,
 work_text_reviews_count FLOAT NOT NULL,
 ratings_1 FLOAT NOT NULL,
 ratings_2 FLOAT NOT NULL,
 ratings_3 FLOAT NOT NULL,
 ratings_4 FLOAT NOT NULL,
 ratings_5 FLOAT NOT NULL,
 details TEXT NOT NULL
);

CREATE TABLE reviews (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  isbn TEXT NOT NULL,
  author TEXT NOT NULL,
  review_source TEXT NOT NULL,
  average_rating FLOAT NOT NULL,
  review_author TEXT NOT NULL,
  review_content TEXT NOT NULL
);
