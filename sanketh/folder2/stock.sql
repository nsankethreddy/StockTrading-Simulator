DROP database stock_simulator_db;
CREATE DATABASE IF NOT EXISTS stock_simulator_db;
USE stock_simulator_db;

CREATE TABLE IF NOT EXISTS customer(
    cid int(4) NOT NULL AUTO_INCREMENT,
    cname varchar(30) NOT NULL,
    pno BIGINT(10) NOT NULL,
    addr varchar(100) NOT NUll,
    dob DATE NOT NULL,
    PRIMARY KEY(cid)
);
CREATE TABLE IF NOT EXISTS logincheck(
    cid int(4) NOT NULL,
    pwd varchar(50) NOT NULL,
    FOREIGN KEY(cid) REFERENCES customer(cid)
);
CREATE TABLE IF NOT EXISTS hotels(
    hid int(4) NOT NULL AUTO_INCREMENT,
    hname varchar(30) NOT NULL,
    hcost BIGINT(10) NOT NULL,
    hcategory varchar(30) NOT NULL,
    PRIMARY KEY(hid)
);

CREATE TABLE IF NOT EXISTS packages(
    pid int(4) NOT NULL AUTO_INCREMENT,
    hid int(4) NOT NULL,
    pcost BIGINT(10) NOT NULL,
    hcategory varchar(30) NOT NULL,
    pavailability int NOT NULL,
    PRIMARY KEY(pid),
    FOREIGN KEY(hid) REFERENCES hotels(hid)
);
    -- FOREIGN KEY(hcategory) REFERENCES hotels(hcategory)


CREATE TABLE IF NOT EXISTS hotelpay(
    hpid int(4) NOT NULL,
    startdate DATE NOT NULL,
    enddate DATE NOT NULL,
    hid int(4) NOT NULL,
    FOREIGN KEY(hid) REFERENCES hotels(hid)
);
CREATE TABLE IF NOT EXISTS transaction(
    tpid int(4) NOT NULL,
    transacdate DATE NOT NULL,
    hid int(4) NOT NULL,
    FOREIGN KEY(hid) REFERENCES hotels(hid)
);
CREATE TABLE IF NOT EXISTS bookings(
    bookingid int(4) NOT NULL AUTO_INCREMENT,
    pid int(4) NOT NULL,
    cid int(4) NOT NULL,
    PRIMARY KEY(bookingid),
    FOREIGN KEY(pid) REFERENCES packages(pid),
    FOREIGN KEY(cid) REFERENCES customer(cid)
);

    INSERT INTO customer values(1,"skete",99,"99",'2000-08-26');
    INSERT INTO logincheck values(1,"99");
    INSERT INTO hotels values(778," Google",8000,"Technology");
    INSERT INTO hotels values(411,"Tesla",750,"Automobiles");
    INSERT INTO hotels values(328,"Microsoft",5000,"Technology");
    INSERT INTO packages values(327, 778, 8000, "Technology", 1);
    INSERT INTO packages values(328, 778, 8000, "Technology", 10);