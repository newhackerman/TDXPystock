# -*- coding: utf-8 -*-
import sys
import requests as req
import time,re,datetime
import  prettytable as pt

from PyQt5.Qt import *
from PySide2.QtWidgets import *

class RunThread(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.stocklist = self.getTopStock()
    def __del__(self):
        self.wait()
    def run(self):
        self.main()
        time.sleep(20)
        self.trigger.emit()

    def callback(self, msg):
        # 信号焕发，我是通过我封装类的回调来发起的
        # self._signal.emit(msg)
        pass

    # 获取龙头
    def getTopStock(self):
        stocklist = []
        url = 'http://page.tdx.com.cn:7615/TQLEX?Entry=CWServ.cfg_fx_ygzl'
        data = {"Params": ["ygts"]}
        try:
            r = req.post(url=url, json=data)
        except BaseException as b:
            count = 0
            while True:
                count += 1
                try:
                    r = req.post(url=url, json=data)
                    if r.status_code != 200:
                        continue
                    else:
                        break
                    if count >= 3:
                        break
                except BaseException as c:
                    continue
        rdata = r.json()
        if rdata['ErrorCode'] != 0:
            print('获取失败!!')
            return None
        else:
            tmplist = rdata['ResultSets'][0]['Content']
            for stock in tmplist:
                code = stock[0]
                ztbs = str(stock[2]) + '天' + str(stock[3]) + '板'
                tmpdict = {'code': code, 'ztbs': ztbs}
                stocklist.append(tmpdict)
        return stocklist


    def getonlineData_sina(self, stocklist):
        onlinequote = []
        if stocklist is None:
            print('无股票数据')
            return None
        else:
            # 取出股票代码
            stocks = []
            for data in stocklist:
                if data['code'][0:2] == '68' or data['code'][0:2] == '60':
                    stock = 'sh' + data['code']
                else:
                    stock = 'sz' + data['code']
                stocks.append(stock)

            url = f'https://hq.sinajs.cn/?list={stocks}'
            url = url.replace('[', '').replace(']', '').replace('\'', '', -1).replace(' ', '', -1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            }
            try:
                proxies = self.get_proxy()
                r = req.get(url=url, headers=headers, proxies=proxies)
                if r'sys_auth="FAILED"' in r.text:
                    print('会话失效！！')
            except BaseException as B:
                count = 0
                while True:
                    count += 1
                    try:
                        proxies = self.get_proxy()
                        r = req.get(url=url, headers=headers, proxies=proxies)
                        if r.status_code != 200:
                            continue
                        else:
                            break
                        if count >= 3:
                            break
                    except BaseException as c:
                        continue
            regx = r'var.hq_str_..(\d{6})="(.*?)"'
            rtext = re.findall(regx, r.text, re.M)
            for data in rtext:
                stockcode = data[0]
                tmpdata = data[1].split(',')
                stockname = tmpdata[0]
                vol = round(float(tmpdata[8]) / 100, 0)  # 换算成手
                wanamont = round(float(tmpdata[9]) / 10000, 2)  # 换算成万元
                price = str(tmpdata[3])  # 当前价格
                zdf = round(((float(price) - float(tmpdata[2])) / float(tmpdata[2])) * 100, 2)
                if '0.0' in price:
                    zdf = 0
                date = str(tmpdata[30]) + ' ' + str(tmpdata[31])  # 具体时间（多少分多少秒）
                tmpdict = {'代码': stockcode, '名称': stockname, '涨跌幅': str(zdf), '成交量': vol, '成交万元': wanamont,
                           '现价': str(price),
                           '成交时间': date}
                onlinequote.append(tmpdict)
        return onlinequote

    def isTradeDay(self):
        alldays = self.pro.trade_cal()  # 得到所有日期，到今年年尾
        tradingdays = alldays[alldays['is_open'] == 1]  # 得到所有交易开盘日
        today = datetime.datetime.now().strftime('%Y%m%d')
        if today in tradingdays['cal_date'].values:
            return True
        else:
            return False

    def get_proxy(self):
        url = 'https://ip.jiangxianli.com/api/proxy_ip'
        try:
            r = req.get(url=url)
        except BaseException as b:
            count = 0
            while True:
                count += 1
                try:
                    r = req.get(url=url)
                    if r.status_code != 200:
                        continue
                    else:
                        break
                    if count >= 3:
                        break
                except BaseException as c:
                    continue
        jsontext = r.json()['data']
        ip = jsontext['ip']
        port = jsontext['port']
        protocol = jsontext['protocol']
        proxy = {str(protocol).lower(): str(protocol).lower() + '://' + ip + ':' + port}
        return proxy

    def main(self):
        Thead = ['代码', '名称', '板数', '涨跌幅', '现价', '成交量', '成交万元', '成交时间']
        t1 = '09:20'
        t2 = '15:35'
        now = datetime.datetime.now().strftime("%H:%M")
        # if self.isTradeDay() and t1 < now < t2:  # 是否在交易日的交易时间内
        # 是否在交易日的交易时间内
        table = pt.PrettyTable()
        table.field_names = Thead
        table.align = 'c'
        table.border = True
        now = datetime.datetime.now().strftime("%H:%M")
        # print('----------------------龙头盯盘轮询:' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '----------------------------------------------')
        # now = datetime.datetime.now().strftime("%H:%M")
        onlineQuote = self.getonlineData_sina(self.stocklist)
        if onlineQuote is None:
            time.sleep(5)
        else:
            len1 = len(onlineQuote)
            for i in range(0, len1, 1):
                code = self.stocklist[i]['code']
                name = onlineQuote[i]['名称']
                ztbs = self.stocklist[i]['ztbs']  # 涨停板数
                zdf = onlineQuote[i]['涨跌幅']
                price = onlineQuote[i]['现价']
                vol = onlineQuote[i]['成交量']
                amt = onlineQuote[i]['成交万元']
                time1 = onlineQuote[i]['成交时间']
                table.add_row([code, name, ztbs, zdf, price, vol, amt, time1])
            # print(table.get_string())
            mainw.result=table.get_string()  #将值传给主窗口

class MainWindow(QMainWindow):
    result=None
    def __init__(self):
        super().__init__()  # 调用父类QWidget中的init方法
        self.setWindowTitle('龙头盯盘 ')
        self.resize(800, 200)
        self.text1 = QTextEdit(self)
        self.text1.resize(800, 200)
        self.text1.setEnabled(False) #禁止编辑
        # self.text1.setStyleSheet('color:white;')
        self.text1.setStyleSheet('color:rgb(255,0,255);background-color:blank;font-size:16px' )
        self.setFixedSize(self.width(), self.height()) #禁止最大化
        self.timer1=QTimer()
        self.timer1.setInterval(30000)
        self.timer1.start()
        self.fun_list()

    def fun_list(self):   #调用要调用的函数
        self.Work()
        self.TimterupdateTime()
        # self.timer()

    def Work(self):
        self.thread = RunThread()
        self.thread.start()
        self.text1.setText(self.result)
        self.thread.trigger.connect(self.Work)

    def TimeStop(self):
        self.timer1.stop()
        self.t = 0

    def TimterupdateTime(self):
        # 新建一个QTimer对象
        self.timer2 = QTimer()
        self.timer2.setInterval(1000)
        self.timer2.start()
        # 信号连接到槽
        self.timer2.timeout.connect(self.updateTime)  # 每隔1秒更新

    # 定义槽
    def updateTime(self):
        self.setWindowTitle('龙头盯盘'+'\t\t\t'+time.strftime("%X",time.localtime()))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainw=MainWindow()
    mainw.show()
    sys.exit(app.exec_())