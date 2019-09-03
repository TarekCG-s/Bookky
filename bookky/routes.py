import requests
from flask import Flask, render_template, url_for, flash, redirect, session, request
from bookky import app, db, bcrypt, posts
from bookky.wrappers import login_required, logout_required
from bookky.forms import RegistrationForm, LoginForm

@app.route('/')
@app.route('/home')
@login_required
def index():
    return render_template('index.html', posts = posts)



@app.route('/account/')
@login_required
def account():
    return render_template('account.html', title="Account")


@app.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if db.execute("SELECT username FROM users WHERE username=:username", {"username":form.username.data}).fetchone() :
            flash(f'{form.username.data} is already taken. Choose another name', 'danger')
            return redirect(url_for('register'))
        elif db.execute("SELECT email FROM users WHERE email=:email", {"email" : form.email.data}).fetchone():
            flash(f'{form.email.data} is already taken. Choose another E-Mail', 'danger')
            return redirect(url_for('register'))

        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.execute("INSERT INTO users (username, email, password, image) VALUES (:username, :email, :password, :image)", {
        "username": form.username.data, "email": form.email.data, "password": hash_pw, "image": 'default.jpg' })
        db.commit()
        flash(f'Hello, {form.username.data}. Thank you for making an account', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title="Login", form=form)


@app.route('/login',  methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.execute("SELECT username, id, password FROM users WHERE email=:email", {"email":form.email.data}).fetchone()
        if not user or not bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'The E-mail or password is incorrect ','danger')
            return redirect(url_for('login'))
        flash(f'Hello {user.username}, Welcome back! ','success')
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = form.remember_me.data
        return redirect(url_for('index'))
    return render_template('login.html',title="Login" , form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/search/', methods=['POST'])
def search():
    book = request.form.get('book')
    if book == "":
        error_message = "You should enter a name of what you're looking for"
        return render_template('error.html', error_message=error_message)
    return redirect(url_for('book_lookup', book=book))

@app.route('/book_lookup/<string:book>', methods=['GET'])
def book_lookup(book):
    book = f"%{book}%"
    books = db.execute("SELECT * FROM books WHERE title LIKE :book", {"book":book}).fetchall()

    return render_template('book_lookup.html',title=book , books=books, results_count=len(books))

@app.route('/book/<string:isbn>', methods=["GET"])
def book(isbn):

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
    if book is None:
        error_message = "There's no such book"
        return render_template('error.html', error_message=error_message)

    api_key = 'pbv0u9wn9bHWm6v5NakhA'
    goodreads_result = requests.get('https://www.goodreads.com/book/review_counts.json', params={"key": api_key, "isbns":isbn})
    goodreads_result = goodreads_result.json()
    return render_template("book.html", book=book, title=book.title, goodreads_result=goodreads_result)
