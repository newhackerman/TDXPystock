import requests as req  #web请求相关
import re,json,sys,datetime
from dateutil.relativedelta import relativedelta
import prettytable as pt   #格式化成表格输出到html文件
from pyecharts.charts import Bar, Page,Line  #画图
from pyecharts import options as opts
import pandas as pd   #数据读取
import webbrowser  #打开浏览器
'''手动安装 talib 去https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 下载对应的版本“TA_Lib‑0.4.19‑cp37‑cp37m‑win_amd64.whl”  然后 pip3 install TA_Lib‑0.4.19‑cp37‑cp37m‑win_amd64.whl'''
import  talib   #Technical Analysis Library”, 即技术分析库 是Python金融量化的高级库，涵盖了150多种股票、期货交易软件中常用的技术分析指标，如MACD、RSI、KDJ、动量指标、布林带等等。
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec#分割子图
import mpl_finance as mpf        # python中可以用来画出蜡烛图、线图的分析工具，目前已经从matplotlib中独立出来，非常适合用来画K线
import tushare as ts
pro = ts.pro_api('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')
ts.set_token('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')
import baostock as bs

###获取股票代码
def get_stockcode(stockname):
    stockdata =pd.DataFrame(pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date'))
    #print(stockdata)
    for stock in stockdata.iterrows():
        if stockname == stock[1]['name']:
            #print(str(stock[1]['ts_code'])[0:6])
            return str(stock[1]['ts_code'])[0:6]
        else:
            continue
    # stocklist='./个股信息列表.txt'
    # readata=pd.read_csv(stocklist,sep=',',header=0,names=['代码','名称'])
    # for row in readata.iterrows():
    #     #print(row)
    #     if row[1]['名称']==stockname:
    #         return str(row[1]['代码']).rjust(6,'0')
    #     else:
    #         continue
#获个人股日线数据
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

def format_tohtml(listdata):
    header = ['日期', '股票代码 ', '股票名称 ', '持股数亿', '占比', '收盘价  ', '当日涨跌幅  ', '持股市值亿  ', '一日市值变化亿', '五日市值变化亿', '十日市值变化亿']
    tb = pt.PrettyTable()
    tb.field_names = header  # 设置表头
    tb.align = 'l'  # 对齐方式（c:居中，l居左，r:居右）
    c = Line()
    c1 = Line()
    page = Page()
    x = ['持股占比']

    HDDATElist = []
    SHAREHOLDSUMlist = []  # 持股数
    SHARESRATElist = []  # 持股占比
    # SHAREHOLDlist=[]#持股数量
    CLOSEPRICElist = [] #收盘价
    #数据分类格式化
    for data in listdata:
        # print(data+'\n----------------------------------------')
        jsdata = json.loads(data)
        #print(type(jsdata), jsdata)
        HDDATE = str(jsdata['HDDATE'])[0:10]
        HDDATE = datetime.datetime.strptime(HDDATE, '%Y-%m-%d').strftime('%Y%m%d')
        HDDATElist.append(HDDATE)
        SCODE = jsdata['SCODE']
        SNAME = jsdata['SNAME']
        SHAREHOLDSUM = format(jsdata['SHAREHOLDSUM'] / 100000000, '.3f')
        SHAREHOLDSUMlist.append(SHAREHOLDSUM)
        SHARESRATE = jsdata['SHARESRATE']
        SHARESRATElist.append(SHARESRATE)
        CLOSEPRICE = jsdata['CLOSEPRICE']
        CLOSEPRICElist.append(CLOSEPRICE)
        ZDF = jsdata['ZDF']
        SHAREHOLDPRICE = format(jsdata['SHAREHOLDPRICE'] / 100000000, '.3f')
        SHAREHOLDPRICEONE = format(jsdata['SHAREHOLDPRICEONE'] / 100000000, '.3f')
        SHAREHOLDPRICEFIVE = format(jsdata['SHAREHOLDPRICEFIVE'] / 100000000, '.3f')
        SHAREHOLDPRICETEN = format(jsdata['SHAREHOLDPRICETEN'] / 100000000, '.3f')
        # # 打印结果
        # print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % (
        # date, code, name, kaipanhuanshuoz, kaipanjine, liangbi, xianliang, liutongsizhi, liutongguyi, xifenhangye))
        tb.add_row(
            [HDDATE, SCODE, SNAME, SHAREHOLDSUM, SHARESRATE, CLOSEPRICE, ZDF, SHAREHOLDPRICE, SHAREHOLDPRICEONE,
             SHAREHOLDPRICEFIVE, SHAREHOLDPRICETEN])
    ##################图表输出
    x1 = HDDATElist[::-1]
    y1 = SHARESRATElist[::-1]  # 将占比数据设置为y轴
    y2 = SHAREHOLDSUMlist[::-1]
    y3 = CLOSEPRICElist[::-1]
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
    # c.render(path=outfile)
    #输出K线图
    #先获取日线历史数据
    date=datetime.date.today() - relativedelta(months=+1)
    #print(date)
    getstockdata=get_stock_dateData(SCODE,str(date), x1[-1])
    #getstockdata = pd.DataFrame(getstockdata)
    #print(getstockdata)
    getstockdata['trade_date'] = pd.to_datetime(getstockdata['trade_date']) #设置字段trade_date 为datetime
    getstockdata = getstockdata.set_index('trade_date') #设置trade_date为索引
    #getstockdata.sort_values(by=['trade_date','close'],ascending=False)
    #设置四个绘图区域    包括    K线（均线），成交量，MACD
    np.seterr(divide='ignore', invalid='ignore')  # 忽略warning
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig,ax = plt.subplots(figsize=(9 , 6))  # 创建fig对象
    # 画绘图区域
    gs = gridspec.GridSpec(2, 1, left=0.08, bottom=0.15, right=0.99, top=0.96, wspace=None, hspace=0,height_ratios=[3.5, 1])
    #添加指标
    graph_KAV = fig.add_subplot(gs[0, :]) #K线图
    graph_VOL = fig.add_subplot(gs[1, :])
    #graph_MACD = fig.add_subplot(gs[2, :])
    #graph_KDJ = fig.add_subplot(gs[3, :])
    mpf.candlestick2_ochl(graph_KAV, getstockdata.open, getstockdata.close, getstockdata.high, getstockdata.low,
                          width=0.5,colorup='r', colordown='g')  # 绘制K线走势
    # 绘制移动平均线图
    getstockdata['Ma5'] = getstockdata.close.rolling(window=5).mean()  # pd.rolling_mean(df_stockload.close,window=20)
    getstockdata['Ma10'] = getstockdata.close.rolling(window=10).mean()  # pd.rolling_mean(df_stockload.close,window=30)
    getstockdata['Ma20'] = getstockdata.close.rolling(window=20).mean()  # pd.rolling_mean(df_stockload.close,window=60)
    # getstockdata['Ma30'] = getstockdata.close.rolling(window=30).mean()  # pd.rolling_mean(df_stockload.close,window=60)
    # getstockdata['Ma60'] = getstockdata.close.rolling(window=60).mean()  # pd.rolling_mean(df_stockload.close,window=60)

    graph_KAV.plot(np.arange(0, len(getstockdata.index)), getstockdata['Ma5'], 'black', label='M5', lw=1.0)
    graph_KAV.plot(np.arange(0, len(getstockdata.index)), getstockdata['Ma10'], 'green', label='M10', lw=1.0)
    graph_KAV.plot(np.arange(0, len(getstockdata.index)), getstockdata['Ma20'], 'blue', label='M20', lw=1.0)
    # graph_KAV.plot(np.arange(0, len(getstockdata.index)), getstockdata['Ma30'], 'pink', label='M30', lw=1.0)
    # graph_KAV.plot(np.arange(0, len(getstockdata.index)), getstockdata['Ma60'], 'yellow', label='M60', lw=1.0)

    # 添加网格
    graph_KAV.grid()
    graph_KAV.legend(loc='best')
    graph_KAV.set_title(SCODE + ' ' + SNAME)
    graph_KAV.set_ylabel(u"价格")
    graph_KAV.set_xlim(0, len(getstockdata.index))  # 设置一下x轴的范围
    # 绘制成交量图
    graph_VOL.bar(np.arange(0, len(getstockdata.index)), getstockdata.vol,
                  color=['g' if getstockdata.open[x] > getstockdata.close[x] else 'r' for x in
                         range(0, len(getstockdata.index))])
    graph_VOL.set_ylabel(u"成交量")
    graph_VOL.set_xlim(0, len(getstockdata.index))  # 设置一下x轴的范围
    graph_VOL.set_xticks(range(0, len(getstockdata.index), 1))  # X轴刻度设定 每1天标一个日期

    # 绘制MACD
    # macd_dif, macd_dea, macd_bar = talib.MACD(getstockdata['close'].values, fastperiod=12, slowperiod=26,
    #                                           signalperiod=9)
    # graph_MACD.plot(np.arange(0, len(getstockdata.index)), macd_dif, 'red', label='macd dif')  # dif
    # graph_MACD.plot(np.arange(0, len(getstockdata.index)), macd_dea, 'blue', label='macd dea')  # dea
    #
    # bar_red = np.where(macd_bar > 0, 2 * macd_bar, 0)  # 绘制BAR>0 柱状图
    # bar_green = np.where(macd_bar < 0, 2 * macd_bar, 0)  # 绘制BAR<0 柱状图
    # graph_MACD.bar(np.arange(0, len(getstockdata.index)), bar_red, facecolor='red')
    # graph_MACD.bar(np.arange(0, len(getstockdata.index)), bar_green, facecolor='green')
    #
    # graph_MACD.legend(loc='best', shadow=True, fontsize='10')
    # graph_MACD.set_ylabel(u"MACD")
    # graph_MACD.set_xlim(0, len(getstockdata.index))  # 设置一下x轴的范围
    # graph_MACD.set_xticks(range(0, len(getstockdata.index), 2))  # X轴刻度设定 每15天标一个日期

    # X-轴每个ticker标签都向右倾斜45度
    for label in graph_KAV.xaxis.get_ticklabels():
        label.set_visible(False)

    for label in graph_VOL.xaxis.get_ticklabels():
        label.set_visible(True)
        label.set_fontsize(10)
    # for label in graph_MACD.xaxis.get_ticklabels():
    #     label.set_visible(True)
    #     label.set_fontsize(10)
    #输出图片
    plt.savefig('./Kline.jpg')

    # for label in graph_KDJ.xaxis.get_ticklabels():
    #     label.set_rotation(45)
    #     label.set_fontsize(10)  # 设置标签字体
    # c1.add_xaxis(xaxis_data=x)
    # c1.add_xaxis(xaxis_data=x1)
    # c1.add_yaxis(series_name='收盘价', y_axis=y3)
    # c1.set_global_opts(title_opts=opts.TitleOpts(title='北向资金持股分析:  ' + SNAME))

    # c1.render(path=outfile)
    #page.add(c, c1)
    page.add(c)
    page.render(path=outfile)
    # 如果要输出柱图
    '''
    bar = Bar()
    然后将c 换成bar
    '''
    s = tb.get_html_string()  #格式化成html文件
    #将画的图片输出
    kline='''<img src=./Kline.jpg />'''
    fw = open(outfile, 'a+', encoding='utf-8')
    fw.write(kline)
    fw.write(s)  # 输出到文件
    fw.close()


#获取个股的所有北向资金数据
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
                'rt': '53732197'}
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
    return listdata
    #print(len(listdata))
   #print(listdata)

    # northdatainfos.append(listdata)
    # return northdatainfos
    #formatresults(listdata, header)#每一页写表


if __name__ == '__main__':
    '002044'
    '002179'
    # code = get_stockcode('科大讯飞')
    # listdata=getnorth(code)
    # format_tohtml(listdata)
    #format_tohtml(listdata)
    #get_stock_dateData('SZ.002179','2021-01-27')
    var = sys.argv  # 可以接收从外部传入参数
    if len(var)>1:
        var1=var[1]
        code=get_stockcode(var1)
        listdata=getnorth(code) #实时查询北向资金
        format_tohtml(listdata)
        webbrowser.open('北向资金_' + var1+ '.html')
    else:
        code = get_stockcode('科大讯飞')
        #print(code)
        listdata = getnorth(code)  # 实时查询北向资金
        format_tohtml(listdata)
        webbrowser.open('北向资金_' +'科大讯飞' + '.html')


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