import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from flask_mail import Mail, Message
import json
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import login_required
from mailconfig import mail_username, mail_password

# Configure application
app = Flask(__name__)
app.debug == True

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

        #   Add a new row to the coffee_use table with user_id set to the new id and other values set to default.
        today = datetime.date.today()
        db.execute("INSERT INTO coffee_use VALUES (?, ?, 0, 0, ?, 0, 0, 0, 0, 0, 0);", id, today, None)

        #   Give confirmation to the user that he has been successfully been registered.
        flash('Registration succesfull!')
        return redirect("/")
        
    else:
        return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    id = session.get("user_id")
    if request.method == "POST":
        #   Get form data
        cups = int(request.form.get('cups'))
        bean = request.form.get('bean')
        dosage = int(request.form.get('dosage'))
        method = request.form.get('method')
        today = datetime.date.today()

        #   Calculate the amount of coffee ground used
        coffee_ground = cups * dosage

        #   Insert the data in the coffee use database
        db.execute("INSERT INTO coffee_use (user_id, date, cups, bean, "+method+", coffee_ground) VALUES (?, ?, ?, ?, 1, ?);",id, today, cups, bean, coffee_ground)
        # Also diminish the relevant bean stock
            # First check if the amount of beans used is not bigger than the amount of beans that was available. If so, set the stock to 0.
        current_amount_dict = db.execute("SELECT amount FROM mybeans WHERE user_id == ? AND bean_name == ?;", id, bean)
        current_amount = current_amount_dict[0]['amount']
        if current_amount - coffee_ground < 0:
            db.execute("UPDATE mybeans SET amount = 0 WHERE user_id == ? AND bean_name == ?;", id, bean)
        else:
            db.execute("UPDATE mybeans SET amount = amount - ? WHERE user_id == ? AND bean_name == ?;", coffee_ground, id, bean)

        #Redirect to the index page (refresh)
        flash("Usage added!")
        return redirect("/")

    else:
        ##  Charts data
        #  Fecth the data for the bar chart representing the stock of the different beans
        chart_data_stock = db.execute("SELECT bean_name, amount FROM mybeans WHERE user_id == ?;", id)
        #print(f"Type: {chart_data_stock}")

        #   Fetch data for the line chart representing the amount of coffee cups per day
        line_chart_data = db.execute("SELECT date, SUM(cups) as cups FROM coffee_use WHERE user_id == ? AND date != 'None' GROUP BY date", id)
        print(f"Line chart data: {line_chart_data}")
        
        ##  'Register use' form data
        #   Fetch all the bean names the user has in its database. Load all these names in the 'add coffee use' option form.
        name_options = db.execute("SELECT bean_name FROM mybeans WHERE user_id == ?", id)
        #print(f"Options: {name_options}")

        ## Favorites data
        # Fetch the favorite beans, type of beans and brewing method from the relevant tables in the database.
        favor_bean_dict= db.execute("SELECT bean FROM (SELECT bean, COUNT(bean) as n FROM coffee_use WHERE user_id == ? AND bean != 'None' GROUP BY bean ORDER BY n DESC LIMIT 1)", id)
        favor_bean = favor_bean_dict[0]['bean']
        favor_type_dict = db.execute("SELECT type FROM (SELECT type, COUNT(type) as n FROM mybeans WHERE user_id == ? AND type != 'None' GROUP BY type ORDER BY n DESC LIMIT 1)", id)
        favor_type = favor_type_dict[0]['type']
        favor_method_dict = db.execute("SELECT SUM(espresso) as Espresso, SUM(moka) as Moka, SUM(french_press) as French_press, SUM(v60) as V60, SUM(chemex) as Chemex, SUM(siphon) as Siphon FROM coffee_use WHERE user_id = ?", id)
        #   Loop through the dict to get the highest value
        m = max(favor_method_dict[0].values())

        favorite_methods = []
        for key in favor_method_dict[0]:
            if favor_method_dict[0][key] == m:
                favorite_methods.append(key)
        
        return render_template("index.html", chart_data_stock = chart_data_stock, name_options = name_options, line_chart_data = line_chart_data, favor_bean = favor_bean, favor_type = favor_type, favor_method = favorite_methods)
        
@app.route("/brewing")
@login_required
def brewing():
    #   Redirect the user to the brewing methods page
    return render_template("brewing.html")

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    """Send email with the filled in contact form"""
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

    #Render the contact page
    else:
        return render_template("contact.html")

