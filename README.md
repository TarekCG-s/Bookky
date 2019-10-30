# Bookky
Hosted on : http://bookky.herokuapp.com
Demo video : https://youtu.be/KB8OOM2LMec

# Overview :
A book review website where users can register and login with their email and password.
Users can see the trending books based on the review count of the books. They can also search for books by querying the title, author's name, year of publish or ISBN of the book.
They can post reviews and see other people's reviews and also see ratings of books from goodreads.
If a user forgot his password, he could request a link to change his password.

# Specifications :
The website was built with Python and Flask.

run.py:
  The file from where you can start the app.

booky/__init__.py :
  In this file, you could find the configurations for Flask, database, Bycrypt and Mail.

booky/routes.py :
  This is where all the routes of the website are defined

booky/helpers.py :
  This is where  the login_required and logout_required wrappers are defined. 
