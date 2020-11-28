#双色球随机生成
import random as rd
from IPython.display import display, Image
list=[2,17,3,4,5,6]
for i in range(6):
       f=int(rd.random()*37)
       for k in list:
           if f==k:
               f = int(rd.random() * 37)
       list[i] = f
list.sort()
lq=rd.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
list.append(lq)
print("本期双色球随机号码为", end=':')
for l in list:
    print(l,end=' ')
print("恭喜发财", end='!')
display(Image('fq.jpg'))