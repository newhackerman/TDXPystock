import pymysql
import os,datetime,time,json
import requests as req
import tushare as ts
import pandas as pd
from dboprater import DB as db
###获取股票代码
def get_stocklist():
    tusharecode = db.get_config()
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
        conn=db.dbconnect()
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

# 使用爱问财只要1个请求
def getstocksinfoFromaiwencai():
    datenow = datetime.datetime.now().strftime('%Y%m%d')
    stockfile = './config/A股公司相关信息.csv'
    stockinfo = []
    url = 'http://ai.iwencai.com/urp/v7/landing/getDataList'
    header = {
        'Host': 'ai.iwencai.com',
        'Connection': 'keep-alive',
        'Content-Length': '880',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://wap.iwencai.com',
        'Referer': 'http://wap.iwencai.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    postdata = {
        'query': '公司亮点与行业与主营业务与可比公司',
        'urp_sort_way': 'desc',
        'urp_sort_index': '最新涨跌幅',
        'page': '1',
        'perpage': '5000',
        'condition': '[{"chunkedResult":"公司亮点与行业与主营业务与可比公司","opName":"and","opProperty":"","sonSize":6,"relatedSize":0},{"indexName":"公司亮点","indexProperties":[],"source":"new_parser","type":"index","indexPropertiesMap":{},"reportType":"null","valueType":"_公司亮点","domain":"abs_股票领域","uiText":"公司亮点","sonSize":0,"queryText":"公司亮点","relatedSize":0,"tag":"公司亮点"},{"opName":"and","opProperty":"","sonSize":4,"relatedSize":0},{"indexName":"所属同花顺行业","indexProperties":[],"source":"new_parser","type":"index","indexPropertiesMap":{},"reportType":"null","valueType":"_所属同花顺行业","domain":"abs_股票领域","uiText":"所属同花顺行业","sonSize":0,"queryText":"所属同花顺行业","relatedSize":0,"tag":"所属同花顺行业"},{"opName":"and","opProperty":"","sonSize":2,"relatedSize":0},{"indexName":"主营产品名称","indexProperties":[],"source":"new_parser","type":"index","indexPropertiesMap":{},"reportType":"null","valueType":"_主营产品名称","domain":"abs_股票领域","uiText":"主营产品名称","sonSize":0,"queryText":"主营产品名称","relatedSize":0,"tag":"主营产品名称"},{"indexName":"财务维度可比公司","indexProperties":["nodate 1","交易日期 20201231"],"source":"new_parser","type":"index","indexPropertiesMap":{"交易日期":"20201231","nodate":"1"},"reportType":"YEAR","dateType":"报告期","valueType":"_最优可比公司","domain":"abs_股票领域","uiText":"财务维度可比公司","sonSize":0,"queryText":"财务维度可比公司","relatedSize":0,"tag":"财务维度可比公司"}]',
        'codelist': '',
        'indexnamelimit': '',
        'logid': 'c7c5c70a5c03f9f686d81b04a830ba4d',
        'ret': 'json_all',
        'sessionid': '6a765f385c2f1cfddd25c05a444fd6a9',
        'date_range[0]': '20201231',
        'iwc_token': '0ac9511916247088780837061',
        'urp_use_sort': '1',
        'user_id': '234319860',
        'uuids[0]': '24087',
        'query_type': 'stock',
        'comp_id': '5722297',
        'business_cat': 'soniu',
        'uuid': '24087'
    }
    content = None
    try:
        content = req.post(url=url, headers=header, data=postdata, timeout=120).json()
        # print(content)
    except BaseException as b:
        print('i wen cai request error', b)
        time.sleep(3)
        count = 0
        while count < 5:
            try:
                content = req.post(url=url, headers=header, data=postdata, timeout=120).json()
            except BaseException as b:
                time.sleep(2)
                continue
            if content != '':
                break
    if content['status_code'] != '0':
        return None
    jsondata = content['answer']['components'][0]['data']['datas']
    if jsondata is None:
        return None
    for tmpdata in jsondata:
        code = tmpdata['code']
        name = tmpdata['股票简称']
        market1=tmpdata['股票代码'][7:9]
        market='1'
        if market1=='SZ':
            market='0'
        tmpbank = str(tmpdata['所属同花顺行业']).split('-')
        bank = tmpbank[1]
        gailan=tmpdata['所属概念']
        gsld = tmpdata['公司亮点']
        if str(gsld) == 'None':
            gsld == ''
        zyfw=tmpdata['经营范围']
        zycpmc= tmpdata['主营产品名称']
        kbgs=''
        try:
            kbgs = tmpdata['财务维度可比公司']
        except BaseException as b:
            kbgs=''
        url=''
        try:
            url=tmpdata['公司网站']
        except BaseException as b:
            url=''
        str1 = str(code) + '$' + str(name) + '$' + str(market) + '$' + str(bank)+ '$' + str(gailan) + '$' + str(gsld) + '$' + str(zyfw)+ '$' + str(kbgs) + '$' + str(zycpmc) + '$' + str(url)
        print(str1)
        stockinfo.append(str1)

    with open(stockfile, 'w', encoding='utf-8') as fw:
        fw.write('代码$名称$市场代码$行业$概念$公司亮点$经营范围$可比公司$主营产品$URL' + '\n')
        for textvalue in stockinfo:
            fw.write(str(textvalue) + '\n')

