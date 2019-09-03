import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import csv


engine = create_engine('postgresql://postgres:5161723@localhost:5432/postgres')
db = scoped_session(sessionmaker(bind=engine))

db.execute("""
    CREATE TABLE users
    (
      id SERIAL PRIMARY KEY,
      username VARCHAR NOT NULL UNIQUE,
      email VARCHAR NOT NULL UNIQUE,
      password VARCHAR NOT NULL,
      image VARCHAR
    )
""")

db.execute("""CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL UNIQUE,
  title VARCHAR NOT NULL,
  author VARCHAR,
  year INTEGER,
  review_count INTEGER NOT NULL DEFAULT 0,
  average_score FLOAT NOT NULL DEFAULT 0.0
)
""")

db.execute("""CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  content TEXT NOT NULL,
  author INTEGER REFERENCES users,
  book INTEGER REFERENCES books,
  date_posted TIMESTAMP DEFAULT NOW()
)
""")


db.commit()

file = open('books.csv')
reader = csv.reader(file)
for isbn, title, author, year in reader:
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title":title, "author":author, "year":int(year)})
    print(f"ADDED {isbn}, {title}, {author}, {int(year)}")

db.commit()
