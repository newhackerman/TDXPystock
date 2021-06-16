# __*__endconding='utf-8'__*__
#信息采集于同花顺
import requests as req
import  pymysql
import time,json,sys
import tushare as ts
import pandas as pd
import prettytable as pt
configfile = './config/mysqlconfig.json'
file = './A股信息简介与主营.csv'
#读取配置文件
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
    return stocklist
#获取股票基本信息
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
        stockdesc=stockdesc.replace('\n','',-1)
        if len(stockdesc)>=100:
            stockdesc=stockdesc[0:100]
        base_business = jsoncontent['data']['base_business']
        if base_business is None or base_business=='':
            base_business = ''
        base_business=base_business.replace('\n','',-1)
        if len(base_business)>=300:
            base_business=base_business[0:300]
        business_scope = jsoncontent['data']['business_scope']
        if business_scope is None or business_scope=='':
            business_scope = ''
        business_scope=business_scope.replace('\n','',-1)
        if len(business_scope)>=300:
            business_scope=business_scope[0:300]
        try:
            str1 = code + '|' + name + '|' + industry + '|' + stockdesc+'|'+base_business+'|'+business_scope
            print(str1)
        except BaseException as e2:
            print(url1+'取值异常！')
        stockinfo.append(str1)


    with open(file, 'w', encoding='utf-8') as fw:
        fw.write('代码|名称|行业|简介|主营业务|业务范围' + '\n')
        for textvalue in stockinfo:
            fw.write(str(textvalue) + '\n')
    return stockinfo

def readstockinFile(file):
    infolists=[]
    f=open(file,'r',encoding='utf-8')
    context=f.readlines()
    for data in context:
        infolists.append(data)
    return infolists
# 将数据入表
def insertstockinfomation(stockinfos):

    if len(stockinfos) == 0:
        return
    conn = dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = '''insert into stockinfomation (CODE,NAME,industry,stockdesc,base_business,business_scope) values (%s,%s,%s,%s,%s,%s)'''
    for datalist in stockinfos:
        row=datalist.split('|')
        CODE=row[0]
        NAME=row[1]
        try:
            industry=row[2]
        except BaseException as e1:
            industry=''
        try:
            stockdesc=row[3]
        except BaseException as e2:
            stockdesc=''

        try:
            base_business=row[4]
        except BaseException as e3:
            base_business=''

        try:
            business_scope=row[5]
        except BaseException as e4:
            business_scope=''

        values = (CODE, NAME, industry,stockdesc, base_business, business_scope)
        try:
            cursor.execute(sql, values)
                # print(values,sql)
        except BaseException as be:
            print(be)
            continue
        conn.commit()
    conn.close()

#######################根据条件查询mysql中的数据#######################
def select_stockinfos(condiction):
    tablename='stockinfomation'
    #dict=indb.file2dict(indb.configfile)  #读取配置信息
    conn=dbconnect()
    cursor= conn.cursor(cursor=pymysql.cursors.DictCursor)  #打开游标
    # condictions= str(condiction).strip('{').strip('}').replace(':','=',1).replace('\'','',2)

    sql = "select CODE, NAME, industry,stockdesc, base_business, business_scope from " + tablename + " where stockdesc like '%" + condiction + "%' ;"

    #print(sql)
    # print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except BaseException as be:
        print(be)
        print("Error: unable to fetch data")
    cursor.close()
    if results is None:
        print('未查到数据！')
        return results
    else:
        # print('未查询到数据，请更新数据！')
        return results

def formatresults(results):
    #results   查询到的数据集
    #header   要输出的表头
    if results is None:
        print('无数据输出！！！')
        return

    header=['代码' , '名称', '行业' , '简介' , '主营业务' ]
    tb = pt.PrettyTable()
    tb.field_names=header #设置表头
    tb.align='l'  #对齐方式（c:居中，l居左，r:居右）
    for row in results:  # 依次获取每一行数据
        CODE = row['CODE']
        NAME = row['NAME']
        industry = row['industry']
        stockdesc = row['stockdesc']
        base_business = row['base_business']
        if len(base_business)>=40:
            base_business=base_business[0:40]
        business_scope = row['business_scope']
        tb.add_row([CODE, NAME, industry,stockdesc, base_business])
    # s=tb.get_html_string()  #获取html格式
    print(tb)

if __name__ == '__main__':
    cond=r"stockdesc like '%世界第一%'"
    var = sys.argv  # 可以接收从外部传入参数
    # 查个股概念信息，或某概念包含的股票信息
    try:
         infolist=select_stockinfos(var[1])
    except BaseException as e:
        print('未入查询条件')
        exit(1)
    formatresults(infolist)


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