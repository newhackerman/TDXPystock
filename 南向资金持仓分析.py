import bs4
import requests as req
import json
import prettytable as pt   #格式化成表格输出到html文件
import time,sys,re
from dboprater import DB as db
from pyecharts.charts import Line
from pyecharts import options as opts
import tushare as ts
import webbrowser  #打开浏览器
'''手动安装 talib 去https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 下载对应的版本“TA_Lib‑0.4.19‑cp37‑cp37m‑win_amd64.whl”  然后 pip3 install TA_Lib‑0.4.19‑cp37‑cp37m‑win_amd64.whl'''
# import  talib   #Technical Analysis Library”, 即技术分析库 是Python金融量化的高级库，涵盖了150多种股票、期货交易软件中常用的技术分析指标，如MACD、RSI、KDJ、动量指标、布林带等等。
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec#分割子图
# import mpl_finance as mpf        # python中可以用来画出蜡烛图、线图的分析工具，目前已经从matplotlib中独立出来，非常适合用来画K线
import pymysql

pro = ts.pro_api('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')
ts.set_token('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')

database='stock'
tablename='stockopendata'
configfile='./config/mysqlconfig.json'
dpath = 'C:\\十档行情\\T0002\\signals\\signals_user_9603\\'

#获取南向数据总页数
def get_pages(headers,url,params):
    response=req.get(url=url,headers=headers,params=params).text
    #print(response)
    regx='pages:(\d{0,3})'
    pages=re.findall(regx,response)[0]
    #print(pages)
    return int(pages)

#写文件
def WriteData(southdatainfos):
    southdatafile = '南向资金数据.txt'
    with open(southdatafile, 'w', encoding='utf-8') as fw:
        fw.write(str(southdatainfos))

