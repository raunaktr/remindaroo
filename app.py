from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Custom secret_key
app.secret_key = 'HR2410'

# Database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'raunak'
app.config['MYSQL_PASSWORD'] = '8089'
app.config['MYSQL_DB'] = 'remindaroo_db'

# Initializing MySQL
mysql = MySQL(app)


@app.route('/login', methods=['GET', 'POST'])
def authenticator():
    msg = ''
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form['username']
        password = request.form['password']

        # verifying if user details exists in DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM remindaroo_user_details WHERE username = %s AND password= %s', (username, password))

        # Fetching record and returning result
        auth = cursor.fetchone()

        # If user exists in DB
        if auth:
            # Create a session
            session['loggedin'] = True
            session['id'] = auth['id']
            session['username'] = auth['username']
            return redirect(url_for('view'))
        else:
            msg = 'Incorrect username/password'
    return render_template('index.html', msg=msg)


@app.route('/logout')
def logout():
    # Removes session data
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # returns user to home page
    return redirect(url_for('authenticator'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # verifying if the account already exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM remindaroo_user_details WHERE username=%s;", (username,))
        account = cursor.fetchone()

        # if account exists
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the valid details'
        else:
            # Account does not exists, create a new account
            details = (username, password, email)
            cursor.execute("INSERT INTO remindaroo_user_details VALUES (NULL, %s,%s,%s)", details)
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # if form is empty
        msg = "Please fill all the details"
    return render_template('register.html', msg=msg)


@app.route('/home')
def view():
    # checking if the user is already signed_in
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    # if user not logged in, then redirecting back to sign in page
    return redirect(url_for('authenticator'))


@app.route('/profile')
def profile():
    # check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM remindaroo_user_details WHERE id=%s', [session['id']])
        account = cursor.fetchone()

        # show user details
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('authenticator'))


if __name__ == '__main__':
    app.run(port=5000)