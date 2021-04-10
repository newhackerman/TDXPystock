import struct as st
import os,re,json
import time
import util.logout as log
import pandas as pd
import tushare as ts
################本程序为早盘竞价异动处理
configfile = 'D:/mysqlconfig.json'

#读取配置文件
def get_config():
    with open(configfile, encoding="utf-8") as f:
        jsoncontent = json.load(f)
    f.close()
    return jsoncontent
###获取股票列表
def get_stockcodelist():
    jsoncontent=get_config()
    pro = ts.pro_api(jsoncontent['tushare'])
    stockdata = pd.DataFrame(pro.stock_basic(exchange='', list_status='L',
                                                      fields='ts_code,symbol,name,area,industry,list_date'))
    return stockdata
####读取股票文件txt 返回一个列表
def readStockinfo(stockfile):
    stocklist=[]
    context=''
    line={}
    with open(stockfile,'r') as bfile:
        while True:
            context = bfile.readline().strip('\n')
            if context:
                codenum,codename=context.split(',')
                #print(codename)
                line=codenum+':'+codename
                stocklist.append(line)
            else:
                break
        #print(list)
    return stocklist

####读取可转债文件 返回一个列表
def readKZZinfo(KZZfile):
    kzzlist=[]
    context=''
    line={}
    with open(KZZfile,'r') as bfile:
        while True:
            context = bfile.readline().strip('\n')
            if context:
                codenum,codename,kzzcode,kzzname=context.split(',')
                #print(codename)
                line=codenum+':'+codename+kzzcode+':'+kzzname
                kzzlist.append(line)
            else:
                break
        #print(list)
    return kzzlist

#/判断列表中是否存该可转债，找到返回可转债
def checkkzzinlist(kzzlist,code1):
    for i in kzzlist:
        codenum,codename,kzzcode,kzzname=i.split(',')
        #print('传入的股票数据为：',i,codenum,codename)
        if code1 == kzzcode:
            return kzzcode,kzzname
        else:
            #print('未找到对应股票',code1)
            pass

# /判断列表中是否存该股票，找到返回股票名称与代码
def checkinlist(list, code1):
    for i in list:
        codenum, codename = i.split(':')
        # print('传入的股票数据为：',i,codenum,codename)
        if code1 == codenum:
            return codenum, codename
        else:
            # print('未找到对应股票',code1)
            pass


            #通达信竞价文件读取 只读取最后两行,并进行计算
def readTDXUerSignals_9601(filename,codenumt,codenamet):
    listdata=[]
    #读取最后16个字节并计算，返回计算后的值与代码
    try:
        with open(filename,'rb') as fr:
            seek=4
            #fr.seek(50,2)
            str=fr.read()          #未找到较好的倒序读取方法，根据偏移量读取后，无法读到数据
            len1 = len(str) - 16   #定位到最后16个字符的位置（）
            #print(len1)
            #print(str)
            text1=st.unpack("I",str[len1:len1+seek])[0]
            text2=st.unpack("f",str[len1+seek:len1+2*seek])[0]
            text3 = st.unpack("I", str[len1+2*seek:len1+3 * seek])[0]
            text4 = st.unpack("f", str[len1+3*seek:len1+4 * seek])[0]
            #print(text1,text2,text3,text4)
            if text2:
                if float(text4)>5000000:   #竞价值太小不参与计算 要大于500万
                    value=round(text4/text2,3)
                else:
                    value=0
                    pass
                #listdata.append(str(codenum)+':'+str(float(value)))
            else:
                #print('股票：%s\t读到的值为空，无法计算' %(codenamet))
                value='0'  #给个0值 ，否则会出错
               #print(text1,text2)
            return codenumt,codenamet,value
    except FileNotFoundError as fnot:
        print('未找到文件：',filename)
        return codenumt, codenamet, 0

##############查找对应的可转债

###########股票异动值排序输出
def listsort(valuelist):
    #valuelist=['880963:消费1:1.89','880965:消费2:5.247','880966:消费3:1.147','880766:消费4:1.947','880666:消费6:9.247']
    date1 =time.strftime("%Y%m%d", time.localtime())
    newlist=[] #存取分离后的值
    newlist2=[]#存取排序后的值
    #print('今日早盘：%s,以下股票异动：'%(date1))
    log.logout('今日早盘： %s,异动股票：\r---------------------------------------'%(date1))
    for line in valuelist:     #把值分离出来 放在newlist里
        codenum1,codename1,value1=line.split(':')
        newlist.append(value1)   #存存分离后的值
    #print(newlist)
    newlist1=sorted(newlist, key = lambda x:float(x),reverse=True)   #对值进行逆序
    #print(newlist1)
    for i in newlist1:  #根据值再找到对应的股票
        for j in valuelist:
            codenum2,codename2,value2=j.split(':')
            if i==value2 and float(value2)>28 and float(value2)<30:  #只取异动值在28到30倍的，容易涨停（待验证）
                newlist2.append(codenum2+':'+codename2+':'+value2)
            else:
                continue
    #输出前15名
    #print(newlist2)
    i=1
    for info in newlist2:

        log.logout(info)
        # i += 1
        # if i>15:
        #     break
    return newlist2


########################### 早盘股票异动提醒（说明：要先写好股票数据）
def tdxstockOpenchange():
    # stockfile = 'D:/pythonTtest/TDXPystock/个股信息列表.txt'
    stocklist = get_stockcodelist()
    #print('股票列表为：',stocklist)
    sdir='C:/十档行情/T0002/signals/signals_user_9601'
    filelist= os.listdir(sdir)
    #print(len(filelist))
    newfilelist=[]       #股票文件列表
    valuelist=[]
    for stock in stocklist.iterrows():
        codenumV=str(stock[1]['ts_code'])[0:6]
        codenamev = stock[1]['name']
        if codenumV[0:2]=='60' or codenumV[0:2]=='68':
            newfile=sdir + '/' + '1_'+codenumV+'.dat'
        else:
            newfile = sdir + '/' + '0_' + codenumV + '.dat'
        newfilelist.append(newfile)
        codenum1, codename1, value = readTDXUerSignals_9601(newfile, codenumV, codenamev)
        try:
            valuelist.append(codenum1+':'+codename1+':'+str(value))
        except BaseException as be:
            print(be)
    #print(newfilelist)
    listsort(valuelist)         #调用列表排序，并输出前15个股票


if __name__=='__main__':
    tdxstockOpenchange()  #调用
    # kzzfile='D:/pythonTtest/TDXPystock/可转债与正股对应表.txt'
    # kzzlist=readKZZinfo(kzzfile)

#######################################################3

# valuelist=['880963:消费1:1.89','880965:消费2:5.247','880966:消费3:1.147','880766:消费4:1.947','880666:消费6:9.247']
# listsort(valuelist)
# filename='C:\\十档行情\\T0002\\signals\\signals_user_9601\\1_880966.dat'
# coden,codname,value=readTDXdata(filename,'880966','消费电子')
# print(coden,codname,value)

