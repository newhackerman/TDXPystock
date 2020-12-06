import 早盘数据入库 as indb
import prettytable as pt  #usege:https://www.cnblogs.com/Mr-Koala/p/6582299.html
import pymysql
outfile='stockopendata.html' #输出到文件

####################输出分析图表#####################################
def outmap(dataframe):
    pass

####################以表格的形式输出##################################
def formatresults(results,header):
    #results   查询到的数据集
    #header   要输出的表头
    tb = pt.PrettyTable()
    tb.field_names=header
    tb.align='r'  #右对齐
    tb.sortby = "日期"
    #tb.set_style(pt.DEFAULT)
    #tb.horizontal_char = '*'
    fw=open(outfile,'w',encoding='utf-8')
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
    s=tb.get_html_string()  #获取html格式
    print(s,file=fw)
    print(tb)

#######################根据条件查询mysql中的数据#######################
def dataselect(*condiction,**keyscondiction):
    #dict=indb.file2dict(indb.configfile)  #读取配置信息
    conn=indb.dbconnect()
    cursor= conn.cursor(cursor=pymysql.cursors.DictCursor)  #打开游标
    condictions= str(keyscondiction).strip('{').strip('}').replace(':','=',1).replace('\'','',2)
    #condictions =str(condiction).strip('(').strip(')')
    sql="select date,code ,name ,kaipanhuanshuoz,kaipanjine,liangbi,xianliang,liutongsizhi,liutongguyi,xifenhangye " \
        "from stockopendata where "+condictions+';'
    #print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # fetchall()获取所有记录，形成的是元组，results = cursor.fetchmany(10)获取前10条，results = cursor.fetchone()获取一条数据
        results = cursor.fetchall()
        #print(results)
        header= ['日期', '股票代码 ', '股票名称 ', '开盘换手Z', '开盘金额', '量比  ', '现量  ', '流通市值  ', '流通股本（亿）', '细分行业']
        formatresults(results,header)   #格式化输出
    except BaseException as be:
        print(be)
        print("Error: unable to fetch data")
    cursor.close()


if __name__ == '__main__':
    dataselect(code='600038')   #传入要查询的条件，例如：name='中直股份‘ ，date='2020-12-01'
