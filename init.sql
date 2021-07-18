create database stock;
grant all privileges on stock.* to stock@'%' identified by '!!' with grant option;
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
code varchar(6),
name varchar(10),
market varchar(6),
bank varchar(300),  /*板块*/
gainan varchar(300), /*概念*/
gsld varchar(300),   /*--公司亮点*/
zyfw varchar(300),/*--经营范围*/
kbgs varchar(300), /*--可比公司*/
zycpmc varchar(300), /*--主营产品名称*/
url varchar(300)  /*--公司URL*/
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create UNIQUE index stockinfocode on stockinfo(code);
create index stockinfoname on stockinfo(name);
create index stockinfobank on stockinfo(bank);
create index stockinfogsld on stockinfo(gsld);
create index stockinfozycpmc on stockinfo(zycpmc);
create index stockinfozyfw on stockinfo(zyfw);

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
`code`            varchar(8),
`name`            varchar(10),
`market`            varchar(12)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE UNIQUE INDEX code_name_market ON stockmark(code,name,market);


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

update stockinfo a set mark =(select left(trim(market),5) from stockmark where code =a.mark);

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
---#竞价数据表
CREATE TABLE IF NOT EXISTS `jinjiadata`(
HDDATE date,
code varchar(8),
name varchar(20),
vol int,
price float,
amount float,
drict varchar(4),
market varchar(4)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX jinjiadatacode on jinjiadata(Code);
create index jinjiadataHDDATE on jinjiadata(HDDATE);
create index jinjiadataname on jinjiadata(name);
CREATE UNIQUE INDEX jinjiadatacodenamedate on jinjiadata(HDDATE,code,name,market);
---存储近三年的日期，判断是否为交易日
CREATE TABLE IF NOT EXISTS `datelist`(
date date,
isopen int
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
--早盘1分钟数据
CREATE TABLE IF NOT EXISTS `stockfirstmindata`(
HDDATE date,
htime  varchar(10),
code varchar(8),
name varchar(20),
vol int,
price float,
amount float,
drict varchar(4),
market int,
buycount int,
sellcount int
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE INDEX stockfirstmindatacode on stockfirstmindata(Code);
CREATE UNIQUE INDEX timecodenamedate on stockfirstmindata(HDDATE,htime,code,name);
create index stockfirstmindataHDDATE on stockfirstmindata(HDDATE);
create index stockfirstmindataname on stockfirstmindata(name);

-- 个股历史大资金，注意与超级大单区别(只记录满足条件那天的记录)
CREATE TABLE IF NOT EXISTS `historysuperaward`(
hddate date,
code varchar(8),
name varchar(20),
market varchar(2),
price float,
zdf float,
ddlry float,
ddb float
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index historysuperawardcode on historysuperaward(code);
create index historysuperawardhddate on historysuperaward(hddate);
create index historysuperawardname on historysuperaward(name);
CREATE UNIQUE INDEX superawardcode_name_date_ddlry ON historysuperaward(hddate,code,name,ddlry);
-- 策略表(表结构还没有确定)
CREATE TABLE IF NOT EXISTS `strategys`(
id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
name varchar(50),
conditions varchar(400),
datadate date,
stockcode varchar(9),
stockname varchar(8),
market varchar(2),
zdf float,
price float,
dde float,
turnover_rate float /*换手率 */,
startdate date, /*回测开始日期 */
maxdate date,   /*回测结束日期 */
maxAnnualYield float,   /*最大年化收益率 */
maxhaveday int, /*最大收益率最佳持股天数 */
maxWinRate float,   /*最大胜率 */
maxwinhaveday int,  /*最大胜率持股天数 */
annualYield int,    /*绝对收益率 */
averageLossRatio int,   /*盈利能力 */
scount int, /*交易次数 */
testdate date,  /*测试日期 */
maxDrawDown int,    /*扩风险能力 */
profitVolatility int,   /*稳定性 */
score int,  /*得份 */
winRate int /*选股能力 */
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index strategysname on strategys(name);
create index strategysstockcode on strategys(stockcode);
create index strategysstockname on strategys(stockname);
create index strategysstockdatadate on strategys(datadate);
CREATE UNIQUE INDEX sid_name_date_list ON strategys(name,datadate,stockcode);
--同步到阿里云
--mysqldump -u root -p密码 stock jinjiadata| mysql -h{host} -p密码 stock
--mysqldump  -u root -p stock  >stock.sql
--mysql -h 47.107.130.152 -u stock -p stock <stock.sql

