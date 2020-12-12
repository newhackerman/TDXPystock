from __future__ import division
import tushare as ts
import datetime, re
import pandas as pds
import util.logout as log
pro = ts.pro_api('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')
ts.set_token('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')
#早盘选股，选量比>25的，现量大于3000手，3日涨幅% <15%,流通盘小150亿
###################sfile早盘竞价后导出EXCEL文件
def getstockopenamo(sfile):
    sfile1=sfile
    newlist=[]  #存取符合条件的个股记录
    #date1 =time.strftime("%Y%m%d", time.localtime())
    #date1 = sfile[-12:-4:1]  #取文件名中的日期
    date1 = re.search(r'\d+.xls$', sfile).group()[0:8]
    #print('日期为%s\t 早盘选股 '%date1)
    log.logout('日期： %s\t 早盘股 \r---------------------------------------'%date1)
    try:
        count=0
        list1=pds.read_excel(sfile1)
        # list2=list1.loc[:,['代码']]
        # list3=list1.loc[:,['开盘金额']]
        # list4 = list1.loc[:, ['开盘换手Z']]
        # list5 = list1.loc[:, ['涨幅%']]
        # list6 = list1.loc[:, ['现量']]
        # list7 = list1.loc[:, ['流通市值']]
        # list8 = list1.loc[:, ['3日涨幅%']]
        # list9 = list1.loc[:, ['20日涨幅%']]
        # list10 = list1.loc[:, ['开盘%']]
        #print(type(list2),type(list3))
        try:
            for i in  list1.index.values:     #一行一行处理
                count+=1
                list2 = list1.loc[i, ['代码']]
                codenum = str(list2['代码']).rjust(6, '0')
                #print('codenum',codenum)
                list11 = list1.loc[i, ['名称']]
                codename=str(format(list11['名称']))
                #print('codename', codename)
                list3 = list1.loc[i, ['开盘金额']]
                if '--' in str(list3) :
                    #print('此股数据有问题',codenum)
                    continue
                codeamo = str(format(list3['开盘金额']))
                #print('codeamo',codeamo)
                list4 = list1.loc[i, ['开盘换手Z']]
                if '--' in str(list4) :
                    #rint('此股数据有问题',codenum)
                    continue
                switchvalue=str(format(list4['开盘换手Z']))
                #print('switchvalue',switchvalue)
                list5 = list1.loc[i, ['涨幅%']]
                if '--' in str(list5):
                    # rint('此股数据有问题',codenum)
                    continue
                increase=str(format(list5['涨幅%']))
                #print('increase',increase)
                list6 = list1.loc[i, ['现量']]
                if '--' in str(list6):
                    # rint('此股数据有问题',codenum)
                    continue
                volline=str(format(list6['现量']))
                #print('volline', volline)
                list7 = list1.loc[i, ['流通市值']]
                if '--' in str(list7):
                    # rint('此股数据有问题',codenum)
                    continue
                temp=str(list7['流通市值'])
                temp1 =re.findall(r"[^\W\d_]+|\d+.\d+", temp)[0]
                Circulationmarketvalue =float(temp1)
                #print('Circulationmarketvalue', Circulationmarketvalue)
                list8 = list1.loc[i, ['3日涨幅%']]
                if '--' in str(list8):
                    # rint('此股数据有问题',codenum)
                    continue
                Threeincrease=str(format(list8['3日涨幅%']))
                #print('Threeincrease', Threeincrease)
                list9 = list1.loc[i, ['20日涨幅%']]
                if '--' in str(list9):
                    # rint('此股数据有问题',codenum)
                    continue
                tewincrease=str(format(list9['20日涨幅%']))
                #print('tewincrease', tewincrease)
                list10 = list1.loc[i, ['开盘%']]
                if '--' in str(list10):
                    # rint('此股数据有问题',codenum)
                    continue
                openpercent=str(format(list10['开盘%']))
                #print('openpercent', openpercent)
                list12 = list1.loc[i, ['量比']]
                if '--' in str(list12):
                    # rint('此股数据有问题',codenum)
                    continue
                volpercent = str(format(list12['量比']))
                #print('volpercent', volpercent)
                #print('{0},{01},{2},{3},{4},{5},{6},{7},{8},{9}'%(codenum,codeamo,switchvalue,
                #increase, volline,Circulationmarketvalue,Threeincrease,tewincrease,openpercent,codename))
                if float(volpercent)>1:     #有数据表示未停牌
                    # 按量比排序，选量比>25的，现量大于3000手，3日涨幅% <15% and 流通市值小于100亿
                    if float(openpercent) <4 and float(openpercent)>-1.5 and float(volpercent)>25 and float(volline)>3000 and float(Threeincrease)<15 and float(Circulationmarketvalue)<100:
                        newlist.append(str(codenum)+':'+str(codename)+':'+str(volpercent)+':'+str(volline)+':'+str(Circulationmarketvalue))
                        #print('量比条件个股代码为：%s: %s'%(codenum,codename))
                        log.logout('量比组合条件个股：  %s:  %s'%(codenum,codename))
                        #print(newlist)
                        # 按换手选 换手在在0.8到2之间，现量大于3000手，3日涨幅% <15% and 流通市值小于100亿
                    if float(openpercent) <4 and float(openpercent)>-1.5 and float(switchvalue) >0.9 and float(switchvalue)<=2 and float(volline) > 3000 and float(Threeincrease) < 15 and float(
                            Circulationmarketvalue) < 100:
                        newlist.append(str(codenum) + ':' + str(codename) + ':' + str(volpercent) + ':' + str(
                            volline) + ':' + str(Circulationmarketvalue))
                        log.logout('换手组合条件个股：  %s:  %s' % (codenum, codename))
                        #print('换手条件个股代码为：%s: %s' % (codenum, codename))
                        # print(newlist)
                else:
                    continue
                    print('该股暂停牌')
        except BaseException as be:
            print(be)
            print('处理%s 数据后出现问题'%count)
            print('处理股票：%s,出现问题'%codename)
            print(codenum,codeamo,switchvalue,
                increase, volline,Circulationmarketvalue,Threeincrease,tewincrease,openpercent,codename,volpercent)
            print('到此未有问题')
        #print(newlist)
    except FileNotFoundError as fnot1:
        print(fnot1)
        return newlist
    return  newlist
    for stockopendata in newlist:   #输出选择到的股膘
        print(stockopendata)

