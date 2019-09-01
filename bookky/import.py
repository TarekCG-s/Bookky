import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import csv


engine = create_engine('postgresql://postgres:5161723@localhost:5432/postgres')
db = scoped_session(sessionmaker(bind=engine))


file = open('books.csv')
reader = csv.reader(file)
for isbn, title, author, year in reader:
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title":title, "author":author, "year":int(year)})
    print(f"ADDED {isbn}, {title}, {author}, {int(year)}")
db.commit()
