import os,time,re,bs4
import requests as req
import json,datetime
import pymysql
import struct as st
import tushare as ts
from lxml import etree

class writeToTdx():
    filepath=''
    database = 'stock'
    tablename = 'northdataAnaly'
    configfile = './config/mysqlconfig.json'
    percentDpath = 'C:\\十档行情\\T0002\\signals\\signals_user_9602\\'
    oneTrunDpath = 'C:\\十档行情\\T0002\\signals\\signals_user_9604\\'
    pro = None
    jsoncontent = None
    stockcode = ''

    def __init__(self):
        self.jsoncontent = self.get_config()
        self.pro = ts.pro_api(self.jsoncontent['tushare'])

    #########编码成通达信可识别的数据
    def stockEncode(self, HdDate, SCode):
        seek = 4
        text1 = st.pack('I', int(HdDate))
        # print(text1)
        text2 = st.pack('f', float(SCode))
        # print(text2)
        return text1 + text2

    def get_config(self):
        with open(self.configfile, encoding="utf-8") as f:
            jsoncontent = json.load(f)
        f.close()
        return jsoncontent

    def dbconnect(self):
        jsoncontent = self.get_config()
        conn = pymysql.connect(jsoncontent['host'], jsoncontent['user'], jsoncontent['password'],
                               jsoncontent['database'], charset='utf8')
        return conn

    #查询有北资数据的股票列表
    def get_Northstocklist(self):
        conn=self.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        stocklist=[]
        sql='''select distinct(SCODE) as scode from  northdataAnaly'''
        cursor.execute(sql)
        result=cursor.fetchall()
        if result:
            for data in result:
                stocklist.append(data['scode'])
            return stocklist
        else:
            print('无数据！！')
            return None
            # return None
        cursor.close()
        conn.close()
        return stocklist

    # 获取当日更新的北向数据
    def getNownorth(self):
        header = ['日期', '股票代码 ', '股票名称 ', '板块', '占流通股%', '最新价  ', '涨跌幅  ', '今日持股股数亿  ', '今日持股市值亿', '占流通股本%',
                  '今日持股占总股本',
                  '市值增幅', '市值增幅%']
        # url='http://data.eastmoney.com/hsgtcg/list.html'
        url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get'
        northdataAnalyinfos = []
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh - CN, zh;    q = 0.9, en;    q = 0.8    ',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Cookie': 'Cookie: pgv_pvi=3794568192; _qddaz=QD.6ofmf2.j6jr4m.kat8wucp; ct=u_GCXp_V0BUfw6EE3hFHtqMglz3afgkppJcv5vbFImFCEcWBrdbJ1czxMgSRvdgdMHMxnKracqlOZgxC4VNfwrkiwCCnYCNVFUzHMie-NyeUGcc8-NdJwvaXLimNiEt9gsOQO3q161JU2fTSAHZYRo5byr67JKvMwuA_2qSbhls; ut=FobyicMgeV5ghfUPKWOH5wak5fe7PCdYa2maZFrymrOdfN-wAEFtpNp1MzH070EBSmKRLG6vmIcYwEk2SvuUDiGwHB7BHzpaN3m4xMthhPoNqi89FTByaNH4MkRCfEYW4JX960vY0ITlmRY-cPk1PQzTvxCYnVj0Ey0NtYOnUdj24K9O1_tKWeyEDf1k_bIV6hcX360Qn8yYsWTrETZTzGYR7tn62AgnDFAq58DbSa3StLkggc5c7wB94try8c_WEpaHHyl5rA7BBAJZkje3dZ7Q7pZSUWri; pi=3323115305075326%3bc3323115305075326%3b%e8%82%a1%e5%8f%8bjHWZa22110%3bAc4gMB%2bahzpZU8kVvDCm4%2f9QLFcpRepVrDlj4DSAFvQS9L41u5PjbhW1g0ATNFBs2U6jdaiAi0v97coryIUwYaBWyHAUTbi1GDBZdDmkrBugnCGTBDTgPjXURUbrtmze597viYIL2RjHQTBKDzTIQqxuco%2b4pIMvD3B%2f2gF3Z2HSKCRGXGX%2bMcFxewJmIXD8wOJYtqii%3bM4Rnsdjx0lNLDrlCNBv6VhW13wgvkjpsoKd52WM1JsrPCSqUd%2fySTvks6nwUjCNsGby4fYU2Y%2bbjGtRBVly22B%2bqdAhoqGh6XrZIWQGX4LDnpd4CKtckek2Rlq7r9qjcQSdzcprF%2bmmkr9EqKBQVnmt9ppYRhg%3d%3d; uidal=3323115305075326%e8%82%a1%e5%8f%8bjHWZa22110; sid=126018279; _ga=GA1.2.1363410539.1596117007; em_hq_fls=js; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; emshistory=%5B%22%E4%BA%BA%E6%B0%94%E6%8E%92%E8%A1%8C%E6%A6%9C%22%2C%22%E6%AF%94%E4%BA%9A%E8%BF%AA%E4%BA%BA%E6%B0%94%E6%8E%92%E5%90%8D%22%2C%22%E5%9F%BA%E9%87%91%E6%8E%92%E8%A1%8C%22%2C%22%E8%BF%913%E4%B8%AA%E6%9C%88%E8%B7%8C%E5%B9%85%E6%9C%80%E5%A4%A7%E7%9A%84%E5%9F%BA%E9%87%91%22%2C%22%E5%85%BB%E8%80%81%E9%87%91%E6%8C%81%E8%82%A1%E5%8A%A8%E5%90%91%E6%9B%9D%E5%85%89%22%2C%22%E5%A4%96%E7%9B%98%E6%9C%9F%E8%B4%A7%22%2C%22A50%22%2C%22%E6%81%92%E7%94%9F%E6%B2%AA%E6%B7%B1%E6%B8%AF%E9%80%9A%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4A%22%2C%22%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4%22%5D; vtpst=%7c; HAList=d-hk-00288%2Cd-hk-00772%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Ca-sz-002008-%u5927%u65CF%u6FC0%u5149%2Ca-sz-002739-%u4E07%u8FBE%u7535%u5F71%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Cd-hk-00981%2Ca-sz-002082-%u4E07%u90A6%u5FB7%2Ca-sz-300511-%u96EA%u6995%u751F%u7269; cowCookie=true; st_si=40836386960323; waptgshowtime=2021126; qgqp_b_id=3a2c1ce1f45a81a3fa7cc2fbad8e2a24; intellpositionL=345px; st_asi=delete; st_pvi=03400063938128; st_sp=2020-05-23%2013%3A48%3A35; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=48; st_psi=20210126213702703-113300303605-1327257583; intellpositionT=1940.09px'
        }
        # date1 =time.strftime("%Y-%m-%d", time.localtime())
        # 从东方财富网获取要取数据的日期
        date1 = self.get_page_newdate()
        params = {'type': 'HSGTHDSTA',
                  'token': '70f12f2f4f091e459a279469fe49eca5',
                  'st': 'HDDATE,SHAREHOLDPRICE',
                  'sr': 3,
                  'p': 1,
                  'ps': 50,
                  'js': 'var vaNPyqhg={pages:(tp),data:(x)}',
                  'filter': '(MARKET in (\'001\',\'003\'))(HDDATE=^' + date1 + '^)',
                  'rt': '53759764'}
        # print(params)
        content = req.get(url=url, headers=headers, params=params).text
        # print(content)
        regex1 = 'pages:(\d{0,2})'
        maxpage = int(re.findall(regex1, content, re.M)[0])
        print('共有  %d  页数据需要更新，请稍等......' % maxpage)

        for i in range(1, maxpage + 1, 1):  # 北向资金数据每天有30页

            params = {'type': 'HSGTHDSTA',
                      'token': '70f12f2f4f091e459a279469fe49eca5',
                      'st': 'SHAREHOLDPRICEONE',
                      'sr': -1,
                      'p': i,
                      'ps': 50,
                      'js': 'var TpSlNIMe={pages:(tp),data:(x)}',
                      'filter': '(MARKET in (\'001\',\'003\'))(HDDATE=^' + date1 + '^)',
                      'rt': '53722283'}
            # print(params)
            try:
                response = req.get(url=url, headers=headers, params=params)
            except BaseException as BE:
                time.sleep(2)
                count = 0
                while count < 3:
                    response = req.get(url=url, headers=headers, params=params)
                    if response.status_code != 200:

                        count += 1
                        print('第%s 次 第%s 页数据获取异常,重试中！！！' % (count, i))
                        time.sleep(2)
                    else:
                        break

            bstext = bs4.BeautifulSoup(response.content, 'lxml')
            tempdata = bstext.find_all('p')
            temp = str(tempdata)
            regex = 'data:(.*?)}</p>'
            jsondata = str(re.findall(regex, temp, re.M))
            data = jsondata.replace('\\r\\n', '', -1).replace('},', '}},', -1).replace('[\'[', '', -1).replace(
                ']\']', '', -1)
            listdata = data.split('},', -1)[::]
            # print(listdata)
            northdataAnalyinfos.append(listdata)
            time.sleep(1)
        return northdataAnalyinfos

    # 将当日获取的数据插入表
    def insertNowdata(self, northdataAnalyinfos):
        if len(northdataAnalyinfos) == 0:
            return
        # print(northdataAnalyinfos)
        conn = self.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行的sql语句
        sql = '''insert into northdataanaly (HDDATE,SCODE,SNAME,SHAREHOLDSUM,SHARESRATE,CLOSEPRICE,ZDF,SHAREHOLDPRICE,SHAREHOLDPRICEONE,SHAREHOLDPRICEFIVE,SHAREHOLDPRICETEN) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        for datalist in northdataAnalyinfos:
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
                        HDDATE, SCODE, SNAME, SHAREHOLDSUM, SHARESRATE, CLOSEPRICE, ZDF, SHAREHOLDPRICE,
                        SHAREHOLDPRICEONE,
                        SHAREHOLDPRICEFIVE, SHAREHOLDPRICETEN)
                    cursor.execute(sql, values)
                    # print(values,sql)
                except BaseException as be:
                    print(be)
                    continue
            conn.commit()
        conn.commit()
        conn.close()

    # 按条件查询比例与持股市值
    def select_NorthDataFromdb(self, scode):  # **kwords :表示可以传入多个键值对， *kwords:表示可传入多个参数
        # conditions = str(kwords).strip('{').strip('}').replace(':', '=', 1).replace('\'', '', 2)
        # print(conditions)
        conn = conn = self.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行的sql语句
        sql = '''select HDDATE,SCODE,SNAME,SHAREHOLDSUM,SHARESRATE,CLOSEPRICE,ZDF ,SHAREHOLDPRICE ,SHAREHOLDPRICEONE ,SHAREHOLDPRICEFIVE ,SHAREHOLDPRICETEN from  northdataAnaly  '''
        sql = sql + ' where  scode=\''+scode  +'\' order by HDDATE '

        cursor.execute(sql)
        resultset = cursor.fetchall()
        cursor.close()
        conn.close()
        if resultset:
            return resultset
        else:
            print('未查询到数据')
            return None

    ###################处理个股北资占比数据写通达信文件
    def writeNorthDataPercentToTdx(self, listdata, percentDpath, SCode):
        # 确定要写的目标文件名：
        if SCode[0:2] == '60' or SCode[0:3] == '688' or SCode[0:3] == '880':
            dfilename = percentDpath + '1_' + SCode + '.dat'
        elif SCode[0:3] == '300' or SCode[0:2] == '00':
            dfilename = percentDpath + '0_' + SCode + '.dat'
        fw1 = open(dfilename, 'wb')
        templist = []
        for data in listdata:
            HdDate = str(data['HDDATE'])[0:10]
            HdDate = datetime.datetime.strptime(HdDate, '%Y-%m-%d').strftime('%Y%m%d')
            SCode = str(data['SCODE'])
            SharesRate = data['SHARESRATE']
            SHAREHOLDPRICEONE =data['SHAREHOLDPRICEONE']
            dict = {'HdDate': HdDate, 'SharesRate': SharesRate, 'SHAREHOLDPRICEONE': SHAREHOLDPRICEONE}
            templist.append(dict)
        # templist = templist[::-1]  # list 反向（由于取的数据默认是降序，但写入通达信需要升序）
        for line in templist:
            HdDate = line['HdDate']
            SharesRate = line['SharesRate']
            fflowdata = self.stockEncode(HdDate, SharesRate)
            fw1.write(fflowdata)
        fw1.close()
        print('文件：%s 写入成功!' % dfilename)

    #处理个股北资持股市变到写通达信文件
    def writeNorthDataOneTrunToTdx(self, listdata, oneTrunDpath, SCode):
        # 确定要写的目标文件名：
        if SCode[0:2] == '60' or SCode[0:3] == '688' or SCode[0:3] == '880':
            dfilename = oneTrunDpath + '1_' + SCode + '.dat'
        elif SCode[0:3] == '300' or SCode[0:2] == '00':
            dfilename = oneTrunDpath + '0_' + SCode + '.dat'
        fw1 = open(dfilename, 'wb')
        templist = []
        for data in listdata:
            HdDate = str(data['HDDATE'])[0:10]
            HdDate = datetime.datetime.strptime(HdDate, '%Y-%m-%d').strftime('%Y%m%d')
            SCode = str(data['SCODE'])
            SharesRate = data['SHARESRATE']
            SHAREHOLDPRICEONE = data['SHAREHOLDPRICEONE']
            dict = {'HdDate': HdDate, 'SharesRate': SharesRate, 'SHAREHOLDPRICEONE': SHAREHOLDPRICEONE}
            templist.append(dict)
        # templist = templist[::-1]  # list 反向（由于取的数据默认是降序，但写入通达信需要升序）
        for line in templist:
            HdDate = line['HdDate']
            SHAREHOLDPRICEONE = line['SHAREHOLDPRICEONE']
            fflowdata = self.stockEncode(HdDate, SHAREHOLDPRICEONE)
            fw1.write(fflowdata)
        fw1.close()
        print('文件：%s 写入成功!' % dfilename)

    # 获取最新的数据日期
    def get_page_newdate(self):
        url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?&type=HSGTTRDT&st=DATE&sr=-1&token=894050c76af8597a853f5b408b759f5d&p=1&ps=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
        response = req.get(url=url, headers=headers).text
        regx='(\d{4}-\d{2}-\d{2})'
        date = re.findall(regx, response,re.M)[0]
        return str(date)

    # 获取表中最新的日期
    def getdb_maxdate(self):
        sql = 'select max(HDDATE) as "HDDATE" from northdataAnaly '
        conn = conn = self.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        for data in result:
            data1 = data['HDDATE']
            print(data1)
        cursor.close()
        conn.close()
        if data1 is None:
            print('表中无数据，请更新数据')
            return None
        return str(data1)

    # 比较数据是否为最新的
    def compare_Date(self):
        isnewdate = True
        pagedate = self.get_page_newdate()
        dbdate = self.getdb_maxdate()
        if dbdate is None:
            return False
        if pagedate > dbdate:
            isnewdate = False
            return isnewdate
        else:
            isnewdate = True
            return isnewdate

    #更新北向数据到表中
    def update_NorthDatatoDB(self):
        isnew = self.compare_Date()  # 判断是否要更新数据
        if isnew:
            print('数据已是最新')
        else:
            print('数据更新中！')
            northdataAnalyinfos = self.getNownorth()
            self.insertNowdata(northdataAnalyinfos)
            print('数据更新成功！！！')

    #一键写通达信
    def FullDataWritetoFile(self):
        stocklist=self.get_Northstocklist()
        if stocklist is None:
            print('无数据！！！')
        for stock in stocklist:
            stockData=self.select_NorthDataFromdb(stock)
            if stockData:
                self.writeNorthDataPercentToTdx( stockData, self.percentDpath, stock)
                self.writeNorthDataOneTrunToTdx(stockData, self.oneTrunDpath, stock)
            else:
                print('未查询到数据！')
                continue
if __name__ == '__main__':
    writefile=writeToTdx()
    writefile.update_NorthDatatoDB()
    writefile.FullDataWritetoFile()



    # 持股市值变化数据一键写通达信