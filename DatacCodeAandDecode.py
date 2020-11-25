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













#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 将通达信的日线文件转换成CSV格式
def stockdaydata2csv(source_dir, file_name, target_dir):
    # 以二进制方式打开源文件
    try:
        source_file = open(source_dir + os.sep + file_name, 'rb')
        buf = source_file.read()
        source_file.close()

        # 打开目标文件，后缀名为CSV
        target_file = open(target_dir + os.sep + file_name + '.csv', 'w')
        buf_size = len(buf)
        rec_count = int(buf_size / 32)
        #print(rec_count)
        begin = 0
        end = 32
        # 4字节 如20091229
        # 开盘价*100
        # 最高价*100
        # 最低价*100
        # 收盘价*100
        # 成交额
        # 成交量
        # 保留值

        header = str('date') + ', ' + str('open') + ', ' + str('high') + ', ' + str('low') + ', ' \
            + str('close') + ', ' + str('amount') + ', ' + str('vol') + ', ' + str('保留') + '\n'
        target_file.write(header)
        for i in range(rec_count):
            # 将字节流转换成Python数据格式
            # I: unsigned int
            # f: float
            a= st.unpack('IIIIIfII', buf[begin:end])
            #print(a)
            line = str(a[0]) + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
                + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
                + str(a[6]) + ', ' + str(a[7]) + '\n'
            #print(line)
            target_file.write(line)
            begin += 32
            end += 32
        target_file.close()
    except FileNotFoundError as fnot:
        print('file is not found')
    except TypeError as tper:
        print(tper)
    except BaseException as ber:
        print(ber)


# source1 = 'C:\\十档行情\\vipdoc\\sz\\lday'
# #source1 = 'E:\\pythondata\\tmp2'
# source2 = 'C:\\十档行情\\vipdoc\\sh\\lday'
# target = 'E:\\pythondata\\tmp1'
# file_list1 = os.listdir(source1)
# for f1 in file_list1:
#     stockdaydata2csv(source1, f1, target)
# file_list2 = os.listdir(source2)
# for f2 in file_list2:
#     stockdaydata2csv(source2, f2, target)

def stockmindata2csv(source_dir, file_name, target_dir):
    # 以二进制方式打开源文件
    try:
        source_file = open(source_dir + os.sep + file_name, 'rb')
        buf = source_file.read()
        source_file.close()

        # 打开目标文件，后缀名为CSV
        target_file = open(target_dir + os.sep + file_name + '.csv', 'w')
        buf_size = len(buf)
        rec_count = int(buf_size / 32)
        #print(rec_count)
        begin = 0
        end = 32
        # 4字节 如20091229
        # 开盘价*100
        # 最高价*100
        # 最低价*100
        # 收盘价*100
        # 成交额
        # 成交量
        # 保留值

        header = str('date') + ', ' + str('open') + ', ' + str('high') + ', ' + str('low') + ', ' \
            + str('close') + ', ' + str('amount') + ', ' + str('vol') + ', ' + str('保留') + '\n'
        target_file.write(header)
        for i in range(rec_count):
            # 将字节流转换成Python数据格式
            # I: unsigned int
            # f: float
            a= st.unpack('IfffffII', buf[begin:end])
            #print(a)
            if len(a) <= 0: break
            #t = st.unpack('IfffffII', buf[begin:end])
            mins = (a[0] >> 16) & 0xffff
            mds = a[0] & 0xffff
            month = int(mds / 100)
            day = mds % 100
            hour = int(mins / 60)
            minute = mins % 60
            # datet = "d-d d:d" % (month,day,hour,minute)
            #data.append((stkID, (month, day, hour, minute), t[1], t[2], t[3], t[4], t[5], t[6], t[7]))
            #date_format = datetime.datetime.strptime(str(a[0]), '%Y%M%d')
            date_format = str(month)+str(day)+str(hour)+str(mins)
            line = date_format + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
                + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
                + str(a[6]) + ', ' + str(a[7]) + '\n'
            #print(line)
            target_file.write(line)
            begin += 32
            end += 32
        target_file.close()
    except FileNotFoundError as fnot:
        print('file is not found')
    except TypeError as tper:
        print(tper)
    except BaseException as ber:
        print(ber)

