#!-*-coding:utf8-*-

import sqlite3
import os

data_dir = os.getcwd()+"/data/"

class SqliteHelper():
    
    def __init__(self):
        self._conn = self.__connect()
        self._cursor = self._conn.cursor if self._conn is not None else None
        
    def __connect(self):
        """function:"""
        connection = None
        try:
            connection = sqlite3.connect(data_dir+'task')
        except:
            raise Exception("[Sqlite]Can not connection local sqlite db.")
        
        return connection 
    
    def execute(self):
        
        return

    def close(self):
        
        return