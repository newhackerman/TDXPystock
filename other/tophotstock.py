# this  fuction to finded top 10 hot stock to list ,help to decide select
import requests as rs
import html
import math
import os
import sys

# tonghuaxumurl='https://basic.10jqka.com.cn/stockph/attentionDegree.html?code=300674&updateDate=' #同花顺人气排名
#
# dfcfurl=''
# tdxurl=''
# xuequiurl='https://xueqiu.com/'#雪球人气排行榜
# dbsqurl='http://heheapp.com/index.html#!/app/rank'  #打板神器人气排行榜
# hotsum=0
#
# tsum=0
# vsum=0
# i=0
# while i<101:
#     if i%2:
#         vsum+=i
#     else :
#         tsum+=i
#     i+=1
#
# print('奇数和为：',vsum)
# print('偶数和为：',tsum)
#
# for item in('hello world!!!'):
#     print(item,'')
#
# for vtem in range(100):
#     print(vtem)
# i=0
# for i in range(100,999):
#     sd=int(i%10)
#     dd=int(i%100)//10
#     cd=i//100
#     #print(sd, dd, cd)
#     if (sd*sd*sd+dd*dd*dd+cd*cd*cd)==i:
#         print(sd,dd,cd)
#         print('水仙花数：',i)

# list1=[12,2,32,3,'sdafsdf',43,3443,'sdfsdf','asdfsdff','fffff']
# print(list1)
# print(list1[::-1])   #反向
# list2=list1[::-1]
# print(list2)
# print(list1[0])
# print(list1[-1])
# print(list1[2:9:])
# print(list1[2:9:2])
# list1.append(100) #在末尾添加元素
# print(list1[::-1])
# list1.remove(100)
# list1.extend('sdfasfsdafsdaf') #在末尾添加元素
# list1.insert(0,'add1') #在指定位置插入元素
# print(list1)
# list1.remove('add1') #移除指定的元素
# print(list1)
# list1.pop(1) #根据索引移除，默认删除最后一个元素
# print(list1,end='')   #不换行输出
# list1=[1,4,5,6,2,7,8,7,9]
# # lst=sorted(list1)   #内置函数会产生新的对象
# # print(lst)
# list1.sort() #对原对象排序，不产生新的对象
# print(list1)
# i=len(list1)
# j=i-1
# while j>=0:           #删除lsit 中的元素
#     list1.pop(j)
#     print(list1)
#     j=j-1

##################元组#########################333
# scores={'zhangsan':58,'lishi':89,'wangwu':71}      #字典
# print(scores)
#
# values=scores.values()
# value1=scores.get('zhangsan')
# keys=scores.keys()
#
# item1=scores.items()
# list2=item1
# print(keys)
# print(item1)
# for item in scores.items():        #遍历
#     print(item)
#
# copy1=scores.copy();
# print(copy1)
# # 元组

# t=(12,'sdsf',23,34,3,'sdfsdf',45,5,4,545,'sf',45,32)
# print(t,end='')
# t2='sdfksalf','sadfls',23
# print(t2,type(t2))
#           集合
# s1={10,20,30,40,50}
# s2={10,20,30,40,50,60.70}
# print(s1|s2) #并集
# print(s1.union(s2) ) #并集
# print(s1.difference(s2)) #交集
# str1='what are you doing here? ,你来干什么'
# index1=str1.index('f')
# index2=str1.rindex('f')
# find1=str1.find('ff')
# find2=str1.rfind('ff')
# find3=str1.find('FF')
# print(index1,index2,find1,find2)
# str2=str1.upper()
# print(str2)
# str2=str1.lower()
# print(str2)
# str3=str1.swapcase()   #大写转小写，小写转大写
# print(str3)
# str4=str1.capitalize() #首字母大写
# print(str4)
# str5=str1.title() #把每个单词的首字母大写其余小写
'''字符串的对齐操作'''
# st6=str1.center(36, '#')#当字符长度不够36时，居中对齐 两边填&
# st7=str1.ljust(36,'#') #左对齐
# st8=str1.rjust(36,'#')#右对齐
# print(st6)
# print(st7)
# print(st8)
'''字符串的分割'''
# s='What is  you name|/where |is to go/ when is|com*ming to here'
# s1=s.split('/')
# s2=s.split()
# s3=s.split('*')
# s4=s.split(sep=' ',maxsplit=4)
# s5=s.rsplit('|',2)
# s6=s.split('|')
# print(s1)
# print(s2)
# print(s3)
# print(s4)
# print(s5)
# print(s6)
# s='What is  you name|/where |is to go/ when is|com*ming to here'
# s1=s.isalnum()
# s2=s.isidentifier()
# s3=s.isspace()
# s4=s.isdigit()
# s5=s.isprintable()
# s6=s.isalpha() #字符组
# print(s1)
# print(s2)
# print(s3)
# print(s4)
# print(s5)
# print(s6)

