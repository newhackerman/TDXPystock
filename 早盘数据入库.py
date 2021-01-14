import xlrd,pymysql
import json,time,re
import os
import logging
import pandas as pds
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
    file = pds.read_excel(excelfile)
    # sheet_1 = file.sheet_by_index(0) #根据sheet页的排序选取sheet
    # row_content = sheet_1.row_values(0) #获取指定行的数据，返回列表，排序自0开始
    # col_number = sheet_1.ncols  # 获取有数据的最大列数
    # row_number = sheet_1.nrows #获取有数据的最大行数
    # head=sheet_1.row_values(0) #获取表头


    #获取字段名对应的ID

    j=0 #控制提交频率
    i=1

    for i in file.index.values:
        j += 1
        try:
            e1 = file.loc[i, ['代码']]
            code = str(e1['代码']).rjust(6, '0')
            name = file.loc[i,['名称']].to_dict()['名称']
            zhangfu = file.loc[i,['涨幅%']].to_dict()['涨幅%']
            if '--' in str(zhangfu):
                zhangfu = 0
            kaipanhuanshuoz = file.loc[i,['开盘换手Z']].to_dict()['开盘换手Z']
            if '--' in str(kaipanhuanshuoz):
                kaipanhuanshuoz = 0
            kaipanjine =str( file.loc[i,['开盘金额']].to_dict()['开盘金额'])
            if '--' in str(kaipanjine):
                kaipanjine = 0
            huanshuonu = str(file.loc[i,['换手%']].to_dict()['换手%'])
            if '--' in str(huanshuonu):
                huanshuonu = 0
            liangbi = str(file.loc[i,['量比']].to_dict()['量比'])
            if '--' in str(liangbi):
                liangbi = 0
            xianliang = str(file.loc[i,['现量']].to_dict()['现量'])
            if '--' in str(xianliang):
                xianliang = 0
            zongliang =  str(file.loc[i,['总量']].to_dict()['总量'])
            if '--' in str(zongliang):
                zongliang = 0
            zongjine = str(file.loc[i,['总金额']].to_dict()['总金额'])
            if '--' in str(zongjine):
                zongjine = 0
            xianjia = str(file.loc[i,['现价']].to_dict()['现价'])
            if '--' in str(xianjia):
                xianjia = 0
            junjia = str( file.loc[i,['均价']].to_dict()['均价'])
            if '--' in str(junjia):
                junjia = 0
            liutongguyi =str( file.loc[i,['流通股(亿)']].to_dict()['流通股(亿)'])
            if '--' in str(liutongguyi):
                liutongguyi = 0
            liutongsizhi = str(file.loc[i,['流通市值']].to_dict()['流通市值'])
            if '--' in str(liutongsizhi):
                liutongsizhi = 0
            renjiusizhi = str(file.loc[i,['人均市值']].to_dict()['人均市值'])
            if '--' in str(renjiusizhi):
                renjiusizhi = 0
            xifenhangye =str(file.loc[i,['细分行业']].to_dict()['细分行业'])

            diqu = str(file.loc[i,['地区']].to_dict()['地区'])

            siyingniu =str( file.loc[i,['市盈(TTM)']].to_dict()['市盈(TTM)'])
            if '--' in str(siyingniu):
                siyingniu = 0
            huoyuedu = str(file.loc[i,['活跃度']].to_dict()['活跃度'])
            if '--' in str(huoyuedu):
                huoyuedu = 0
            lianzhangtiansu =str( file.loc[i,['连涨天']].to_dict()['连涨天'])
            if '--' in str(lianzhangtiansu):
                lianzhangtiansu = 0
            shanrizhangfu = str(file.loc[i,['3日涨幅%']].to_dict()['3日涨幅%'])
            if '--' in str(shanrizhangfu):
                shanrizhangfu = 0
            ershirizhangfu = str(file.loc[i,['20日涨幅%']].to_dict()['20日涨幅%'])
            if '--' in str(ershirizhangfu):
                ershirizhangfu = 0
            liushirizhangfu = str(file.loc[i,['60日涨幅%']].to_dict()['60日涨幅%'])
            if '--' in str(liushirizhangfu):
                liushirizhangfu = 0
            huanshuoz = str(file.loc[i,['换手Z']].to_dict()['换手Z'])
            if '--' in str(huanshuoz):
                huanshuoz = 0
            liutongsizhiz = str(file.loc[i,['流通市值Z']].to_dict()['流通市值Z'])
            if '--' in str(liutongsizhiz):
                liutongsizhiz = 0
            # print(liutongsizhi)
            beitaxishuo = str(file.loc[i,['贝塔系数']].to_dict()['贝塔系数'])
            if '--' in str(beitaxishuo):
                beitaxishuo = 0
            kaipan = str(file.loc[i,['开盘%']].to_dict()['开盘%'])
            if '--' in str(kaipan):
                kaipan = 0
            gudongrenshuo =str( file.loc[i,['股东人数']].to_dict()['股东人数'])
            if '--' in str(gudongrenshuo):
                gudongrenshuo = 0
            renjunchigu = str(file.loc[i,['人均持股']].to_dict()['人均持股'])
            if '--' in str(renjunchigu):
                renjunchigu = 0
            liruntongbi = str(file.loc[i,['利润同比%']].to_dict()['利润同比%'])
            if '--' in str(liruntongbi):
                liruntongbi = 0
            shuyutongbi = str(file.loc[i,['收入同比%']].to_dict()['收入同比%'])
            if '--' in str(shuyutongbi):
                shuyutongbi = 0
            shijingniu = str(file.loc[i,['市净率']].to_dict()['市净率'])
            if '--' in str(shijingniu):
                shijingniu = 0
            meigujingzhi = str(file.loc[i,['每股净资']].to_dict()['每股净资'])
            if '--' in str(meigujingzhi):
                meigujingzhi = 0
            meigugongji = str(file.loc[i,['每股公积']].to_dict()['每股公积'])
            if '--' in str(meigugongji):
                meigugongji = 0
            meiguweifenpei =str(file.loc[i,['每股未分配']].to_dict()['每股未分配'])
            if '--' in str(meiguweifenpei):
                meiguweifenpei = 0
            meiguxianjinliu = str(file.loc[i,['每股现金流']].to_dict()['每股现金流'])
            if '--' in str(meiguxianjinliu):
                meiguxianjinliu = 0
            maoliniu = str(file.loc[i,['毛利率%']].to_dict()['毛利率%'])
            #print(maoliniu)
            if '--' in str(maoliniu):
                maoliniu = 0
                #print(maoliniu)
            yinyeilirunniu = str(file.loc[i,['营业利润率%']].to_dict()['营业利润率%'])

            if '--' in str(yinyeilirunniu):
                yinyeilirunniu = 0
            jinlirunniu = str(file.loc[i,['净利润率%']].to_dict()['净利润率%'])
            if '--' in str(jinlirunniu):
                jinlirunniu = 0
            date=str(date1)
            values = (code,name,zhangfu,kaipanhuanshuoz,kaipanjine,huanshuonu,liangbi,xianliang,zongliang, zongjine,
                      xianjia,junjia,liutongguyi, liutongsizhi ,renjiusizhi ,xifenhangye,diqu , siyingniu,huoyuedu,
                      lianzhangtiansu,shanrizhangfu,ershirizhangfu,liushirizhangfu,huanshuoz,liutongsizhiz,beitaxishuo,
                      kaipan,gudongrenshuo,renjunchigu,liruntongbi ,shuyutongbi,shijingniu,meigujingzhi,meigugongji,
                      meiguweifenpei, meiguxianjinliu,maoliniu,yinyeilirunniu,jinlirunniu,date)
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
create bitmap index stockdate on stockopendata(date);
select date,code ,name ,kaipanhuanshuoz,kaipanjine,liangbi,xianliang,liutongsizhi,liutongguyi,xifenhangye from stockopendata where name='中水渔业';
'''