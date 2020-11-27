from __future__ import division
import os
import struct as st
import tushare as ts
import string
import datetime, re
import time
import pandas as pds
import shutil
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
            if '指数' in sfile1:        #处理指数时统一用1—
                dfilename = dpath + '1_' + codenum + '.dat'
                try:
                    fw1 = open(dfilename, 'ab+')
                    print(dfilename)
                except FileNotFoundError as fnot:
                    fw1 = open(dfilename, 'wb')
                fw1.write(fflowdata)
                fw1.close()
            elif codenum[0:2]=='60' or codenum[0:3]=='688' or codenum[0:3]=='880':
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
                dfilename = dpath + '1_' + codenum + '.dat'
                try:
                    fw1 = open(dfilename, 'ab+')
                except FileNotFoundError as fnot:
                    fw1 = open(dfilename, 'wb')
                fw1.write(fflowdata)
                fw1.close()
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
            if '指数' in sfile1:        #处理指数时统一用1—
                dfilename = dpath + '1_' + codenum + '.dat'
                try:
                    fw1 = open(dfilename, 'ab+')
                    print(dfilename)
                except FileNotFoundError as fnot:
                    fw1 = open(dfilename, 'wb')
                fw1.write(fflowdata)
                fw1.close()
            elif codenum[0:2]=='60' or codenum[0:3]=='688' or codenum[0:3]=='880':
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
                dfilename = dpath + '1_' + codenum + '.dat'
                try:
                    fw1 = open(dfilename, 'ab+')
                except FileNotFoundError as fnot:
                    fw1 = open(dfilename, 'wb')
                fw1.write(fflowdata)
                fw1.close()

    except FileNotFoundError as fnot1:
        print(fnot1)
        return
################处理后移动到bak目录
def movefile(sfile1,dfile1):
    try:
        shutil.move(sfile1, dfile1)
    except BaseException as be:
        print(be)
#每天调用一次即可(板块调一次，个股调用一次)
def procesdata(sfile,dpath):
    try:
        sfile1=sfile
        getbandopenprice(sfile1, dpath)  #读取导出的EXCEL 并写入当天的文件中
    except BaseException as ee:
        print(ee)
        print('处理异常请检查')
    print('处理完成')



spath='c:\\十档行情\\T0002\\export'
spathbak='c:\\十档行情\\T0002\\exportbak'
sfile1='c:\\十档行情\\T0002\\export\\板块指数20201126.xls'  #导出数据为excel /后每天执行一次
sfile2='c:\\十档行情\\T0002\\export\\沪深Ａ股20201126.xls'  #导出数据为excel /后每天执行一次
dpath='C:\\十档行情\\T0002\\signals\\signals_user_9601\\'
listfile =os.listdir(spath)
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



            #通达信竞价文件读取
def readTDXdata(filename):     #可以解出日期了,竞价数据要用f解
    with open(filename,'rb') as fr:
        seek=4
        str=fr.read()
        listdata=[]
       # aa=st.pack('f', 0)
        for a in range(0,len(str),seek*2):
           text1=st.unpack("I",str[a:a+seek])[0]
           text2=st.unpack("f",str[a+seek:a+seek+seek])[0]
           # text3=st.pack('I',text1)  #整型编码
           # text4=st.pack('f',text2)   #float 编码
           listdata.append(text1+text2)
           #print(text1,text2)
        return listdata
#STOCKuncode()

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
# ##################调用代码
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
