# main.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import string
import random

app = Flask(__name__)

app.secret_key = 'skete'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'asdfghjkl$123'
app.config['MYSQL_DB'] = 'stock_simulator_db'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/viewbook', methods=['GET', 'POST'])
def viewbook():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    q1 = 'SELECT * FROM bookings WHERE cid =%s'
    cursor.execute(q1, (session['id'],))
    bookings = cursor.fetchall()
    done = dict()

    msg = " "
    i = 1
    for items in bookings:
        done[i] = items
        i = i + 1

    if request.method == 'POST':

        bid = request.form['cancel']
        print("BID", bid)
        cursor.execute("SELECT pid from bookings where bookingid=%s", (bid,))
        pid = cursor.fetchone()
        print(pid)
        if pid != None:
            cursor.execute(
                'UPDATE packages SET pavailability= packages.pavailability+1 WHERE pid=%s', (pid['pid'],))
            mysql.connection.commit()
            cursor.execute('DELETE FROM bookings WHERE bookingid=%s', (bid,))
            mysql.connection.commit()

            msg = "Successfully cancelled "
        else:
            msg = "Some error occured, please try again"

    return render_template('viewbook.html', msg=session['username'], bookings=done, mesg=msg)


@app.route('/book', methods=['GET', 'POST'])
def book():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    q1 = 'SELECT * FROM packages WHERE pavailability>0 '
    cursor.execute(q1)
    pkg = cursor.fetchall()
    msg = ""
    available = dict()
    book_id = ""

    i = 1
    for items in pkg:
        available[i] = items
        i = i + 1

    if request.method == 'POST':

        pid = request.form['book']

        q1 = 'SELECT bookingid FROM bookings WHERE pid= %s AND cid = %s'
        cursor.execute(q1, (pid, session['id']))
        book_id = cursor.fetchall()
        # print(book_id)

        if len(book_id) >= 1:
            msg = "There is already a booking on this package."

        else:
            cursor.execute('INSERT INTO bookings VALUES (NULL,%s,%s)',
                           (int(pid), int(session['id'])))
            mysql.connection.commit()
            q1 = 'SELECT bookingid FROM bookings WHERE pid= %s AND cid = %s ORDER BY bookingid DESC'
            cursor.execute(q1, (pid, session['id']))
            book_id = cursor.fetchone()
            # print(book_id)
            cursor.execute(
                'UPDATE packages SET pavailability= packages.pavailability-1 WHERE pid=%s', (pid,))
            mysql.connection.commit()

    return render_template('book.html', available=available, pk=book_id, msg=msg)


@app.route('/profile')
def profile():

    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE cid = %s',
                       (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        q1 = 'SELECT cid FROM customer WHERE cname = %s AND pno = %s'
        cursor.execute(q1, (username, phone))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO customer VALUES (NULL, %s, %s, %s,%s)',
                           (username, phone, address, dob,))
            cursor.execute(q1, (username, phone))

            cid = cursor.fetchone()
            cursor.execute('INSERT INTO logincheck VALUES (%s,%s)',
                           (cid['cid'], password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


@app.route('/', methods=['GET', 'POST'])
def login():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        q1 = 'SELECT cid FROM customer WHERE cname = %s AND pno = %s'
        cursor.execute(q1, (username, phone))
        cid = cursor.fetchone()

        if cid:

            cursor.execute(
                'SELECT * FROM logincheck WHERE cid = %s AND pwd = %s', (cid['cid'], password,))

            account = cursor.fetchone()
            cursor.execute(
                'SELECT * FROM customer WHERE cid = %s', (cid['cid'],))

            customer = cursor.fetchone()

            if account:

                session['loggedin'] = True
                session['id'] = account['cid']
                session['username'] = customer['cname']
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect username/password!'

        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


if __name__ == "__main__":
    app.run(port=5050, debug=1)
