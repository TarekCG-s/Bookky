from flask import url_for, flash, redirect, session
from bookky import app, serializer, mail
from functools import wraps
from PIL import Image
from flask_mail import Message
import os
import secrets


def login_required(func):
    @wraps(func)
    def check_session(*args, **kargs):
        if session.get('user_id') is None:
            flash(f'You need to log in first', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kargs)
    return check_session


def logout_required(func):
    @wraps(func)
    def check_logout(*args, **kargs):
        if session.get('user_id'):
            flash(f'You are already logged in', 'success')
            return redirect(url_for('index'))
        return func(*args, **kargs)
    return check_logout


def update_picture(form_picture, user_id):
    _, pic_extension = os.path.splitext(form_picture.filename)
    random_name = secrets.token_hex(8)
    profile_pic = str(user_id) + random_name + pic_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', profile_pic)
    size = (256,256)
    image = Image.open(form_picture)
    image.thumbnail(size)
    image.save(picture_path)
    return profile_pic

def send_email(email, title, msgBody):

    msg = Message(title, sender='info@Bookky.com', recipients=[email])
    msg.body = msgBody
    mail.send(msg)
