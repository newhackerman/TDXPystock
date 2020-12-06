import xlrd,pymysql
import json,time,re
import os
import logging
database='stock'
tablename='stockopendata'
configfile='D:/mysqlconfig.json'
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
#读取excel 数据入mysql
def datainsert(configfile,excelfile):
    date1 = re.search(r'\d+.xls$', excelfile).group()[0:8]       #截取文件名中的日期
    # 创建数据库连接
    conn =  dbconnect()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #执行的sql语句
    sql ='''insert into stockopendata (code, name,zhangfu,  kaipanhuanshuoz,kaipanjine,huanshuonu,
    liangbi,xianliang ,zongliang, zongjine, xianjia ,junjia,  liutongguyi,  liutongsizhi ,renjiusizhi ,   
    xifenhangye,  diqu ,siyingniu,huoyuedu,lianzhangtiansu,shanrizhangfu,ershirizhangfu,liushirizhangfu,
    huanshuoz,  liutongsizhiz, beitaxishuo, kaipan, gudongrenshuo, renjunchigu,  liruntongbi ,shuyutongbi,    
    shijingniu, meigujingzhi,meigugongji,meiguweifenpei,meiguxianjinliu,maoliniu,yinyeilirunniu,jinlirunniu,    
date           
) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    #打开文件
    file = xlrd.open_workbook(excelfile)
    sheet_1 = file.sheet_by_index(0) #根据sheet页的排序选取sheet
    row_content = sheet_1.row_values(0) #获取指定行的数据，返回列表，排序自0开始
    col_number = sheet_1.ncols  # 获取有数据的最大列数
    row_number = sheet_1.nrows #获取有数据的最大行数
    j=0 #控制提交频率
    for i in range(1,row_number):
        j += 1
        code = sheet_1.cell(i, 0).value
        name = sheet_1.cell(i, 1).value
        zhangfu = sheet_1.cell(i, 2).value
        if '--' in str(zhangfu):
            zhangfu = 0
        kaipanhuanshuoz = sheet_1.cell(i, 3).value
        if '--' in str(kaipanhuanshuoz):
            kaipanhuanshuoz = 0
        kaipanjine = sheet_1.cell(i, 4).value
        if '--' in str(kaipanjine):
            kaipanjine = 0
        huanshuonu = sheet_1.cell(i, 6).value
        if '--' in str(huanshuonu):
            huanshuonu = 0
        liangbi = sheet_1.cell(i, 7).value
        if '--' in str(liangbi):
            liangbi = 0
        xianliang = sheet_1.cell(i, 9).value
        if '--' in str(xianliang):
            xianliang = 0
        zongliang = sheet_1.cell(i, 10).value
        if '--' in str(zongliang):
            zongliang = 0
        zongjine = sheet_1.cell(i, 11).value
        if '--' in str(zongjine):
            zongjine = 0
        xianjia = sheet_1.cell(i, 12).value
        if '--' in str(xianjia):
            xianjia = 0
        junjia = sheet_1.cell(i, 13).value
        if '--' in str(junjia):
            junjia = 0
        liutongguyi = sheet_1.cell(i, 14).value
        if '--' in str(liutongguyi):
            liutongguyi = 0
        liutongsizhi = sheet_1.cell(i, 15).value
        if '--' in str(liutongsizhi):
            liutongsizhi = 0
        renjiusizhi = sheet_1.cell(i, 16).value
        if '--' in str(renjiusizhi):
            renjiusizhi = 0
        xifenhangye = sheet_1.cell(i, 21).value
        diqu = sheet_1.cell(i, 22).value
        siyingniu = sheet_1.cell(i, 24).value
        if '--' in str(siyingniu):
            siyingniu = 0
        huoyuedu = sheet_1.cell(i, 34).value
        if '--' in str(huoyuedu):
            huoyuedu = 0
        lianzhangtiansu = sheet_1.cell(i, 36).value
        if '--' in str(lianzhangtiansu):
            lianzhangtiansu = 0
        shanrizhangfu = sheet_1.cell(i, 37).value
        if '--' in str(shanrizhangfu):
            shanrizhangfu = 0
        ershirizhangfu = sheet_1.cell(i, 38).value
        if '--' in str(ershirizhangfu):
            ershirizhangfu = 0
        liushirizhangfu = sheet_1.cell(i, 39).value
        if '--' in str(liushirizhangfu):
            liushirizhangfu = 0
        huanshuoz = sheet_1.cell(i, 41).value
        if '--' in str(huanshuoz):
            huanshuoz = 0
        liutongsizhiz = sheet_1.cell(i, 42).value
        if '--' in str(liutongsizhiz):
            liutongsizhiz = 0
        # print(liutongsizhi)
        beitaxishuo = sheet_1.cell(i, 45).value
        if '--' in str(beitaxishuo):
            beitaxishuo = 0
        kaipan = sheet_1.cell(i, 49).value
        if '--' in str(kaipan):
            kaipan = 0
        gudongrenshuo = sheet_1.cell(i, 84).value
        if '--' in str(gudongrenshuo):
            gudongrenshuo = 0
        renjunchigu = sheet_1.cell(i, 85).value
        if '--' in str(renjunchigu):
            renjunchigu = 0
        liruntongbi = sheet_1.cell(i, 86).value
        if '--' in str(liruntongbi):
            liruntongbi = 0
        shuyutongbi = sheet_1.cell(i, 87).value
        if '--' in str(shuyutongbi):
            shuyutongbi = 0
        shijingniu = sheet_1.cell(i, 88).value
        if '--' in str(shijingniu):
            shijingniu = 0
        meigujingzhi = sheet_1.cell(i, 93).value
        if '--' in str(meigujingzhi):
            meigujingzhi = 0
        meigugongji = sheet_1.cell(i, 95).value
        if '--' in str(meigugongji):
            meigugongji = 0
        meiguweifenpei = sheet_1.cell(i, 96).value
        if '--' in str(meiguweifenpei):
            meiguweifenpei = 0
        meiguxianjinliu = sheet_1.cell(i, 97).value
        if '--' in str(meiguxianjinliu):
            meiguxianjinliu = 0
        maoliniu = sheet_1.cell(i, 100).value
        #print(maoliniu)
        if '--' in str(maoliniu):
            maoliniu = 0
            #print(maoliniu)
        yinyeilirunniu = sheet_1.cell(i, 101).value
        if '--' in str(yinyeilirunniu):
            yinyeilirunniu = 0
        jinlirunniu = sheet_1.cell(i, 102).value
        if '--' in str(jinlirunniu):
            jinlirunniu = 0
        date=str(date1)
        values = (code,name,zhangfu,kaipanhuanshuoz,kaipanjine,huanshuonu,liangbi,xianliang,zongliang, zongjine,
                  xianjia,junjia,liutongguyi, liutongsizhi ,renjiusizhi ,xifenhangye,diqu , siyingniu,huoyuedu,
                  lianzhangtiansu,shanrizhangfu,ershirizhangfu,liushirizhangfu,huanshuoz,liutongsizhiz,beitaxishuo,
                  kaipan,gudongrenshuo,renjunchigu,liruntongbi ,shuyutongbi,shijingniu,meigujingzhi,meigugongji,
                  meiguweifenpei, meiguxianjinliu,maoliniu,yinyeilirunniu,jinlirunniu,date)
    #执行sql语句插入数据
        cursor.execute(sql,values)
        if j%500==0:
            conn.commit()
        else:
            continue
    conn.commit()  #最后少于500条，执行完循环后，提交一次。
    cursor.close()
    conn.close()
#列出所给目录中的所有excel 文件
def listdir(path): #传入根目录
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file) #获取绝对路径
        if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
            listdir(file_path)
        elif os.path.splitext(file_path)[1] == '.xls' or os.path.splitext(file_path)[1] == '.xlsx': #判断文件是否是Excel文件
            file_list.append(file_path)
    return file_list #返回Excel文件路径列表


if __name__ == '__main__':
    path='C:/十档行情/T0002/export/'     #入库数据存放的目录
    filelist=listdir(path)
    for file in filelist:
        if '沪深Ａ股20' in str(file):  #只处理 个股数据
            print('start inserttodb', file)
            datainsert(configfile, file)
            print('insert complete', file)


''' 表结构如下
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
select date,code ,name ,kaipanhuanshuoz,kaipanjine,liangbi,xianliang,liutongsizhi,liutongguyi,xifenhangye from stockopendata where name='中水渔业';
'''