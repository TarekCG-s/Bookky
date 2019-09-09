import os
from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd99ba4661b8599b8f4f139df838c9d8d'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
bcrypt = Bcrypt(app)



engine = create_engine('postgres://hgsyswtktdvbwq:fe0088fdefc1052e4dc9a9bdb48c3d9a1a182d448974bc911065a64741c99039@ec2-174-129-27-3.compute-1.amazonaws.com:5432/d4jtj0nfnuhkg5')
db = scoped_session(sessionmaker(bind=engine))


posts = [
    {
        "author":"Tarek",
        "title":"chernobyl",
        "content": "To be a scientist is to be naive. We are so focused on our search for truth, we fail to consider how few actually want us to find it." +
            "But it is always there whether we see it or not, whether we choose to or not." + "The truth doesn’t care about our needs or wants - it doesn’t care about our governments, " +
            "our ideologies, our religions - to lie in wait for all time.",
        "date": "23 Aug 2019"
    }
]
from bookky import routes
