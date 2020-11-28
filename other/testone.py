import sys
import io


import matplotlib
import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt

# import math #数字相关操作
# import requests  #爬虫
# import pandas as pd #对文件的处理
# import keyword #保留关键字
# import pymysql #操作mysql DB
# import json  #json与python 数据类型对应处理.
# import pickle #用于【python特有的类型】 和 【python基本数据类型】间进行转换
# import xml  #XML是实现不同语言或程序之间进行数据交换的协议
# import configparser #用于处理特定格式的文件，其本质上是利用open来操作文件。
# import shutil #高级的 文件、文件夹、压缩包 处理模块
# import logging #用于便捷记录日志且线程安全的模块
# import yaml #对yaml 进行处理
# import re # 正则表达式
# import random #
# import os
# import search
# import subprocess #调用shell命令的神器
# import cProfile # 性能测量模块
# import lxml
# import numpy  # scipy 科学计算  只要涉及到数值计算，基本上三件套都会用上
# import matplotlib # 画图只要涉及到数值计算，基本上三件套都会用上
# # import scrapy #     只要涉及到数值计算，基本上三件套都会用上
# import httpie #http 客户端
# import Pillow #操作图像库
# import Flake8 #代码规则检查
# import scikit-learn #机器学习库
# import jieba #非常简单易用的中文分词工具
# import theano #非常流行的一个深度学习库，在学术界用的比较多



# print ('hello world')
# file1=open('./test.log','a')
# filename=file1.name
# # if filename !="":
# #     print(filename)
# #     num=10
# #     i=0
# #     while(i<2):
# #         print('please input text realy write to file ')
# #         f1=file1.write('\n'+input())
# #         print(f1)
# #         i=i+1
# #     file1.close()
# # else:
# #     print("file name %s is not exist" %(filename))
#
#
#
# var = keyword.kwlist
# print (var)
#
# for i in range(0,5,2):
#     print (i,)
#
# for k in range(-100,0,100):
#     print(k)
#
# if True:
#     print ("true")
# else:
#     print ('false')
#
# if False:
#     print("false")
# else:
#     print("true")
#
# strtol="item"+"sdfk"+'sdfas'+"fsfs"+"\t\n"\
#         +"sdf"+'sfdsadfas'+"""\\t\t\n """+'''asdfsd\\t\\nafsad''' + r'sdfsdf=\\\\\\n\t\t\t\t\t'
# print (strtol,end="")
# sys.stdout.write(strtol)

# from io import _WindowsConsoleIO
# from sys import argv,path
# for i in sys.argv:
#     print(i)
# print ("this path is :%s" %sys.path)
# print(path,argv)
# a, b, c, d = 20, 5.5, True, 4+3j
# print(type(a),type(b),type(c),type(d))
# print(isinstance(a,int))
# dd='123456789'
# da=dd*2
# print(da)
# print(dd[::-1] )
# ''' 这是一个注释
# 而矣
# '''
# def add(a ,b):
#     if type(a)=='int' and type(b)=='int':
#         return a+b
#     else:
#         return str(a)+str(b)
# print(add(4,19))
# print(add('24fdsaf','asdjf23324'))
# print(add(12,'asdjf23324'))
# print(add(True,False))
# print(help(max))
# alist=[1,2,3,4,5,6,7,4,3,2,2,1,1,2,44,33,0,4,4,4,2,2,2,998,33]
# blist=[1,2,3,4,5,6,7,4,3,11111111111,2,1,1,2,44,33,0,4,4,4,2,2,2,998,33]
# print (max(alist,blist))
# for i in alist:
#     print(i,end=" ")
#     print(i)
#
# stra='jkadjfkldajfkdla;jfklfda;jklf;dasf'
#
# for i in stra:
#     a=(i)
#
#     print(a, end= ' ')
# list = ['Google', 'Runoob', 1997, 2000]
# print ("第三个元素为:%s " %(list[2]))
#
# for i in (range(len(list))):
#     print (list[i])
# lista=[1,23,7,3,3,4]
# listb=[3232,3222,'sdf',323,lista,23,32]
#
# for i in (range(len(listb))):
#     print(listb[i])
# listb.append("dsafkdsl")
# print(listb)
# print("3 在lista中出了:%d次" %lista.count(3))
# print(listb.insert(1,"3ewrwer"),listb)
# del listb[3]
# print(listb)
# listb.remove(listb[3])
# print(listb)
# # lista.reverse()
#
# print("排序前:",lista)
# lista.sort()
# print('排序后:' ,lista)
# listc=lista.copy()
# print(listc)
# listc.clear()
# print(listc)
# l = [i for i in range(0,1000,2)]
# print("偶数:",l[::1])
# l = [i for i in range(1,10000,2)]
# print("奇数:",l[::1])

