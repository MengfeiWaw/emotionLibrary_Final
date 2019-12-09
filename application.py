import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///emotionlibrary.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        print(name)
        if not name:
            return apology("You must type in a username")
        # names = db.execute("SELECT username FROM users")
        names = db.execute("SELECT username FROM users WHERE username = :username", username = name)
        print(names)
        # for i in range(len(names)):
        #     if name == names[i]["username"]:
        #         return apology("This username already exists")
        if len(names) != 0:
            return apology("This username already exists")
        password = request.form.get("password")
        if not password:
            return apology("You must type in a password")
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("You must type in confirmation")
        if confirmation != password:
            return apology("The passwords do not match")
        email = request.form.get("email")
        if not email:
            return apology("You must type in an email")
        userid = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = name, hash = generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = userid

        # flash("Registered!")

        # Redirect user to home page
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/myspace")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/myspace", methods=["GET", "POST"])
@login_required
def myspace():
    if request.method == "POST":
        first = db.execute("SELECT * FROM firstcard")
        if not first:
            return render_template("firstcard_front.html")
        else:
            return render_template("card_front.html")
    else:
        return render_template("myspace.html")

@app.route("/firstcard_front", methods=["GET", "POST"])
@login_required
def firstcard_front():
    if request.method == "POST":
        hostschool = request.form.get("school")
        if not hostschool:
            return apology("you must select a school")
        place = request.form.get("place")
        if not place:
            return apology("you must type in a place")
        feeling = request.form.get("feeling")
        if not feeling:
            return apology("you must type in a feeling")
        reason = request.form.get("reason")
        if not reason:
            return apology("you must type in a reason")
        wonder = request.form.get("need")
        if not wonder:
            return apology("you must type in your needs")
        a = db.execute("INSERT INTO firstcard (user_id, hostschool, place, feeling, reason, wonder) VALUES (:user_id, :hostschool, :place, :feeling, :reason, :wonder)", user_id = session["user_id"], hostschool = hostschool, place = place, feeling = feeling, reason = reason, wonder = wonder)
        print(a)
        return render_template("card_back.html")
    else:
        return render_template("firstcard_front.html")

@app.route("/card_back", methods=["GET", "POST"])
@login_required
def card_back():
    if request.method == "GET":
        no = db.execute("SELECT no FROM firstcard WHERE user_id = :user_id", user_id = session["user_id"])
        first = db.execute("SELECT * FROM firstcard")
        if not no and not first:
            return render_template("firstcard_front.html")
        elif not no:
            return render_template("card_front.html")
        else:
            return render_template("card_back.html")
    else:
        cardno = db.execute("SELECT * FROM card")
        if not cardno:
            return render_template("firstcard_front.html")
        else:
            return render_template("card_front.html")

@app.route("/card_instructions")
@login_required
def card_instructions():
    return render_template("card_instructions.html")

@app.route("/card_back2")
@login_required
def card_back2():
    return render_template("card_back2.html")

@app.route("/card_back3")
@login_required
def card_back3():
    return render_template("card_back3.html")

@app.route("/card_back4")
@login_required
def card_back4():
    return render_template("card_back4.html")

@app.route("/card_finished")
@login_required
def card_card_finished():
    return render_template("card_finished.html")

@app.route("/browse")
@login_required
def browse():
    return render_template("browse.html")

@app.route("/bookpage_front")
@login_required
def bookpage_front():
    cards = db.execute("SELECT * FROM firstcard")
    print(cards)
    return render_template("bookpage_front.html", cards = cards)

@app.route("/bookpage_back")
@login_required
def bookpage_back():
    return render_template("bookpage_back.html")

@app.route("/search")
@login_required
def search():
    return render_template("search.html")

@app.route("/search_results")
@login_required
def search_results():
    return render_template("search_results.html")

@app.route("/card_front", methods=["GET", "POST"])
@login_required
def card_front():
    if request.method == "POST":
        text = request.form.get("txt_comments")
        if not text:
            return apology("you must type in some texts")
        else:
            db.execute("INSERT INTO card (user_id, diary) VALUES (:user_id, :text)", user_id = session["user_id"], text = text)
            return render_template("card_back.html")
    else:
        return render_template("card_front.html")

@app.route("/sunnyroom")
@login_required
def sunnyroom():
    return render_template("sunnyroom.html")

@app.route("/rainyroom")
@login_required
def rainyroom():
    return render_template("rainyroom.html")

@app.route("/hand_waiting")
@login_required
def hand_waiting():
    return render_template("hand_waiting.html")

@app.route("/video")
def video():
    return render_template("video.html")

@app.route("/hand_holding")
@login_required
def hand_holding():
    return render_template("hand_holding.html")
