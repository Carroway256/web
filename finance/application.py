#export API_KEY=pk_7f62aca6ff9447bb86b887ad677e3374
import os
import datetime

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
    if request.method=="GET":
        sess = int(session["user_id"])
        db = SQL("sqlite:///finance.db")
        b=db.execute('SELECT DISTINCT stock_symbol FROM boughts WHERE persons_id=(?)',sess)
        number=[]
        a=db.execute("SELECT * FROM boughts WHERE persons_id=(?)",sess)
        for i in range(len(b)):
            print(b[i]["stock_symbol"])
            number.append(0)
            for rows in a:
                if(rows["stock_symbol"]==(b[i]["stock_symbol"])):
                    number[i]=number[i]+rows["amount"]
        for i in range(0,len(b)) :
                b[i]["amount"]=number[i]
                b[i]["price"]=lookup(b[i]["stock_symbol"])["price"]
                b[i]["total"]= b[i]["price"]* b[i]["amount"]
        return render_template("index.html",table=b)


    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method =="GET" :
        return render_template("buy.html")
    if request.method =="POST":
        amount=int(request.form.get("amount"))
        stocks=request.form.get("symbol")
        stocks=stocks.casefold()
        if amount <=0 :
            return apology("number of shares must be positive integer")
        dicts=lookup(stocks)
        per_one=dicts["price"]
        price=amount * per_one
        sess = int(session["user_id"])
        curent_cash=db.execute("SELECT cash FROM users WHERE id=(?)",sess)
        if price>curent_cash[0]["cash"]:
            return apology("too little money")
        time=datetime.datetime.now()
        cash_after=curent_cash[0]["cash"]-price
        yes=1
        db.execute("INSERT INTO boughts(persons_id,stock_symbol,amount,time,bought,cash_after,price) VALUES(?,?,?,?,?,?,?)",sess,stocks,amount,time,yes,cash_after,per_one)
        db.execute('UPDATE users SET cash=(?) WHERE id=(?);',cash_after,sess)
        #db.execute("CREATE TABLE boughts(persons_id int,stock_symbol CHAR(5),amount int,time DATETIME,bought BOOL);")
        return render_template("index.html")
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    if request.method =="GET" :
        sess = session["user_id"]
        return render_template("try.html",sess=sess)
    return apology("TODO")


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
        if len(rows) != 1 :
            return apology("invalid username", 403)
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        quotee=(request.form.get("quote"))
        dbquote={}
        dbquote=lookup(quotee)
        return render_template("quoted.html", dbquote=dbquote)
@app.route("/quoted", methods=["GET"])
def quoted():
    if request.method == "GET":
        return render_template("quoted.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
            password=(request.form.get("password"))
            password_2=(request.form.get("password_again"))
            if not request.form.get("username"):
                return apology("must provide username", 403)

            # Ensure password was submitted
            elif not request.form.get("password"):
                return apology("must provide password", 403)

            elif password!=password_2 :
                        return apology("passwords dont match")

            hashpassword=generate_password_hash(request.form.get("password"))
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

            if len(rows) !=0 :
                return apology("username taken", 403)

            else:
                db.execute("INSERT INTO users(username,hash)VALUES(?,?)",request.form.get("username"),hashpassword,)
    else:
        return render_template("register.html")

    return apology("registration complete")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET" :
        return render_template("sell.html")
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
