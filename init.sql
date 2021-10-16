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

--大资金净流入历史数据
CREATE TABLE IF NOT EXISTS `superfundhistory`(
HDDATE date,
code varchar(8),
name varchar(20),
price float,
superfund float,
superpect float,
zdf float,
bigfund float,
bigpect float,
midfund float,
midpect float,
minfund float,
minpect float,
mainfund float,
mainpect float,
market int

)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE INDEX superhistorycode on superhistory(code);
create index superhistoryHDDATE on superhistory(HDDATE);
create index superhistoryname on superhistory(name);
create index superhistorysuperfund on superhistory(superfund);
create index superhistorysuperpect on superhistory(superpect);
CREATE UNIQUE INDEX  superhistoryUNIQUE  on superhistory(HDDATE,code,superfund);




--rps 计算的主营产品类型分类
CREATE TABLE IF NOT EXISTS `rpszycplx`(
code varchar(8),
name varchar(20),
zycplx varchar(50)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index rpszycplxcode on rpszycplx(code);
CREATE UNIQUE INDEX  rpszycplxunique  on rpszycplx(code,name,zycplx);

--rps 计算的三级分类
CREATE TABLE IF NOT EXISTS `rpsxfhy`(
code varchar(8),
name varchar(20),
xfhy varchar(50),  /*同花顺指数自定义 */
SWEJFL varchar(50),  /*申万二级分类 */
SJFL varchar(50)  /*四级分类 */
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index rpsxfhycode on rpsxfhy(code);
create index rpsxfhyxfhy on rpsxfhy(xfhy);
create index rpsxfhySWEJFL on rpsxfhy(SWEJFL);
create index rpsxfhySJFL on rpsxfhy(SJFL);
CREATE UNIQUE INDEX  rpsxfhyunique  on rpsxfhy(code,name,SJFL);

---业绩报表：
CREATE TABLE IF NOT EXISTS `yjbb`(
code varchar(8),
name varchar(20),
market varchar(2),
publishname varchar(50),  /*行业*/
basic_eps float,   /*每股收益*/
deduct_basic_eps float,  /*扣除每股收益*/
total_operate_income float,  /*营业收入*/
ystz float,  /*营业收入同比*/
yshz  float,  /*营业收入季度环比*/
parent_netprofit float,  /*净利润*/
sjltz  float,  /*净利润同比*/
sjlhz  float, /*净利润季度环比*/
bps float, /*每股净资产*/
weightavg_roe float, /*净资产收益率*/
mgjyxjje  float, /*每股经营现金流*/
xsmll float , /*销售毛利率*/
assigndscrpt varchar(200) , /*利润分配方案*/
zxgxl float , /*股息率*/
datatype  varchar(50) , /*报告类型*/
datayear varchar(8) ,  /*报告年度*/
datemmdd varchar(8) ,  /*半年报/季报 */
reportdate varchar(10),  /*报告日期 */
update_date date   /*更新日期*/
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index yjbbcode on yjbb(code);
create index yjbbname on yjbb(name);
create index yjbbbasic_eps on yjbb(basic_eps);
create index yjbbroe on yjbb(weightavg_roe);
create index yjbbystz on yjbb(ystz);
create index yjbbsjltz on yjbb(sjltz);
create index yjbbreportdate on yjbb(reportdate);
create index yjbbupdate_date on yjbb(update_date);

CREATE UNIQUE INDEX yjbbunique  on yjbb(code,name,reportdate,update_date);

--- 板块RPS
CREATE TABLE IF NOT EXISTS `bankrps`(
hddate varchar(15),
bankname varchar(30),
bkvol float,
bkamount float,
bkzf float,
bk3zf float,
bk5zf float,
bk10zf float,
bk20zf float,
bk60zf float,
bk120zf float,
bk250zf float,
bkzfrt float,
bk3zfrt float,
bk5zfrt float,
bk10zfrt float,
bk20zfrt float,
bk60zfrt float,
bk120zfrt float,
bk250zfrt float,
bkrps float,
bk3rps float,
bk5rps float,
bk10rps float,
bk20rps float,
bk60rps float,
bk120rps float,
bk250rps float
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index bankrpsname on bankrps(bankname);
create index bankrpshddate on bankrps(hddate);
create index bankrpsbkzf on bankrps(bkzf);
create index bankrpsbkrps on bankrps(bkrps);
CREATE UNIQUE INDEX bankrpsunique  on bankrps(bankname,hddate,bk3zf); /* 有可能根据不能的板块分类进行RPS计算 */

----个股rps结果表
CREATE TABLE IF NOT EXISTS `stockrps`(
hddate varchar(15),
code varchar(8),
name varchar(12),
swejfl varchar(50),
sjfl varchar(50),
vol float,
amount float,
zf float,
zf3 float,
zf5 float,
zf10 float,
zf20 float,
zf60 float,
zf120 float,
zf250 float,
zfrt float,
zf3rt float,
zf5rt float,
zf10rt float,
zf20rt float,
zf60rt float,
zf120rt float,
zf250rt float,
rps float,
rps3 float,
rps5 float,
rps10 float,
rps20 float,
rps60 float,
rps120 float,
rps250 float
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockrpscode on stockrps(code);
create index stockrpshddate on stockrps(hddate);
create index stockrpshzf on stockrps(zf);
create index stockrpshzf3 on stockrps(zf3);
CREATE UNIQUE INDEX stockrpsunique  on stockrps(hddate,code,zf3);


--个股评分数据
CREATE TABLE IF NOT EXISTS `stockscore`(
hddate  varchar(12),
code varchar(8),
name varchar(12),
zhdf float, /* 综合得分 */
jsdf float,/* 技术得分 */
zjdf float,/* 资金得分 */
xxdf float,/* 消息得分 */
hydf float,/* 行业得分 */
jbmdf float/* 基本面得分 */
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockscorecode on stockscore(code);
create index stockscorename on stockscore(name);
create index stockscorezhdf on stockscore(zhdf);
CREATE UNIQUE INDEX stockscoreunique  on stockscore(code,name,hddate,zhdf);

--个股涨停信息入库
CREATE TABLE IF NOT EXISTS `stocklimitup`(
hddate  varchar(12),
code varchar(8),
name varchar(12),
price float, /* 当前价 */
zdf float,/* 涨跌幅 */
limituptime float,/* 涨停时间 */
updays float,/* 连板次数 */
openlimits float,/* 开板次数 */
gainan varchar(20) ,/* 所属概念 */
reason  varchar(200)/* 原因 */

)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index stocklimitupcode on stocklimitup(code);
create index stocklimitupname on stocklimitup(name);
create index stocklimituphddate on stocklimitup(hddate);
create index stocklimitupreason on stocklimitup(reason);
CREATE UNIQUE INDEX stocklimitupunique  on stocklimitup(code,name,hddate);

-- 个股股本，流通股本，股东占比信息【问财】
CREATE TABLE IF NOT EXISTS `stockshareholder`(
hddate  varchar(12),
code varchar(8),
name varchar(12),
total_share int, /* 总股本 */
total_market_value float, /* 总市值 */
circulating_share int, /* 流通股本 */
circulating_market_value float, /* 流通市值 */
circulating_ratio float, /* 流通股占比 */
top10_share_holders float, /* 前十大股东持股市值 */
top10_share_sum int, /* 前十大股东持股数量合计 */
top10_share_ratio float, /* 前十大股东持股比例合计 */
free_circulation_marke_value float,/* 自由流通市值  【流通市值-10大股东市值<0|总市值-10大股东市值】当有股东增减持时，数据不准确 */
free_circulation_share float,/* 自由流通股本  【流通股本-前十大股东持股数量合计<0->总本股-前十大股东持股数量合计】当有股东增减持时，数据不准确 */
top10_share_name varchar(500)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index stockshareholdercode on stockshareholder(code);
create index stockshareholdername on stockshareholder(name);
create index stockshareholderhddate on stockshareholder(hddate);
create index stockshareholderfree on stockshareholder(free_circulation_marke_value);
create index stockshareholderfree_share on stockshareholder(free_circulation_share);
CREATE UNIQUE INDEX stockshareholderunique  on stockshareholder(code,name,hddate);


--个股财务数据【wind】
CREATE TABLE IF NOT EXISTS `stockfinancial`(
hddate  varchar(12),
code varchar(8),
name varchar(12),
mgjxjll float , /*  每股净现金流量(元) */
mgjyxjl float , /* 每股经营现金流(元) */
mgjzc float , /*  每股净资产(元/股) */
mgsy float , /*  每股收益(元/股)	  */
mgsytb float , /* 每股收益(摊薄)(元) */
mgyylr float , /* 每股营业利润(元)	  */
mgyysr float , /* 每股营业收入(元)  */
gsymgssyzdjlr float , /* 归属于母公司净利润(元)  */
jlr float , /* 净利润(元)  */
lrze float , /* 利润总额(元) */
yylr float , /* 营业利润(元) */
yysr float , /* 营业收入(元) */
jll float , /* 净利率(%) */
mll float , /* 毛利率(%) */
roe float , /* ROE(%)净资产收益率 */
yylrl float , /* 营业利润率(%)	 */
cwfyl float , /* 财务费用率(%)*/
glfyl float , /* 管理费用率(%) */
roic float , /* ROIC */
xsfyl float , /* 销售费用率(%) */
xsqjfyl float , /* 销售期间费用率(%) */
xsqlr float , /* 息税前利润(元) */
cqbl float , /* 产权比率（%）	 */
ldbl_r float , /* 流动比率（倍） */
lxbzbs float , /* 利息保障倍数 */
mgjyhdxjllzzl float , /* 每股经营活动现金流量增长率（%） */
sdbl_r float , /* 速动比率（倍） */
xjbl float , /* 现金比率（%） */
xjldfzb float , /* 现金流动负债比 */
zcfzl float , /* 资产负债率（%） */
chzzl float , /* 存货周转率（次） */
gdzczzl float , /* 固定资产周转率（次） */
ldzczzl float , /* 流动资产周转率（次） */
yszkzzl float , /* 应收帐款周转率（次） */
zzczzl float  /* 资产周转率（次） */
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index stockfinancialcode on stockfinancial(code);
create index stockfinancialname on stockfinancial(name);
create index stockfinancialhddate on stockfinancial(hddate);
CREATE UNIQUE INDEX stockfinancialunique  on stockfinancial(code,name,hddate);





--同步到阿里云
--mysqldump -u root -p密码 stock jinjiadata| mysql -h{host} -p密码 stock
--mysqldump  -u root -p stock  >stock.sql
--mysql -h  -u stock -p stock <stock.sql

