import requests as req
from lxml import etree
import datetime ,time
import pandas as pds
import matplotlib.pyplot as plt
import prettytable as pt  # 格式化成表格输出到html文件
from pyecharts import options as opts
from pyecharts.charts import Page, Line

def get_participant(code,**defineDate):
    url = 'https://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspx'
    today = time.strftime('%Y-%m-%d', time.localtime())
    today = datetime.datetime.strptime(today, "%Y-%m-%d")
    if defineDate:
        yesterday=defineDate['date']
    else:
        yesterday = str((today + datetime.timedelta(days=-1)).strftime("%Y-%m-%d"))
    print(today, yesterday)

    tb = pt.PrettyTable()
    tb.align = 'c'  # 对齐方式（c:居中，l居左，r:居右）
    page = Page()
    c = Line()
    data={
    'today': today,
    '__EVENTTARGET': 'btnSearch',
    '__EVENTARGUMENT':'',
    'txtShareholdingDate': yesterday,
    'txtStockCode': code,
    'txtStockName':'' ,
    'txtParticipantID':'',
    'txtParticipantName':''
    }
    requst=req.session()
    response=requst.post(url=url,data=data)
    tree=etree.HTML(response.text)
    code=code
    txtStockName=tree.xpath('//input[@name="txtStockName"]/@value')[0]

    head=tree.xpath('//div[@id="pnlResultNormal"]/div[@class="search-details-table-container table-mobile-list-container"]//table/thead/tr')
    header=[]
    for line in head:
        participantid=line.xpath('./th[@data-column-class="col-participant-id"]/text()')[0]  #机构编号
        participantname=line.xpath('./th[@data-column-class="col-participant-name"]/text()')[0] #机构名称
        address=line.xpath('./th[@data-column-class="col-address"]/text()')[0] #机构地址
        shareholding=line.xpath('./th[@data-column-class="col-shareholding"]/text()')[0] #持股数量
        shareholding_percent=str(line.xpath('./th[@data-column-class="col-shareholding-percent"]/text()')[0]).split('/')[-1][2:].strip() #持股百分比
    header.append(participantid)
    header.append(participantname)
    # header.append(address)
    header.append(shareholding)
    header.append(shareholding_percent)
    print(code,txtStockName)
    data=[]
    tempdata=tree.xpath('//div[@id="pnlResultNormal"]/div[@class="search-details-table-container table-mobile-list-container"]//table/tbody//tr')
    i=0
    for line in tempdata:
        i+=1
        if i==10:
            break
        else:
            participantid=line.xpath('./td[@class="col-participant-id"]/div[2]/text()')[0]
            participantname=line.xpath('./td[@class="col-participant-name"]/div[2]/text()')[0]
            # address=line.xpath('./td[@class="col-address"]/div[2]/text()')[0]
            shareholding=line.xpath('./td[@class="col-shareholding text-right"]/div[2]/text()')[0]
            shareholding_percent=line.xpath('./td[@class="col-shareholding-percent text-right"]/div[2]/text()')[0]
        dict={'机构编号':participantid,'机构名称':participantname,'持股数量':shareholding,'持股百分比':shareholding_percent}
        tb.add_row([participantid,participantname,shareholding,shareholding_percent])
        data.append(dict)
    pdf=pds.DataFrame(data)
    tb.field_names = header  # 设置表头
    print(tb.get_string())
    #print(pdf)
    return pdf
if __name__ == '__main__':
    get_participant('00981')