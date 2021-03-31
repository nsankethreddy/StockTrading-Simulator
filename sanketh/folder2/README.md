# globetrotter

# Tourism Booking / management system

## Functionalities to be implemented:
1. Managing event ( login - logout - Book - cancel )
2. Inventory management
3. Recommender systems


## Required environment:
1. Python3.8 , Ubuntu
2. Flask 
3. MySQL

## To run: 
1. `pip install -r requirements.txt`
2. `python app.py`

### Error while installing flask_mysqldb :
1. `sudo apt-get install python-dev default-libmysqlclient-dev libssl-dev`
2. `pip install flask-mysqldb`

### Change root password on local mysql server:
1. `sudo mysql -u root -p`
2. `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'asdfghjkl$123';`
3. `use stock_simulator_db;`
4. `source stock.sql`
