import pymysql
from sqlalchemy import create_engine
import os
import pandas as pds
import 早盘数据入库 as indb  #此文件里已经写好连库方法直接调用


def insertsql(tablename,code1,name1):
    try:
        conn = indb.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql='insert into '+tablename +' values(%s,%s)'
        values=(code1,name1)
        #print(sql)
        flag=cursor.execute(sql,values)
        conn.commit()
        cursor.close()
        conn.close()
    except BaseException as be:
        print(be)

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

def inserttodb(conn,file,tablename):
    try:
        #conn = indb.dbconnect()
        # dict=indb.file2dict(configfile)
        # engine =create_engine("mysql+pymysql://"+dict['user']+":"+dict['password']+'@'+dict['host']+":3306/"+dict['database']+"?charset=utf8")
        # context=pds.read_csv(file,sep=",", encoding='utf-8')
        # len= len(context)
        with open(file,'r',encoding='utf-8') as fr:
            context=fr.readlines()
            for line in context:
                # print(type(line),str(line))
                code=line.split(",")[0]
                name=line.split(",")[1]
                #print(code,name)

                flag=insertsql(tablename,code,name)
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
    conn = indb.dbconnect()
    #inserttodb(conn,bindfile, bandtb)  #插入板块对应信息
    inserttodb(conn,stockfile, stocktb) #插入个股对应信息

    #insertstockinfos(conn, stockinfofile, stockinfo) #插入个股概念主营信息

'''
#股票代码表
CREATE TABLE IF NOT EXISTS `bands`(           
`code`            varchar(8),                  
`name`            varchar(12), 
primary key (`code`) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index codes on bands(code);
create index bands on bands(name);


#板块表
CREATE TABLE IF NOT EXISTS `stocks`(           
`code`            varchar(8),                  
`name`            varchar(12), 
primary key (`code`) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockcodes on stocks(code);
create index stocknames on stocks(name);

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