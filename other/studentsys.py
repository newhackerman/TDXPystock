# student  management system
import os
import re

def menu():
    print('---------------students information manager system------------------------------------')
    print('----------------funtion list-----------------------------------')
    print('\t\t\t\t0.if choice 0  exit system---------------------------')
    print('\t\t\t\t1.input student information----------------------------')
    print('\t\t\t\t2.find student informantion----------------------------')
    print('\t\t\t\t3.delete student infomantion---------------------------')
    print('\t\t\t\t4.modify student infomation----------------------------')
    print('\t\t\t\t5.sort by your select --------------------------------')
    print('\t\t\t\t6.count student infomation ---------------------------')
    print('\t\t\t\t7.show all students information -----------------------')
def insert():
    allstudents=[]
    while True:
        perstudent= {}
        id=input('plsease input id Ex:  1001 ')
        if id=='':
            break
        name = input('plsease input name')
        if name == '':
            break
        sex = input('plsease input sex')
        if sex == '':
            break
        try:
            java = float(input('plsease input java score '))
            if java == '':
                break
            python = float(input('plsease input python score '))
            if python =='':
                break
            english =float(input('plsease input english score '))
            if english== '':
                break
        except:
            print('input error')
            continue
        perstudent= {'id':id,'name':name,'sex':sex,'java':java,'python':python,'english':english}
        allstudents.append(perstudent)
        answer=input('are sure to continue inpput student information y/n ')
        if answer.upper()=='Y':
            continue
        else:
             break
    savefile(allstudents)
    print('input information save to file success!!')
def search():
    pass
def delete():
    pass
def modify():
    pass
def sort():
    pass
def total():
    if os.path.exists(filename):
        fr=open(filename,'r',encoding='utf-8')
        studentlist=fr.readlines()
        if studentlist:
            print('student sum :'+str(len(studentlist))+' person!!')
        else:
            print('context is null!!!!')
    else:
        print('file not found!!!')

def showall():
    if os.path.exists(filename):
        fr=open(filename,'r',encoding='utf-8')
        studentlist=fr.readlines()
        if studentlist!='':
            for item in studentlist:
                d=dict(eval(item))
                print(d)
        else:
            print('file context is null')
    else:
        print('file not found!')
    fr.close()

def savefile(allstudents):
    try:
        fw=open(filename,'w',encoding='utf-8')
    except FileNotFoundError as fnot:
        fw = open(filename, 'w', encoding='utf-8')
    for item in allstudents:
        fw.write(str(item)+'\n')
    fw.close()

def main():
    flag=True
    while flag:
        menu()
        choise=int(input('please input 0~7 select the funtion!!'))
        if choise==0:
            answer=input('Are you sure  to exit system! ?y/n')
            if answer=='Y' or answer=='y':
                flag=False
                print('Thank your use the system!')
                break
            else:
                continue
        elif choise==1:
            insert()
        elif choise==2:
            search()
        elif choise==3:
            modify()
        elif choise==4:
            sort()
        elif choise==5:
            modify()
        elif choise==6:
            total()
        elif choise==7:
            showall()
        if flag==False:
            break

if __name__=='__main__':
    filename= 'allstudents.txt'
    main()



