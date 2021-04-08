'''
此程序用于监控盘中出现万手大单的股票，数据来源于新浪，不保证数据的准确性
另外是采用http协议获取数据，性能不能保证，如果发现有socket接口一定要告诉我哦
访问频繁极有可能被封IP,
author:newhackerman@163.com
'''
import requests as req
import time,datetime,json
import re
import pandas as  pd
import tushare as ts
from lxml import etree
import prettytable as pt  # 格式化成表格输出到html文件
import util.proxy as proxy
class Wanshouge():
    configfile = 'D:/mysqlconfig.json'
    moniStockFile = 'C:/十档行情/T0002/export/长期跟踪股20210408.txt'

    #读取自义的股票列表
    def getstocklist(self):
        stocklist=[]
        f=open(self.moniStockFile,'r')
        data=f.readlines()

        for stock in data:
            if stock[0:2]=='68' or stock[0:2]=='60':
                stock='sh'+stock.strip()
            else:
                stock = 'sz' + stock.strip()
            stocklist.append(stock)
        f.close()
        # print(stocklist)
        return stocklist

    def __init__(self):
        self.jsoncontent=self.get_config()
        self.pro = ts.pro_api(self.jsoncontent['tushare'])

    def get_config(self):
        with open(self.configfile, encoding="utf-8") as f:
            jsoncontent = json.load(f)
        f.close()
        return jsoncontent

    #获取股票列表
    def getAllstock(self):
        try:
            stockdata = pd.DataFrame(
                self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date'))
            stocklist=stockdata['ts_code'].to_list()
        except BaseException as B:  #出错后重试一次
            stockdata = pd.DataFrame(
                self.pro.stock_basic(exchange='', list_status='L',
                                     fields='ts_code,symbol,name,area,industry,list_date'))
            stocklist = stockdata['ts_code'].to_list()

        if stocklist is None:
            print('未获取到股票列表')
            return None
        else:
            newlist=[]
            for code in stocklist:
                newlist.append((code[7:9]).lower()+code[0:6])  #由于返回的数据是XXXXXX.SZ,需要转一下
            # print(newlist)
            return newlist
    #输出万手数据
    def getonlineData(self,stocklist):
        wanshoustock=[]
        Thead = ['代码', '名称', '万手', '成交万元', '价格', '成交时间']
        # tb = pt.PrettyTable()
        # tb.field_names = Thead  # 设置表头
        # tb.align = 'c'  # 对齐方式（c:居中，l居左，r:居右）
        if stocklist is None:
            print('无股票数据')
            return None
        else:
            print(Thead)
            count=len(stocklist)
            # count=20
            step=25
            for i in range(0,count,step):  #每次取25个股的实时数据
                stocks = ','.join([str(x) for x in stocklist[i:i+step]])  # 将列表转换成字符串  如果全时字符串的时候，直接 ','.join(list)
                url = f'https://hq.sinajs.cn/?list={stocks}'
                # print(url)
                headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                 }
                try:
                    r=req.get(url=url,headers=headers)
                    regx=r'var.hq_str_..(\d{6})="(.*?)"'
                    rtext=re.findall(regx,r.text,re.M)

                    for data in rtext:
                        vcount=0
                        stockcode=data[0]
                        tmpdata=data[1].split(',')
                        '''000001 ['平安银行', '21.460', '21.640', '21.560', '21.730', '21.330', '21.520', '21.560', '38302950', '825170840.990', '42500', '21.520', '4300', '21.510', '45400', '21.500', '10100', '21.490', '142700', '21.480', '6705', '21.560', '43700', '21.570', '147200', '21.580', '48200', '21.590', '107500', '21.600', '2021-04-08', '15:00:03', '00']
                                        '''
                        stockname=tmpdata[0]

                        wanvol=round(float(tmpdata[8])/100/10000,2) # 换算成万手
                        wanamont=round(float(tmpdata[9])/10000,2) #换算成万元
                        price=tmpdata[3]    #当前价格
                        date=str(tmpdata[30])+' '+str(tmpdata[31])  #具体时间（多少分多少秒）
                        if wanvol>=1:
                            vcount=vcount+1
                            # tb.add_row([stockcode,stockname,wanvol,wanamont,price,date])
                            tmpstr=[stockcode,stockname,str(wanvol)+'万手',str(wanamont)+'万元',price,date]
                            tmpdict={'代码':stockcode,'名称':stockname,'万手':wanvol,'成交万元':wanamont,'价格':price,'成交时间':date}
                            wanshoustock.append(tmpdict)
                            print(tmpstr)
                            # pdata=pd.DataFrame(tmpstr,columns=Thead)
                            # tmpstr.append(vcount)
                    # print(stockcode,tmpdata)
                except BaseException as B:
                    print(B)
                    continue
                    time.sleep(0.1)
            # stockdf=pd.read_table(tb.get_string())
        return wanshoustock

    #查看实时交易详情
    def get_tradedetail(self,stocklist):
        if stocklist is None:
            return
        else:
            # stocklist=['sh601919']
            for stock in stocklist:
                try:
                    proxies=proxy.get_proxy()
                    print(proxies)
                    url = f'https://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol={stock}'
                    # print(url)
                    r=req.get(url=url,proxies=proxies)
                except BaseException as BE:
                    time.sleep(1)
                    count = 0
                    while count < 3:
                        r = req.get(url=url)
                        if r.status_code != 200:
                            count += 1
                            print('第%s 次 重试中！！！' % (count))
                            time.sleep(2)
                        else:
                            break
                # r = req.get(url=url)
                tree=etree.HTML(r.text)
                trlist=   tree.xpath('/html/body/div[6]/div/div[@class="R"]/div[@class="dataOuter"]/table/tbody/tr')
                # stockname=tree.xpath('/html/body/div[6]/div/div[@class="R"]//div[@class="hq_title"]/a[4]//text()')
                # print(stockname)
                interval=0
                for tr in trlist:
                    interval+=1
                    time=tr.xpath('./th/text()')[0]
                    price=tr.xpath('./td[1]/text()')[0]
                    zdf=tr.xpath('./td[2]/text()')[0]
                    vol = tr.xpath('./td[4]/text()')[0]
                    amt=str(tr.xpath('./td[5]/text()')[0]).replace(',','',-1)
                    director=tr.xpath('./th[2]//text()')[0]
                    # tmpdata = {'代码': stock[2:7], '名称': stockname, '时间': time, '价格': price, '涨跌幅': zdf, '成交量': vol,
                    #            '成交额':amt,'方向': director}
                    # print(tmpdata)
                    if float(vol)/10000>1 and float(amt)/10000>500:  #成交量大于1万且成交额大于500万
                        tmpdata = {'代码': stock[2:7],  '时间': time, '价格': price, '涨跌幅': zdf, '成交量': vol,
                                   '成交额': amt, '方向': director}
                        print(tmpdata)
                    if interval/20==0:
                        time.sleep(0.5)
if __name__ == '__main__':
     analysis=Wanshouge()
     stocklist=analysis.getstocklist() #只监控自己关注的
     # stocklist=analysis.getAllstock()  #全部监控

     t1 = '09:20'
     t2 = '15:30'
     while True:
         now = datetime.datetime.now().strftime("%H:%M")
         if t1 < now < t2:
             # Data=analysis.getonlineData(stocklist)
             # # rint(Data)
             # tmpdata=pd.DataFrame(Data)
             # print(tmpdata)
             # sortData=tmpdata.sort_values(by=['成交万元'], ascending=False)  # 按成交额降序
             # print( sortData)
             analysis.get_tradedetail(stocklist)  # 获取实情交易详情，并输出万手哥
             time.sleep(3)
         else:
            break