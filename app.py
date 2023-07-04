import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_mail import Mail, Message
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import login_required
from mailconfig import mail_username, mail_password

# Configure application
app = Flask(__name__)

# Configue mail application
app.config['MAIL_SERVER']='smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

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
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Must provide username')
            return render_template("login.html")
            
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Must provide password')
            return render_template("login.html")
  
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Invalid username and/or password')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash('Logged in!')
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

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
@login_required
def index():
    return render_template("index.html")
        
@app.route("/brewing")
@login_required
def brewing():
    return render_template("brewing.html")

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        email = request.form.get("email")
        message = request.form.get("subject")

        print(f"Name: {fname}\nLast name: {lname}\ne-mail: {email}\nMessage: {message}")

        msg = Message(subject=f"Contact form message from {fname} {lname}:", sender = mail_username, recipients = ['pierre_bruyninckx@hotmail.com'])
        msg.body = f"Name: {fname}\nLast name: {lname}\ne-mail: {email}\nMessage: {message}"
        mail.send(msg)

        flash('Form sent.')
        return render_template("contact.html")

    else:
        return render_template("contact.html")

@app.route("/mybeans")
@login_required
def mybeans():
    return render_template("mybeans.html")

@app.route("/reviews")
@login_required
def reviews():
    return render_template("reviews.html")