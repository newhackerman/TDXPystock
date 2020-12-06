import xlrd,pymysql
import json,time,re
import os
import logging
database='stock'
tablename='stockopendata'
configfile='D:/mysqlconfig.json'
excelfile='C:/十档行情/T0002/exportbak/沪深Ａ股20201130.xls'
#读取json格式的配置文件
def file2dict(path):
    with open(path, encoding="utf-8") as f:
        jsoncontent=json.load(f)
        # ##if jsoncontent.startswith(u'\ufeff'):
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
        j+=1
        code = sheet_1.cell(i,0).value
        name = sheet_1.cell(i,1).value
        zhangfu = sheet_1.cell(i,2).value
        kaipanhuanshuoz= sheet_1.cell(i,3).value
        kaipanjine =  sheet_1.cell(i,4).value
        huanshuonu = sheet_1.cell(i,6).value
        liangbi = sheet_1.cell(i,7).value
        xianliang = sheet_1.cell(i,9).value
        zongliang = sheet_1.cell(i,10).value
        zongjine =sheet_1.cell(i,11).value
        xianjia =sheet_1.cell(i,12).value
        junjia = sheet_1.cell(i,13).value
        liutongguyi = sheet_1.cell(i,14).value
        liutongsizhi =sheet_1.cell(i,15).value
        renjiusizhi = sheet_1.cell(i,16).value
        xifenhangye = sheet_1.cell(i,21).value
        diqu = sheet_1.cell(i,22).value
        siyingniu = sheet_1.cell(i,24).value
        huoyuedu = sheet_1.cell(i,34).value
        lianzhangtiansu=sheet_1.cell(i,36).value
        shanrizhangfu = sheet_1.cell(i,37).value
        ershirizhangfu = sheet_1.cell(i,38).value
        liushirizhangfu=sheet_1.cell(i,39).value
        huanshuoz = sheet_1.cell(i,41).value
        liutongsizhiz = sheet_1.cell(i,42).value
        #print(liutongsizhi)
        beitaxishuo =sheet_1.cell(i,45).value
        kaipan =sheet_1.cell(i,49).value
        gudongrenshuo = sheet_1.cell(i,84).value
        renjunchigu = sheet_1.cell(i,85).value
        liruntongbi = sheet_1.cell(i,86).value
        shuyutongbi =sheet_1.cell(i,87).value
        shijingniu = sheet_1.cell(i,88).value
        meigujingzhi =sheet_1.cell(i,93).value
        meigugongji = sheet_1.cell(i,95).value
        meiguweifenpei =sheet_1.cell(i,96).value
        meiguxianjinliu=sheet_1.cell(i,97).value
        maoliniu = sheet_1.cell(i,100).value
        yinyeilirunniu =sheet_1.cell(i,101).value
        jinlirunniu = sheet_1.cell(i,102).value
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
`zhangfu`         varchar(10),                 // 涨幅%,      
`kaipanhuanshuoz` varchar(10),                 // 开盘换手Z,  
`kaipanjine`      varchar(10),                 // 开盘金额,   
`huanshuonu`      varchar(10),                 // 换手%,      
`liangbi`         varchar(10),                 // 量比,       
`xianliang`       varchar(10),                 // 现量,       
`zongliang`       varchar(10),                  //总量,       
`zongjine`        varchar(10),                 // 总金额,     
`xianjia`         varchar(10),                 // 现价,       
`junjia`          varchar(10),                 // 均价,       
`liutongguyi`     varchar(10),                 // 流通股(亿), 
`liutongsizhi`    varchar(10),                 // 流通市值,   
`renjiusizhi`     varchar(10),                 // 人均市值,   
`xifenhangye`     varchar(10),                 // 细分行业,   
`diqu`            varchar(10),                  //地区,       
`siyingniu`       varchar(10),                 // 市盈(动,    
`huoyuedu`        varchar(10),                  //活跃度,     
`lianzhangtiansu` varchar(10),                 // 连涨天,     
`shanrizhangfu`   varchar(10),                  //3日涨幅%,   
`ershirizhangfu`  varchar(10),                 // 20日涨幅%,  
`liushirizhangfu` varchar(10),                 // 60日涨幅%,  
`huanshuoz`       varchar(10),               //   换手Z,      
`liutongsizhiz`   varchar(10),                 // 流通市值Z,  
`beitaxishuo`     varchar(10),                  //贝塔系数,   
`kaipan`          varchar(10),                 // 开盘%,      
`gudongrenshuo`   varchar(10),                 // 股东人数,   
`renjunchigu`     varchar(10),                 // 人均持股,   
`liruntongbi`     varchar(10),                //  利润同比%,  
`shuyutongbi`     varchar(10),                 // 收入同比%,  
`shijingniu`      varchar(10),                //  市净率,     
`meigujingzhi`    varchar(10),                 // 每股净资,   
`meigugongji`     varchar(10),                 // 每股公积,   
`meiguweifenpei`  varchar(10),                 // 每股未分配, 
`meiguxianjinliu` varchar(10),                 // 每股现金流, 
`maoliniu`        varchar(10),                 //毛利率%,    
`yinyeilirunniu`  varchar(10),                //  营业利润率%,
`jinlirunniu`     varchar(10),                 // 净利润率%		
`date`            DATE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index stockcode on stockopendata(code);
create index stockcode on stockopendata(name);
create index stockhanyi on stockopendata(xifenhangye);
select date,code ,name ,kaipanhuanshuoz,kaipanjine,liangbi,xianliang,liutongsizhi,liutongguyi,xifenhangye from stockopendata where name='中水渔业';
'''