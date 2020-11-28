import pymysql

mysqldb = pymysql.connect('localhost', 'test', 'test')
cursor = mysqldb.cursor()
deldb = 'drop database python'
createdb = 'create database python'
try:
    cursor.execute(deldb)
    cursor.execute(createdb)
    cursor.execute('use python')
except:
    print('invoke failed')

createtable = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""
cursor.execute(createtable)
insertsql = '''INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)'''
try:
    cursor.execute(insertsql)
    mysqldb.commit()
    print('insert sucess!')
except:
    mysqldb.rollback()
    print("insert fail")

selectsql = '''SELECT * FROM EMPLOYEE \
       WHERE FIRST_NAME ='Mac' '''
try:
    cursor.execute(selectsql)
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        print("select sucess!")
        print("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
              (fname, lname, age, sex, income))

except:
    print("Error: unable to fetch data")

delsql = '''delete from EMPLOYEE where FIRST_NAME='Mac' '''
try:
    cursor.execute(delsql)
    mysqldb.commit()
    print('delete sucess')
except:
    mysqldb.rollback()
# cursor.execute('show databases')
mysqldb.close()