import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///coffee.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ...
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username == ?;", username)

        #   Check  the username
        if username == "" or username.isspace() == 1:
            flash('Please fill in a username')
            return 400

        elif len(rows) != 0:
            flash('This username is already in use. Please choose another one.')
            return 400

        #   Check the password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password == "" or password.isspace() == 1:
            flash('Please fill in a valid password')
            return 400
            

        elif password != confirmation:
            flash('Passwords do not match')
            return 400

        #   Hash the password
        pw_hash = generate_password_hash(password)

        #   Add the login details to the user database and redirect to the login page.

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, pw_hash)

        #   Get the id of the user and log the user in.
        id_list = db.execute("SELECT id FROM users WHERE username == ?;", username)
        id = id_list[0]["id"]
        print("this id", id)
        session["user_id"] = id

        #   Give confirmation to the user that he has been successfully been registered.

        flash('Registration succesfull!')
        return redirect("/")
        
    else:
        return render_template("register.html")


@app.route("/")
##@login_required##
def index():
    return render_template("index.html")
        
@app.route("/brewing")
##@login_required
def brewing():
    return render_template("brewing.html")