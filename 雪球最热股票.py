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
    print(tb)
    s = tb.get_html_string()  #格式化成html文件
    fw = open(outfile, 'a+', encoding='gbk')
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
    cookeis = 'device_id=e6b8423858c6fa03fa5f8ea2cc164e8e; s=c9133wut45; bid=8eb7a82092e1387f689981b0cdac6fde_kibfx3s0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1609921402,1610091659,1610671835,1810717039; xq_a_token=176b14b3953a7c8a2ae4e4fae4c848decc03a883; xqat=176b14b3953a7c8a2ae4e4fae4c848decc03a883; xq_r_token=2c9b0faa98159f39fa3f96606a9498edb9ddac60; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxMzQ0MzE3MSwiY3RtIjoxNjEwODg4ODUyNzA3LCJjaWQiOiJkOWQwbjRBWnVwIn0.HhQ3EXskYpztLUpaST9VzxvxZOGA3rnNYl_N5HDwL61PTJeY2qRcP1ABbc-zCybKBjRiI6d1_0B_OXyUX9qHO4OHLbC8VaTrfXRgcMJxCRT2pv8xmWgNJUIEoLvVw7qRPVhHzcWtdDr1f0wCKRJMnRtZPvuzjs5lHgGGsPSGXtoqY-pH5pwcWikAxXHeqN3uMPzS4M4Y-UG371UZoz4cbt-6KBckdi3d9pge2fGzj0W4MpCm1286zGCatSUf_bY6_DclMPRCqftIJD0v1TsMToMc3K2Kd5mPeGoHD1FvfvYIg-Ji79d8lC4myc3hdWXHLXHKmDuKZ2kMT5SVFsJ6Gw; u=261610888892323; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1610888894'

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