# dd={"aa":11,"bb":12,"cc":13}
# print (dd["aa"])
# for a in dd:
#     print(a.upper().lower() ,end="")
#     print (dd[a])
# ee={"aa":11,"bc":12,"cd":13}
# ee["aadd"]=134
# ee["kldl"]=45
# ee["aa"]=3243
# print(ee.items())
# print(len(ee))
# print(str(ee))
# print(type(ee))
# print(ee.get("aa"),ee.values(),ee.keys(),ee.items())
# for key in ee.keys():
#     print(key,ee[key])
# for value in ee.values():
#     print(value)
# ee.update(dd)
# print(dd.items(),ee.items())
# ee.popitem()
# print(ee.items())
from _ast import In

from IPython.core.display import Image

'''
字典层层遍历:
'''
# citys={
#     '北京':{
#         '朝阳':['国贸','CBD','天阶','我爱我家','链接地产'],
#         '海淀':['圆明园','苏州街','中关村','北京大学'],
#         '昌平':['沙河','南口','小汤山',],
#         '怀柔':['桃花','梅花','大山'],
#         '密云':['密云A','密云B','密云C']
#     },
#     '河北':{
#         '石家庄':['石家庄A','石家庄B','石家庄C','石家庄D','石家庄E'],
#         '张家口':['张家口A','张家口B','张家口C'],
#         '承德':['承德A','承德B','承德C','承德D']
#     }
# }
# for i in citys:
#      print(i,":")
#      for k in citys[i]:
#          # print(k,citys[i].get(k))
#          print("\t",k,":")
#          for l in citys[i][k]:
#             print("\t \t",l)
'''-------------------------------------------'''
# a,b=0,1
# while b<10000:
#     print(b,end= ',')
#     a,b=b,a+b



# s=pd.Series([1,3,5,'np','nam',6,8])
# print(s)
# dates=pd.date_range('20130110',periods=3)
# print(dates)
# df=pd.dataFrame(np.random.randn(6,4),index=dates,columns=list('A','B','C','D'))
# print(str(df))

# if __name__ == '__main__':
#    print('程序自身在运行')
# else:
#    print('我来自另一模块')
#
# ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
# ts = ts.cumsum()
# ts.plot()

# import matplotlib
# import pandas as pd
# import numpy as np
# import  matplotlib.pyplot as plt

# import matplotlib
# import pandas as pd
# import numpy as np
# import  matplotlib.pyplot as plt
# ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
# ts = ts.cumsum()
# ts.plot()
# df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
# df = df.cumsum()
# plt.figure(); df.plot()
# '''一个模块被另一个模块引入时 其主程序自动运行'''

import sys
# os.chdir('../')
# list=os.get_exec_path()
# for i in list:
#     if i.__contains__("thon"):
#         print (i)
#     else:
#         print("",end="")
# try:
#     fd = open('test.log', 'a+')
#     if fd.fileno():
#         fd.write("adfasdfad\n")
#         # os.fsync(fd)
#         for b in fd.readlines():
#             print(str(b))
#         fd.close()
# except IOError as ioerr:
#     print(format(ioerr))
# fa=open('test.log','r')
# for i in fa.readlines():
#     print(i)
#     fa.close()
import os
# print(os.getcwd())
# os.chdir("../")
# print("返回上一级目录为:",os.getcwd())
# list=dir(os)
# for i in list:
#     print(i)
# os.system("ls -a")
# help(os)
# import shutil
# shutil.copy("./test.log",'./test..log2')

# import glob
# filelist=glob.glob('*.log*')
# l=[]
# print(filelist)
# for file in filelist:
#     f=open(file,'r+')
#     text=f.readlines()
#     l=text+l
#     f.close()
# print(l)
# filelist=['test..log2', 'test.log']
# for i in filelist:
#     print(i)
# os.system('rm -rf test..log2') #调用系统命令
# import copy
# list=[1,2,3,4,5]
# list2=[1,23,45,22,54]
# list3=copy.copy(list)+list2
# for i in list3:
#     print(i)
# print (sys.argv)
# sys.exit()
# re 正则表达式
# import  re
# l=re.match('[a-z]*','hello word 11 test file ')
# # print('lr.re',l.re)
# print('lr.string',l.string)
# print('lr.pos',l.pos)
# print('lr.endpos',l.endpos)
# print('lr.lastindex',l.lastindex)
# print('lr.end',l.end())
# print('lr.group',l.group())
# print('lr.re',l.lastgroup)
# print('lr.lastindex',l.lastindex)
#
# import math
# l=math.pi/44
# print(l)
# import random as rd
# l=rd.choice(["lzb","lb","xjg","hzs","lzc","",""])
# print(l)
# m=rd.sample([100,21,3,3,3,3,4,5,7,7,0],3)
# print(m)
#双色球随机生成
# import random as rd
# import IPython.core.display
# list=[2,17,3,4,5,6]
# for i in range(6):
#        f=int(rd.random()*37)
#        for k in list:
#            if f==k:
#                f = int(rd.random() * 37)
#        list[i] = f
#
# list.sort()
# lq=rd.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
# list.append(lq)
# print("本期双色球随机号码为", end=':')
# for l in list:
#     print(l,end=' ')
# print("恭喜发财", end='!')
# Image('fc.jpg')
import requests
requests.get('https://www.baidu.com/')


print(bin(1000000),ascii(1000000))