import xlrd,pymysql
import json,time,re
import shutil
import pandas as pds
from pywinauto import application
from pywinauto.application import *
from pywinauto import mouse
database='stock'
tablename='stockopendata'
configfile='./config/mysqlconfig.json'
#excelfile='C:/十档行情/T0002/exportbak/沪深Ａ股20201130.xls'
#读取json格式的配置文件
def file2dict(path):
    with open(path, encoding="utf-8") as f:
        jsoncontent=json.load(f)
        #if jsoncontent.startswith(u'\ufeff'):
        #     jsoncontent = jsoncontent.encode('utf8')[3:].decode('utf8')
        return jsoncontent

def dbconnect():      #建立连接
    dict = []
    dict = file2dict(configfile)  # 获取连接数据库需要的相关信息
      # 创建数据库连接
    conn = pymysql.connect(dict['host'], dict['user'], dict['password']
                           , dict['database'], charset='utf8')
    return conn

def TDX_OpenDataOutputTXT():
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
def getdbdate(date):
    sql = 'select  date from stockopendata where date=\''+date+'\' limit 1;'
    conn = dbconnect()
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
def datainsert(configfile,excelfile):
    date1 = re.search(r'\d+.txt$', excelfile).group()[0:8]       #截取文件名中的日期
    # 创建数据库连接
    conn =  dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # newdate=getdbdate(date1)
    # if newdate:
    #     print('表中数据已是最新！！')
    #     return 0

    #执行的sql语句
    sql ='''insert into stockopendata (code,name,zhangfu,liangbi,kaipan,huanshuonu,kaipanjine,zongjine,liutongguyi,liutongsizhi,lianzhangtiansu,shanrizhangfu,ershirizhangfu,liushirizhangfu,date          
) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    #打开文件
    # file = pds.read_excel(excelfile)
    file=pds.read_csv(excelfile, sep="\t",encoding='gbk')
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
def listdir(path): #传入根目录
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file) #获取绝对路径
        if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
            listdir(file_path)
        elif os.path.splitext(file_path)[1] == '.txt' : #判断文件是否是Excel文件
            file_list.append(file_path)
    return file_list #返回Excel文件路径列表

################处理后移动到bak目录
def movefile(sfile1,dfile1):
    try:
        shutil.move(sfile1, dfile1)
    except BaseException as be:
        print(be)


if __name__ == '__main__':
    # 数据导出
    # TDX_OpenDataOutputTXT()
    #将导出的数据写入表中
    path='C:/十档行情/T0002/export/'     #入库数据存放的目录
    spathbak='C:/十档行情/T0002/exportbak/'
    filelist=listdir(path)
    for file in filelist:
        print('start inserttodb', file)
        datainsert(configfile, file)
        print('insert complete', file)
        #movefile(file,spathbak) #不移走，其它代码还要用



''' 表结构如下

CREATE TABLE IF NOT EXISTS `stockopendata`(
`code`            varchar(8),
`name`            varchar(12),
`zhangfu`         float,
`liangbi`         float,
`kaipan`          float,
`huanshuonu`      float,
`kaipanjine`      float,
`zongjine`        float,
`liutongguyi`     varchar(15),
`liutongsizhi`    varchar(15),
`lianzhangtiansu` int,   
`shanrizhangfu`   float,     
`ershirizhangfu`  float,       
`liushirizhangfu` float, 
`date`            DATE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockcode on stockopendata(code);
create index stockname on stockopendata(name);
create index stockdate on stockopendata(date);
CREATE UNIQUE INDEX code_name_stockdate ON stockopendata(code,name,date);
----

CREATE TABLE IF NOT EXISTS `stockopendata`(           
`code`            varchar(8),                   //代码,       
`name`            varchar(12),                  //名称,       
`zhangfu`         float,                 // 涨幅%,      
`kaipanhuanshuoz` float,                 // 开盘换手Z,  
`kaipanjine`      float,                 // 开盘金额,   
`huanshuonu`      float,                 // 换手%,      
`liangbi`         float,                 // 量比,       
`xianliang`       float,                 // 现量,       
`zongliang`       float,                  //总量,       
`zongjine`        float,                 // 总金额,     
`xianjia`         float,                 // 现价,       
`junjia`          float,                 // 均价,       
`liutongguyi`     varchar(15),                 // 流通股(亿), 
`liutongsizhi`    varchar(15),                 // 流通市值,   
`renjiusizhi`     varchar(10),                 // 人均市值,   
`xifenhangye`     varchar(10),                 // 细分行业,   
`diqu`            varchar(10),                  //地区,       
`siyingniu`       float,                 // 市盈(动,    
`huoyuedu`        float,                  //活跃度,     
`lianzhangtiansu` int,                 // 连涨天,     
`shanrizhangfu`   float,                  //3日涨幅%,   
`ershirizhangfu`  float,                 // 20日涨幅%,  
`liushirizhangfu` float,                 // 60日涨幅%,  
`huanshuoz`       float,               //   换手Z,      
`liutongsizhiz`   varchar(15),                 // 流通市值Z,  
`beitaxishuo`     float,                  //贝塔系数,   
`kaipan`          float,                 // 开盘%,      
`gudongrenshuo`   int,                 // 股东人数,   
`renjunchigu`     int,                 // 人均持股,   
`liruntongbi`     float,                //  利润同比%,  
`shuyutongbi`     float,                 // 收入同比%,  
`shijingniu`      float,                //  市净率,     
`meigujingzhi`    float,                 // 每股净资,   
`meigugongji`     float,                 // 每股公积,   
`meiguweifenpei`  float,                 // 每股未分配, 
`meiguxianjinliu` float,                 // 每股现金流, 
`maoliniu`        float,                 //毛利率%,    
`yinyeilirunniu`  float,                //  营业利润率%,
`jinlirunniu`     float,                 // 净利润率%		
`date`            DATE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockcode on stockopendata(code);
create index stockname on stockopendata(name);
create index stockhanyi on stockopendata(xifenhangye);
create bitmap index stockdate on stockopendata(date);
select date,code ,name ,kaipanhuanshuoz,kaipanjine,liangbi,xianliang,liutongsizhi,liutongguyi,xifenhangye from stockopendata where name='中水渔业';
'''