# source1 = 'C:\\十档行情\\vipdoc\\sz\\lday'
# source1 = 'E:\\pythondata\\tmp2'
# # source2 = 'C:\\十档行情\\vipdoc\\sh\\lday'
# target = 'E:\\pythondata\\tmp1'
# file_list1 = os.listdir(source1)
# for f1 in file_list1:
#     stockmindata2csv(source1, f1, target)
# file_list2 = os.listdir(source2)
# for f2 in file_list2:
#     stockdaydata2csv(source2, f2, target)



#from readths2 import *
# 2010-09-02 by 厚朴

basedir = r'e:pythondatatmp2' #如果你的安装路径不同,请改这里

exp_dir    = basedir + r'T0002export'
#exp_dir    = basedir + r'T0002export_back'
lc5_dir_sh = basedir + r'Vipdocshfzline'
#lc5_dir_sh = r'D:2965ydzqwsjyVipdocshfzline'
lc5_dir_sz = basedir + r'Vipdocszfzline'
day_dir_sh = basedir + r'Vipdocshlday'
day_dir_sz = basedir + r'Vipdocszlday'

stkdict = {} #存储股票ID和上海市、深圳市的对照


#############################################################
# read 5分钟数据
# example readlc5(r'E:new_gxzq_v6Vipdocshfzlinesh600000.lc5')
#############################################################

def readlc5(p_name):
       """tdx 5min 数据
          日期上低16位表示月日，高16位表示分钟
          这个结构个人感觉就不如同花顺做的巧妙
              在一个4字节中把 年 月 日 时 分 都记录下来了
       """
       f = open(p_name,'rb')
       stkID = os.path.split(p_name)[1]
       stkID = os.path.splitext(stkID)[0]
       if(stkID[0:2]).lower() == 'sh' or (stkID[0:2]).lower() == 'sz':
           stkID = stkID[2:]
       icnt = 0
       data = []
       while 1:
           raw = f.read(4*8)
           if len(raw) <= 0 : break
           t = st.unpack('IfffffII',raw)
           mins = (t[0] >> 16) & 0xffff
           mds  = t[0] & 0xffff
           month = int(mds / 100)
           day   =int( mds % 100)
           hour = int(mins / 60)
           minute =int(mins % 60)
           #print(mins,mds,month,day,hour,minute)
           #datet = "d-d d:d" % (month,day,hour,minute)
           #data=str(stkID)+str(month)+str(day)+str(hour)+str(minute)+t[1]+t[2]+t[3]+t[4]+t[5]+t[6]+t[7]
           data.append((stkID,(month,day,hour,minute),t[1],t[2],t[3],t[4],t[5],t[6],t[7]))
           #print datet,t[1],t[2],t[3],t[4],t[5],t[6],t[7]
           icnt += 1
       ## end while
       f.close()
       return data
p_name='E:\\pythondata\\tmp2\\sz002004.lc1'

# data=readlc5(p_name)
# for line in data:
#     print(line)
#############################################################
#构造通达信5min数据文件
# data 结构
#[stkID,(月,日,时,分),open,high,low,close,amt,vol,0]
#############################################################
def writelc5(p_name,data,addwrite = True):
    if addwrite :
       fout = open(p_name,'ab')
    else:
       fout = open(p_name,'wb')
    for i in data:
       t = i[1][0]*100+i[1][1] + ( (i[1][2] * 60 + i[1][3]) << 16)
       raw = st.unpack('IfffffII',t,i[2],i[3],i[4],i[5],i[6],i[7],i[8])
       fout.write(raw)
    ## end for
    fout.close()

'''

上述fmt中，支持的格式为：
FORMAT	C TYPE	PYTHON TYPE	STANDARD SIZE	NOTES
x	pad byte	no value	 	 
c	char	string of length 1	1	 
b	signed char	integer	1	(3)
B	unsigned char	integer	1	(3)
?	_Bool	bool	1	(1)
h	short	integer	2	(3)
H	unsigned short	integer	2	(3)
i	int	integer	4	(3)
I	unsigned int	integer	4	(3)
l	long	integer	4	(3)
L	unsigned long	integer	4	(3)
q	long long	integer	8	(2), (3)
Q	unsigned long long	integer	8	(2), (3)
f	float	float	4	(4)
d	double	float	8	(4)
s	char[]	string	 	 
p	char[]	string	 	 
P	void *	integer	 	(5), (3)

'''

