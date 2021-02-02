import 早盘数据入库 as indb
import prettytable as pt  #useage:https://www.cnblogs.com/Mr-Koala/p/6582299.html
import pymysql
import pyecharts       #可视化图表输出  useage:https://blog.csdn.net/update7/article/details/89086454
import sys
outfile='stockopendata.html' #输出到文件

####################输出分析图表#####################################
def outmap(dataframe):
    bar=pyecharts.charts.Bar()
    bar.add_dataset(dataframe)
    bar.render()
####################以表格的形式输出##################################
def formatresults(tablename,results,header):
    #results   查询到的数据集
    #header   要输出的表头
    tb = pt.PrettyTable()
    tb.field_names=header #设置表头
    tb.align='l'  #对齐方式（c:居中，l居左，r:居右）
    #tb.sortby = "日期"
    #tb.set_style(pt.DEFAULT)
    #tb.horizontal_char = '*'
    fw=open(outfile,'w',encoding='utf-8')
    if tablename=='stockopendata':
        for row in results:  # 依次获取每一行数据

            date = row['date']  # 第1列
            # print(date)
            code = row['code']
            name = row['name']
            kaipanhuanshuoz = row['kaipanhuanshuoz']
            kaipanjine = row['kaipanjine']
            liangbi = row['liangbi']
            xianliang = row['xianliang']
            liutongsizhi = row['liutongsizhi']
            liutongguyi = row['liutongguyi']
            xifenhangye = row['xifenhangye']
            # # 打印结果
            # print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % (
            # date, code, name, kaipanhuanshuoz, kaipanjine, liangbi, xianliang, liutongsizhi, liutongguyi, xifenhangye))
            tb.add_row([date,code,name,kaipanhuanshuoz,kaipanjine,liangbi,xianliang,liutongsizhi,liutongguyi,xifenhangye])
    print('记录条数：\t',len(results))
    if tablename=='stockinfo':
        for row in results:  # 依次获取每一行数据
            #print(row)
            #date = row['date']  # 第1列
            # print(date)
            mcode = row['mcode']
            code = row['code']
            name = row['name']
            mark = row['mark']
            markname=row['markname']
            info = str(row['info']).strip()
            if len(info)>65:
                info = str(row['info']).strip()[0:65]

            #value = row['value']

            # # 打印结果
            # print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % (
            # date, code, name, kaipanhuanshuoz, kaipanjine, liangbi, xianliang, liutongsizhi, liutongguyi, xifenhangye))
            tb.add_row([mcode,code,name,mark,markname,info])

    s=tb.get_html_string()  #获取html格式
    print(s,file=fw)
    print(tb)
    #outmap(tb)

#######################根据条件查询mysql中的数据#######################
def dataselect(tablename,*condiction,**keyscondiction):
    #dict=indb.file2dict(indb.configfile)  #读取配置信息
    conn=indb.dbconnect()
    cursor= conn.cursor(cursor=pymysql.cursors.DictCursor)  #打开游标

    condictions= str(keyscondiction).strip('{').strip('}').replace(':','=',1).replace('\'','',2)
    #print('condiction',condiction)
    #print('keyscondiction',keyscondiction)
    if len(condiction) >= 1:
        condictions=str(condiction).strip('(').strip(')').replace('\"','',-1).rstrip(',');
        #print(condictions)
    #condictions =str(condiction).strip('(').strip(')')
    if tablename == 'stockopendata':
        sql="select date,code ,name ,kaipanhuanshuoz,kaipanjine,liangbi,xianliang,liutongsizhi,liutongguyi,xifenhangye " \
        "from "+ tablename +" where "+condictions+";"
    if tablename=='stockinfo':
        sql = "select mcode,code,name,mark,markname,info from " + tablename + " where " + condictions + ";"
        #print(sql)
    #print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # fetchall()获取所有记录，形成的是元组，results = cursor.fetchmany(10)获取前10条，results = cursor.fetchone()获取一条数据
        results = cursor.fetchall()
        #print(results)
        if tablename=='stockopendata':
            header= ['日期', '股票代码 ', '股票名称 ', '开盘换手Z', '开盘金额', '量比  ', '现量  ', '流通市值  ', '流通股本（亿）', '细分行业']
        if tablename=='stockinfo':
            header = ['市场代码', '股票代码 ','股票名称', '信息ID','信息名称', '对应信息']
        formatresults(tablename,results,header)   #格式化输出
    except BaseException as be:
        print(be)
        print("Error: unable to fetch data")
    cursor.close()


if __name__ == '__main__':
    tablename1='stockopendata'
    tablename2='stockinfo'
    var=sys.argv #可以接收从外部传入参数
    #查个股概念信息，或某概念包含的股票信息
    lon=len(var)
    if lon==2:
        var1=sys.argv[1]
        dataselect(tablename2, var1)
    elif lon<2:
        var1=r"info like '%降解塑料%'"
        dataselect(tablename2,var1)   #传入要查询的条件，例如：name="中直股份‘ ，date='2020-12-01' 支持单条件如 (r"name in ('中直股份','珠江啤酒','深物业A')")
    elif lon==3:
        var1=sys.argv[1]
        var2=sys.argv[2]
        dataselect(var1,var2)
    else:
        print('parameters error!')
    #查早盘数据
    #dataselect(tablename1, name='科隆股份')  #r"name in('','','') "  //
    #dataselect(tablename2, name='科隆股份')