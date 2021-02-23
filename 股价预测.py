import requests
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline
import pandas_datareader as  pdr
import pandas_datareader.data as web
import webbrowser  as br
import tushare as ts
import datetime
import time
from lxml import etree
import prettytable as pt
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.tsa.stattools as stat
from keras.layers import LSTM, Dense
from keras.models import Sequential


class StockQuoteForward():
    pro = ts.pro_api('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')

    #获取日线行情数据
    def getStockDatelQuote(self,stockcode,start,end):
        if stockcode[0:3] == '600' or stockcode[0:2] == '68':
            stockcode = stockcode + '.SH'
        else:
            stockcode = stockcode + '.SZ'
        # start='2020-09-30'
        # end=datetime.datetime.today().strftime('%Y-%m-%d')

        data = self.pro.daily(ts_code=stockcode, start_date=start, end_date=end)
        data = data.sort_values(by=['trade_date'], ascending=True)  # 按日期升序
        return data

    def get_stockname(self,stockcode):
        if stockcode.isdigit():  # 如果输入的是代码
            stockdata = pd.DataFrame(
                self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date'))
            # print(stockdata)
            for stock in stockdata.iterrows():
                # print(stock)
                if stockcode in stock[1]['ts_code']:
                    print(stock[1]['name'])
                    # print(str(stock[1]['ts_code'])[0:6])
                    return str(stock[1]['name'])
                else:
                    continue
        else:
            return stockcode

    ###获取股票代码
    def get_stockcode(self, stockname):
        if stockname.isdigit():  # 如果输入的是代码
            return stockname
        else:
            stockdata = pd.DataFrame(
                self.pro.stock_basic(exchange='', list_status='L',
                                     fields='ts_code,symbol,name,area,industry,list_date'))
            # print(stockdata)
            for stock in stockdata.iterrows():
                # print(stock)
                if stockname == stock[1]['name']:
                    # print(stock[1]['name'])
                    # print(str(stock[1]['ts_code'])[0:6])
                    return str(stock[1]['ts_code'])[0:6]
                else:
                    continue

    def drawLine(self,data,stockcode):
        print(data)
        # stockcode=self.get_stockcode()
        stockname=self.get_stockname(stockcode)
        kldata = data.values[:, [1,2, 3, 4, 5]]  # 分别对应日期，开盘价、收盘价、最低价和最高价
        print(kldata)
        kdate=kldata[0]
        kobj = Kline().add_xaxis(kdate)
        kobj.add_yaxis(stockname+"-日K线图", kldata.tolist())
        kobj.set_global_opts(
            yaxis_opts=opts.AxisOpts(is_scale=True),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title=""))

        renderfile = stockcode + 'render.html'
        kobj.render(renderfile)

        br.open(renderfile)

    def getHK_stockQuote(self,scode):  #调用的是yahoo财经，速度很慢
        stockData=[]
        table=pt.PrettyTable()

        url='https://hk.finance.yahoo.com/quote/'+scode+'.HK/history?p='+scode+'.HK'
        header= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 Chrome/78.0.3904.108Safari/537.36',
                  }
        session=requests.session()
        session.headers=header
        try:
            response=session.get(url=url)
        except BaseException as be:
            print('访问错误，重试')
            response = session.get(url=url)

        tree = etree.HTML(response.text)
        if response.status_code==200:
            table_head=tree.xpath('//div[@id="app"]//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/thead/tr/th//text()')
            table_data=tree.xpath('//div[@id="app"]//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr')
            for tr in table_data:
                # print(tr)
                date=tr.xpath('./td[1]/span/text()')[0]
                date =date = datetime.datetime.strptime(date,'%Y年%m月%d日').strftime('%Y-%m-%d')
                open=tr.xpath('./td[2]/span/text()')[0]
                high = tr.xpath('./td[3]/span/text()')[0]
                low = tr.xpath('./td[4]/span/text()')[0]
                close = tr.xpath('./td[5]/span/text()')[0]
                adjclose=tr.xpath('./td[6]/span/text()')[0]
                volumn=tr.xpath('./td[7]/span/text()')
                dict={'date':date,'open':open,'high':high,'low':low,'close':close,'adjclose':adjclose,'volumn':volumn}
                table.add_row([date,open,high,low,close,adjclose,volumn])
                stockData.append(dict)
            # print(table_head)
            table.field_names = table_head  # 设置表头
            table.align = 'c'  # 对齐方式（c:居中，l居左，r:居右）

            return table_head,table,stockData  #以多处形式返回，按需要接处理
        else:
            print('访问错误，未取到数据')
            return None
    def QuoteForward(self,data):

        subdata = data.iloc[:-30, :4]
        for i in range(4):
            pvalue = stat.adfuller(subdata.values[:, i], 1)[1]
            print("指标 ", data.columns[i], " 单位根检验的p值为：", pvalue)

        subdata_diff1 = subdata.iloc[1:, :].values - subdata.iloc[:-1, :].values
        for i in range(4):
            pvalue = stat.adfuller(subdata_diff1[:, i], 1)[1]
            print("指标 ", data.columns[i], " 单位根检验的p值为：", pvalue)

        # 模型阶数从1开始逐一增加
        rows, cols = subdata_diff1.shape
        aicList = []
        lmList = []

        for p in range(1, 11):
            baseData = None
            for i in range(p, rows):
                tmp_list = list(subdata_diff1[i, :]) + list(subdata_diff1[i - p:i].flatten())
                if baseData is None:
                    baseData = [tmp_list]
                else:
                    baseData = np.r_[baseData, [tmp_list]]
            X = np.c_[[1] * baseData.shape[0], baseData[:, cols:]]
            Y = baseData[:, 0:cols]
            coefMatrix = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.T, X)), X.T), Y)
            aic = np.log(np.linalg.det(np.cov(Y - np.matmul(X, coefMatrix), rowvar=False))) + 2 * (
                        coefMatrix.shape[0] - 1) ** 2 * p / baseData.shape[0]
            aicList.append(aic)
            lmList.append(coefMatrix)
        #基于lmList[1]中获取各指标对应的线性模型，对未来30期的数据进行预测，并与验证数据集进行比较分析
        p = np.argmin(aicList) + 1
        n = rows

        preddf = None
        for i in range(30):
            predData = list(subdata_diff1[n + i - p:n + i].flatten())
            predVals = np.matmul([1] + predData, lmList[p - 1])
            # 使用逆差分运算，还原预测值
            predVals = data.iloc[n + i, :].values[:4] + predVals
            if preddf is None:
                preddf = [predVals]
            else:
                preddf = np.r_[preddf, [predVals]]
            # 为subdata_diff1增加一条新记录
            subdata_diff1 = np.r_[subdata_diff1, [data.iloc[n + i + 1, :].values[:4] - data.iloc[n + i, :].values[:4]]]

        #进一步，绘制二维图表观察预测数据与真实数据的逼近情况
        plt.figure(figsize=(10, 7))
        for i in range(4):
            plt.subplot(2, 2, i + 1)
            plt.plot(range(30), data.iloc[-30:data.shape[0], i].values, 'o-', c='black')
            plt.plot(range(30), preddf[:, i], 'o--', c='gray')
            plt.ylim(1000, 1200)
            plt.ylabel("$" + data.columns[i] + "$")
        plt.show()
        v = 100 * (1 - np.sum(np.abs(preddf - data.iloc[-30:data.shape[0], :4]).values) / np.sum(
            data.iloc[-30:data.shape[0], :4].values))
        print("Evaluation on test data: accuracy = %0.2f%% \n" % v)

        # 分析预测残差情况
        (np.abs(preddf - data.iloc[-30:data.shape[0], :4]) / data.iloc[-30:data.shape[0], :4]).describe()

        plt.figure(figsize=(10, 7))
        for i in range(4):
            plt.subplot(2, 2, i + 1)
            plt.plot(range(30), data.iloc[-30:data.shape[0], i].values, 'o-', c='black')
            plt.plot(range(30), preddf[:, i], 'o--', c='gray')
            plt.ylim(1000, 1200)
            plt.ylabel("$" + data.columns[i] + "$")
        plt.show()
        v = 100 * (1 - np.sum(np.abs(preddf - data.iloc[-30:data.shape[0], :4]).values) / np.sum(
            data.iloc[-30:data.shape[0], : 4].values))
        print("Evaluation on test data: accuracy = %0.2f%% \n" % v)

    #基于LSTM算法的预测
    def LSTM_QuoteForward(self,data):
        SEQLEN = 21  #SEQLEN表示使用前期数据的长度
        dim_in = 4      #输入数据的维度
        dim_out = 4     #表示输出数据的维度
        pred_len = 30   #预测数据的长度
        vmean = data.iloc[:, :4].apply(lambda x: np.mean(x))
        vstd = data.iloc[:, :4].apply(lambda x: np.std(x))
        t0 = data.iloc[:, :4].apply(lambda x: (x - np.mean(x)) / np.std(x)).values
        X_train = np.zeros((t0.shape[0] - SEQLEN - pred_len, SEQLEN, dim_in))
        Y_train = np.zeros((t0.shape[0] - SEQLEN - pred_len, dim_out), )
        X_test = np.zeros((pred_len, SEQLEN, dim_in))
        Y_test = np.zeros((pred_len, dim_out), )
        #以上为数据初始化
        for i in range(SEQLEN, t0.shape[0] - pred_len):
            Y_train[i - SEQLEN] = t0[i]
            X_train[i - SEQLEN] = t0[(i - SEQLEN):i]
        for i in range(t0.shape[0] - pred_len, t0.shape[0]):
            Y_test[i - t0.shape[0] + pred_len] = t0[i]
            X_test[i - t0.shape[0] + pred_len] = t0[(i - SEQLEN):i]

        model = Sequential()
        model.add(LSTM(64, input_shape=(SEQLEN, dim_in), activation='relu', recurrent_dropout=0.01))
        model.add(Dense(dim_out, activation='linear'))
        model.compile(loss='mean_squared_error', optimizer='rmsprop')
        history = model.fit(X_train, Y_train, epochs=200, batch_size=10, validation_split=0)
        preddf = model.predict(X_test) * vstd.values + vmean.values
        #输出预测
        preddf
        preddf.shape
        #预测效果评估
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 7))
        for i in range(4):
            plt.subplot(2, 2, i + 1)
            plt.plot(range(30), data.iloc[-30:data.shape[0], i].values, 'o-', c='black')
            plt.plot(range(30), preddf[:, i], 'o--', c='gray')
            plt.ylim(1000, 1200)
            plt.ylabel("$" + data.columns[i] + "$")
        plt.show()
        v = 100 * (1 - np.sum(np.abs(preddf - data.iloc[-30:data.shape[0], :4]).values) / np.sum(
            data.iloc[-30:data.shape[0], : 4].values))
        print("Evaluation on test data: accuracy = %0.2f%% \n" % v)
        # Evaluation on test data: accuracy = 99.01%

if __name__ == '__main__':
    sq=StockQuoteForward()
    # data=sq.getStockDatelQuote('600511')
    # sq.drawLine(data,'600511')
    table_head,table_data,stockData=sq.getHK_stockQuote('1765')
    print(table_data,stockData)

