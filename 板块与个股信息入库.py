import pymysql
from sqlalchemy import create_engine
import os
import pandas as pds
import 早盘数据入库 as indb  #此文件里已经写好连库方法直接调用
import tushare as ts
import json
import pandas as pd

def get_config():
    with open(configfile, encoding="utf-8") as f:
        jsoncontent = json.load(f)
    f.close()
    return jsoncontent
#连接数据库
def dbconnect():
    # 读取json格式的配置文件
    jsoncontent =get_config()
    conn = pymysql.connect(jsoncontent['host'], jsoncontent['user'], jsoncontent['password'],
                           jsoncontent['database'], charset='utf8')
    return conn
###获取股票代码
def get_stocklist():
    tusharecode = get_config()
    pro = ts.pro_api(tusharecode['tushare'])
    stocklist=pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    stocklist=pd.DataFrame(stocklist)
    print(stocklist.head(10))
    return stocklist

def insertstock(stocklist):
    for line in stocklist.iterrows():
        code = line[1]['ts_code'][0:6]
        name = line[1]['name']
        area=line[1]['area']
        industry = line[1]['industry']
        sql='''insert into stocks values(%s,%s,%s,%s)'''
        values=(code,name,area,industry)
        conn=dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql,values)
        conn.commit()
    cursor.close()
    conn.close()

def insertstockinfos(conn,file,tablename):
    try:

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #i=0
        with open(file,'r',encoding='utf-8') as fr:
            context=fr.readlines()
            for line in context:
                mcode=line.split("|")[0]
                code=line.split("|")[1]
                mark = line.split("|")[2]
                info = line.split("|")[3]
                #value = line.split("|")[4]
                sql='insert into '+tablename +'(mcode,code,mark,info) '+' values(%s,%s,%s,%s)'
                values=(mcode,code,mark,info)
                flag=cursor.execute(sql,values)
                #i+=1
                #print(flag,i)
            conn.commit()
            cursor.close()
            conn.close()

                # if flag!=-1:
                #     print('执行成功！')
    except BaseException as be:
        print(be)
        print('执行错误！！！')



if __name__ == '__main__':
    bindfile='D:/pythonTtest/TDXPystock/板块列表.txt'
    stockfile='D:/pythonTtest/TDXPystock/个股信息列表.txt'
    configfile = 'D:/mysqlconfig.json'
    stockinfofile='D:/pythonTtest/TDXPystock/stockinfos.txt'
    bandtb='bands'
    stocktb='stocks'
    stockinfo='stockinfo'
    conn = dbconnect()
    stocklist=get_stocklist()
    insertstock(stocklist)
    #以下调用语句，需要用时放开注释即调用相关功能
    #inserttodb(conn,bindfile, bandtb)  #插入板块对应信息
    #inserttodb(conn,stockfile, stocktb) #插入个股对应信息

    #insertstockinfos(conn, stockinfofile, stockinfo) #插入个股概念主营信息

'''
#股票代码表
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


#个股描述信息与概念表
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

#自定义数据标记
CREATE TABLE IF NOT EXISTS `stockmark`(           
`markcode`            varchar(8),                  
`markname`            varchar(12), 
primary key (`markcode`) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


update stockinfo a set markname =(select left(trim(markname),5) from stockmark where markcode =a.mark);
'''