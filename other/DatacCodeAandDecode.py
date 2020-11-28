from __future__ import division
import os
import struct as st
import tushare as ts
import string
import datetime, re
import time
import pandas as pds
import dateutil as dt
pro = ts.pro_api('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')
ts.set_token('d0bf482fc51bedbefa41bb38877e169a43d00bd9ebfa1f21d28151c7')

#########解码
def STOCKuncode(date,codeamo):     #可以解出日期了,竞价数据要用f解
    text1=st.unpack("I",date)[0]
    text2 = st.unpack("f", codeamo)[0]
    return text1,text2
    # with open('C:\\Users\\test\\Desktop\\0_300563.dat','rb') as fr:
    #     seek=4
    #     str=fr.read()
    #    # aa=st.pack('f', 0)
    #     for a in range(0,len(str),seek*2):
    #        text1=st.unpack("I",str[a:a+seek])[0]
    #        text2=st.unpack("f",str[a+seek:a+seek+seek])[0]
    #        text3=st.pack('I',text1)  #整型编码
    #        text4=st.pack('f',text2)   #float 编码
    #        print(text1,text2)
#STOCKuncode()
#########编码
def stockcode(date,codeamo):
    seek =4
    text1=st.pack('I', int(date))
    #print(text1)
    text2=st.pack('f', float(codeamo))
    #print(text2)
    return text1+text2

###################处理板块竞价数据
def getbandopenprice(sfile,dpath):
    test_data=[]
    sfile1=sfile
    #date1 =time.strftime("%Y%m%d", time.localtime())
    #date1 = sfile[-12:-4:1]  #取文件名中的日期
    date1 = re.search(r'\d+.xls$', sfile).group()[0:8]
    print('文件名中的日期为%s',date1)
    try:
        count=0
        list1=pds.read_excel(sfile1)
        list2=list1.loc[:,['代码']]
        list3=list1.loc[:,['开盘金额']]
        dict1={}
        #print(type(list2),type(list3))
        flag=0
        for i in  list1.index.values:
            #row_data = list1.loc[i, ['代码', '开盘金额']].to_dict()
            e1=list1.loc[i, ['代码']].to_dict()
            codenum=str(e1['代码']).rjust(6,'0')
            e2=list1.loc[i, ['开盘金额']].to_dict()
            codeamo=str(format(e2['开盘金额']))
            #print(codenum,codeamo)
            #test_data.append(row_data)
            # dat=date1.join(codenum).join(codeamo)
            # print(dat)
            #需要写编码功能)
            fflowdata=stockcode(date1,codeamo)
            #print(fflowdata) #编码后的数据
            #print(codenum[0:3], codenum[0:3], codenum[0:3])
            if codenum[0:3]=='600' or codenum[0:3]=='688' or codenum[0:3]=='880':
                dfilename=dpath+'1_'+codenum+'.dat'
                try:
                    fw1=open(dfilename,'ab+')
                    print(dfilename)
                except FileNotFoundError as fnot:
                    fw1=open(dfilename,'wb')
                fw1.write(fflowdata)
                fw1.close()

            elif codenum[0:3]=='300' or codenum [0:2]=='00':
                dfilename = dpath + '0_' + codenum + '.dat'
                try:
                    fw1 = open(dfilename, 'ab+')
                    print(dfilename)
                except FileNotFoundError as fnot:
                    fw1 = open(dfilename, 'wb')
                fw1.write(fflowdata)
                fw1.close()
            else:
                print('股票代码不存或不支持')
                continue
    except FileNotFoundError as fnot1:
        print(fnot1)
        return

#################处理个股竞价数据
def getstockopenprice(sfile,dpath):
    test_data=[]
    sfile1 = sfile
    #date1 =time.strftime("%Y%m%d", time.localtime())
    date1 = re.search(r'\d+.xls$', sfile).group()[0:8]
    #date1 = sfile[-12:-4:1]  # 取文件名中的日期（文件名路径长度不能变）
    try:
        count=0
        list1=pds.read_excel(sfile1)
        list2=list1.loc[:,['代码']]
        list3=list1.loc[:,['开盘金额']]
        flag=0
        for i in  list1.index.values:
            #row_data = list1.loc[i, ['代码', '开盘金额']].to_dict()
            e1=list1.loc[i, ['代码']].to_dict()
            codenum=str(e1['代码']).rjust(6,'0')
            e2=list1.loc[i, ['开盘金额']].to_dict()
            codeamo=str(format(e2['开盘金额']))
            #需要写编码功能)
            fflowdata=stockcode(date1,codeamo) #调用编码功能
            #print(fflowdata) #编码后的数据
            #print(codenum[0:3], codenum[0:3], codenum[0:3])
            if codenum[0:3]=='600' or codenum[0:3]=='688' or codenum[0:3]=='880':
                dfilename=dpath+'1_'+codenum+'.dat'
                try:
                    fw1=open(dfilename,'aw+')
                except FileNotFoundError as fnot:
                    fw1=open(dfilename,'wb')
                fw1.write(fflowdata)
                fw1.close()
            elif codenum[0:3]=='300' or codenum [0:2]=='00':
                dfilename = dpath + '0_' + codenum + '.dat'
                try:
                    fw1 = open(dfilename, 'ab+')
                except FileNotFoundError as fnot:
                    fw1 = open(dfilename, 'wb')
                fw1.write(fflowdata)
                fw1.close()
            else:
                print('股票代码不存或不支持')
                continue
    except FileNotFoundError as fnot1:
        print(fnot1)
        return

#每天调用一次即可(板块调一次，个股调用一次)
def procesdata(sfile,dpath):
    try:
        sfile1=sfile
        getbandopenprice(sfile1, dpath)  #读取导出的EXCEL 并写入当天的文件中
    except BaseException as ee:
        print(ee)
        print('处理异常请检查')
    print('处理完成')
sfile='D:\\十档行情\\T0002\\export\\板块指数20201125.xls'  #导出数据为excel /后每天执行一次
sfile2='C:\\十档行情\\T0002\\export\\沪深Ａ股20201125.xls'  #导出数据为excel /后每天执行一次
dpath='D:\\十档行情\\T0002\\signals\\signals_user_9601\\'
#procesdata(sfile2,dpath)

def getdate():
    filename='D:\\十档行情\\T0002\\export\\板块指数20201125.xls'
    reg=re.search(r'\d+.xls$',filename).group()[0:8]
    print(reg)

getdate()
#######早盘竞价异动板块处理######读取最后两行的数据计算异动比 所有的文件都读完后，进行排序
#######分别读取文件最后两行
#######分别对最后两行数据进行解码
#######对解码后的数据进行计算
#######对计算结果 排序
#################################################
def yidong(dpath):
    priceamo=''   #竞价额
    codename=''    #名称
    codenum=''     #代码
    lastline1=''   #最后一行
    lastline2=''   #最后第二行
    dict1={}      #存取解释后的行
    list1=[]      #存取所有解释后的行
    listpath=os.listdir(dpath)
    for filename in listpath:
        if filename.encode('dat'):
            pass
        else:
            continue
    return list1


def sortlist(list1):
    list2=[]
    return list2