#获取所有南向资金数据
def getsouth():
    #url='http://data.eastmoney.com/hsgtcg/lz.html'
    url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh - CN, zh;    q = 0.9, en;    q = 0.8    ',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Cookie': 'pgv_pvi=3794568192; _qddaz=QD.6ofmf2.j6jr4m.kat8wucp; ct=u_GCXp_V0BUfw6EE3hFHtqMglz3afgkppJcv5vbFImFCEcWBrdbJ1czxMgSRvdgdMHMxnKracqlOZgxC4VNfwrkiwCCnYCNVFUzHMie-NyeUGcc8-NdJwvaXLimNiEt9gsOQO3q161JU2fTSAHZYRo5byr67JKvMwuA_2qSbhls; ut=FobyicMgeV5ghfUPKWOH5wak5fe7PCdYa2maZFrymrOdfN-wAEFtpNp1MzH070EBSmKRLG6vmIcYwEk2SvuUDiGwHB7BHzpaN3m4xMthhPoNqi89FTByaNH4MkRCfEYW4JX960vY0ITlmRY-cPk1PQzTvxCYnVj0Ey0NtYOnUdj24K9O1_tKWeyEDf1k_bIV6hcX360Qn8yYsWTrETZTzGYR7tn62AgnDFAq58DbSa3StLkggc5c7wB94try8c_WEpaHHyl5rA7BBAJZkje3dZ7Q7pZSUWri; pi=3323115305075326%3bc3323115305075326%3b%e8%82%a1%e5%8f%8bjHWZa22110%3bAc4gMB%2bahzpZU8kVvDCm4%2f9QLFcpRepVrDlj4DSAFvQS9L41u5PjbhW1g0ATNFBs2U6jdaiAi0v97coryIUwYaBWyHAUTbi1GDBZdDmkrBugnCGTBDTgPjXURUbrtmze597viYIL2RjHQTBKDzTIQqxuco%2b4pIMvD3B%2f2gF3Z2HSKCRGXGX%2bMcFxewJmIXD8wOJYtqii%3bM4Rnsdjx0lNLDrlCNBv6VhW13wgvkjpsoKd52WM1JsrPCSqUd%2fySTvks6nwUjCNsGby4fYU2Y%2bbjGtRBVly22B%2bqdAhoqGh6XrZIWQGX4LDnpd4CKtckek2Rlq7r9qjcQSdzcprF%2bmmkr9EqKBQVnmt9ppYRhg%3d%3d; uidal=3323115305075326%e8%82%a1%e5%8f%8bjHWZa22110; sid=126018279; _ga=GA1.2.1363410539.1596117007; em_hq_fls=js; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; emshistory=%5B%22%E4%BA%BA%E6%B0%94%E6%8E%92%E8%A1%8C%E6%A6%9C%22%2C%22%E6%AF%94%E4%BA%9A%E8%BF%AA%E4%BA%BA%E6%B0%94%E6%8E%92%E5%90%8D%22%2C%22%E5%9F%BA%E9%87%91%E6%8E%92%E8%A1%8C%22%2C%22%E8%BF%913%E4%B8%AA%E6%9C%88%E8%B7%8C%E5%B9%85%E6%9C%80%E5%A4%A7%E7%9A%84%E5%9F%BA%E9%87%91%22%2C%22%E5%85%BB%E8%80%81%E9%87%91%E6%8C%81%E8%82%A1%E5%8A%A8%E5%90%91%E6%9B%9D%E5%85%89%22%2C%22%E5%A4%96%E7%9B%98%E6%9C%9F%E8%B4%A7%22%2C%22A50%22%2C%22%E6%81%92%E7%94%9F%E6%B2%AA%E6%B7%B1%E6%B8%AF%E9%80%9A%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4A%22%2C%22%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4%22%5D; vtpst=%7c; HAList=d-hk-00288%2Cd-hk-00772%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Ca-sz-002008-%u5927%u65CF%u6FC0%u5149%2Ca-sz-002739-%u4E07%u8FBE%u7535%u5F71%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Cd-hk-00981%2Ca-sz-002082-%u4E07%u90A6%u5FB7%2Ca-sz-300511-%u96EA%u6995%u751F%u7269; st_si=85201197981579; cowCookie=true; waptgshowtime=2021121; qgqp_b_id=3a2c1ce1f45a81a3fa7cc2fbad8e2a24; st_asi=delete; intellpositionL=581px; st_pvi=03400063938128; st_sp=2020-05-23%2013%3A48%3A35; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=60; st_psi=2021012310245852-113300303605-1019447906; intellpositionT=2133.55px'
    }
    params = {'type': 'HSGTHDSTA',
              'token': '894050c76af8597a853f5b408b759f5d',
              'filter': '(MARKET=\'S\')',
              'st': 'HDDATE',
              'sr': -1,
              'p': 1,
              'ps': 50,
              'js': 'var DYCpZajM={pages:(tp),data:(x)}',
              'rt': '53712406'}
    #获取北向数据总页数
    pages=get_pages(headers,url,params)
    #print(pages)
    southdatainfos=[]
    for i in range(1,pages+1,1):   #南向数据每天只有10页的数据量(取总量)
        try:
            params = {'type': 'HSGTHDSTA',
                     'token': '894050c76af8597a853f5b408b759f5d',
                     'filter': '(MARKET=\'S\')',
                     'st': 'HDDATE',
                     'sr': -1,
                     'p': i,
                     'ps': 50,
                     'js': 'var DYCpZajM={pages:(tp),data:(x)}',
                     'rt': '53712406'}

            response=req.get(url=url,headers=headers,params=params)
            bstext=bs4.BeautifulSoup(response.content,'lxml')
            tempdata = bstext.find_all('p')
            temp = str(tempdata)
            regex = 'data:(.*?)}</p>'
            jsondata=str(re.findall(regex,temp,re.M))
            #print((jsondata))
            data=jsondata.replace('\\r\\n','',-1).replace('},','}},',-1).replace('[\'[','',-1).replace(']\']','',-1)
            listdata=data.split('},',-1)
            header = ['日期', '股票代码 ', '股票名称 ', '持股数亿', '占比', '收盘价  ', '当日涨跌幅  ', '持股市值亿  ', '一日市值变化亿', '五日市值变化亿', '十日市值变化亿']
            #print(len(listdata))
            '''data: [{
                "HDDATE": "2020-12-30T00:00:00", 日期
                "HKCODE": "1000145950",
                "SCODE": "00700",  代码
                "SNAME": "腾讯控股", 名称
                "SHAREHOLDSUM": 425931727.0, 持股数
                "SHARESRATE": 4.43,占比
                "CLOSEPRICE": 559.5,收盘价
                "ZDF": 5.4665,当日涨跌幅
                "SHAREHOLDPRICE": 238308801256.5, 持股市值
                "SHAREHOLDPRICEONE": 19102759903.0,一日市值变化
                "SHAREHOLDPRICEFIVE": 2113479276.5,五日市值变化
                "SHAREHOLDPRICETEN": 3843934536.5,十日市值变化   '''
            southdatainfos.append(listdata)
            time.sleep(1)
        except BaseException as BE:
            print(BE)
            continue
    #print(jsondata)
    print('所有南向数据获取成功！！')
    #将数据写到文件，以便读取使用，免得每次都要去网上爬，造成大量访问
    WriteData(southdatainfos)
    return southdatainfos
