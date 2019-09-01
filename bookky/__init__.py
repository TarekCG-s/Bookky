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



engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))


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
from bookky import routes
