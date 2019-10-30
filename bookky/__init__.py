import os
from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail_sendgrid import MailSendGrid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MAIL_SENDGRID_API_KEY'] = os.getenv('SendGridAPI')

Session(app)
bcrypt = Bcrypt(app)
mail = MailSendGrid(app)

serializer = Serializer(app.config['SECRET_KEY'], 1800)


engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

from bookky import routes
