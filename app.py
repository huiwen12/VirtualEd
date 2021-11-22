import os
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
def home():
    """Show portfolio of stocks"""

    stocks = db.execute(
        "SELECT symbol, name, SUM(shares) AS share_sum FROM transactions WHERE user_id=? GROUP BY symbol HAVING share_sum>0", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

    total = cash
    for stock in stocks:
        stock['price'] = lookup(stock["symbol"])['price']
        total += stock["share_sum"]*stock['price']
        
    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])

def buy():
    """Buy shares of stock"""
    
    if request.method == "POST":
        
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol exists
        elif lookup(request.form.get("symbol")) == None:
            return apology("symbol does not exist", 400)

        # Ensure number of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        # Ensure number of shares is positive
        elif not request.form.get("shares").isdigit():
            return apology("number of is not a digit", 400)

        elif int(request.form.get("shares")) < 0:
            return apology("number of shares must be positive", 400)

        # Look up stock
        stock = lookup(request.form.get("symbol"))

        # Check user balance
        id = session["user_id"]
        account = db.execute("SELECT cash FROM users WHERE users.id=?;", id)

        # Return error if user cannot purchase stock
        if stock["price"]*int(request.form.get("shares")) > account[0]["cash"]:
            return apology("your balance is too low for this transaction", 403)

        # Insert into transaction table
        total = stock["price"]*int(request.form.get("shares"))
        db.execute("INSERT INTO transactions (user_id, name, price, symbol, shares, total) VALUES (?, ?, ?, ?, ?, ?);", 
                   id, stock["name"], stock["price"], stock["symbol"], int(request.form.get("shares")), total)

        # Deduct value from user's profile
        db.execute("UPDATE users SET cash = ? WHERE id = ?", account[0]["cash"] - total, id)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    
    stocks = db.execute("SELECT symbol, price, shares, time FROM transactions WHERE user_id = ?", session["user_id"])

    return render_template("history.html", stocks=stocks)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    if request.method == "POST":
        
        if not request.form.get("symbol"):
            return apology("no symbol submitted", 400)
        
        if lookup(request.form.get("symbol")) == None:
            return apology("corresponding stock does not exist", 400)

        return render_template("quoted.html", quote=lookup(request.form.get("symbol")))
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Check that password has special characters
        pwd = request.form.get("password")
        special_char = "@_!#$%^&*()<>?/\|}{~:"
        if not any(char in special_char for char in pwd):
            return apology("your password must include a special char.", 400)

        # Check that password has uppercase and lowercase letters
        if not any(char.isupper() for char in pwd):
            return apology("your password must include an uppercase letter.", 400)
        if not any(char.islower() for char in pwd):
            return apology("your password must include a lowercase letter.", 400)

        # Check that password has numbers
        if not any(char.isdigit() for char in pwd):
            return apology("your password must include a number.", 400)

        # Check that password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match confirmation", 400)

        # Ensure username does not already exist
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("invalid username", 400)

        # Insert new user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Check user account
    id = session["user_id"]
    account = db.execute("SELECT cash FROM users WHERE users.id=?;", id)

    if request.method == "POST":
        
        # Ensure that stock was selected
        if not request.form.get("symbol"):
            return apology("failed to select a stock", 403)
        
        # Ensure that user owns shares
        share = db.execute("SELECT SUM(shares) AS sum FROM transactions WHERE user_id = ? AND symbol = ?", 
                           id, request.form.get("symbol"))

        if share[0]["sum"] < int(request.form.get("shares")):
            return apology("you do not own enough shares", 400)

        # Ensure that number of shares to sell is positive
        elif int(request.form.get("shares")) < 0:
            return apology("number of shares must be positive", 403)

        # Look up stock
        stock = lookup(request.form.get("symbol"))

        # Insert into transaction table
        total = stock["price"]*int(request.form.get("shares"))
        db.execute("INSERT INTO transactions (user_id, name, price, symbol, shares, total) VALUES (?, ?, ?, ?, ?, ?);", 
                   id, stock["name"], stock["price"], stock["symbol"], -int(request.form.get("shares")), total)

        # Add value from user's profile
        db.execute("UPDATE users SET cash = ? WHERE id = ?", account[0]["cash"] + total, id)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        
        stocks = db.execute("SELECT symbol FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares)>0", id)

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
