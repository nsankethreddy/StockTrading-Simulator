# Stock Trading Simulation Platform

This is a platform for simulating stock trading.  
Registered users can buy and sell stocks and view their transaction history and grouped transactions.  

Project for OOAD-SE course in the sixth semester, PES University.  

## Required environment:
1. Python3.8 , Ubuntu
2. Flask 
3. MySQL

## To run: 
1. `cd app`
2. `pip3 install -r requirements.txt`
3. `python3 app.py`  
The app is now running on localhost:5050.  

### Change root password on local mysql server:
1. `sudo mysql -u root -p`
2. `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';`
3. `source stock.sql`
