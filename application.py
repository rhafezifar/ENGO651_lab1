import os

from flask import Flask, session, request, render_template, redirect, url_for, flash
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
        flash("Logged in successfully. You can now search the books in the blow form.")
        return redirect(url_for('search'))
    flash("Error: username and password doesn't match.")
    return redirect(url_for('index'))


@app.route("/register_form", methods=['GET'])
def register_form():
    return render_template("register.html")


@app.route("/register", methods=['POST'])
def register():
    username = request.form.get('uname').lower()
    password = request.form.get('password')
    result = db.execute(f"SELECT * from users where username='{username}'")
    if result.rowcount == 1:
        flash("Error: The entered username is taken. please try a different username.")
        return redirect(url_for('register_form'))

    db.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    db.commit()
    session['username'] = username
    flash("You are now registered and logged in successfully. You can now search the books in the blow form.")
    return redirect(url_for('search'))


@app.route("/login_test", methods=['GET'])
def login_test():
    if 'username' in session:
        return f"you are currently logged in as {session['username']}."
    return "Nobody is logged in :("


@app.route("/logout", methods=['GET'])
def logout():
    del session['username']
    flash("Logged out successfully.")
    return redirect(url_for('index'))


@app.route("/search", methods=['GET'])
def search():
    if 'username' not in session:
        flash("You are not logged in!")
        return redirect(url_for('index'))
    isbn = request.args.get('isbn')
    title = request.args.get('title')
    author = request.args.get('author')
    # print(isbn, title, author)
    if not (isbn or title or author):
        return render_template('search.html')

    results = db.execute(f"select * from books where isbn ILIKE '%{isbn}%' and title ILIKE '%{title}%' and author ILIKE '%{author}%'")
    result_list = []
    for r in results:
        result_list.append({'isbn': r[0], 'title': r[1], 'author': r[2], 'year': r[3]})
    return render_template('search.html', search_result=result_list, isbn=isbn, title=title, author=author)


@app.route("/book/<isbn>", methods=['GET'])
def book_page(isbn):
    if 'username' not in session:
        flash("You are not logged in!")
        return redirect(url_for('index'))

    results = db.execute(f"select * from books where isbn = '{isbn}'")
    if results.rowcount == 0:
        return "Book Not found!"
    book = results.first()

    return render_template('book_single.html', isbn=book[0], title=book[1], author=book[2], year=book[3])
