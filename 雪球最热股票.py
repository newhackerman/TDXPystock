import requests as req
import prettytable as pt
import re,time,datetime
# from selenium import webdriver
# options=webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 允许开发者模式
# brow=webdriver.Chrome(executable_path='../chromedriver.exe',options=options)

def format_tohtml(datalist):
    header = ['股票代码 ', '股票名称 ', '热度值', '热度值变化']
    tb = pt.PrettyTable()
    tb.add_row(['+-----------+', '+-----------+', '+-----------+', '+-----------+'])
    tb.field_names = header  # 设置表头
    tb.align = 'l'  # 对齐方式（c:居中，l居左，r:居右）
    for data1 in datalist:
        try:
            for value in data1:
                stockcode = value['code']
                stockname = value['name']
                hotvalue = value['value']
                hotincrement = value['increment']
                tb.add_row(
                    [stockcode, stockname, hotvalue, hotincrement])
        except BaseException as Be:
            print(value)
            print(Be)
            #print('代码：%s 名称： %s 热度值：%s  热度值变动：%s' % (stockcode, stockname, hotvalue, hotincrement))


        tb.add_row(['+-----------+','+-----------+','+-----------+','+-----------+'])
    outfile = '雪球最热股票.html'
    # outfile = '/opt/lampp/htdocs/hotstock.html'
    print(tb)
    jscode=''' <script language="JavaScript">setTimeout(function(){location.reload()},30000); </script>'''
    s = tb.get_html_string()  #格式化成html文件
    fw = open(outfile, 'w', encoding='gbk')
    fw.write(jscode)
    fw.write(s)  # 输出到文件
    fw.close()

def getdata():
    # 全球热
    url1 = 'https://stock.xueqiu.com/v5/stock/hot_stock/list.json?size=8&_type=10&type=10'
    # 沪深
    url2 = 'https://stock.xueqiu.com/v5/stock/hot_stock/list.json?size=8&_type=12&type=12'
    # 港股
    url3 = 'https://stock.xueqiu.com/v5/stock/hot_stock/list.json?size=8&_type=13&type=13'
    # 美股
    url4 = 'https://stock.xueqiu.com/v5/stock/hot_stock/list.json?size=8&_type=11&type=11'
    urllist = []
    urllist.append(url1)
    urllist.append(url2)
    urllist.append(url3)
    urllist.append(url4)
    cookeis = 'device_id=e6b8423858c6fa03fa5f8ea2cc164e8e; s=c9133wut45; bid=8eb7a82092e1387f689981b0cdac6fde_kibfx3s0; xq_a_token=a4b3e3e158cfe9745b677915691ecd794b4bf2f9; xqat=a4b3e3e158cfe9745b677915691ecd794b4bf2f9; xq_r_token=b80d3232bf315f8710d36ad2370bc777b24d5001; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxNzc2MzQxOCwiY3RtIjoxNjE2NDg3NDU0MDE0LCJjaWQiOiJkOWQwbjRBWnVwIn0.cd5UY5x3RZM4sFWGN60ukLvlwsoocMN4tyMMCCbtn9fEfV9X55UGRvYiQh2UUpq6HRxnz_9E6aB5EdWs88O83a4zOSI-pHunyVf6mrqeh2Fk5hijLmLE5ZqIX6bG0_lF3Lsx4z9oGf1CqPfsqhICZ0ftMC8qugX0FmlU2AanNBxW-_rghOYf0lBuEwzbm41oXbalT0fBQ2Vd5n-A7WWranWpdWopu8eZA-yNWyarAeleZ-XjKXnysrDQA3fv0-FoczJh_MAEVJ2qmj7liKyMQ1PHqMa6K09bERw8iLQ4kdW3nWeBxDOdZdkV9tx1XJpWKRHRuVZ84cgXkt8DtQxBUA; u=151616487492624; Hm_lvt_1db88642e346389874251b5a1eded6e3=1616487495,1616594355,1616813517; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1616814049'

    headers = {'accept': 'application/json, text/plain, */*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
               'cookie': cookeis}
    datalist=[]
    for url in urllist:
        hotstock = req.get(url=url, headers=headers).json()
        # print(hotstock)
        data1 = hotstock['data']['items']
        datalist.append(data1)
    header = ['股票代码 ', '股票名称 ', '热度值', '热度值变化']
    return datalist

