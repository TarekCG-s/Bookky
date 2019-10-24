import requests
import os
from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from bookky import app, db, bcrypt, serializer
from bookky.helpers import login_required, logout_required, update_picture, send_email
from bookky.forms import RegistrationForm, LoginForm, UpdatePicture, ResetRequestForm, ResetPasswordForm

# **********************************************************************************************************************************
# Dashboard route

@app.route('/')
@app.route('/home')
@login_required
def index():
    # Select the most trending books based on the number of reviews count.
    books = db.execute("SELECT * FROM books ORDER BY review_count DESC LIMIT 12").fetchall()
    return render_template('index.html', books = books)





# **********************************************************************************************************************************
# Profile route

@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    # Select user's data
    user = db.execute("SELECT username, email, image FROM users WHERE id=:id", {"id":session['user_id']}).fetchone()
    form = UpdatePicture()
    if form.validate_on_submit():
        # resizing the uploaded photo and generating a random name for it.
        profile_pic = update_picture(form.profile_picture.data, session['user_id'])
        # storing the name of picture in the database in the row of the user.
        db.execute("UPDATE users SET image = :image WHERE id=:id", {"image": profile_pic, "id":session['user_id']})
        db.commit()
        return redirect(url_for('account'))
    profile_picture = url_for('static', filename='profile_pics/' + user.image)
    return render_template('account.html', title="Account", user=user, profile_picture=profile_picture, form=form)




# **********************************************************************************************************************************
# Registeration routes

@app.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        if db.execute("SELECT username FROM users WHERE username=:username", {"username":form.username.data}).fetchone() :
            flash(f'{form.username.data} is already taken. Choose another name', 'danger')
            return redirect(url_for('register'))
        elif db.execute("SELECT email FROM users WHERE email=:email", {"email" : form.email.data.lower()}).fetchone():
            flash(f'{form.email.data} is already taken. Choose another E-Mail', 'danger')
            return redirect(url_for('register'))

        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        token = serializer.dumps({"username":form.username.data, "email":form.email.data.lower(), "password":hash_pw}).decode('utf-8')
        msgBody = f'''
        Confirm Account Link:
        {url_for('confirm_account', token=token, _external=True)}
        '''
        send_email(form.email.data, 'Account Confirmation' ,msgBody)
        flash(f'Hello, {form.username.data}. Thank you for registering. We have sent you a confirmation E-mail', 'warning')
        return redirect(url_for('login'))

    return render_template('register.html', title="Login", form=form)


@app.route('/confirm_account/<token>')
@logout_required
def confirm_account(token):

    try:
        user = serializer.loads(token)
    except:
        flash('Your secret key is either invalid or has expired', 'warning')
        return redirect(url_for('login'))

    if db.execute("SELECT email FROM users WHERE email=:email", {"email" : user['email']}).fetchone():
        flash(f'Your account has already been confirmed.', 'warning')
        return redirect(url_for('login'))

    db.execute("INSERT INTO users (username, email, password, image) VALUES (:username, :email, :password, :image)", {
    "username": user['username'], "email": user['email'].lower(), "password": user['password'], "image": 'default.jpg' })
    db.commit()
    flash(f"Hello, {user['username']}. You have successfully confirmed your account.", 'success')

    return redirect(url_for('login'))






# **********************************************************************************************************************************
# Login and logout routes


@app.route('/login',  methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.execute("SELECT username, id, password FROM users WHERE email=:email", {"email":form.email.data.lower()}).fetchone()
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






# **********************************************************************************************************************************
# Reset password routes

@app.route('/reset_request', methods=['GET', 'Post'])
@logout_required
def reset_request():
    form=ResetRequestForm()
    if form.validate_on_submit():
        user = db.execute("SELECT id, email FROM users WHERE email=:email",{'email':form.email.data.lower()}).fetchone()
        if user != None:
            token = serializer.dumps({'user_id':user.id}).decode('UTF-8')
            msgBody = f'''
            Password Reset Link
            {url_for('reset_password', token=token, _external=True)}
            '''
            send_email(form.email.data, 'Password Reset', msgBody)
            flash('An Email Reset Password has been sent to your E-mail', 'warning')
            return redirect(url_for('login'))
        flash("There's no such email registered", 'danger')
    return render_template('reset_request.html', title='Reset Password Request', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
@logout_required
def reset_password(token):
    form = ResetPasswordForm()
    try:
        user_id = serializer.loads(token)
    except:
        flash('Your secret key is either invalid or has expired', 'warning')
        return redirect(url_for('login'))

    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.execute("UPDATE users SET password=:password WHERE id=:id",{"password":hash_pw, "id":user_id['user_id']})
        db.commit()
        flash("Your password has been reset successfully", 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)





# **********************************************************************************************************************************
# Searching books routes

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






# **********************************************************************************************************************************
# book info page route

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






# **********************************************************************************************************************************
# Add Review route


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







# **********************************************************************************************************************************
# Book info JSON API route

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
