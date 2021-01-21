import bs4
import requests as req
import re,json
import prettytable as pt


def formatresults(listdata,header):
    #results   查询到的数据集
    #header   要输出的表头
    tb = pt.PrettyTable()
    tb.field_names=header #设置表头
    tb.align='l'  #对齐方式（c:居中，l居左，r:居右）
    #tb.sortby = "日期"
    #tb.set_style(pt.DEFAULT)
    #tb.horizontal_char = '*'
    for row in listdata:  # 依次获取每一行数据
        jsdata = json.loads(row)
        HdDate = str(jsdata['HdDate'])[0:10]
        SCode = jsdata['SCode']
        SName = jsdata['SName']
        HYName = jsdata['HYName']
        SharesRate = jsdata['SharesRate']
        NewPrice = jsdata['NewPrice']
        Zdf = jsdata['Zdf']
        ShareHold = format(jsdata['ShareHold']/100000000,'.3f')
        ShareSZ = format(jsdata['ShareSZ']/100000000,'.3f')
        LTZB = format(jsdata['LTZB']*100, '.3f')
        ZZB = format(jsdata['ZZB'] *100, '.3f')
        ShareSZ_Chg_One = format(jsdata['ShareSZ_Chg_One'] / 100000000, '.3f')
        ShareSZ_Chg_Rate_One = format(jsdata['ShareSZ_Chg_Rate_One']*100, '.3f')
        # # 打印结果
        # print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % (
        # date, code, name, kaipanhuanshuoz, kaipanjine, liangbi, xianliang, liutongsizhi, liutongguyi, xifenhangye))
        tb.add_row([HdDate,SCode,SName,HYName,SharesRate,NewPrice,Zdf,ShareHold,ShareSZ,LTZB,ZZB,ShareSZ_Chg_One,ShareSZ_Chg_Rate_One])
    print('记录条数：\t',len(listdata))
    s=tb.get_html_string()  #获取html格式
    outfile='./北向资金_'+HdDate+'.html'
    fw = open(outfile, 'w', encoding='utf-8')
    print(s,file=fw)
    print(tb)
def getnorth():
    url='http://data.eastmoney.com/hsgtcg/list.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    params = {'type': 'HSGTHDSTA',
             'token': '894050c76af8597a853f5b408b759f5d',
             'filter': '''(MARKET="S")''',
             'st': 'HDDATE',
             'sr': -1,
             'p': 1,
             'ps': 100,
             'js': 'var VbSqySzU={pages:(tp),data:(x)}',
             'rt': '53707495'}

    response=req.get(url=url,headers=headers)
    bstext=bs4.BeautifulSoup(response.content,'lxml')
    # print(bstext)

    tempdata=bstext.find_all('script', {'type': 'text/javascript'})[11]

    temp=str(tempdata)
    #print(temp)
    regex=' "data":([\s\S]*\{.*?[\s\S]*),\r\n  "pages": 30'
    #print(temp)
    jsondata=str(re.findall(regex,temp,re.M))
    #print((jsondata))
    data=jsondata.replace('\\r\\n','',-1).replace('},','}},',-1).replace('[\' [','',-1).replace('  ]\']','',-1)
    print(data)
    listdata=data.split('},',-1)
    header = ['日期', '股票代码 ', '股票名称 ', '板块', '占流通股比', '最新价  ', '涨跌幅  ', '今日持股股数亿  ', '今日持股市值亿', '占流通股本%', '今日持股占总股本','市值增幅','市值增幅%']
    #print(len(listdata))
    '''{
      "DateType": "1",
      "HdDate": "2021-01-20",
      "Hkcode": "1000002452",
      "SCode": "600036",
      "SName": "招商银行",
      "HYName": "银行",
      "HYCode": "016029",
      "ORIGINALCODE": "475",
      "DQName": "广东板块",
      "DQCode": "020005",
      "ORIGINALCODE_DQ": "153",
      "JG_SUM": 70.0,
      "SharesRate": 5.67,
      "NewPrice": 51.72,
      "Zdf": -0.2507,
      "Market": "001",
      "ShareHold": 1171539916.0,
      "ShareSZ": 60592044455.52,
      "LTZB": 0.0567910743097964,
      "ZZB": 0.0464530962851552,
      "LTSZ": 1066929005867.88,
      "ZSZ": 1304370414483.72,
      "ShareHold_Before_One": 0.0,
      "ShareSZ_Before_One": 0.0,
      "ShareHold_Chg_One": 10862250.0,
      "ShareSZ_Chg_One": 561795570.0,
      "ShareSZ_Chg_Rate_One": 0.00933507737095592,
      "LTZB_One": 0.000525233651781947,
      "ZZB_One": 0.000429622606984593
    },'''
    formatresults(listdata, header) #格式化输出
    #print(jsondata)
if __name__ == '__main__':
    getnorth()