def get_sina_HotStock():
    url='https://touzi.sina.com.cn/public/strategy'
    # response=req.get(url=url)
    response = brow.get(url=url)
    response=brow.find_element_by_xpath('//*[@id="ms_table_wrap"]/tbody')
    print(response.text)
    # print(response)
    # reg=r'(<tbody><tr>.+?</tbody>)'
    # content=re.findall(reg,response)
    # print(content)
    brow.close()

def hotBank():
    tb = pt.PrettyTable()
    dateTime = datetime.datetime.strptime("2022-06-25 00:37:02", "%Y-%m-%d %H:%M:%S")
    # time1=time.strftime("%Y-%m-%d %H:%M:%S")
    time1=time.mktime(dateTime.timetuple())
    tb.align = 'l'  # 对齐方式（c:居中，l居左，r:居右）
    session=req.session()
    url='https://wzq.tenpay.com/cgi-bin/stockpicking_plat.fcgi?action=xg_get_concept_index.fcgi&urldata=user_type=5'
    time1=str(time.time()).split('.')[0]
    header={
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; M2010J19SC Build/QKQ1.200830.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045521 Mobile Safari/537.36 MMWEBID/3483 MicroMessenger/8.0.1.1841(0x2800015D) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://wzq.tenpay.com/cgi-bin/stockpicking_plat.fcgi?action=xg_get_concept_index.fcgi&urldata=user_type%3D5',
        'cookie': 'pgv_pvid=2093226412; ts_uid=5774253200; pgv_info=ssid=s4641134600; ts_refer=zqact.tenpay.com/activity/page/activityForward/; qv_als=BOUTYSdyJRhlr1xJA11616558737+RjMuw==; qlappid=wx9cf8c670ebd68ce4; qlskey=v0aaf8a8220605ecfc95daf6157c92e4; qluin=085e9858e08a564fbb2a77475@wx.tenpay.com; qq_logtype=16; wx_session_time='+time1+'000; wzq_qlappid=wx9cf8c670ebd68ce4; wzq_qlskey=v0aaf8a8220605ecfc95daf6157c92e4; wzq_qluin=os-ppuBfapRIpK5KtE9LtuQSZTqA; zxg_openid=oA0GbjgEFB8yyOWfE5VzCpav0W_w; wzq_channel=..orv53p00gf001',
    }
    proxies = {                       "https": "https://127.0.0.1:8888"    }
    data='exchange=12&page_no=0&page_size=10&sign=e50889757ab13ec60683c580d865c175&source=xg&time=1616987645&type=hot&user_type=5'
    print(data)
    session.headers.update(header)
    r=session.post(url=url,headers=header,data=data,verify=False)
    # print(r.json())
    contentjson=r.json()['data']['concept_list']
    listdata=[]
    for data in contentjson:
        concept_name=data['concept_name']
        concept_zdf=data['concept_zdf']
        hot_rank=data['hot_rank']
        hot_reason=data['hot_spot']['hot_reason'][0]
        if len(hot_reason)>50:
            hot_reason = hot_reason[0:50]
        retext='领涨股：'
        tmp=''
        top2_stocks=data['top2_stocks']
        for stock in top2_stocks:
            topstockname=str(stock['stock_name'])
            topstockzdf = str(stock['stock_zdf'])
            tmp=tmp+topstockname+'  涨幅：'+topstockzdf+'|'
        tb.add_row([concept_name, concept_zdf, hot_rank, hot_reason, tmp])
        tmpdict={'热点板块':concept_name,'涨跌幅':concept_zdf,'排名':hot_rank,'原因':hot_reason,retext:tmp}
        listdata.append(tmpdict)

    header1 = ['热点板块 ', '涨跌幅 ', '排名', '原因','领涨股']
    tb.field_names = header1  # 设置表头
    outfile = '雪球最热股票.html'
    # outfile = '/opt/lampp/htdocs/hotstock.html'
    print(tb)
    s = tb.get_html_string()  # 格式化成html文件
    fw = open(outfile, 'a+', encoding='gbk')
    fw.write(s)  # 输出到文件
    fw.close()

if __name__ == '__main__':
    datalist=getdata()
    format_tohtml(datalist)
    hotbank = hotBank()#cookies里的值未解密，不能实时去获取信息


