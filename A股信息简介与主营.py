# __*__endconding='utf-8'__*__
#信息采集于同花顺
import requests as req
# from lxml import etree
import  pymysql
import time,datetime,json
import tushare as ts
import pandas as pd

configfile = 'D:/mysqlconfig.json'
file = './A股信息简介与主营.csv'

def get_config():
    with open(configfile, encoding="utf-8") as f:
        jsoncontent = json.load(f)
    f.close()
    return jsoncontent

def dbconnect():
    # 读取json格式的配置文件
    jsoncontent =get_config()
    conn = pymysql.connect(jsoncontent['host'], jsoncontent['user'], jsoncontent['password'],
                           jsoncontent['database'], charset='utf8')
    return conn

def get_stockInfo(stocklist):
    sn = req.session()
    stockinfo = []  # 存储符合条件的企业
    # 同花顺的接口
    url = 'http://basic.10jqka.com.cn/mapp/%s/company_base_info.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Cookie': 'searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1608770907,1609917926,1610114215,1611192209; reviewJump=nojump; usersurvey=1; v=A-xOcNJfoJFX0bSt1GiqynybvcEdpZBLkkmkE0Yt-Bc6UYL3brVg3-JZdKSV',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'basic.10jqka.com.cn'
        }
    i = 0
    j = 0  # 符合条件记录数
    for line in stocklist.iterrows():
        code = line[1]['ts_code'][0:6]
        name = line[1]['name']
        industry = line[1]['industry']
        if industry is None or industry =='':
            industry=''
        url1 = url % code
        sn.headers = headers
        # pro = proxy.get_proxy()
        # print(pro)
        try:
            # sn.proxies=pro
            response=sn.get(url=url1)
            # jsoncontent = sn.get(url=url1, headers=headers).json()
        except BaseException:
            time.sleep(10)
            count=0
            while True:
                response=sn.get(url=url1)
                if response.status_code==200:
                    break
                else:
                    count+=1
                    print('获取%s股票信息 第 %s 次重试中！！！'%(name,count))
                    time.sleep(5)
                    if count>=5:
                        print('重试了%d 次仍失败，跳过！！！'%count)
                        break
        try:
            jsoncontent = response.json()
        except BaseException as e1:
            print('解释:%s 返回信息出错,跳过此股！！！' %name)
            continue

        # print(jsoncontent)
        time.sleep(1)  # 不休息会封IP
        stockdesc = jsoncontent['data']['describe']
        if stockdesc is None or stockdesc=='':
            stockdesc=''
        base_business = jsoncontent['data']['base_business']
        if base_business is None or base_business=='':
            base_business = ''
        business_scope = jsoncontent['data']['business_scope']
        if business_scope is None or business_scope=='':
            business_scope = ''
        try:
            str1 = code + '|' + name + '|' + industry + '|' + stockdesc+'|'+base_business+'|'+business_scope
        except BaseException as e2:
            print(url1+'取值异常！')
        stockinfo.append(str1)


    with open(file, 'w', encoding='utf-8') as fw:
        fw.write('代码|名称|行业|简介|主营业务|业务范围' + '\n')
        for textvalue in stockinfo:
            fw.write(str(textvalue) + '\n')
    return stockinfo
###获取股票代码
def get_stocklist():
    tusharecode = get_config()
    pro = ts.pro_api(tusharecode['tushare'])
    stocklist=pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    stocklist=pd.DataFrame(stocklist)
    return stocklist
# 将数据入表
def insertstockinfomation(stockinfos):
    if len(stockinfos) == 0:
        return
    #print(northdataAnalyinfos)
    conn = dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
       # 执行的sql语句
    sql = '''insert into stockinfomation (CODE,NAME,stockdesc,base_business,business_scope) values (%s,%s,%s,%s,%s)'''
    for datalist in stockinfos:
        row=datalist.split('|')
        CODE=row[0]
        NAME=row[1]
        industry=row[2]
        stockdesc=row[3]
        base_business=row[4]
        business_scope=row[5]
        values = (CODE, NAME, industry,stockdesc, base_business, business_scope)
        # sql = '''select code from stockinfomation where code='''''

        try:
            cursor.execute(sql, values)
                # print(values,sql)
        except BaseException as be:
            print(be)
            continue
        conn.commit()
    conn.close()

def Select_stockInfo(self):  # **kwords :表示可以传入多个键值对， *kwords:表示可传入多个参数
    header = ['日期', '代码', '名称', '行业', '简介', '主营业务', '业务范围']
    newdate = self.get_page_newdate()
    outdate = datetime.datetime.strptime(newdate, "%Y-%m-%d")
    yesterday = self.get_lastDay(outdate)
    sql = 'select * from stockinfomation where hddate=\'' + newdate + '\'and SHAREHOLDPRICEONE>5 and SHAREHOLDPRICEFIVE>1 and Zdf >-2 and SCode in ( select SCode from northdataAnaly where hddate=\'' + yesterday + '\' and SHAREHOLDPRICEONE<0 )  order by SHAREHOLDPRICEONE desc'
    print(sql)
    conn = self.dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # print(sql)
    cursor.execute(sql)
    resultset = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(resultset)
    if resultset:
        return resultset
    else:
        # print('未查询到数据，请更新数据！')
        return None


if __name__ == '__main__':
    stocklist=get_stocklist()
    stockInfo=get_stockInfo(stocklist)
    insertstockinfomation(stockInfo)



'''CREATE TABLE IF NOT EXISTS `stockinfomation`( 
CODE varchar(8),
NAME varchar(20),
industry varchar(100),
stockdesc varchar(100),  
base_business varchar(300),
business_scope varchar(300)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockinfomationcode on stockinfomation(CODE);
create index stockinfomationname on stockinfomation(NAME);
create index stockinfomationstockdesc on stockinfomation(stockdesc);'''

    # writetoFile(stockInfo,file)