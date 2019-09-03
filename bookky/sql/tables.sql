CREATE TABLE users
(
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL UNIQUE,
  email VARCHAR NOT NULL UNIQUE,
  password VARCHAR NOT NULL,
  image VARCHAR
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  content TEXT NOT NULL,
  author INTEGER REFERENCES users,
  book INTEGER REFERENCES books,
  date_posted TIMESTAMP DEFAULT NOW()
);

CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL UNIQUE,
  title VARCHAR NOT NULL,
  author VARCHAR,
  year INTEGER,
  review_count INTEGER NOT NULL DEFAULT 0,
  average_score FLOAT NOT NULL DEFAULT 0.0
);
