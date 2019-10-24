import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import csv

# connecting to the database
engine = create_engine('postgres://hgsyswtktdvbwq:fe0088fdefc1052e4dc9a9bdb48c3d9a1a182d448974bc911065a64741c99039@ec2-174-129-27-3.compute-1.amazonaws.com:5432/d4jtj0nfnuhkg5')
db = scoped_session(sessionmaker(bind=engine))

#defining tables
db.execute("""CREATE TABLE users
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
  total_score INTEGER NOT NULL DEFAULT 0,
  average_score FLOAT NOT NULL DEFAULT 0.0
)
""")

db.execute("""CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  rating INTEGER NOT NULL,
  review TEXT NOT NULL,
  reviewer INTEGER REFERENCES users,
  book INTEGER REFERENCES books,
  date_posted TIMESTAMP DEFAULT NOW()
)
""")


db.commit()

# reading the csv file of the books
file = open('books.csv')
reader = csv.reader(file)
for isbn, title, author, year in reader:
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title":title.lower(), "author":author.lower(), "year":int(year)})
    print(f"ADDED {isbn}, {title}, {author}, {int(year)}")

db.commit()