def procesopenstockprice(sfile):
    try:
        sfile1=sfile
        getstockopenamo(sfile1)  #读取导出的EXCEL 并写入当天的文件中
    except BaseException as ee:
        print(ee)
        print('处理异常请检查')
    print('处理完成')


spath='c:\\十档行情\\T0002\\export'
spathbak='c:\\十档行情\\T0002\\exportbak'
sfile1='c:\\十档行情\\T0002\\export\\板块指数20201126.xls'  #导出数据为excel /后每天执行一次
sfile2='c:\\十档行情\\T0002\\export\\沪深Ａ股20201126.xls'  #导出数据为excel /后每天执行一次
dpath='C:\\十档行情\\T0002\\signals\\signals_user_9601\\'


if __name__=='__main__':
    procesopenstockprice('C:\\十档行情\\T0002\\export\\沪深Ａ股20201211.xls')


#listfile =os.listdir(spath)
#下面代码每天调用一次即可
# for fl in listfile:
#     print('代处理的文件为：',spath+'\\'+fl)
#     if fl.endswith('xls'):
#         procesdata(spath+'\\'+fl, dpath)
#         print('文件：%s,处理成功！',spath+'\\'+fl)
#         if not os.path.exists(spathbak):
#             os.makedirs(spathbak)
#         else:
#             movefile(spath+'\\'+fl,spathbak+'\\'+fl)
#             print("move %s -> %s",fl,(spathbak+fl))

 #             #movefile(sfile2,spathbak+'\\'+'沪深Ａ股20201126.xls')
