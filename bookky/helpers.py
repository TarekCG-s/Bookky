from flask import url_for, flash, redirect, session
from bookky import app, serializer, mail
from functools import wraps
from PIL import Image
from flask_mail import Message
import os
import secrets

# defining the login required decorator
def login_required(func):
    @wraps(func)
    def check_session(*args, **kargs):
        # checking if user is not logged in
        if session.get('user_id') is None:
            flash(f'You need to log in first', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kargs)
    return check_session


# defining the logout required decorator
def logout_required(func):
    @wraps(func)
    def check_logout(*args, **kargs):
        # checking if user is logged in
        if session.get('user_id'):
            flash(f'You are already logged in', 'success')
            return redirect(url_for('index'))
        return func(*args, **kargs)
    return check_logout


# generating random name for the picture and resizing it
def update_picture(form_picture, user_id):
    # extracting the extension of the picture.
    _, pic_extension = os.path.splitext(form_picture.filename)
    # genereating a random name for the picture.
    random_name = secrets.token_hex(8)
    # combining the random name with the user id and the extension for the picture.
    profile_pic = str(user_id) + random_name + pic_extension
    # generating the path of the picture.
    picture_path = os.path.join(app.root_path, 'static/profile_pics', profile_pic)
    # configuring the size for the picture to be resized
    size = (256,256)
    image = Image.open(form_picture)
    # resizing the picture and saving if the path.
    image.thumbnail(size)
    image.save(picture_path)
    return profile_pic


# sending emails
def send_email(email, title, msgBody):

    msg = Message(title, sender='info@Bookky.com', recipients=[email])
    msg.body = msgBody
    mail.send(msg)
