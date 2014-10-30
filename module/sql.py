#!-*-coding:utf8-*-
import os
import sys
import MySQLdb

class Sql(object):
    def __init__(self,host="",port=3306,user="root",passwd="",dbname=""):
        self._host=host
        self._port=port
        self._user=user
        self._passwd=passwd
        self._cursor=None
        self._conn=None
        self._dbname=dbname
        self._result=self._check_conn()

    def _connection(self):
        try:
            self._conn = MySQLdb.connect(host=self._host,port=self._port,user=self._user,passwd=self._passwd,db=self._dbname,charset='utf8',connect_timeout=10)
            self._cursor=self._conn.cursor()
        except MySQLdb.Error,e:
            print "MySql Error %d:%s"%(e.args[0],e.args[1])
        except Exception,e:
            print "Exception:%s"%(str(e))
        return self._conn

    def _check_conn(self):
        '''function:check connection is alive or not'''
        try:
            if self._conn is None:
                self._conn=self._connection()
            return True    
        except Exception,e:
            print "[Check Conn]Exception:%s"%str(e)
            return False           
     
    def close(self):
        if self._cursor is not None:   
            self._cursor.close()
            self._cursor=None
        if self._conn is not None:
            self._conn.close()
            self._conn=None

    def select(self,sql):
        return self.execute(sql)
    
    def update(self,sql):
        return self.execute(sql)

    def delete(self,sql):
        return self.execute(sql)
    
    def execute(self,sql):
        '''function:execute sql return result'''
        self._cursor.execute(sql)
        ret_info=self._cursor.fetchall()
        self._conn.commit()
        return ret_info

class Helper(object):
    '''function:'''
    def __init__(self):
        self._group=[]
        self._order=[]
        self._select=[]
        self._where=[]
        self._limit=[]
        self._from=[]
    
    def select(self):

        return


if __name__ =='__main__':

    sql=Sql('172.25.50.13',3306,'root','matrix','oss')
    sql_command="select u_id,u_login_name from t_users;"
    result=sql.select(sql_command)
    print result
    for item in result:
        print "ID:",item[0]
        print "Name:",item[1]
    sql.close()
