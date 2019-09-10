import requests
from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from bookky import app, db, bcrypt, posts
from bookky.wrappers import login_required, logout_required
from bookky.forms import RegistrationForm, LoginForm

@app.route('/')
@app.route('/home')
@login_required
def index():
    books = db.execute("SELECT * FROM books ORDER BY review_count DESC LIMIT 12").fetchall()
    return render_template('index.html', books = books)



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
    books = db.execute("SELECT * FROM books WHERE title LIKE :book OR author LIKE :book OR isbn LIKE :book", {"book":book}).fetchall()
    return render_template('book_lookup.html',title=book , books=books, results_count=len(books))



@app.route('/book/<string:isbn>', methods=["GET"])
def book(isbn):
    user_review = None
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
    if book is None:
        error_message = "There's no such book"
        return render_template('error.html', error_message=error_message)

    api_key = 'pbv0u9wn9bHWm6v5NakhA'
    goodreads_result = requests.get('https://www.goodreads.com/book/review_counts.json', params={"key": api_key, "isbns":isbn})
    goodreads_result = goodreads_result.json()

    if session.get('user_id') != None:
        reviews = db.execute("SELECT * FROM reviews JOIN users ON users.id= reviews.reviewer WHERE book = :book_id AND reviewer != :reviewer", {"book_id":book.id, "reviewer": session['user_id']}).fetchall()
        user_review = db.execute("SELECT * FROM reviews JOIN users ON users.id= reviews.reviewer WHERE book = :book_id AND reviewer = :reviewer", {"book_id":book.id, "reviewer": session['user_id']}).fetchone()
        return render_template("book.html", book=book, title=book.title, goodreads_result=goodreads_result, reviews=reviews, user_review=user_review)


    reviews = db.execute("SELECT * FROM reviews JOIN users ON users.id= reviews.reviewer WHERE book = :book_id", {"book_id":book.id}).fetchall()
    return render_template("book.html", book=book, title=book.title, goodreads_result=goodreads_result, reviews=reviews, user_review=user_review)





@app.route('/add_review/<string:id>/<string:isbn>', methods=["POST"])
@login_required
def add_review(id, isbn):
    id = int(id)
    rating = int(request.form.get('rating'))
    review = request.form.get('review')
    db.execute("INSERT INTO reviews (rating, review, reviewer, book) VALUES (:rating, :review, :reviewer, :book)", {"rating" : rating, "review" : review, "reviewer": session['user_id'], "book": id})
    book = db.execute("SELECT * FROM books WHERE id=:id", {"id":id}).fetchone()
    db.execute("UPDATE books SET review_count = :review_count, total_score = :total_score, average_score = :average_score WHERE id=:id", {
    "review_count": book.review_count + 1,
    "total_score": book.total_score + rating,
    "average_score": (book.total_score + rating) / ( book.review_count + 1),
    "id":id
    })
    db.commit()
    return redirect(url_for('book', isbn=isbn))


@app.route('/api/book/<string:isbn>')
def api_book(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if book == None:
        return jsonify({"Error":"There's no book with such ISBN"}), 422

    book_json = jsonify({
        "title":book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": book.review_count,
        "average_score": book.average_score
    })

    return book_json
