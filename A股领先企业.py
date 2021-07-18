# -*- coding:utf-8 -*-
import tushare as ts
import pandas as pd
import time
import requests
from util import proxy

supperstock = u'./config/A股领先企业列表.txt'
###获取股票代码
def get_stocklist():
    pro = ts.pro_api('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')
    stocklist=pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    stocklist=pd.DataFrame(stocklist)
    return stocklist

def get_TopStocks(stocklist):
    sn=requests.session()
    stockinfo = []  # 存储符合条件的企业
    #同花顺的接口
    url='http://basic.10jqka.com.cn/mapp/%s/company_base_info.json'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
             'Cookie': 'searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1608770907,1609917926,1610114215,1611192209; reviewJump=nojump; usersurvey=1; v=A-xOcNJfoJFX0bSt1GiqynybvcEdpZBLkkmkE0Yt-Bc6UYL3brVg3-JZdKSV',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
             'Cache-Control': 'max-age=0',
             'Connection': 'keep-alive',
             'Host': 'basic.10jqka.com.cn'
             }
    i=0
    j = 0  # 符合条件记录数
    for line in stocklist.iterrows():
        code=line[1]['ts_code'][0:6]
        name = line[1]['name']
        linebank = line[1]['industry']
        url1 = url % code
        sn.headers = headers
        # pro = proxy.get_proxy()
        # print(pro)
        try:
            # sn.proxies=pro
            jsoncontent=sn.get(url=url1).json()
            # jsoncontent = sn.get(url=url1, headers=headers).json()
        except BaseException :
            print(url1,proxy)
            time.sleep(1)
            jsoncontent = sn.get(url=url1).json()
            continue
        #print(jsoncontent)
        time.sleep(1) #不休息会封IP
        stockdesc=jsoncontent['data']['describe']
        #print(stockdesc)
        list = ['卓越领先','世界领先','全球领先', '行业第一', '全球第一', '市占率第一', '全球最', '龙头', '全球唯一', '中国最大']
        for desc in list:
            if str(desc) in str(stockdesc) and '之一' not in str(stockdesc):
                str1 = code + ',' + name + ',' + linebank + ',' + stockdesc
                print(str1)
                stockinfo.append(str1)
                j += 1
                break
    print('共有%d家' % j)
    with open(supperstock, 'w', encoding='utf-8') as fw:
        fw.write('代码，名称，行业，简介' + '\n')
        for textvalue in stockinfo:
            fw.write(str(textvalue) + '\n')
if __name__ == '__main__':
    stocklist=get_stocklist()
    get_TopStocks(stocklist)