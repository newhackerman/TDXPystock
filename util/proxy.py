import bs4
import requests  as req
from random import *
import prettytable as pt

headers = {
        'Cookie': 'UM_distinctid=1770efbd8b55c-08e67b79499c89-303464-144000-1770efbd8b676; Hm_lvt_b72418f3b1d81bbcf8f99e6eb5d4e0c3=1610864122; CNZZDATA1278691459=828572365-1610863866-https%253A%252F%252Fwww.google.com%252F%7C1611145428; Hm_lpvt_b72418f3b1d81bbcf8f99e6eb5d4e0c3=1611150489',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

def test_proxy(proxy):
    url='http://www.baidu.com'
    response=req.get(url=url,headers=headers,proxies=proxy,timeout=5)
    if response.status_code ==200:
        return proxy
    else:
        return None
def get_proxy():
    url = 'https://ip.jiangxianli.com/?page=1'  # 提供代理IP的页面
    response = req.get(url=url, headers=headers)
    listhead = ['IP', '端口', '匿名度', '类型', '位置', '所属地区', '运营商', '响应速度', '存活时间', '最后验证时间']
    listbody = []
    tempbody = bs4.BeautifulSoup(response.text, 'lxml')
    # print(tempbody)
    context = tempbody.find('div', class_="layui-form").findChild('tbody').find_all('tr')
    # print(context)
    tempdict = {}
    tb = pt.PrettyTable()
    tb.field_names = ['IP', '端口', '匿名度', '类型', '位置', '所属地区', '运营商', '响应速度', '存活时间', '最后验证时间']  # 设置表头
    tb.align = 'l'
    for tempda in context:
        tdlist = tempda.find_all('td')
        '''IP', '端口', '匿名度', '类型', '位置', '所属地区', '运营商', '响应速度', '存活时间', '最后验证时间'''
        ip1 = tdlist[0].text
        port1 = tdlist[1].text
        nmd1 = tdlist[2].text
        type1 = tdlist[3].text
        local1 = tdlist[4].text
        area1 = tdlist[5].text
        provider1 = tdlist[6].text
        speed1 = tdlist[7].text
        activetime1 = tdlist[8].text
        testtime1 = tdlist[9].text
        tempdict = {'ip': ip1, 'port': port1, 'nmd': nmd1, 'type': type1, 'local': local1, 'area': area1,
                    'provider': provider1, 'speed': speed1, 'activetime': activetime1, 'testtime': testtime1}
        listbody.append(tempdict)
        #并添加出格式化列表中
        tb.add_row([ip1,port1,nmd1,type1,local1,area1,provider1,speed1,activetime1,testtime1])
    # print(listbody)
    # 格式化成表格
    formatstring =tb.get_html_string()
    fw = open('./proxy_list.html', 'w', encoding='utf-8')
    #输出到文件
    print(formatstring,file=fw)
    chocieproxy= choice(listbody)
    proxy = {str(chocieproxy['type']).lower(): str(chocieproxy['type']).lower()+'://' + chocieproxy['ip'] + ':' + chocieproxy['port']}
    result=test_proxy(proxy)
    if response is None:
        get_proxy()
    else:
     return proxy

if __name__ == '__main__':
    proxy=get_proxy()
    print(proxy)
    #print(proxy)
