DROP database stock_simulator_db;
CREATE DATABASE IF NOT EXISTS stock_simulator_db;
USE stock_simulator_db;

CREATE TABLE IF NOT EXISTS customer(
    cid int(4) NOT NULL AUTO_INCREMENT,
    cname varchar(30) NOT NULL,
    pno BIGINT(10) NOT NULL,
    addr varchar(100) NOT NUll,
    dob DATE NOT NULL,
    balance DOUBLE NOT NULL DEFAULT 5000.0,
    PRIMARY KEY(cid)
);
CREATE TABLE IF NOT EXISTS logincheck(
    cid int(4) NOT NULL,
    pwd varchar(50) NOT NULL,
    FOREIGN KEY(cid) REFERENCES customer(cid)
);
CREATE TABLE IF NOT EXISTS company(
    comid int(4) NOT NULL AUTO_INCREMENT,
    comname varchar(30) NOT NULL,
    cost BIGINT(10) NOT NULL,
    category varchar(30) NOT NULL,
    PRIMARY KEY(comid)
);

CREATE TABLE IF NOT EXISTS stock(
    sid int(4) NOT NULL AUTO_INCREMENT,
    comid int(4) NOT NULL,
    availability int NOT NULL,
    PRIMARY KEY(sid),
    FOREIGN KEY(comid) REFERENCES company(comid)
);

CREATE TABLE IF NOT EXISTS bookings(
    bookingid int(4) NOT NULL AUTO_INCREMENT,
    sid int(4) NOT NULL,
    cid int(4) NOT NULL,
    PRIMARY KEY(bookingid),
    FOREIGN KEY(sid) REFERENCES stock(sid),
    FOREIGN KEY(cid) REFERENCES customer(cid)
);

create table if not exists transactions(id int primary key, type varchar(5), company varchar(25), amount double,date timestamp);

INSERT INTO customer values(1,"skete",99,"99",'2000-08-26');
INSERT INTO logincheck values(1,"99");

INSERT INTO company values(11," Google",8000,"Technology");
INSERT INTO company values(21,"Tesla",7500,"Automobiles");
INSERT INTO company values(31,"Microsoft",5000,"Technology");

INSERT INTO stock values(4, 11, 1);
INSERT INTO stock values(5, 21, 10);
INSERT INTO stock values(6, 31, 7);