@app.route("/mybeans", methods=["GET", "POST"])
@login_required
def mybeans():
    """If user wants to add new beans, add all the required fields to the 'mybeans' table in the database"""
    #   First, get the user id of the user in the current session
    id = session.get("user_id")
    if request.method == "POST":
        #   Get all the information from the form and perform some checks on the data.
        ## Required info
        name = request.form.get("BeanName")

        ##  Check that this beans isn't in the database yet
        name_check = db.execute("SELECT * FROM mybeans WHERE user_id == ? AND bean_name == ?", id, name)
        if len(name_check) != 0:
            flash("This coffee bean already exists in your table!")
            return redirect("/mybeans")

        origin = request.form.get("BeanOrigin")
        roastDate = request.form.get("RoastDate")
        expiryDate = request.form.get("ExpiryDate")
        retailer = request.form.get("Retailer")
        stock = request.form.get("Stock")
        ## Optional info
        type = request.form.get("Type")
        roast = request.form.get("Roast")
        notes = request.form.get("Notes")
        acidity = request.form.get("Acidity")
        CR_review = request.form.get("CR_Review")
        description = request.form.get("Description")
        comments = request.form.get("Comments")

        ## Print all the info for verification
        print(f"Name: {name}\nOrigin: {origin}\nRoast date: {roastDate}\nExpiry date: {expiryDate}\nRetailer: {retailer}\nStock: {stock}\nType: {type}\nRoast: {roast}\nNotes: {notes}\nAcidity: {acidity}\nCR Review: {CR_review}\nDescription: {description}\nComments: {comments}\n")

        ## Send all the info to the mybeans table in the database.
        db.execute("INSERT into mybeans (user_id, bean_name, origin, roast_date, expiry_date, retailer, amount, type, roasting_level, notes, acidity, CR_review, description, comments) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", id, name, origin, roastDate, expiryDate, retailer, stock, type, roast, notes, acidity, CR_review, description, comments)
        
        
        flash('Bean information added')
        return redirect("/mybeans"), 200

    # Else, redirect the user to the my beans overview page

    else:
        # When loading this page, update the table in this HTML page with the latest data for the beans.
        # Create a list of dictionaries with the fields required for the table on the html page: bean name, origin, roast date, expiry date, retailer, and the amount in stock.+
        table_data = db.execute("SELECT bean_name, type, origin, roast_date, expiry_date, retailer, amount FROM mybeans WHERE user_id == ? GROUP BY bean_name", id)
        # print(table_data)

        #  Also add the data for the charts from the database.
        chart_data_type = db.execute("SELECT type, COUNT(type) as n FROM mybeans WHERE user_id == ? GROUP BY type;", id)
        chart_data_origin = db.execute("SELECT origin, COUNT(type) as n FROM mybeans WHERE user_id == ? GROUP BY origin;", id)
        print(f"Type: {chart_data_type}")
        print(f"Origin: {chart_data_origin}")
        return render_template("mybeans.html", beans_data = table_data, chart_data_type = chart_data_type, chart_data_origin = chart_data_origin)

@app.route("/ajaxfile", methods=["GET", "POST"])
@login_required
def ajaxfile():
    #   Get id of the user in the current session
    id = session.get("user_id")
    #   If a request is made to get detailed information, gather all the required info from the selected bean
    if request.method == "POST":
        detailedBeanName = request.form.get("name")
        print(f"Detail of {detailedBeanName}: ...")

        ##  Get the detailed information for that bean from the database
        detailedInfo = db.execute("SELECT bean_name, type, origin, roasting_level, notes, acidity, CR_review, description, comments FROM mybeans WHERE user_id == ? AND bean_name == ?", id, detailedBeanName)
        print(f"Detailed info: {detailedInfo}")
        return jsonify({'htmlresponse': render_template("details.html",beans_detailed_data = detailedInfo)})


@app.route("/addstock", methods=["GET", "POST"])
@login_required
def addstock():
    id = session.get("user_id")
    if request.method == "POST":
        #   Get data from form
        target_bean = request.form.get("BeanName")
        amount_to_add = request.form.get("stock")



        #   Update the stock in the database
        db.execute("UPDATE mybeans SET amount = ((SELECT amount FROM mybeans WHERE bean_name == ? AND user_id == ?) + ?) WHERE bean_name == ? AND user_id == ?", target_bean, id, amount_to_add, target_bean, id)

        print(f"Bean: {target_bean}\nTo add: {amount_to_add}")
        flash("Stock successfully added!")
        return redirect("/mybeans")
    else:
        return redirect("/mybeans")

@app.route("/reviews")
@login_required
def reviews():
    return render_template("reviews.html")

@app.route("/espresso")
@login_required
def espresso():
    return render_template("espresso.html")