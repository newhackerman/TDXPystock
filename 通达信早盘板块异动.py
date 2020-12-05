#######################本程序为通达信早盘板块异动分析

import struct as st
import os,re
import time
import util.logout as log
import 通达信写自定义竞价数据文件 as soamo
#传入一个板块列表文件，用于判断是否为板，然后再读取板块对应的文件
#
#
####读取板块文件 返回一个列表
def readbandinfo(bandfile):
    list=[]
    context=''
    line={}
    with open(bandfile,'r') as bfile:
        while True:
            context = bfile.readline().strip('\n')
            if context:
                codenum,codename=context.split(',')
                #print(codename)
                line=codenum+':'+codename
                list.append(line)
            else:
                break
        #print(list)
    return list
#/判断列表中是否存该板块，找到返回板块名称与代码
def checkinlist(list,code1):
    for i in list:
        codenum,codename=i.split(':')
        #print('传入的板块数据为：',i,codenum,codename)
        if code1 == codenum:
            return codenum,codename
        else:
            #print('未找到对应板块',code1)
            pass

            #通达信竞价文件读取 只读取最后两行,并进行计算
def readTDXdata(filename,codenumt,codenamet):
    listdata=[]
    #读取最后16个字节并计算，返回计算后的值与代码
    try:
        with open(filename,'rb') as fr:
            seek=4
            #fr.seek(50,2)
            str=fr.read()          #未找到较好的倒序读取方法，根据偏移量读取后，无法读到数据
            len1 = len(str) - 16   #定位到最后16个字符的位置（）
            if len1<16:   #当文件中不足两行时，直接返回
                return codenumt, codenamet, 0
            #print(len1)
            #print(str)
            try:
                text1=st.unpack("I",str[len1:len1+seek])[0]
                #print(text1)
                text2=st.unpack("f",str[len1+seek:len1+2*seek])[0]
                #print(text2)
                text3 = st.unpack("I", str[len1+2*seek:len1+3 * seek])[0]
                text4 = st.unpack("f", str[len1+3*seek:len1+4 * seek])[0]
            except:
                print('error file is :',filename,codenumt,codenamet)
                value=0
            #print(text1,text2,text3,text4)
            if text2:
                value=round(text4/text2,3)
                #listdata.append(str(codenum)+':'+str(float(value)))
            else:
                print('读到的值为空，无法计算')
               #print(text1,text2)
            return codenumt,codenamet,value
    except FileNotFoundError as fnot:
        print('未找到文件：',filename)
        return codenumt, codenamet, 0
###########板块异动值排序
def listsort(valuelist):
    #valuelist=['880963:消费1:1.89','880965:消费2:5.247','880966:消费3:1.147','880766:消费4:1.947','880666:消费6:9.247']
    date1 =time.strftime("%Y%m%d", time.localtime())
    newlist=[] #存取分离后的值
    newlist2=[]#存取排序后的值
    #print('今日早盘：%s,以下板块异动：'%(date1))
    log.logout('今日早盘：%s,\t板块异动：\r---------------------------------------'%(date1))

    for line in valuelist:     #把值分离出来 放在newlist里
        codenum1,codename1,value1=line.split(':')
        newlist.append(value1)   #存存分离后的值
    #print(newlist)
    newlist1=sorted(newlist, key = lambda x:float(x),reverse=True)   #对值进行逆序
    #print(newlist1)
    for i in newlist1:  #根据值再找到对应的板块
        for j in valuelist:
            codenum2,codename2,value2=j.split(':')
            if i==value2:
                newlist2.append(codenum2+':'+codename2+':'+value2)
            else:
                continue
    #输出前15名
    #print(newlist2)
    i=0
    for info in newlist2:
        i+=1
        #print(info)
        log.logout(info)
        if i>14:
            break
    return newlist2

########################以下代码为处理早盘竞价数据################################
# spath='c:\\十档行情\\T0002\\export'
# spathbak='c:\\十档行情\\T0002\\exportbak'
# sfile1='c:\\十档行情\\T0002\\export\\板块指数20201126.xls'  #导出数据为excel /后每天执行一次
# sfile2='c:\\十档行情\\T0002\\export\\沪深Ａ股20201126.xls'  #导出数据为excel /后每天执行一次
# dpath='C:\\十档行情\\T0002\\signals\\signals_user_9601\\'
# listfile =os.listdir(spath)
# spath='c:\\十档行情\\T0002\\export'
# spathbak='c:\\十档行情\\T0002\\exportbak'
# sfile1='c:\\十档行情\\T0002\\export\\板块指数20201126.xls'  #导出数据为excel /后每天执行一次
# sfile2='c:\\十档行情\\T0002\\export\\沪深Ａ股20201126.xls'  #导出数据为excel /后每天执行一次
# dpath='C:\\十档行情\\T0002\\signals\\signals_user_9601\\'
# listfile =os.listdir(spath)
# #下面代码每天调用一次即可
# for fl in listfile:
#     print('代处理的文件为：',spath+'\\'+fl)
#     if fl.endswith('xls'):
#         soamo.procesdata(spath+'\\'+fl, dpath)
#         print('文件：%s,处理成功！',spath+'\\'+fl)
#         if not os.path.exists(spathbak):
#             os.makedirs(spathbak)
#         else:
#             soamo.movefile(spath+'\\'+fl,spathbak+'\\'+fl)
#             print("move %s -> %s",fl,(spathbak+fl))


########################以上代码为处理早盘竞价数据################################


########################### 早盘板块异动提醒（说明：要先写好板块数据）
def tdxbandchange():
    bandfile = 'D:\\pythonTtest\\TDXPystock\\板块列表.txt'
    bandlist = readbandinfo(bandfile)
    #print('板块列表为：',bandlist)
    sdir='C:\\十档行情\\T0002\\signals\\signals_user_9601'
    filelist= os.listdir(sdir)
    #print(len(filelist))
    newfilelist=[]       #板块文件列表
    valuelist=[]
    for band in bandlist:    #只需要处理板块文件
        codenumV,codenamev=band.split(':') #取得板块代码与名称
        newfile=sdir + '\\' + '1_'+codenumV+'.dat'
        newfilelist.append(newfile)
        codenum1, codename1, value = readTDXdata(newfile, codenumV, codenamev)
        try:
            valuelist.append(codenum1+':'+codename1+':'+str(value))
        except BaseException as be:
            print(be)
    listsort(valuelist)         #调用列表排序，并输出前15个板块

if __name__=='__main__':
    tdxbandchange()  #调用
#######################################################3

# valuelist=['880963:消费1:1.89','880965:消费2:5.247','880966:消费3:1.147','880766:消费4:1.947','880666:消费6:9.247']
# listsort(valuelist)
# filename='C:\\十档行情\\T0002\\signals\\signals_user_9601\\1_880966.dat'
# coden,codname,value=readTDXdata(filename,'880966','消费电子')
# print(coden,codname,value)

