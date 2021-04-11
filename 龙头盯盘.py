import requests as req
import time,re,datetime
import  prettytable as pt

class topstockMoniter():

    #获取龙头
    def getTopStock(self):
        stocklist=[]
        url='http://page.tdx.com.cn:7615/TQLEX?Entry=CWServ.cfg_fx_ygzl'
        data={"Params":["ygts"]}
        try:
            r=req.post(url=url,json=data)
            # print(r.status_code)
            # print(r.content)
        except BaseException as b:
            count = 0
            while True:
                count += 1
                try:
                    r=req.post(url=url,json=data)
                    if r.status_code != 200:
                        continue
                    else:
                        break
                    if count >= 3:
                        break
                except BaseException as c:
                    continue
        rdata=r.json()
        if rdata['ErrorCode'] !=0:
            print('获取失败!!')
            return None
        else:
            tmplist=rdata['ResultSets'][0]['Content']
            for stock in tmplist:
                code=stock[0]
                ztbs=str(stock[2])+'天'+str(stock[3])+'板'
                tmpdict={'code':code,'ztbs':ztbs}
                stocklist.append(tmpdict)
            # print(stocklist)
        return stocklist

    #获取龙实时行情
    def getonlineData_sina(self, stocklist):
        onlinequote = []
        if stocklist is None:
            print('无股票数据')
            return None
        else:
            #取出股票代码
            stocks=[]
            for data in stocklist:
                print(data)
                if data['code'][0:2] =='68' or data['code'][0:2] =='60':
                    stock='sh'+data['code']
                    # print(stock)
                else:
                    stock = 'sz' + data['code']
                    # print(stock)
                stocks.append(stock)

            url = f'https://hq.sinajs.cn/?list={stocks}'
            url=url.replace('[','').replace(']','').replace('\'','',-1).replace(' ','',-1)
            # print(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            }
            try:
                proxies=self.get_proxy()
                r = req.get(url=url, headers=headers,proxies=proxies)
                if r'sys_auth="FAILED"' in r.text:
                    print('会话失效！！')
                # print(r.text)
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
                '''000001 ['平安银行', '21.460', '21.640', '21.560', '21.730', '21.330', '21.520', '21.560', '38302950', '825170840.990', '42500', '21.520', '4300', '21.510', '45400', '21.500', '10100', '21.490', '142700', '21.480', '6705', '21.560', '43700', '21.570', '147200', '21.580', '48200', '21.590', '107500', '21.600', '2021-04-08', '15:00:03', '00']
                               '''
                stockname = tmpdata[0]
                vol = round(float(tmpdata[8]) / 100,0)  # 换算成手
                wanamont = round(float(tmpdata[9]) / 10000, 2)  # 换算成万元
                price = str(tmpdata[3] ) # 当前价格
                print(price)
                zdf=round(((float(price)-float(tmpdata[2]))/float(tmpdata[2]))*100,2)
                if '0.0' in price:
                    zdf =0
                date = str(tmpdata[30]) + ' ' + str(tmpdata[31])  # 具体时间（多少分多少秒）
                tmpdict = {'代码': stockcode, '名称': stockname,'涨跌幅':str(zdf), '成交量': vol, '成交万元': wanamont, '现价': str(price),
                           '成交时间': date}
                onlinequote.append(tmpdict)
        return onlinequote

    # 判断是否为交易日
    def isTradeDay(self):
        alldays = self.pro.trade_cal()  # 得到所有日期，到今年年尾
        # print(alldays)
        tradingdays = alldays[alldays['is_open'] == 1]  # 得到所有交易开盘日
        # print(tradingdays)
        today = datetime.datetime.now().strftime('%Y%m%d')
        if today in tradingdays['cal_date'].values:
            return True
        else:
            return False


    def get_proxy(self):
        url='https://ip.jiangxianli.com/api/proxy_ip'
        try:
            r=req.get(url=url)
        except BaseException as b:
            count=0
            while True:
                count += 1
                try:
                    r = req.get(url=url)
                    if r.status_code!=200:
                        continue
                    else:
                        break
                    if count>=3:
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
        stocklist=self.getTopStock()
        # print('返回数据为：')
        # print(stocklist)
        t1 = '09:20'
        t2 = '15:35'
        while True:
            # if self.isTradeDay() and t1 < now < t2:  # 是否在交易日的交易时间内
            if True:  # 是否在交易日的交易时间内
                table=pt.PrettyTable()
                table.field_names=Thead
                table.align='c'
                table.border=True

                now = datetime.datetime.now().strftime("%H:%M")
                print('----------------------轮询开始:' + datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + '----------------------------------------------')
                # now = datetime.datetime.now().strftime("%H:%M")

                onlineQuote = self.getonlineData_sina(stocklist)
                if onlineQuote is None:
                    time.sleep(50)
                    continue
                else:
                    len1=len(onlineQuote)
                    for i in range(0,len1,1):
                        code=stocklist[i]['code']
                        name=onlineQuote[i]['名称']
                        ztbs=stocklist[i]['ztbs']   #涨停板数
                        zdf=onlineQuote[i]['涨跌幅']
                        price=onlineQuote[i]['现价']
                        vol=onlineQuote[i]['成交量']
                        amt=onlineQuote[i]['成交万元']
                        time1=onlineQuote[i]['成交时间']
                        table.add_row([code,name,ztbs,zdf,price,vol,amt,time1])
                    print(table.get_string())
                time.sleep(50)
            else:
                time.sleep(50)
                print('非交易日休息中...')
                time.sleep(300)

if __name__ == '__main__':
    monitor=topstockMoniter()
    monitor.main()