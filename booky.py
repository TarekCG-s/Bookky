import os
from flask import Flask, render_template, url_for, flash, redirect, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegisterationForm, LoginForm
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd99ba4661b8599b8f4f139df838c9d8d'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
bcrypt = Bcrypt(app)


engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

def login_required(func):
    @wraps(func)
    def check_session():
        if session.get('username') is None:
            flash(f'You need to log in first', 'warning')
            return redirect(url_for('login'))
        return func()
    return check_session

def logout_required(func):
    @wraps(func)
    def check_logout():
        if session.get('username'):
            flash(f'You are already logged in', 'success')
            return redirect(url_for('index'))
        return func()
    return check_logout



posts = [
    {
        "author":"Tarek",
        "title":"chernobyl",
        "content": "To be a scientist is to be naive. We are so focused on our search for truth, we fail to consider how few actually want us to find it." +
            "But it is always there whether we see it or not, whether we choose to or not." + "The truth doesn’t care about our needs or wants - it doesn’t care about our governments, " +
            "our ideologies, our religions - to lie in wait for all time.",
        "date": "23 Aug 2019"
    },
    {
        "author":"Sarah",
        "title":"I hate you and I love you",
        "content": "TDiscovering old songs is my new hobby - I've found a lot of hidden treasures and amazing voices in the last 4 months." +
            "I felt soo happy when I listened to Strangers in the night by Frank Sinatra." +
             "I felt like: Ok I've found my favorite song. But no, I was wrong! This song is my new addiction and my favorite song ever!!! Their voices areeee magical!!",
        "date": "17 Feb 2018 "
    }
]

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


if __name__ == '__main__':
    app.run(debug=True)
