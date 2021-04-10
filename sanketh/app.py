# main.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random
import time
import threading

app = Flask(__name__)

app.secret_key = 'skete'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'asdfghjkl$123'
app.config['MYSQL_DB'] = 'stock_simulator_db'

# Intialize MySQL
mysql = MySQL(app)


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
        q1 = 'SELECT cid FROM customer WHERE cname = %s'
        cursor.execute(q1, [username])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO customer VALUES (NULL, %s, %s, %s,%s)',(username, phone, address, dob))
            cursor.execute(q1, [username])
            cid = cursor.fetchone()
            cursor.execute('INSERT INTO logincheck VALUES (%s,%s)',(cid['cid'], password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    elif request.method == 'GET':
        msg = 'Please enter details in all the fields'
    return render_template('register.html', msg=msg)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        q1 = 'SELECT cid FROM customer WHERE cname = %s'
        cursor.execute(q1, [username])
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
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE cid = %s',(session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/buy', methods=['GET', 'POST'])
def book():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    q1 = 'select stock.sid, company.comid, company.comname, company.category, company.cost, stock.availability from company left join stock on company.comid=stock.comid where stock.availability > 0;'
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
        sid = request.form['buy']
        cursor.execute('INSERT INTO bookings VALUES (NULL,%s,%s)',(int(sid), int(session['id'])))
        mysql.connection.commit()
        q1 = 'SELECT bookingid FROM bookings WHERE sid= %s AND cid = %s ORDER BY bookingid DESC'
        cursor.execute(q1, (sid, session['id']))
        book_id = cursor.fetchone()
        cursor.execute('UPDATE stock SET availability= stock.availability - 1 WHERE sid=%s', (sid,))
        mysql.connection.commit()
    return render_template('buy.html', available=available, pk=book_id, msg=msg)


@app.route('/sell', methods=['GET', 'POST'])
def sell():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    q1 = 'select bookings.bookingid, company.comid, company.comname, company.category, stock.sid, company.cost from bookings left join stock on bookings.sid=stock.sid left join company on stock.comid=company.comid where bookings.cid = %s'
    cursor.execute(q1, [session['id']])
    bookings = cursor.fetchall()
    done = dict()
    msg = " "
    i = 1
    for items in bookings:
        done[i] = items
        i = i + 1
    if request.method == 'POST':
        bid = request.form['sell']
        print("BID", bid)
        cursor.execute("SELECT sid from bookings where bookingid = %s", [bid])
        sid = cursor.fetchone()
        print(sid)
        if sid != None:
            cursor.execute(
                'UPDATE stock SET availability = stock.availability + 1 WHERE sid = %s', (sid['sid'],))
            mysql.connection.commit()
            cursor.execute('DELETE FROM bookings WHERE bookingid = %s', (bid,))
            mysql.connection.commit()
            msg = "Successfully sold"
        else:
            msg = "Some error occured, please try again"
    return render_template('sell.html', msg=session['username'], bookings=done, mesg=msg)


if __name__ == "__main__":
    def thread_function():
        while(1):
            with app.app_context():
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                n = random.randint(-10,10)
                if(n>0):
                    s = str(n)
                    cursor.execute('UPDATE company SET cost = cost + %s',[s])
                else:
                    s = str(n*(-1))
                    cursor.execute('UPDATE company SET cost = cost - %s',[s])
                mysql.connection.commit()
                time.sleep(1)

    x = threading.Thread(target=thread_function, args=())
    x.start()

    app.run(port=5050, debug=1)