# s='What is  you name|/where |is to go/ when is|com*ming to here'
# v='skladkskfjsklkfks'
# print(s>v)
# print(ord('c')>ord('b')) #AScii 码大小比较
# print(ord('c'),ord('b'))#对应的ascii值
# print(chr(99),chr(98)) #ascii对应的字符
# print(type(s))
# name='zhangsha'
# age=18
# sex='1'
# print('my name is%s,age=%d,sex=%s'%(name,age,sex))
# print('my name is {0} ,age={2} sex={1}'.format(name,sex,age))
# print('{0:.3f}'.format(3.1415926))
# s='会当凌绝顶，一览众山小'
# print(s.encode(encoding='GBK'))
# print(s.encode(encoding='utf-8'))
def filewcopy(source,dist):
    try:
        fw=open(dist,'ab')
        fw.seek(0)
        str='this is add context!'
        fw.write(str.encode())
        with open(source,'rb') as fp:
            i=0
            byte1=fp.readlines()
            for by in byte1:
               fw.write(by)
    except FileNotFoundError as fnot:
        print(fnot)
    except FileExistsError as fper:
        print(fper)
    except BaseException as be:
        print(be)
    finally:
        fw.close()
    #    fp.close()  #离开WITH 语句自动关闭
# source='C:\\Users\\test\\Desktop\\0_300563.dat'
# dist='C:\\Users\\test\\Desktop\\0_300564.dat'
# #filewcopy(source,dist)
# with open(dist,'rb') as fa:
#     print(fa.readlines())
#fp.close()
#函数的定义

# def add(a,b,c):
#     i = 0
#     while 1:
#         i += 1
#         if i>10:
#             return a+b+c+i
#         else:
#             print(a+b+c+i)
#
# sum=add(100,200,1.1)
# print(sum,sys.path)
# print(add(b=50,c=10,a=20))
#
# def fun(*args1):
#     i=len(args1)
#     print(i,args1)
#
# fun(1,3,1,5,5,1,1,55)
################异常处理
# def fun1():
#    a= input('a=')
#    b= input('b=')
#    try:
#         print(int(a)/int(b))
#    except BaseException as e:
#         if(a.isalpha() or b.isalpha()):
#             print("只能为数字")
#         print('出错了')
#         print(e)
#    else:
#         print(a/b)
#    finally:
#         print(a.join(b))
# fun1()

# try:
#    s1={'name':'zhangshan','age':14}
#    print(s1['age1'])
# except KeyError:
#    print('error')
#    print(KeyError)
# else:
#    print(s1['age1'])
#
########## 类              ##
# class Stuent:
#     name=''
#     sex=''
#     age=0
#     score=0
#     game=''
#     def __init__(self,name,sex,age,score,game):
#         self.name=name
#         self.sex=sex
#         self.age=age
#         self.score=score
#         self.game=game
# 
#     def add(self,aa,bb):
#         print(aa,bb)
#         return aa+bb
# 
#     def mules(self,a,b):
#         return a-b
# 
#     @classmethod
#     def drink(cls):
#         print('inner drink----------')
# 
#     @staticmethod
#     def play(str1):
#         print("faverater is play ",str1)
# 
# 
# stu1=Stuent(name='zhangshan',sex='1',age=19,score=88,game='football')
# stu2=Stuent(name='zhangshan',sex='1',age=19,score=88,game='football')
# #stu1.__init__(name='zhangshan',sex='1',age=19,score=88,game='football')
# print(stu1.name,stu1.age,stu1.score,stu1.game)
# ad1=stu1.add(44,66)
# mu1=stu1.mules(54,343)
# print(stu1.add(aa=55,bb=44),ad1,mu1,stu1.play('baskatiball'),stu1.drink())
# stu1.name=Stuent.name
# stu1.name='sadfsafsdaf'
# print(stu1.name,stu2.name)
# 
# def drink():
#     print('out his is drinking ....')
# 
# 
# print(stu1.drink)
# stu1.drink()
# stu1.drink=drink
# stu1.drink()
# print(stu1.drink)
# import  schedule
# import time
#
# def testschedule():
#     print('hello ')
# i=0
# schedule.every(3).seconds.do(testschedule)
# while True:
#     schedule.run_pending()
#     time.sleep(3)
#     i+=1
#     if i>10:
#         schedule.cancel_job(testschedule())
#         break
#
import os
def osopreation(command):
    os.system(command)
#cmd1=osopreation('notepad.exe')  #打开系统应用程序
#cmd2=os.startfile('C:\\Program\ Files\ (x86)\\Fiddler2\\Fiddler.exe')  #打开安装的应用程序
def listpwd():
    dirlist = os.getcwd()
    lstfile=os.walk(dirlist)
    for dirpath,dirname,filename in lstfile:
        for dir in dirname:
            print(os.path.join(dirpath,dir))
        for file in filename:
            if file.endswith('py'):
                print(os.path.join(dirpath,file))
        print('--------------')
#listpwd()    #遍历












import struct as st
import base64
