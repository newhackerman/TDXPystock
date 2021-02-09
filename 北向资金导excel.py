import bs4
import requests as req
import re,json,time
import prettytable as pt
from lxml import  etree

def result_to_htmlAExcel(all_Everydata,DateType):
    header = ['日期', '股票代码 ', '股票名称 ', '板块', '占流通股%', '最新价  ', '涨跌幅  ', '今日持股股数亿  ', '今日持股市值亿', '占流通股本%', '今日持股占总股本',
              '市值增幅', '市值增幅%']
    tb = pt.PrettyTable()
    tb.field_names=header #设置表头
    tb.align='l'  #对齐方式（c:居中，l居左，r:居右）
    j=0
    for listdata in all_Everydata:
        for row in listdata:  # 依次获取每一行数据
            j+=1
            jsdata = json.loads(row)
            HdDate = str(jsdata['HdDate'])[0:10]
            SCode = jsdata['SCode']
            SName = jsdata['SName']
            HYName = jsdata['HYName']
            SharesRate = jsdata['SharesRate']
            NewPrice = jsdata['NewPrice']
            Zdf = jsdata['Zdf']
            ShareHold = format(jsdata['ShareHold']/100000000,'.3f')
            ShareSZ = format(jsdata['ShareSZ']/100000000,'.3f')
            LTZB = format(jsdata['LTZB']*100, '.3f')
            ZZB = format(jsdata['ZZB'] *100, '.3f')
            ShareSZ_Chg_One = format(jsdata['ShareSZ_Chg_One'] / 100000000, '.3f')
            ShareSZ_Chg_Rate_One = format(jsdata['ShareSZ_Chg_Rate_One']*100, '.3f')
            tb.add_row([HdDate,SCode,SName,HYName,SharesRate,NewPrice,Zdf,ShareHold,ShareSZ,LTZB,ZZB,ShareSZ_Chg_One,ShareSZ_Chg_Rate_One])
            values=(HdDate,SCode,SName,HYName,SharesRate,NewPrice,Zdf,ShareHold,ShareSZ,LTZB,ZZB,ShareSZ_Chg_One,ShareSZ_Chg_Rate_One)

    print('记录条数：\t',j)
    sb=tb.get_csv_string()  #输出csv格式

    s=tb.get_html_string()  #获取html格式
    if DateType!=1:
        outfile='./北向资金_'+HdDate+'_'+str(DateType)+'.html'
        fw = open(outfile, 'w', encoding='gbk')
        print(s,file=fw)
        fw.close()

        with open('./北向资金_'+HdDate+'_'+str(DateType)+'.csv','w',encoding='gbk') as fcsv:
            fcsv.write(sb)
        fcsv.close()

        outfile='./北向资金'+'_'+str(DateType)+'.html'
        fw = open(outfile, 'w', encoding='gbk')
        print(s,file=fw)
        fw.close()

        outfile='./北向资金'+'_'+str(DateType)+'.csv'
        fw = open(outfile, 'w', encoding='gbk')
        print(sb,file=fw)
        fw.close()
    else:
        outfile = './北向资金_' + HdDate + '.html'
        fw = open(outfile, 'w', encoding='gbk')
        print(s, file=fw)
        fw.close()

        with open('./北向资金_' + HdDate  + '.csv', 'w', encoding='gbk') as fcsv:
            fcsv.write(sb)
        fcsv.close()

        outfile = './北向资金' + '.html'
        fw = open(outfile, 'w', encoding='gbk')
        print(s, file=fw)
        fw.close()

        outfile = './北向资金' + '.csv'
        fw = open(outfile, 'w', encoding='gbk')
        print(sb, file=fw)
        fw.close()
    #print(tb)
 #获取最近一个交易日的数据日期
def get_dfcfdate():
    url='http://data.eastmoney.com/hsgtcg/list.html'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    response=req.get(url=url,headers=headers).text
    tree=etree.HTML(response)
    tit=tree.xpath('//div[@class="maincont"]/div[@class="contentBox"]/div[@class="titbar"]/div[@class="tit"]//span/text()')[0]
    #print(tit)
    rex='(\d{4}-\d{2}-\d{2})'
    date=re.findall(rex,tit)[0]
    #print(date)
    return str(date)
 #从东方财富获取北资金数据
