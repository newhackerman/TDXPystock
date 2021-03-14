import os
import requests as req
import pandas as pd
import json,datetime
import pymysql
import struct as st
import tushare as ts

class writeToTdx():
    filepath=''
    database = 'stock'
    tablename = 'northdataAnaly'
    configfile = 'D:/mysqlconfig.json'
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



    # 按条件查询比例与持股市值
    def select_NorthDataFromdb(self, **kwords):  # **kwords :表示可以传入多个键值对， *kwords:表示可传入多个参数
        conditions = str(kwords).strip('{').strip('}').replace(':', '=', 1).replace('\'', '', 2)
        print(conditions)
        conn = conn = self.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行的sql语句
        sql = '''select HDDATE,SCODE,SNAME,SHAREHOLDSUM,SHARESRATE,CLOSEPRICE,ZDF ,SHAREHOLDPRICE ,SHAREHOLDPRICEONE ,SHAREHOLDPRICEFIVE ,SHAREHOLDPRICETEN from  northdataAnaly  '''
        sql = sql + 'where ' + conditions + '  order by HDDATE '
        print(sql)
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
        for tempdata in listdata:
            for row in tempdata:  # 依次获取每一行数据
                jsdata = json.loads(row)
                HdDate = str(jsdata['HDDATE'])[0:10]
                HdDate = datetime.datetime.strptime(HdDate, '%Y-%m-%d').strftime('%Y%m%d')
                SCode = str(jsdata['SCODE'])
                SharesRate = jsdata['SHARESRATE']
                SHAREHOLDPRICEONE = format(jsdata['SHAREHOLDPRICEONE'] / 100000000, '.3f')
                dict = {'HdDate': HdDate, 'SharesRate': SharesRate, 'SHAREHOLDPRICEONE': SHAREHOLDPRICEONE}
                templist.append(dict)
        templist = templist[::-1]  # list 反向（由于取的数据默认是降序，但写入通达信需要升序）
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
        for tempdata in listdata:
            for row in tempdata:  # 依次获取每一行数据
                jsdata = json.loads(row)
                HdDate = str(jsdata['HDDATE'])[0:10]
                HdDate = datetime.datetime.strptime(HdDate, '%Y-%m-%d').strftime('%Y%m%d')
                SCode = str(jsdata['SCODE'])
                SharesRate = jsdata['SHARESRATE']
                SHAREHOLDPRICEONE = format(jsdata['SHAREHOLDPRICEONE'] / 100000000, '.3f')
                dict = {'HdDate': HdDate, 'SharesRate': SharesRate, 'SHAREHOLDPRICEONE': SHAREHOLDPRICEONE}
                templist.append(dict)
        templist = templist[::-1]  # list 反向（由于取的数据默认是降序，但写入通达信需要升序）
        for line in templist:
            HdDate = line['HdDate']
            SHAREHOLDPRICEONE = line['SHAREHOLDPRICEONE']
            fflowdata = self.stockEncode(HdDate, SHAREHOLDPRICEONE)
            fw1.write(fflowdata)
        fw1.close()
        print('文件：%s 写入成功!' % dfilename)

    #一键写通达信

    def FullDataWritetoFile(self,Dpath):
        if os.path.exists(Dpath):
            path=Dpath
        else:
            os.mkdir(Dpath)

        stocklist=[]
        for stock in stocklist:
            pass
            stockData=self.select_NorthDataFromdb("scode='"+stock+"'")
            if stockData:
                pass
            else:
                print('未查询到数据！')
                continue




    # 持股市值变化数据一键写通达信