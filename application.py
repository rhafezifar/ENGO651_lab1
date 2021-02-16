import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('uname').lower()
    password = request.form.get('password')
    result = db.execute(f"SELECT * from users where username='{username}' AND password='{password}'")
    if result.rowcount == 1:
        session['username'] = username
        return f"Welcome {username}!"
    return "Error: username and password doesn't match."


@app.route("/register_form", methods=['GET'])
def register_form():
    return render_template("register.html")


@app.route("/register", methods=['POST'])
def register():
    username = request.form.get('uname').lower()
    password = request.form.get('password')
    result = db.execute(f"SELECT * from users where username='{username}'")
    if result.rowcount == 1:
        return "Error: The entered username is taken. please try a different username."
    db.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    db.commit()
    return "OK. registration done"


@app.route("/login_test", methods=['GET'])
def login_test():
    if 'username' in session:
        return f"you are currently logged in as {session['username']}."
    return "Nobody is logged in :("


@app.route("/logout", methods=['GET'])
def logout():
    del session['username']
    return "Logged out successfully."
