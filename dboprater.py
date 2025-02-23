import pandas as pd
import pymysql
from pymysqlpool import ConnectionPool
import json
from mainconfig import configfile
# configfile = './config/mysqlconfig.json'  #全局变量，不可改名

class DB(object):
    def __init__(self):
        self.pool = DB.create_conn_pool()
        self.conn = None
        self.cursor = None
    @staticmethod
    def get_config():
        with open(configfile, encoding="utf-8") as f:
            jsoncontent = json.load(f)
        f.close()
        return jsoncontent
    @staticmethod
    def dbconnect():
        jsoncontent = DB.get_config()
        conn = pymysql.connect(host=jsoncontent['host'], user=jsoncontent['user'], password=jsoncontent['password'],database=jsoncontent['database'], charset='utf8')
        # conn = pymysql.connect(jsoncontent['host'], jsoncontent['user'], jsoncontent['password'],jsoncontent['database'], charset='utf8')
        return conn
    @staticmethod
    def create_conn_pool():
        jsoncontent=DB.get_config()
        config = {
            'pool_name': 'pool1',
            'host': jsoncontent['host'],
            'port': 3306,
            'user':jsoncontent['user'],
            'password':jsoncontent['password'],
            'database': jsoncontent['database']
        }
        pool = ConnectionPool(**config)
        pool.connect()
        return pool
    @staticmethod
    def close_conn(conn, cursor):
        conn.close()
        cursor.close()

    @staticmethod
    def inserttodb(sql) ->bool:
        try:
            conn=DB.dbconnect()
            cursor=conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except BaseException as b:
            return False
    @staticmethod
    def selectFromdb(sql):
        resultpd=pd.DataFrame()
        try:
            conn = DB.dbconnect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            resultpd=pd.DataFrame(cursor.fetchall())
            if resultpd is None or len(resultpd)==0:
                return None
            cursor.close()
            conn.close()
            return resultpd
        except BaseException as b:
            return None

    @staticmethod
    def deleteFromdb(sql):
        try:
            conn = DB.dbconnect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            return True
        except BaseException as b:
            print('delete is Error',b)
            return False
if __name__ == '__main__':
    print(DB.get_config())
    print(DB.dbconnect())