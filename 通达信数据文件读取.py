from __future__ import division
import os
import struct as st
import tushare as ts
import string
import datetime, re
import time
import pandas as pds
import dateutil as dt
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

