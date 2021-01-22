import bs4
import requests as req
import re,json
import prettytable as pt   #格式化成表格输出到html文件
#import csvtotable      #格式化成表格输出到html文件

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
        HDDATE = str(jsdata['HDDATE'])[0:10]
        SCODE = jsdata['SCODE']
        SNAME = jsdata['SNAME']
        SHAREHOLDSUM = format(jsdata['SHAREHOLDSUM']/100000000,'.3f')
        SHARESRATE = jsdata['SHARESRATE']
        CLOSEPRICE = jsdata['CLOSEPRICE']
        ZDF = jsdata['ZDF']
        SHAREHOLDPRICE = format(jsdata['SHAREHOLDPRICE']/100000000,'.3f')
        SHAREHOLDPRICEONE = format(jsdata['SHAREHOLDPRICEONE']/100000000,'.3f')
        SHAREHOLDPRICEFIVE = format(jsdata['SHAREHOLDPRICEFIVE']/100000000,'.3f')
        SHAREHOLDPRICETEN = format(jsdata['SHAREHOLDPRICETEN']/100000000,'.3f')

        # # 打印结果
        # print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % (
        # date, code, name, kaipanhuanshuoz, kaipanjine, liangbi, xianliang, liutongsizhi, liutongguyi, xifenhangye))
        tb.add_row([HDDATE,SCODE,SNAME,SHAREHOLDSUM,SHARESRATE,CLOSEPRICE,ZDF,SHAREHOLDPRICE,SHAREHOLDPRICEONE,SHAREHOLDPRICEFIVE,SHAREHOLDPRICETEN])
    print('记录条数：\t',len(listdata))
    s=tb.get_html_string()  #获取html格式
    outfile='./南向资金_'+HDDATE+'.html'
    fw = open(outfile, 'w', encoding='utf-8')
    print(s,file=fw)  #输出到文件
    print(tb)   #输出到控制台
    #方法二：使用csvto table


def getsouth():
    url='http://data.eastmoney.com/hsgtcg/lz.html'
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

    tempdata=bstext.find_all('script', {'type': 'text/javascript'})[12]
    #print(str(tempdata.find))
    temp=str(tempdata)
    regex=' "data":([\s\S]*\{.*?[\s\S]*),\r\n  "pages": 200'
    #print(temp)
    jsondata=str(re.findall(regex,temp,re.M))
    #print((jsondata))
    data=jsondata.replace('\\r\\n','',-1).replace('},','}},',-1).replace('[\' [','',-1).replace('  ]\']','',-1)
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
    formatresults(listdata, header) #格式化输出
    #print(jsondata)
if __name__ == '__main__':
    getsouth()