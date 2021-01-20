import requests as req
import bs4
import pandas as pds
import time


if __name__ == '__main__':
    stockfile='./港股代码列表.csv'
    supperstock='./港股领先企业列表.txt'
    pdsdata=pds.read_csv(stockfile,sep=",",header=None,names=['代码','名称','所属行业'])  #指定标题，标题可以是自定义，header=0:表示有标题行，会把第一行当作标题
    stockinfo=[] #存储符合条件的企业
    url='https://news.futunn.com/wiki/hk'
    headers={'cookie': 'cipher_device_id=1591067673921885; UM_distinctid=174ec9f4455336-04e8f533cfdc4a-f7d1d38-144000-174ec9f4456591; device_id=1591067673921885; _gcl_au=1.1.433007375.1610672342; Hm_lvt_f3ecfeb354419b501942b6f9caf8d0db=1610937598; _gid=GA1.2.724981852.1610937611; _ga=GA1.1.420142175.1594607736; uid=5646366; web_sig=iSRA0IT%2BU7EZeNoatFEGnAbG5%2BmhgDxBffXzkGAK5rjYaHBAVoOeo9IGnSnye7caxp44fAc6IfMR8D%2BLgO%2FduJU34P4UbOB%2Fq3ZsAsTbPtTuM4a6uD9NQ9bxQ6%2B2G%2FTN; _ga_K1RSSMGBHL=GS1.1.1610937610.2.1.1610937627.0; news-locale=zh-cn; _ga_XG64WM4H33=GS1.1.1610956257.1.1.1610956814.0; _csrf=ZWvu1ArD61HLlIzKWn4X18KqhtLmsoi4; FUTU_TOOL_STAT_UNIQUE_ID=16109591757087978; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221727305fb50248-05e6c28a6bddcc-f7d1d38-1327104-1727305fb534e%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_medium%22%3A%22futu_niuniu_share%22%2C%22%24latest_utm_campaign%22%3A%22news%22%2C%22%24latest_utm_content%22%3A%22web_share%22%2C%22%24latest_utm_term%22%3A%22123279%22%7D%2C%22%24device_id%22%3A%221727305fb50248-05e6c28a6bddcc-f7d1d38-1327104-1727305fb534e%22%7D; PHPSESSID=i9imiluhj7mfrkn3asq5esuue6; tgw_l7_route=c63808a9490ee953df1166b7a4165d35; Hm_lpvt_f3ecfeb354419b501942b6f9caf8d0db=1610975886',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document'
                }
    #print(pdsdata)
    i=0
    j = 0  # 符合条件记录数
    for data in pdsdata.iterrows():
        i+=1
        #请求50次后休息2秒钟
        if i%100==0:
            time.sleep(10)
        code=str(data[1]['代码']).rjust(5,'0')  #data[0] 表示索引行，读进来后会自加一列为行号
        #print(code)
        name=str(data[1]['名称'])
        linebank = str(data[1]['所属行业'])
        try:
            response=req.get(url+code,headers=headers) #发起get请求
        except BaseException as be:
            #print(be)
            response = req.get(url + code, headers=headers)  #重试一次
            continue
        if response.status_code != 200:
            continue
        #print(url)
        bsdata=bs4.BeautifulSoup(response.text,'lxml')
        #print(bsdata)
        stockdesc=bsdata.find('div',class_='fRight').findChild('p',class_='stockIntro').text
        #print(stockdesc)
        #sampledsc = bsdata.find('div',class_='c01')
        list=['全球领先' , '行业第一' , '全球第一' ,'市占率第一', '全球最大' , '龙头' ,'全球唯一','中国最大']

        for desc in list:
            if str(desc) in  str(stockdesc) and  '之一' not in str(stockdesc):
                str1=code+','+name+','+linebank+','+stockdesc
                print(str1)
                stockinfo.append(str1)
                j+=1
    print('共有%d家' %j)
    with open(supperstock,'w',encoding='utf-8') as fw:
        fw.write('代码，名称，行业，简介'+'\n')
        for textvalue in stockinfo:
            fw.write(str(textvalue)+'\n')
