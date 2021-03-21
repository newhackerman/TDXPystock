###################本程序为通信达早盘自定义数据的写盘与读取###########################
from __future__ import division
import struct as st
import tushare as ts
import pymysql
import json, re
import shutil
import pandas as pds
from pywinauto import application
from pywinauto.application import *
from pywinauto import mouse

class opendatainTodb():
    database = 'stock'
    tablename = 'stockopendata'
    configfile = 'D:/mysqlconfig.json'  #为ｊｓｏｎ格式的配置文件

    def __init__(self):
        self.jsoncontent=self.get_config()
        self.pro = ts.pro_api(self.jsoncontent['tushare'])

    def get_config(self):
        with open(self.configfile, encoding="utf-8") as f:
            jsoncontent = json.load(f)
        f.close()
        return jsoncontent

    def file2dict(self,path):
        with open(path, encoding="utf-8") as f:
            jsoncontent=json.load(f)
            #if jsoncontent.startswith(u'\ufeff'):
            #     jsoncontent = jsoncontent.encode('utf8')[3:].decode('utf8')
            return jsoncontent

    def dbconnect(self):      #建立连接
        dict = []
        dict = self.file2dict(self.configfile)  # 获取连接数据库需要的相关信息
          # 创建数据库连接
        conn = pymysql.connect(dict['host'], dict['user'], dict['password']
                               , dict['database'], charset='utf8')
        return conn

    def TDX_OpenDataOutputTXT(self):
        app=application.Application()
        tool_name = r'C:\十档行情\tdxw.exe'
        window_name = '通达信金融终端通赢版V7.47'
        app.start(tool_name)
        time.sleep(3)
        app.connect(path=tool_name)
        time.sleep(2)
        #登录
        mouse.move([985,420])
        mouse.click('left',[990,422])  #左键在什么位置点击
        time.sleep(15) #休息8秒，等等数据初始化加载
        # app.GetCursorPos()
        #点击A股，导出所有A股早盘数据
        mouse.click('left', [970, 990])
        ###点击选项数据导出，导出数据
        mouse.click('left',[1608, 11])
        time.sleep(1)
        mouse.click('left', [1655, 404])
        time.sleep(1)
        mouse.click('left', [705, 400])
        time.sleep(1)
        mouse.click('left', [1055, 547])
        time.sleep(1)
        mouse.click('left', [1110, 653])

        time.sleep(60)
        #点击取消，完成导出
        mouse.click('left', [1035, 583])
        time.sleep(1)
        ###########导出版块早盘数据
        # 点击版本块指数，导出所有版块数据
        mouse.click('left', [710, 995])
        time.sleep(1)
        mouse.click('left', [42, 67])
        ###点击选项数据导出，导出数据
        mouse.click('left', [1608, 11])
        time.sleep(1)
        mouse.click('left', [1655, 404])
        time.sleep(1)
        mouse.click('left', [705, 400])
        time.sleep(1)
        mouse.click('left', [1055, 547])
        time.sleep(1)
        mouse.click('left', [1110, 653])

        time.sleep(10)
        # 点击取消，完成导出
        mouse.click('left', [1016, 580])
        #沪深主要指数导出
        time.sleep(3)
        # 点击分类--》沪深主要指数，导出所有指数数据
        time.sleep(2)
        mouse.click('left', [110, 990])
        time.sleep(1)
        mouse.click('left', [120, 782])
        time.sleep(1)
        # ###点击选项数据导出，导出数据
        mouse.click('left',[1608, 11])
        time.sleep(1)
        mouse.click('left', [1655, 404])
        time.sleep(1)
        mouse.click('left', [705, 400])
        time.sleep(1)
        mouse.click('left', [1055, 547])
        time.sleep(1)
        mouse.click('left', [1110, 653])

        time.sleep(10)
        # 点击取消，完成导出
        mouse.click('left', [1016, 580])
    # 比较数据是否为最新的
    # 获取表中指定的日期
    def getdbdate(self,date):
        sql = 'select  date from stockopendata where date=\''+date+'\' limit 1;'
        conn = self.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        data1=None
        for data in result:
            data1 = data['date']
            print(data1)
            if data1 is None:
                return None
        cursor.close()
        conn.close()

    #读取excel 数据入mysql
    def datainsert(self,txtfile):
        date1 = re.search(r'\d+.txt$', txtfile).group()[0:8]       #截取文件名中的日期
        # 创建数据库连接
        conn =  self.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # newdate=getdbdate(date1)
        # if newdate:
        #     print('表中数据已是最新！！')
        #     return 0

        #执行的sql语句
        sql ='''insert into stockopendata (code,name,zhangfu,liangbi,kaipan,huanshuonu,kaipanjine,zongjine,liutongguyi,liutongsizhi,lianzhangtiansu,shanrizhangfu,ershirizhangfu,liushirizhangfu,date          
    ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        #打开文件
        # file = pds.read_excel(txtfile)
        file=pds.read_csv(txtfile, sep="\t",encoding='gbk')
        # print(file)
        # sheet_1 = file.sheet_by_index(0) #根据sheet页的排序选取sheet
        # row_content = sheet_1.row_values(0) #获取指定行的数据，返回列表，排序自0开始
        # col_number = sheet_1.ncols  # 获取有数据的最大列数
        # row_number = sheet_1.nrows #获取有数据的最大行数
        # head=sheet_1.row_values(0) #获取表头
        j=0 #控制提交频率
        for i in file.index.values:
            j += 1
            try:
                e1 = file.loc[i, ['代码']]
                code = str(e1['代码']).rjust(6, '0')
                name = file.loc[i,['名称']].to_dict()['名称']
                zhangfu = str(file.loc[i,['涨幅%']].to_dict()['涨幅%']).strip()
                if '--' in str(zhangfu):
                    zhangfu = 0
                liangbi = str(file.loc[i, ['量比']].to_dict()['量比']).strip()
                if '--' in str(liangbi):
                    liangbi = 0
                kaipan = str(file.loc[i, ['开盘%']].to_dict()['开盘%']).strip()
                if '--' in str(kaipan):
                    kaipan = 0
                huanshuonu = str(file.loc[i, ['换手%']].to_dict()['换手%']).strip()
                if '--' in str(huanshuonu):
                    huanshuonu = 0

                kaipanjine =str( file.loc[i,['开盘金额']].to_dict()['开盘金额']).strip()
                if '--' in str(kaipanjine):
                    kaipanjine = 0

                zongjine = str(file.loc[i, ['总金额']].to_dict()['总金额']).strip()
                if '--' in str(zongjine):
                    zongjine = 0
                liutongguyi = str(file.loc[i, ['流通股(亿)']].to_dict()['流通股(亿)']).strip()
                if '--' in str(liutongguyi):
                    liutongguyi = 0
                liutongsizhi = str(file.loc[i, ['流通市值']].to_dict()['流通市值']).strip()
                if '--' in str(liutongsizhi):
                    liutongsizhi = 0
                lianzhangtiansu =str( file.loc[i,['连涨天']].to_dict()['连涨天']).strip()
                if '--' in str(lianzhangtiansu):
                    lianzhangtiansu = 0
                shanrizhangfu = str(file.loc[i,['3日涨幅%']].to_dict()['3日涨幅%']).strip()
                if '--' in str(shanrizhangfu):
                    shanrizhangfu = 0
                ershirizhangfu = str(file.loc[i,['20日涨幅%']].to_dict()['20日涨幅%']).strip()
                if '--' in str(ershirizhangfu):
                    ershirizhangfu = 0
                liushirizhangfu = str(file.loc[i,['60日涨幅%']].to_dict()['60日涨幅%']).strip()
                if '--' in str(liushirizhangfu):
                    liushirizhangfu = 0
                date=str(date1)
                values = (code,name,zhangfu,liangbi,kaipan,huanshuonu,kaipanjine,zongjine,liutongguyi,liutongsizhi,lianzhangtiansu,shanrizhangfu,ershirizhangfu,liushirizhangfu,date)

            #执行sql语句插入数据
                # print(code,name,zhangfu,kaipanhuanshuoz,kaipanjine,huanshuonu,liangbi,xianliang,zongliang, zongjine,
                #           xianjia,junjia,liutongguyi, liutongsizhi ,renjiusizhi ,xifenhangye,diqu , siyingniu,huoyuedu,
                #           lianzhangtiansu,shanrizhangfu,ershirizhangfu,liushirizhangfu,huanshuoz,liutongsizhiz,beitaxishuo,
                #           kaipan,gudongrenshuo,renjunchigu,liruntongbi ,shuyutongbi,shijingniu,meigujingzhi,meigugongji,
                #           meiguweifenpei, meiguxianjinliu,maoliniu,yinyeilirunniu,jinlirunniu,date)
                #print('%s \n %s' %(sql,values))
                cursor.execute(sql,values)
                if j%50==0:
                    conn.commit()
                else:
                    continue
            except BaseException as be:
                print(be)
                # print(values)
                continue
        conn.commit()  #最后少于50条，执行完循环后，提交一次。
        print('插入数据：%d 条' %j)
        cursor.close()
        conn.close()
    # #列出所给目录中的所有excel 文件
    # def listdir(path): #传入根目录
    #     file_list = []
    #     for file in os.listdir(path):
    #         file_path = os.path.join(path, file) #获取绝对路径
    #         if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
    #             listdir(file_path)
    #         elif os.path.splitext(file_path)[1] == '.xls' or os.path.splitext(file_path)[1] == '.xlsx': #判断文件是否是Excel文件
    #             file_list.append(file_path)
    #     return file_list #返回Excel文件路径列表

    #列出所给目录中的所有txt 文件
    def listdir(self,path): #传入根目录
        file_list = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file) #获取绝对路径
            if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
                self.listdir(file_path)
            elif os.path.splitext(file_path)[1] == '.txt' : #判断文件是否是txt文件
                file_list.append(file_path)
        return file_list #返回Excel文件路径列表

    ################处理后移动到bak目录
    def movefile(self,sfile1,dfile1):
        try:
            shutil.move(sfile1, dfile1)
        except BaseException as be:
            print(be)


#获取当前鼠标位置
def GetCursorPos():
    while True:
        print(win32api.GetCursorPos())
        time.sleep(3)
#通达信早盘数据导出

#########解码
def STOCKdecode(date,codeamo):     #可以解出日期了,竞价数据要用f解
    text1=st.unpack("I",date)[0]
    text2 = st.unpack("f", codeamo)[0]
    return text1,text2
    # with open('C:/Users/test/Desktop/0_300563.dat','rb') as fr:
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
    date1 = re.search(r'\d+.txt$', sfile).group()[0:8]
    print('文件名中的日期为%s'%date1)
    try:
        count=0
        list1=pds.read_csv(sfile, sep="\t",encoding='gbk')

        for i in  list1.index.values:
            #row_data = list1.loc[i, ['代码', '开盘金额']].to_dict()
            e1=list1.loc[i, ['代码']].to_dict()
            codenum = str(e1['代码']).rjust(6, '0')
            if not codenum.isdigit():   #如果读到的不是数字，则跳过
                continue
            e2 = list1.loc[i, ['开盘金额']].to_dict()
            codeamo=str(format(e2['开盘金额']))

            #需要写编码功能)
            if codenum=='' or  codeamo=='':  #如果开盘金额是空的，或代码是空的则跳过（股票未开盘无意义）
                continue
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

#下面代码每天调用一次即可
if __name__=='__main__':
    spath = 'c:/十档行情/T0002/export/'
    spathbak = 'c:/十档行情/T0002/exportbak/'
    dpath = 'c:/十档行情/T0002/signals/signals_user_9601/'
    listfile = os.listdir(spath)
    print(listfile)


    #########将导出数据写入stockopendata表
    intodb=opendatainTodb()
    intodb.TDX_OpenDataOutputTXT()  # 导出竞价数据为ＴＸＴ
    # filelist = intodb.listdir(spath)
    for file in listfile:
        if file.endswith('txt'):
            print('start inserttodb', file)
            intodb.datainsert(spath+file)
            print('insert complete', file)
    #########将数据写入stockopendata表完成

    if not os.path.exists(dpath):
        print('目标目录不存在，请检查！')
        exit(1)
    for fl in listfile:
        if fl.endswith('txt'):
            print('待处理的文件为：', spath + fl)
            procesdata(spath+fl, dpath)
            print('文件：%s处理成功！'%(spath+fl))
            if not os.path.exists(spathbak):
                os.makedirs(spathbak)
            else:
                movefile(spath+fl,spathbak+fl)  #处理完移走
                print("move %s -> %s" %(fl,(spathbak+fl)))