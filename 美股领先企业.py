# -*- coding:utf-8 -*-
import requests as req
import bs4
import pandas as pds
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
options=ChromeOptions()

options.add_argument('--headless')
options.add_argument('--disable-gpu')


if __name__ == '__main__':
    stockfile='./美股代码列表.csv'
    supperstock='./美股领先企业列表.txt'
    pdsdata=pds.read_csv(stockfile,sep=",",header=None,names=['代码','名称','所属行业'])  #指定标题，标题可以是自定义，header=0:表示有标题行，会把第一行当作标题
    pdsdata=pdsdata.drop_duplicates(subset=['代码'],keep='first',inplace=True) #去重
    stockinfo=[] #存储符合条件的企业
    url='http://quotes.sina.com.cn/usstock/hq/summary.php?s=%s'
    browser = webdriver.Chrome(executable_path='./../chromedriver.exe',options=options)
    i=0
    j = 0  # 符合条件记录数
    #print(pdsdata)

    for data in pdsdata.iterrows():
        i+=1
        #请求50次后休息2秒钟
        if i%100==0:
            time.sleep(10)
        code=str(data[1]['代码'])
        #print(code)
        name=str(data[1]['名称'])
        linebank = str(data[1]['所属行业'])
        try:
            url1=url %code
            # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"')
            # cookeis={
            #     'cipher_device_id': '1591067673921885',
            #     'UM_distinctid': '174ec9f4455336-04e8f533cfdc4a-f7d1d38-144000-174ec9f4456591',
            #     'device_id': '1591067673921885',
            #     '_gcl_au': '1.1.433007375.1610672342',
            #     '_ga': 'GA1.1.420142175.1594607736',
            #     'uid': '5646366',
            #     'web_sig': 'iSRA0IT+U7EZeNoatFEGnAbG5+mhgDxBffXzkGAK5rjYaHBAVoOeo9IGnSnye7caxp44fAc6IfMR8D+LgO/duJU34P4UbOB/q3ZsAsTbPtTuM4a6uD9NQ9bxQ6+2G/TN',
            #     'sensorsdata2015jssdkcross': '{"distinct_id":"ftv1AmA3ksZHKq2Vkv3emEVymYac+96JbeEUjN+TsD1MxS4HAT9bFTocICYOmESQoVVh","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":"","$latest_utm_medium":"futu_niuniu_share","$latest_utm_campaign":"news","$latest_utm_content":"web_share","$latest_utm_term":"123279"},"$device_id":"1727305fb50248-05e6c28a6bddcc-f7d1d38-1327104-1727305fb534e"}',
            #     'Hm_lvt_f3ecfeb354419b501942b6f9caf8d0db': '1610937598,1611738667,1612533350',
            #     'tgw_l7_route': '9c0c6f548091415e4705a7f5457fbbe2',
            #     'PHPSESSID': 'sutqt7ujtsf0vrlpdeo9ask627'
            # }

            # web.add_cookie(cookie_dict=cookeis)
            # print(url1)
            browser.get(url1) #发起get请求
        except BaseException as be:
            print(be)
            browser.get(url1)  #重试一次
            continue

        stockdesc=browser.find_element_by_xpath('//div[@class="news"]//table/tbody/tr[1]/td/p').text

        # print(stockdesc)
        #sampledsc = bsdata.find('div',class_='c01')
        list=['全球领先' , '行业第一' , '全球第一' ,'市占率第一', '全球最' , '龙头' ,'全球唯一','中国最大']

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