def updatestockinfotodb():
    filename = './config/A股公司相关信息.csv'
    #首先从通达信获取对象列表，并写文件
    pddata = pd.read_csv(filename,sep='$',error_bad_lines=False)
    pddata.drop_duplicates(keep="first", inplace=True)
    print(pddata.head())
    if pddata.empty:
        return
    sql = '''insert into stockinfo (code,name,market,bank,gainan,gsld,zyfw,kbgs,zycpmc,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    conn = db.dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    '代码$名称$市场代码$行业$概念$公司亮点$经营范围$可比公司$主营产品$URL'
    for data in pddata.iterrows():
        code = data[1]['代码']
        code = str(code).rjust(6, '0')
        name = str(data[1]['名称'])
        market = str(data[1]['市场代码'])
        bank = str(data[1]['行业'])
        gailan = str(data[1]['概念'])
        zyfw = str(data[1]['经营范围'])
        gsld = str(data[1]['公司亮点'])
        kbgs = str(data[1]['可比公司'])
        zycpmc = str(data[1]['主营产品'])
        url = str(data[1]['URL'])
        values = (code, name, market,bank,gailan,gsld,zyfw,kbgs,zycpmc,url)
        # print(values)
        # break
        # print(values)
        try:
            cursor.execute(sql, values)
        except BaseException as b:
            print(b)
            continue
    conn.commit()
    cursor.close()
    conn.close()
    # except BaseException as b:
    #     pass

#概念个股查询
def getrelationgainanstocksFromDB(str1):
    try:
        conn=db.dbconnect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        sql='select code,name,gainan,bank,gsld,zyfw,zycpmc,kbgs from stockinfo where gainan like \'%'+str1 +'%\' or gsld like \'%'+str1 +'%\''
        cursor.execute(sql)
        result=cursor.fetchall()
        # print(result)
        if result is None:
            return None
        return pd.DataFrame(result)
    except BaseException as b:
        return None

if __name__ == '__main__':
    bindfile='./config/板块列表.txt'
    stockfile='./config/个股信息列表.txt'
    configfile = './config/mysqlconfig.json'
    stockinfofile='./config/stockinfos.txt'
    bandtb='bands'
    stocktb='stocks'
    stockinfo='stockinfo'
    # getstocksinfoFromaiwencai()
    # updatestockinfotodb()
    # stocklist=get_stocklist()
    # insertstock(stocklist)
    #以下调用语句，需要用时放开注释即调用相关功能
    #inserttodb(conn,bindfile, bandtb)  #插入板块对应信息
    #inserttodb(conn,stockfile, stocktb) #插入个股对应信息

    #insertstockinfos(conn, stockinfofile, stockinfo) #插入个股概念主营信息
    result=getrelationgainanstocksFromDB('龙头')
    print(result)
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



#自定义数据标记
CREATE TABLE IF NOT EXISTS `stockmark`(           
`markcode`            varchar(8),                  
`markname`            varchar(12), 
primary key (`markcode`) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


update stockinfo a set markname =(select left(trim(markname),5) from stockmark where markcode =a.mark);
'''