#写数据库
def insertdb (southdatainfos):

    if len(southdatainfos)==0:
        return
    conn = db.dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #由于每次取的是全量数据，先将表清空
    sql1='delete from southdataanly'
    cursor.execute(sql1)
    conn.commit()

    # 执行的sql语句
    sql = '''insert into southdataanly (HDDATE,SCODE,SNAME,SHAREHOLDSUM,SHARESRATE,CLOSEPRICE,ZDF,SHAREHOLDPRICE,SHAREHOLDPRICEONE,SHAREHOLDPRICEFIVE,SHAREHOLDPRICETEN) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    for datalist in southdatainfos:
        for row in datalist:  # 依次获取每一行数据
            try:
                jsdata = json.loads(row)
                HDDATE = str(jsdata['HDDATE'])[0:10]
                SCODE = jsdata['SCODE']
                SNAME = jsdata['SNAME']
                SHAREHOLDSUM = format(jsdata['SHAREHOLDSUM'] / 100000000, '.3f')
                SHARESRATE = jsdata['SHARESRATE']
                CLOSEPRICE = jsdata['CLOSEPRICE']
                ZDF = jsdata['ZDF']
                SHAREHOLDPRICE = format(jsdata['SHAREHOLDPRICE'] / 100000000, '.3f')
                SHAREHOLDPRICEONE = format(jsdata['SHAREHOLDPRICEONE'] / 100000000, '.3f')
                SHAREHOLDPRICEFIVE = format(jsdata['SHAREHOLDPRICEFIVE'] / 100000000, '.3f')
                SHAREHOLDPRICETEN = format(jsdata['SHAREHOLDPRICETEN'] / 100000000, '.3f')
                values = (
                HDDATE, SCODE, SNAME, SHAREHOLDSUM, SHARESRATE, CLOSEPRICE, ZDF, SHAREHOLDPRICE, SHAREHOLDPRICEONE,
                SHAREHOLDPRICEFIVE, SHAREHOLDPRICETEN)
                cursor.execute(sql, values)
                # print(values,sql)
            except BaseException as be:
                print(be)
                continue
        conn.commit()
    conn.commit()
    conn.close()
    print('入库成功！！！')

#按条件查询持续比例与持股市值
def selectdb(**kwords):      #**kwords :表示可以传入多个键值对， *kwords:表示可传入多个参数
    conditions=str(kwords).strip('{').strip('}').replace(':','=',1).replace('\'','',2)
    print(conditions)
    conn = db.dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行的sql语句
    sql = '''select HDDATE,SCODE,SNAME,SHAREHOLDSUM,SHARESRATE,CLOSEPRICE,ZDF,SHAREHOLDPRICE,SHAREHOLDPRICEONE,SHAREHOLDPRICEFIVE,SHAREHOLDPRICETEN from  southdataanly  '''
    sql=sql+ 'where '+ conditions + '  order by HDDATE '
    print(sql)
    cursor.execute(sql)
    resultset=cursor.fetchall()
    return  resultset
#获取日线数据
def get_stock_dateData(stockcode,start_date,end_date):
    if stockcode[0:2] =='600' or stockcode[0:2]=='68':
        stockcode=stockcode+'.SH'
    else:
        stockcode =  stockcode+'.SZ'
    #从tushare 获取日线数据
    df = pro.daily(ts_code=stockcode, start_date=start_date,end_date=end_date)
    df=df.sort_values(by=['trade_date'],ascending=True)  #按日期升序
    #从baostock获取数据
    # lg = bs.login()
    # rs = bs.query_history_k_data_plus(stockcode,
    #                                   "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    #                                   start_date=start_date, end_date=end_date,
    #                                   frequency="30m", adjustflag="3")
    # data_list = []
    # while (rs.error_code == '0') & rs.next():
    #     # 获取一条记录，将记录合并在一起
    #     data_list.append(rs.get_row_data())
    # result = pd.DataFrame(data_list, columns=rs.fields)

    #print(df)
    return df

#将查询到的数据分析后输出到html
def rendertohtml(resultset):
    header = ['日期', '股票代码 ', '股票名称 ', '持股数亿', '占比', '收盘价  ', '当日涨跌幅  ', '持股市值亿  ', '一日市值变化亿', '五日市值变化亿', '十日市值变化亿']
    tb = pt.PrettyTable()
    tb.field_names = header  # 设置表头
    tb.align = 'c'  # 对齐方式（c:居中，l居左，r:居右）

    c = Line()
    x = ['持股占比']
    name=''
    HDDATELIST=[]
    SHAREHOLDSUMlist=[]  #持股数
    SHARESRATElist=[]#持股占比
    SHAREHOLD=[]#持股数量
    #取出占比数据
    for data in resultset:
        HDDATE=data['HDDATE']
        #HDDATE = datetime.datetime.strptime(HDDATE1, '%Y-%m-%d').strftime('%Y%m%d')
        HDDATELIST.append(HDDATE)

        SCODE = data['SCODE']
        SHAREHOLDSUM=data['SHAREHOLDSUM']
        SHAREHOLDSUMlist.append(SHAREHOLDSUM)

        SNAME = data['SNAME']
        SHARESRATE = data['SHARESRATE']
        SHARESRATElist.append(SHARESRATE)

        CLOSEPRICE = data['CLOSEPRICE']
        ZDF = data['ZDF']
        SHAREHOLDPRICE = format(data['SHAREHOLDPRICE'], '.3f')
        SHAREHOLDPRICEONE = format(data['SHAREHOLDPRICEONE'] , '.3f')
        SHAREHOLDPRICEFIVE = format(data['SHAREHOLDPRICEFIVE'] , '.3f')
        SHAREHOLDPRICETEN = format(data['SHAREHOLDPRICETEN'] , '.3f')

        tb.add_row(
            [HDDATE, SCODE, SNAME, SHAREHOLDSUM, SHARESRATE, CLOSEPRICE, ZDF, SHAREHOLDPRICE, SHAREHOLDPRICEONE,
             SHAREHOLDPRICEFIVE, SHAREHOLDPRICETEN])

    OUTFILE='南向资金_'+SNAME+'.html'
    #print(SHARESRATE)
    x1=HDDATELIST
    y1 = SHARESRATElist #将占比数据设置为y轴
    y2=SHAREHOLDSUMlist
    #y2 = [1000, 300, 500]
    #bar = Bar()
    # 设置x轴
    c.add_xaxis(xaxis_data=x)
    c.add_xaxis(xaxis_data=x1)
    # 设置y轴
    c.add_yaxis(series_name='持股百分比', y_axis=y1)
    c.add_yaxis(series_name='持股数量亿', y_axis=y2)
    c.set_global_opts(title_opts=opts.TitleOpts(title='南向资金持股分析:  '+SNAME))
    # 生成html文件
    c.render(path=OUTFILE)
    #如果要输出柱图
    '''
    bar = Bar()
    然后将c 换成bar
    '''
    #将数据也输出到文件
    s=tb.get_html_string()
    with open(OUTFILE,'a+',encoding='utf-8') as fw:
        fw.write(s)
    fw.close()
    #outfile='file://'+OUTFILE

    webbrowser.open(OUTFILE)#调用浏览器打开文件
if __name__ == '__main__':
    # southdata=getsouth() #获取南向数据 ，获取数据后，将它注释掉
    # insertdb (southdata) #将南向数据写表  获取数据后，将它注释掉
    # SNAME='腾讯控股'
    SNAME='建设银行'
    SNAME='小米集团 - W'
    var = sys.argv  # 可以接收从外部传入参数
    if len(var)>1:
        SNAME=var[1]
        if var[1].isdigit():
            resultset = selectdb(SCODE=SNAME)  # 按名称查询南向资金占比
        else:
            resultset=selectdb(SNAME=SNAME)#按名称查询南向资金占比
        rendertohtml(resultset)
    else:
        resultset = selectdb(SNAME='腾讯控股')  # 按名称查询南向资金占比
        rendertohtml(resultset)



'''
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
'''