def get_north_EveryDaydata(DateType):
    header = ['日期', '股票代码 ', '股票名称 ', '板块', '占流通股%', '最新价  ', '涨跌幅  ', '今日持股股数亿  ', '今日持股市值亿', '占流通股本%', '今日持股占总股本',
              '市值增幅', '市值增幅%']
    if DateType not in (1,3,5,10):
        print('日期类型错误，只支持1日，3日，5日，10日')
        return None

    url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':'zh - CN, zh;    q = 0.9, en;    q = 0.8    ',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Cookie': 'Cookie: pgv_pvi=3794568192; _qddaz=QD.6ofmf2.j6jr4m.kat8wucp; ct=u_GCXp_V0BUfw6EE3hFHtqMglz3afgkppJcv5vbFImFCEcWBrdbJ1czxMgSRvdgdMHMxnKracqlOZgxC4VNfwrkiwCCnYCNVFUzHMie-NyeUGcc8-NdJwvaXLimNiEt9gsOQO3q161JU2fTSAHZYRo5byr67JKvMwuA_2qSbhls; ut=FobyicMgeV5ghfUPKWOH5wak5fe7PCdYa2maZFrymrOdfN-wAEFtpNp1MzH070EBSmKRLG6vmIcYwEk2SvuUDiGwHB7BHzpaN3m4xMthhPoNqi89FTByaNH4MkRCfEYW4JX960vY0ITlmRY-cPk1PQzTvxCYnVj0Ey0NtYOnUdj24K9O1_tKWeyEDf1k_bIV6hcX360Qn8yYsWTrETZTzGYR7tn62AgnDFAq58DbSa3StLkggc5c7wB94try8c_WEpaHHyl5rA7BBAJZkje3dZ7Q7pZSUWri; pi=3323115305075326%3bc3323115305075326%3b%e8%82%a1%e5%8f%8bjHWZa22110%3bAc4gMB%2bahzpZU8kVvDCm4%2f9QLFcpRepVrDlj4DSAFvQS9L41u5PjbhW1g0ATNFBs2U6jdaiAi0v97coryIUwYaBWyHAUTbi1GDBZdDmkrBugnCGTBDTgPjXURUbrtmze597viYIL2RjHQTBKDzTIQqxuco%2b4pIMvD3B%2f2gF3Z2HSKCRGXGX%2bMcFxewJmIXD8wOJYtqii%3bM4Rnsdjx0lNLDrlCNBv6VhW13wgvkjpsoKd52WM1JsrPCSqUd%2fySTvks6nwUjCNsGby4fYU2Y%2bbjGtRBVly22B%2bqdAhoqGh6XrZIWQGX4LDnpd4CKtckek2Rlq7r9qjcQSdzcprF%2bmmkr9EqKBQVnmt9ppYRhg%3d%3d; uidal=3323115305075326%e8%82%a1%e5%8f%8bjHWZa22110; sid=126018279; _ga=GA1.2.1363410539.1596117007; em_hq_fls=js; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; emshistory=%5B%22%E4%BA%BA%E6%B0%94%E6%8E%92%E8%A1%8C%E6%A6%9C%22%2C%22%E6%AF%94%E4%BA%9A%E8%BF%AA%E4%BA%BA%E6%B0%94%E6%8E%92%E5%90%8D%22%2C%22%E5%9F%BA%E9%87%91%E6%8E%92%E8%A1%8C%22%2C%22%E8%BF%913%E4%B8%AA%E6%9C%88%E8%B7%8C%E5%B9%85%E6%9C%80%E5%A4%A7%E7%9A%84%E5%9F%BA%E9%87%91%22%2C%22%E5%85%BB%E8%80%81%E9%87%91%E6%8C%81%E8%82%A1%E5%8A%A8%E5%90%91%E6%9B%9D%E5%85%89%22%2C%22%E5%A4%96%E7%9B%98%E6%9C%9F%E8%B4%A7%22%2C%22A50%22%2C%22%E6%81%92%E7%94%9F%E6%B2%AA%E6%B7%B1%E6%B8%AF%E9%80%9A%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4A%22%2C%22%E7%BB%86%E5%88%86%E8%A1%8C%E4%B8%9A%E9%BE%99%E5%A4%B4%22%5D; vtpst=%7c; HAList=d-hk-00288%2Cd-hk-00772%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Ca-sz-002008-%u5927%u65CF%u6FC0%u5149%2Ca-sz-002739-%u4E07%u8FBE%u7535%u5F71%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Cd-hk-00981%2Ca-sz-002082-%u4E07%u90A6%u5FB7%2Ca-sz-300511-%u96EA%u6995%u751F%u7269; cowCookie=true; st_si=40836386960323; waptgshowtime=2021126; qgqp_b_id=3a2c1ce1f45a81a3fa7cc2fbad8e2a24; intellpositionL=345px; st_asi=delete; st_pvi=03400063938128; st_sp=2020-05-23%2013%3A48%3A35; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=48; st_psi=20210126213702703-113300303605-1327257583; intellpositionT=1940.09px'
    }
    date1=get_dfcfdate()
    all_Everydata=[]
    for i in range(1,31,1): #北向资金数据每天有30页
        try:
            params = {'type': 'HSGT20_GGTJ_SUM',
                     'token': '894050c76af8597a853f5b408b759f5d',
                     'st': 'ShareSZ_Chg_One',
                     'sr': -1,
                     'p': i,
                     'ps': 50,
                     'js': 'var TpSlNIMe={pages:(tp),data:(x)}',
                     'filter': '(DateType='+str(DateType)+' and HdDate=\''+date1+'\')',
                     'rt': '53722283'}

            response=req.get(url=url,headers=headers,params=params)
            bstext=bs4.BeautifulSoup(response.content,'lxml')
            tempdata = bstext.find_all('p')
            temp=str(tempdata)
            regex = 'data:(.*?)}</p>'
            jsondata=str(re.findall(regex,temp,re.M))
            data=jsondata.replace('\\r\\n','',-1).replace('},','}},',-1).replace('[\'[','',-1).replace(']\']','',-1)
            listdata=data.split('},',-1)
            all_Everydata.append(listdata)
            time.sleep(1)
        except BaseException as be:
            print(be)
            continue
    return all_Everydata

if __name__ == '__main__':
    DateTy=[1,3,5,10]
    for DateType in DateTy:
        all_Everydata=get_north_EveryDaydata(DateType)
        result_to_htmlAExcel(all_Everydata,DateType)
        time.sleep(3)
