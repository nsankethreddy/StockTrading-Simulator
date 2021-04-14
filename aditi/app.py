# main.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import string
import random
import time
import threading

app = Flask(__name__)

app.secret_key = 'skete'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
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
            cursor.execute('INSERT INTO customer VALUES (5000.0, %s, %s, %s,%s)',(username, phone, address, dob))
            cursor.execute(q1, [username])
            cid = cursor.fetchone()
            cursor.execute('INSERT INTO logincheck VALUES (%s,%s)',(cid['cid'], password))
            mysql.connection.commit()
            cursor.execute('INSERT INTO balance values(%s,0);',(username,))
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
        mysql.connection.commit()
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
    flag=1
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
        mysql.connection.commit()
        cursor.execute('select cost from company,stock where company.comid=stock.comid and stock.sid=%s;',(sid,))
        cost = cursor.fetchone()
        mysql.connection.commit()

        cursor.execute('select balance from customer where cname=%s;',(session['username'],)) 
        curr_balance = cursor.fetchone()['balance']
        mysql.connection.commit()
        if curr_balance >= cost['cost']:
            cursor.execute('UPDATE stock SET availability= stock.availability - 1 WHERE sid=%s', (sid,))
            mysql.connection.commit()
            cursor.execute('INSERT INTO transactions VALUES(%s,"Buy",%s,NOW(),%s,%s);',(book_id['bookingid'],cost['cost'],session['username'],sid,))
            mysql.connection.commit()
            cursor.execute('update customer set balance=balance-%s where cname=%s;',(cost['cost'],session['username'],))
            mysql.connection.commit()
            flag=1

        else:
            print("balance too low!")
            flag=0
    return render_template('buy.html', available=available, pk=book_id, msg=msg,show_results=flag)

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
        print("SID", sid)
        mysql.connection.commit()
        cursor.execute('select distinct company.cost from company,stock,bookings where company.comid=stock.comid and stock.sid=%s;',(sid['sid'],))
        cost = cursor.fetchone()
        print("cost", cost)
        mysql.connection.commit()
        cursor.execute('update customer set balance=balance+%s where cname=%s;',(cost['cost'],session['username']))
        mysql.connection.commit()

        if sid != None:
            cursor.execute(
                'UPDATE stock SET availability = stock.availability + 1 WHERE sid = %s', (sid['sid'],))
            mysql.connection.commit()
            cursor.execute('DELETE FROM bookings WHERE bookingid = %s', (bid,))
            mysql.connection.commit()
            cursor.execute('INSERT INTO transactions VALUES(%s,"Sell",%s,NOW(),%s,%s);',(bid,cost['cost'],session['username'],sid['sid'],))
            mysql.connection.commit()

            msg = "Successfully sold"
        else:
            msg = "Some error occured, please try again"
    return render_template('sell.html', msg=session['username'], bookings=done, mesg=msg)

@app.route('/view',methods=['GET'])
def view():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id,type,company.comname,transactions.sid,amount,date FROM transactions,company,stock where username=%s and stock.sid=transactions.sid and stock.comid=company.comid order by date desc;',(session['username'],))
    transactions = cursor.fetchall()
    mysql.connection.commit()

    return render_template('view.html',transactions=transactions)

#query - group stocks by company, for current user

@app.route('/transactions',methods=['GET','POST'])
def groupedTransactions():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT comname from company;')
    companies = [x['comname'] for x in cursor.fetchall()]
    mysql.connection.commit()

    selected_transactions = tuple()
    trans_colour = dict()
    colours = dict()
    i=0
    summary = dict()

    sample_colours = ['blue','green']

    for c in companies:
        trans_colour[c] = []
        colours[c] = sample_colours[i%2]
        i=i+1
        summary[c] = dict()
        summary[c] = {'Buy': 0,'Sell': 0,'Net': 0,'Bought': 0,'Sold': 0}

    if request.method == 'GET':
        for company in companies:
            cursor.execute('SELECT id,type,company.comname,transactions.sid,amount,date FROM transactions,company,stock where username=%s and stock.sid=transactions.sid and stock.comid=company.comid and company.comname=%s order by date desc;',(session['username'],company,))
            selected_transactions = cursor.fetchall()
            mysql.connection.commit()
            for st in selected_transactions:
                trans_colour[st['comname']].append(st)


            cursor.execute('SELECT type,sum(amount),count(*) FROM transactions,company,stock where stock.sid=transactions.sid and stock.comid=company.comid and username=%s and company.comname=%s group by type;',(session['username'],company,))
            temp = cursor.fetchall()
            summary[company][temp[0]['type']] = temp[0]['sum(amount)']
            summary[company][temp[1]['type']] = temp[1]['sum(amount)']
            summary[company]['Net'] = -summary[company]['Buy'] + summary[company]['Sell']
            summary[company]['Bought'] = temp[0]['count(*)']
            summary[company]['Sold'] = temp[1]['count(*)']
            mysql.connection.commit()

    return render_template('transactions.html',companies=companies,transactions=trans_colour,colours=colours,summary=summary)

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
