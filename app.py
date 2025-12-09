# Rafi Talukder Final Project
"""---------------------------------------------------------------------------------"""
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import requests
"""---------------------------------------------------------------------------------"""
app = Flask(__name__)
app.secret_key = "simplekey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book_catalogue.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
"""---------------------------------DATABASE------------------------------------------------"""
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    pages = db.Column(db.Integer)
    rating = db.Column(db.Float)
    isbn = db.Column(db.String(20))

with app.app_context():
    db.create_all()
"""------------------------------------LOGIN---------------------------------------------"""
USERNAME = "admin"
PASSWORD = "password"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        return "Invalid login"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
"""-----------------------------------PROTECTED HOME----------------------------------------------"""
@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    books = Book.query.all()
    return render_template("index.html", books=books)
"""--------------------------------------ADD BOOK-------------------------------------------"""
@app.route("/add", methods=["GET", "POST"])
def add():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        isbn = request.form["isbn"]
        res = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}").json()

        if "items" not in res:
            return "Book not found."

        info = res["items"][0]["volumeInfo"]
        new_book = Book(
            title=info.get("title", "Unknown"),
            author=", ".join(info.get("authors", ["Unknown"])),
            pages=info.get("pageCount", 0),
            rating=info.get("averageRating", 0),
            isbn=isbn
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("add.html")
"""-----------------------------------DELETE----------------------------------------------"""
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))
"""---------------------------------------------------------------------------------"""
if __name__ == "__main__":
    app.run()
