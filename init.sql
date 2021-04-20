create database stock;
grant all privileges on stock.* to stock@'%' identified by 'STOCK@test!!' with grant option;
flush privileges;

--#股票代码表
CREATE TABLE IF NOT EXISTS `stocks`(
`code`            varchar(8),
`name`            varchar(12),
`area`            varchar(12),
`industry`  varchar(12),
primary key (`code`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockcodes on stocks(code);
create index stocknames on stocks(name);
create index stockarea on stocks(area);
create index stockindustry on stocks(industry);

--#个股描述信息与概念表
CREATE TABLE IF NOT EXISTS `stockinfo`(
mcode varchar(2),
code varchar(6),
mark varchar(6),
info varchar(300),
value varchar(10),
name varchar(10),
markname varchar(12)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index stockinfocode on stockinfo(code);
create index stockinfomcode on stockinfo(mcode);
create index stockinfomname on stockinfo(name);
update stockinfo a set name =(select left(trim(name),4) from stocks where code =a.code);


--个股信息简介表，此表数据来源于同花顺
CREATE TABLE IF NOT EXISTS `stockinfomation`(
CODE varchar(8),
NAME varchar(20),
industry varchar(100),
stockdesc varchar(100),
base_business varchar(300),
business_scope varchar(300)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockinfomationcode on stockinfomation(CODE);
create index stockinfomationname on stockinfomation(NAME);
create index stockinfomationstockdesc on stockinfomation(stockdesc);

--早盘数据
CREATE TABLE IF NOT EXISTS `stockopendata`(
`code`            varchar(8),
`name`            varchar(12),
`zhangfu`         float,
`liangbi`         float,
`kaipan`          float,
`huanshuonu`      float,
`kaipanjine`      float,
`zongjine`        float,
`liutongguyi`     varchar(15),
`liutongsizhi`    varchar(15),
`lianzhangtiansu` int,
`shanrizhangfu`   float,
`ershirizhangfu`  float,
`liushirizhangfu` float,
`date`            DATE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockcode on stockopendata(code);
create index stockname on stockopendata(name);
create index stockdate on stockopendata(date);
CREATE UNIQUE INDEX code_name_stockdate ON stockopendata(code,name,date);

--#自定义数据标记
CREATE TABLE IF NOT EXISTS `stockmark`(
`markcode`            varchar(8),
`markname`            varchar(12),
primary key (`markcode`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


--南向资金数据
CREATE TABLE IF NOT EXISTS `southdataanly`(
HDDATE date,
SCODE varchar(8),
SNAME varchar(20),
SHAREHOLDSUM float,
SHARESRATE float,
CLOSEPRICE float,
ZDF float,
SHAREHOLDPRICE float,
SHAREHOLDPRICEONE float,
SHAREHOLDPRICEFIVE float,
SHAREHOLDPRICETEN float
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index southdataanlycode on southdataanly(SCODE);
create index southdataanlyHdDate on southdataanly(HDDATE);
create index southdataanlySName on southdataanly(SNAME);
CREATE UNIQUE INDEX southcode_name_stockdate ON southdataanly(SCODE,SNAME,HDDATE,SHARESRATE);
--北向资金数据
CREATE TABLE IF NOT EXISTS `northdataAnaly`(
HDDATE date,
SCODE varchar(8),
SNAME varchar(20),
SHAREHOLDSUM float,
SHARESRATE float,
CLOSEPRICE float,
ZDF float,
SHAREHOLDPRICE float,
SHAREHOLDPRICEONE float,
SHAREHOLDPRICEFIVE float,
SHAREHOLDPRICETEN float
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index northdataAnalycode on northdataAnaly(SCODE);
create index northdataAnalyHdDate on northdataAnaly(HDDATE);
create index nnorthdataAnalySName on northdataAnaly(SNAME);
CREATE UNIQUE INDEX northcode_name_stockdate ON northdataAnaly(SCODE,SNAME,HDDATE,SHARESRATE);

update stockinfo a set markname =(select left(trim(markname),5) from stockmark where markcode =a.mark);

-- 用户信息表
CREATE TABLE IF NOT EXISTS `users`(
id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
username   VARCHAR(20) NOT NULL,
password  varchar(1024) NOT NULL,
phone varchar(15) NOT NULL,
email  varchar(25),
idcard varchar(15),
qqid varchar(15),
wechat varchar(25),
payid varchar(25),
registime date,
updatetime date,
level int,
availdate int,
useddate int,
amount float,
availbalance float,
Rechargedate date,
memo varchar(50)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create UNIQUE index usersusername on users(username);
create UNIQUE index usersphone on users(phone);
create UNIQUE index usersemail on users(username,phone,email);
create index usersidcard on users(idcard);
create index userseqqid on users(qqid);
create index usersewechat on users(wechat);
create index usersepayid on users(payid);

