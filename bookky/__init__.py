import os
from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail_sendgrid import MailSendGrid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd99ba4661b8599b8f4f139df838c9d8d'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MAIL_SENDGRID_API_KEY'] ='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'

Session(app)
bcrypt = Bcrypt(app)
mail = MailSendGrid(app)

serializer = Serializer(app.config['SECRET_KEY'], 1800)


engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

from bookky import routes
