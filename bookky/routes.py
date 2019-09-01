from flask import Flask, render_template, url_for, flash, redirect, session
from bookky import app, db, bcrypt, posts
from bookky.wrappers import login_required, logout_required
from bookky.forms import RegisterationForm, LoginForm

@app.route('/')
@app.route('/home')
@login_required
def index():
    return render_template('index.html', posts = posts)



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title="Profile")


@app.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegisterationForm()
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
        session['username'] = user.username
        session.permanent = form.remember_me.data
        return redirect(url_for('index'))
    return render_template('login.html',title="Login" , form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
