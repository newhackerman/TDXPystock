
try:
    fw=open('testfile.txt', 'w', encoding='utf-8')
    fw.write('骚年，奋斗吧')
    print('骚年，奋斗吧', file=fw)
except BaseException as be:
    print(be)
    fw.close()

with open('testfile.txt', 'a+', encoding='utf-8') as fw1:
    txt='骚年，奋斗吧'
    fw1.write(txt)

