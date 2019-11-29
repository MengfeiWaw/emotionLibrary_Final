import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    symbol_names = db.execute("SELECT symbol, SUM(shares) AS shares FROM history WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0", user_id = session["user_id"])
    # print(symbol_names)
    grandtotal = 0
    for row in symbol_names:
        q = lookup(row["symbol"])
        row["price"] = q["price"]
        row["name"] = q["name"]
        rowtotal = row["price"] * row["shares"]
        grandtotal += rowtotal
        row["total"] = usd(rowtotal)
        row["price"] = usd(q["price"])
    temp = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
    cash_left = temp[0]["cash"]
    grandtotal += cash_left
    # print(cash_left)
    # row["total"] = usd(row["total"])
    return render_template("index.html", symbol_names = symbol_names, cash_left = usd(cash_left), grandtotal = usd(grandtotal))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please type in a symbol")
        price = lookup(symbol)
        if not price:
            return apology("Invalide symbol")
        price_value = price["price"]
        # print(price_value)
        # print(type(price_value))
        shares_value = request.form.get("shares")
        if not shares_value:
            return apology("Please type in shares")
        if not shares_value.isdigit():
            return apology("Please type in a valid integer")
        else:
            shares = (int)(shares_value)
        # print(shares)
        # print(type(shares))
        if shares <= 0:
            return apology("Please type in a positive integer")
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
        print(cash)
        cash_value = cash[0]["cash"]
        print(cash_value)
        print(type(cash_value))
        #check if cash is enough to pay for shares
        if cash_value >= price_value*shares:
            #insert buying info to table
            db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id = session["user_id"], symbol = symbol, shares = shares, price = price_value)

            db.execute("UPDATE users SET cash = :cash_after WHERE id = :user_id", cash_after = cash_value - price_value*shares, user_id = session["user_id"])
        else:
            return apology("Not enough cash")
        flash("Bought successfully!")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    historydata = db.execute("SELECT * FROM history WHERE user_id = :user_id ORDER BY time DESC", user_id = session["user_id"])
    for r in historydata:
        p = r["price"]
        r["price"] = usd(p)
    # print(historydata)
    return render_template("history.html", historydata = historydata)
    # return apology("TODO")


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
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please input a symbol")
        price = lookup(symbol)
        price_usd = usd(price["price"])
        if not price:
            return apology("Invalide symbol")
        else:
            return render_template("quoted.html", price = price, price_usd = price_usd)


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
        if confirmation != password:
            return apology("The passwords do not match")
        userid = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = name, hash = generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = userid

        # flash("Registered!")

        # Redirect user to home page
        return redirect("/login")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Register user"""
    if request.method == "GET":
        return render_template("changepassword.html")
    else:
        oldpassword = request.form.get("oldpassword")
        if not oldpassword:
            return apology("Please type in old password")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])
        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("oldpassword")):
            return apology("invalid oldpassword")
        newpassword = request.form.get("newpassword")
        if not newpassword:
            return apology("Please type in new password")
        confirmation = request.form.get("confirmation")
        if confirmation != newpassword:
            return apology("The New passwords do not match")
        db.execute("UPDATE users SET hash = :password_hash WHERE id =:user_id", password_hash = generate_password_hash(newpassword), user_id = session["user_id"])
        flash("Change password successfully!")
        return redirect("/")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please type in a symbol")
        match = db.execute("SELECT symbol FROM history WHERE symbol = :symbol AND user_id =:user_id", symbol = symbol, user_id = session["user_id"])
        if not match:
            return apology("You have no share/invalide symbol")
        shares_value = request.form.get("shares")
        if not shares_value:
            return apology("Please type in a number")
        if not shares_value.isdigit():
            return apology("Please type in an integer")
        else:
            shares = (int)(shares_value)
        shares_exist = db.execute("SELECT SUM(shares) AS sum_shares FROM history WHERE symbol = :symbol AND user_id =:user_id GROUP BY symbol", symbol = symbol, user_id = session["user_id"])
        shares_exist_value = shares_exist[0]["sum_shares"]
        if shares > shares_exist_value:
            return apology("No enough shares")
        if shares <= 0:
            return apology("Please type in a positive integer")
        #update the history table
        price = lookup(symbol)
        price_value = price["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
        cash_value = cash[0]["cash"]
        cash_after = cash_value + price_value * shares
        db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id = session["user_id"], symbol = symbol, shares = - shares, price = price_value)
        db.execute("UPDATE users SET cash = :cash_after WHERE id = :user_id", cash_after = cash_after, user_id = session["user_id"])

        flash("Sold successfully!")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
