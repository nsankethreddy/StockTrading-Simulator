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
    hpno BIGINT(10) NOT NULL,
    haddress varchar(100) NOT NUll,
    hrating int NOT NULL,
    hcost BIGINT(10) NOT NULL,
    hcategory varchar(10) NOT NULL,
    PRIMARY KEY(hid)
);
CREATE TABLE IF NOT EXISTS transport(
    tid int(4) NOT NULL AUTO_INCREMENT,
    tname varchar(30) NOT NULL,
    startstop varchar(40) NOT NULL,
    destination varchar(40) NOT NUll,
    trating int NOT NULL,
    tcost BIGINT(10) NOT NULL,
    tcategory varchar(10) NOT NULL,
    PRIMARY KEY(tid)
);
CREATE TABLE IF NOT EXISTS packages(
    pid int(4) NOT NULL AUTO_INCREMENT,
    tid int(4) NOT NULL,
    hid int(4) NOT NULL,
    pcost BIGINT(10) NOT NULL,
    pcategory varchar(10) NOT NULL,
    pavailability int NOT NULL,
    pduration varchar(20) NOT NULL,
    PRIMARY KEY(pid),
    FOREIGN KEY(tid) REFERENCES transport(tid),
    FOREIGN KEY(hid) REFERENCES hotels(hid)
);
CREATE TABLE IF NOT EXISTS hotelpay(
    hpid int(4) NOT NULL,
    startdate DATE NOT NULL,
    enddate DATE NOT NULL,
    hid int(4) NOT NULL,
    FOREIGN KEY(hid) REFERENCES hotels(hid)
);
CREATE TABLE IF NOT EXISTS travelpay(
    tpid int(4) NOT NULL,
    startdate DATE NOT NULL,
    enddate DATE NOT NULL,
    tid int(4) NOT NULL,
    FOREIGN KEY(tid) REFERENCES transport(tid)
);
CREATE TABLE IF NOT EXISTS transaction(
    tpid int(4) NOT NULL,
    transacdate DATE NOT NULL,
    tid int(4) NOT NULL,
    hid int(4) NOT NULL,
    FOREIGN KEY(tid) REFERENCES transport(tid),
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
/*Insert statements*/
-- INSERT INTO customer values(123,"ash",99,"Blah blah blah",'2000-12-29');
-- INSERT INTO customer values(112,"sky",99,"Gong",'2000-09-27');
-- INSERT INTO customer values(127,"skete",99,"Gg",'2000-08-26');
-- INSERT INTO logincheck values(123,"ash");
-- INSERT INTO logincheck values(112,"sky");
-- INSERT INTO logincheck values(127,"skete");
INSERT INTO hotels values(778,"Vivanta by Taj",9902475577,"Bleh",5,8000,"luxury");
INSERT INTO hotels values(411,"GG Lodge",1234567890,"Lol",2,750,"lodge");
INSERT INTO hotels values(328,"Le Meridien",8988998998,"GG",4,5000,"luxury");
INSERT INTO transport values(911,"Air India","Bengaluru","Hyderabad",3,2300,"air");
INSERT INTO transport values(121,"Indigo","Bengaluru","Delhi",3,4500,"air");
INSERT INTO transport values(119,"GG Travels","Bengaluru","Mysore",3,900,"road");
INSERT INTO packages values(327,911,778,23000,"luxury",1,"3 days");
INSERT INTO packages values(328,121,778,25000,"luxury",10,"5 days");
-- INSERT INTO bookings values(327,123);
