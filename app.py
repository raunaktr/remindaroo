from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime
import time

app = Flask(__name__, root_path='app/')

# Custom secret_key
app.secret_key = "HR2410"

# Database connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "raunak"  # Enter your MySQL user
app.config["MYSQL_PASSWORD"] = "8089"  # Enter your MYSQL password
app.config["MYSQL_DB"] = "remindaroo_db"

# Initializing MySQL
mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def authenticator():
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]

        # verifying if user details exists in DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM r_user_details WHERE username = %s AND password= %s",
            (username, password),
        )

        # Fetching record and returning result
        auth = cursor.fetchone()

        # If user exists in DB
        if auth:
            # Create a session
            session["loggedin"] = True
            session["id"] = auth["id"]
            session["username"] = auth["username"]
            return redirect(url_for("view"))
        else:
            msg = "Incorrect username/password"
    return render_template("index.html", msg=msg)


@app.route("/logout")
def logout():
    # Removes session data
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)

    # redirects user to home page
    return redirect(url_for("authenticator"))


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
        and "mobile" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        mobile = request.form["mobile"]

        # verifying if the account already exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM r_user_details WHERE username=%s;", (username,))
        account = cursor.fetchone()

        # if account exists
        if account:
            msg = "Account already exists!"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address!"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers!"
        elif not username or not password or not email or not mobile:
            msg = "Please fill out the valid details"
        else:
            # Account does not exists, create a new account
            created_at = datetime.date.today()
            details = (username, password, email, created_at, mobile)
            cursor.execute(
                "INSERT INTO r_user_details(username, password, email, date, mobile) VALUES (%s,%s,%s,%s,%s)",
                details,
            )
            mysql.connection.commit()
            msg = "You have successfully registered!"
    elif request.method == "POST":
        # if form is empty
        msg = "Please fill all the details"
    return render_template("register.html", msg=msg)


@app.route("/home")
def view():
    # checking if the user is already signed_in
    if "loggedin" in session:
        return render_template("home.html", username=session["username"])

    # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


@app.route("/profile")
def profile():
    # check if user is loggedin
    if "loggedin" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM r_user_details WHERE id=%s", [session["id"]])
        account = cursor.fetchone()

        # show user details
        return render_template("profile.html", account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


def rem_id_generator():
    rem_value = str(time.time())
    return rem_value


@app.route("/set_reminder", methods=["GET", "POST"])
def set_reminder():
    # check if user is loggedin
    if "loggedin" in session:
        value = "Set a new"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM r_user_details WHERE id=%s", [session["id"]])
        reminder = cursor.fetchone()
        print(session["id"])

        msg = ""
        if (
            request.method == "POST"
            and "subject" in request.form
            and "description" in request.form
            and "r_date" in request.form
        ):
            user_id = session["id"]
            rem_id = rem_id_generator()
            r_date = request.form["r_date"]
            subject = request.form["subject"]
            status = "TRUE"
            desc = request.form["description"]
            details = (user_id, rem_id, subject, desc, status, r_date)

            cursor.execute(
                "INSERT INTO r_app_details(id,rem_id,subject,description,status,r_date) VALUES (%s,%s,%s,%s,%s,%s)",
                details,
            )
            mysql.connection.commit()
            msg = "Reminder is set!"
            return render_template("reminder.html", msg=msg)
        elif request.method == "POST":
            msg = "Please fill all the details"
            return render_template("reminder.html", msg=msg)
        return render_template("reminder.html", reminder=reminder, value=value)
    # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


@app.route("/view_reminder", methods=["GET", "POST"])
def view_reminder():
    # check if the user is logged
    if "loggedin" in session:
        value = "View"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM r_app_details WHERE id=%s", [session["id"]])
        records = cursor.fetchall()
        print(session["id"])
        msg = ""

        return render_template("reminder_extras.html", data=records, value=value)
    # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


@app.route("/edit_reminder", methods=["GET", "POST"])
def edit_reminder():
    # check if the user is logged
    if "loggedin" in session:
        value = "Modify"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM r_app_details WHERE id=%s", [session["id"]])
        reminder = cursor.fetchall()
        print(session["id"])

        msg = ""
        # cursor.execute("SELECT * FROM r_app_details WHERE id=%s", [session["id"]])
        # rem = cursor.fetchall()

        if (
            request.method == "POST"
            and "subject" in request.form
            and "description" in request.form
            and "r_date" in request.form
        ):

            print([session["id"]])

            user_id = [session["id"]]
            r_date = request.form["r_date"]
            subject = request.form["subject"]
            status = "TRUE"
            desc = request.form["description"]

            details = (user_id, subject, desc, status, r_date)
            cursor.execute(
                "UPDATE r_app_details SET (%s,%s,%s,%s,%s)", details,
            )
            mysql.connection.commit()
            msg = "successfully edited!"
            return render_template("reminder_extra.html", msg=msg)
        elif request.method == "POST":
            msg = "Please fill all the details to be edited."
            return render_template("reminder_extra.html", msg=msg)
        return render_template("reminder_extras.html", data=reminder, value=value)
    # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


@app.route("/delete_reminder", methods=["GET", "POST"])
def delete_reminder():
    # check if the user is logged
    if "loggedin" in session:
        value = "Delete"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute("SELECT * FROM r_user_details WHERE id=%s", [session['id']])
        cursor.execute("SELECT * FROM r_app_details WHERE id=%s", [session["id"]])
        records = cursor.fetchall()
        msg = ""

        if request.method == "POST" and request.form:
            print("hello")

        return render_template("reminder_extras.html", data=records, value=value)
    # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


@app.route("/disable_reminder", methods=["GET", "POST"])
def disable_reminder():
    # check if the user is logged
    if "loggedin" in session:
        value = "Disable"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute("SELECT * FROM r_user_details WHERE id=%s", [session['id']])
        cursor.execute("SELECT * FROM r_app_details WHERE id=%s", [session["id"]])
        records = cursor.fetchall()
        msg = ""
        return render_template("reminder_extras.html", data=records, value=value)
        # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


@app.route("/enable_reminder", methods=["GET", "POST"])
def enable_reminder():
    # check if the user is logged
    if "loggedin" in session:
        value = "Enable"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute("SELECT * FROM r_user_details WHERE id=%s", [session['id']])
        cursor.execute("SELECT * FROM r_app_details WHERE id=%s", [session["id"]])
        records = cursor.fetchall()
        msg = ""
        return render_template("reminder_extras.html", data=records, value=value)
        # User is not loggedin redirect to login page
    return redirect(url_for("authenticator"))


if __name__ == "__main__":
    app.run(port=5000)
