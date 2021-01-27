import requests as req
import re
import bs4
import json
from lxml import etree
import prettytable as pt   #格式化成表格输出到html文件
from pyecharts.charts import Bar, Page,Line
from pyecharts import options as opts
import datetime
import pandas as pd
import sys

#获取所有南向资金数据
def getnorth(code):
    url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get'
    northdatainfos=[]
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh - CN, zh;    q = 0.9, en;    q = 0.8    ',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Cookie': 'pgv_pvi=3794568192; _qddaz=QD.6ofmf2.j6jr4m.kat8wucp; ct=u_GCXp_V0BUfw6EE3hFHtqMglz3afgkppJcv5vbFImFCEcWBrdbJ1czxMgSRvdgdMHMxnKracqlOZgxC4VNfwrkiwCCnYCNVFUzHMie-NyeUGcc8-NdJwvaXLimNiEt9gsOQO3q161JU2fTSAHZYRo5byr67JKvMwuA_2qSbhls; ut=FobyicMgeV5ghfUPKWOH5wak5fe7PCdYa2maZFrymrOdfN-wAEFtpNp1MzH070EBSmKRLG6vmIcYwEk2SvuUDiGwHB7BHzpaN3m4xMthhPoNqi89FTByaNH4MkRCfEYW4JX960vY0ITlmRY-cPk1PQzTvxCYnVj0Ey0NtYOnUdj24K9O1_tKWeyEDf1k_bIV6hcX360Qn8yYsWTrETZTzGYR7tn62AgnDFAq58DbSa3StLkggc5c7wB94try8c_WEpaHHyl5rA7BBAJZkje3dZ7Q7pZSUWri; pi=3323115305075326%3bc3323115305075326%3b%e8%82%a1%e5%8f%8bjHWZa22110%3bAc4gMB%2bahzpZU8kVvDCm4%2f9QLFcpRepVrDlj4DSAFvQS9L41u5PjbhW1g0ATNFBs2U6jdaiAi0v97coryIUwYaBWyHAUTbi1GDBZdDmkrBugnCGTBDTgPjXURUbrtmze597viYIL2RjHQTBKDzTIQqxuco%2b4pIMvD3B%2f2gF3Z2HSKCRGXGX%2bMcFxewJmIXD8wOJYtqii%3bM4Rnsdjx0lNLDrlCNBv6VhW13wgvkjpsoKd52WM1JsrPCSqUd%2fySTvks6nwUjCNsGby4fYU2Y%2bbjGtRBVly22B%2bqdAhoqGh6XrZIWQGX4LDnpd4CKtckek2Rlq7r9qjcQSdzcprF%2bmmkr9EqKBQVnmt9ppYRhg%3d%3d; uidal=3323115305075326%e8%82%a1%e5%8f%8bjHWZa22110; sid=126018279; _ga=GA1.2.1363410539.1596117007; em_hq_fls=js; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; emshistory=%5B%22%E4%BA%BA%E6%B0%94%E6%8E%92%E8%A1%8C%E6%A6%9C%22%2C%22%E6%AF%94%E4%BA%9A%E8%BF%AA%E4%BA%BA%E6%B0%94%E6%8E%92%E5%90%8D%22%2C%22%E5%9F%BA%E9%87%91%E6%8E%92%E8%A1%8C%22%2C%22%E8%BF%913%E4%B8%AA%E6%9C%88%E8%B7%8C%E5%B9%85%E6%9C%80%E5%A4%A7%E7%9A%84%E5%9F%BA%E9%87%91%22%2C%22%E5%85%BB%E8%80%81%E9%87%91%E6%8C%81%E8%82%A1%E5%8A%A8%E5%90%91%E6%9B%9D%E5%85%89%22%2C%22%E5%A4%96%E7%9B%98%E6%9C%9F%E8%B4%A7%22%2C%22A50%22%2C%22%E6%81%92%E7%94%9F%E6%B2%AA%E6%B7%B1%E6%B8%AF%E9%80%9A%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4A%22%2C%22%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4%22%5D; vtpst=%7c; HAList=d-hk-00288%2Cd-hk-00772%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Ca-sz-002008-%u5927%u65CF%u6FC0%u5149%2Ca-sz-002739-%u4E07%u8FBE%u7535%u5F71%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Cd-hk-00981%2Ca-sz-002082-%u4E07%u90A6%u5FB7%2Ca-sz-300511-%u96EA%u6995%u751F%u7269; st_si=85201197981579; cowCookie=true; waptgshowtime=2021121; qgqp_b_id=3a2c1ce1f45a81a3fa7cc2fbad8e2a24; st_asi=delete; intellpositionL=581px; st_pvi=03400063938128; st_sp=2020-05-23%2013%3A48%3A35; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=60; st_psi=2021012310245852-113300303605-1019447906; intellpositionT=2133.55px'
    }
    params = {'type': 'HSGTHDSTA',
                'token': '70f12f2f4f091e459a279469fe49eca5',
                'filter':' (SCODE=\''+code+'\')',
                'st': 'HDDATE',
                'sr': -1,
                'p': 1,
                'ps': 50,
                'js': 'var nLvHRzKi={pages:(tp),data:(x)}',
                'rt': '53722197'}
    #print(params)
    response=req.get(url=url,headers=headers,params=params).text
    #print(response.url)
    #print(response.text+'\n----------------------------------------')

    regex = r'data:\[({.*?)\]}'
    jsondata=str(re.findall(regex,response))
    #print((jsondata))

    data=jsondata.replace('[\'','',-1).replace('\']','',-1).replace('},','}},',-1)
    #print(len(data))
    listdata=data.split('},',-1)
    #print(len(listdata))
   #print(listdata)
    header = ['日期', '股票代码 ', '股票名称 ', '持股数亿', '占比', '收盘价  ', '当日涨跌幅  ', '持股市值亿  ', '一日市值变化亿', '五日市值变化亿', '十日市值变化亿']

    tb = pt.PrettyTable()
    tb.field_names = header  # 设置表头
    tb.align = 'l'  # 对齐方式（c:居中，l居左，r:居右）

    c = Line()
    x = ['持股占比']
    name=''
    HDDATElist=[]
    SHAREHOLDSUMlist=[]  #持股数
    SHARESRATElist=[]#持股占比
    #SHAREHOLDlist=[]#持股数量
    #print(listdata)
    for data in listdata:
        #print(data+'\n----------------------------------------')
        jsdata = json.loads(data)
        print(type(jsdata),jsdata)
        HDDATE = str(jsdata['HDDATE'])[0:10]
        HDDATE =datetime.datetime.strptime(HDDATE, '%Y-%m-%d').strftime('%Y%m%d')
        HDDATElist.append(HDDATE)

        SCODE = jsdata['SCODE']
        SNAME = jsdata['SNAME']

        SHAREHOLDSUM = format(jsdata['SHAREHOLDSUM'] / 100000000, '.3f')
        SHAREHOLDSUMlist.append(SHAREHOLDSUM)

        SHARESRATE = jsdata['SHARESRATE']
        SHARESRATElist.append(SHARESRATE)

        CLOSEPRICE = jsdata['CLOSEPRICE']
        ZDF = jsdata['ZDF']
        SHAREHOLDPRICE = format(jsdata['SHAREHOLDPRICE'] / 100000000, '.3f')
        SHAREHOLDPRICEONE = format(jsdata['SHAREHOLDPRICEONE'] / 100000000, '.3f')
        SHAREHOLDPRICEFIVE = format(jsdata['SHAREHOLDPRICEFIVE'] / 100000000, '.3f')
        SHAREHOLDPRICETEN = format(jsdata['SHAREHOLDPRICETEN'] / 100000000, '.3f')
        # # 打印结果
        # print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % (
        # date, code, name, kaipanhuanshuoz, kaipanjine, liangbi, xianliang, liutongsizhi, liutongguyi, xifenhangye))
        tb.add_row(
            [HDDATE,SCODE,SNAME,SHAREHOLDSUM,SHARESRATE,CLOSEPRICE,ZDF,SHAREHOLDPRICE,SHAREHOLDPRICEONE,SHAREHOLDPRICEFIVE,SHAREHOLDPRICETEN])


    x1 = HDDATElist[::-1]
    y1 = SHARESRATElist[::-1] # 将占比数据设置为y轴
    y2 = SHAREHOLDSUMlist[::-1]
    # y2 = [1000, 300, 500]
    # bar = Bar()
    # 设置x轴
    c.add_xaxis(xaxis_data=x)
    c.add_xaxis(xaxis_data=x1)
    # 设置y轴
    c.add_yaxis(series_name='持股百分比', y_axis=y1)
    c.add_yaxis(series_name='持股数量亿', y_axis=y2)
    c.set_global_opts(title_opts=opts.TitleOpts(title='北向资金持股分析:  ' + SNAME))
    # 生成html文件
    outfile = '北向资金_' + SNAME + '.html'
    c.render(path=outfile)
    # 如果要输出柱图
    '''
    bar = Bar()
    然后将c 换成bar
    '''
    s = tb.get_html_string() #

    fw = open(outfile, 'a+', encoding='utf-8')
    fw.write(s)  # 输出到文件
    fw.close()
    '''
        data: [{
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
    northdatainfos.append(listdata)
    #formatresults(listdata, header)#每一页写表

def get_stockcode(stockname):
    stocklist='./个股信息列表.txt'
    readata=pd.read_csv(stocklist,sep=',',header=0,names=['代码','名称'])
    for row in readata.iterrows():
        #print(row)
        if row[1]['名称']==stockname:
            return str(row[1]['代码'])
        else:
            continue

if __name__ == '__main__':
    '002044'
    '002179'
    var = sys.argv  # 可以接收从外部传入参数
    if len(var)>1:
        var1=var[1]
        code=get_stockcode(var1)
        getnorth(code) #实时查询北向资金
    else:
        code = get_stockcode('南大光电')
        getnorth(code)