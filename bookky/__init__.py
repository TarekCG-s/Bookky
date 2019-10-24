import os
from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd99ba4661b8599b8f4f139df838c9d8d'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = 'BookkyWebsite@gmail.com'
app.config["MAIL_PASSWORD"] = 'bookkyheroku'

Session(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

serializer = Serializer(app.config['SECRET_KEY'], 1800)


engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

from bookky import routes
