import requests as req
import prettytable as pt

def format_tohtml(datalist):
    header = ['股票代码 ', '股票名称 ', '热度值', '热度值变化']
    tb = pt.PrettyTable()
    tb.add_row(['+-----------+', '+-----------+', '+-----------+', '+-----------+'])
    tb.field_names = header  # 设置表头
    tb.align = 'l'  # 对齐方式（c:居中，l居左，r:居右）
    for data1 in datalist:
        for value in data1:
            stockcode = value['code']
            stockname = value['name']
            hotvalue = value['value']
            hotincrement = value['increment']
            #print('代码：%s 名称： %s 热度值：%s  热度值变动：%s' % (stockcode, stockname, hotvalue, hotincrement))

            tb.add_row(
                [stockcode, stockname, hotvalue, hotincrement])
        tb.add_row(['+-----------+','+-----------+','+-----------+','+-----------+'])
    outfile = '雪球最热股票.html'
    # outfile = '/opt/lampp/htdocs/hotstock.html'
    print(tb)
    jscode=''' <script language="JavaScript">setTimeout(function(){location.reload()},30000); </script>'''
    s = tb.get_html_string()  #格式化成html文件
    fw = open(outfile, 'a+', encoding='gbk')
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
    cookeis = 'device_id=e6b8423858c6fa03fa5f8ea2cc164e8e; s=c9133wut45; bid=8eb7a82092e1387f689981b0cdac6fde_kibfx3s0; cookiesu=641612859392955; Hm_lvt_1db88642e346389874251b5a1eded6e3=1611565185,1611826882,1612859385,1612919940; xq_a_token=62effc1d6e7ddef281d52c4ea32f6800ce2c7473; xqat=62effc1d6e7ddef281d52c4ea32f6800ce2c7473; xq_r_token=53a0f79d5bae795fb7abc6814dc0fc0410413016; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxNTYwMzIxNSwiY3RtIjoxNjEzMTg0Mjk2NDU4LCJjaWQiOiJkOWQwbjRBWnVwIn0.a3EmTx4ekMzI8fl17YcLZPsmWkawPJJF9yZZNF5lWr9oAoWmH2CvElUV49Xkg_SglA_sWGiN2uF1OBwkT4ii_yQOW45CViqaVvCAW3--qvOUIMWJDHvuvAQRbfitxkWztSUZ3feRSZVukTEZcd2VBZ6nXN_Bk2HghgjJdvJpu4awLMjnXWbhTbxxUqHZ_k7lgch3MulDEsnOEDFnuerbQ52UCc3lYcZ027wOoRDiUtQX6fNIzD-zFPEbn-i7BpN44hs8VDURnl53pr92Oj5T5KBUguBT23M6V9NYjMzTJSYX5OLP83JYYkNeX3tl5dcM2ihRU1KqkiJGx22nWSe4EA; u=951613184345028; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1613184347'

    headers = {'accept': 'application/json, text/plain, */*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
               'cookie': cookeis}
    datalist=[]
    for url in urllist:
        hotstock = req.get(url=url, headers=headers).json()
        data1 = hotstock['data']['items']
        datalist.append(data1)
    return datalist

if __name__ == '__main__':
    datalist=getdata()
    format_tohtml(datalist)
