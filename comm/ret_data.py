#!-*-coding:utf8-*-
import time
import os

try:
    import simplejson as json
except:
    import json
"""
struct:
{
"header":{
    "version":"",
    "time":"",
    "ip":""
    "code":0,
    "msg":""
    },
"body":{
    
    }
}
"""

class ReturnData(object):
    
    def __init__(self):
        self._result = {"header":{},"body":{}}
        self.set_header()
    
    def set_header(self,code=0,msg="",version="1.0"):
        self._result["header"]["code"]=code
        self._result["header"]["msg"]=msg
        self._result["header"]["version"]=version
    
    def add_result(self,key,value):
        self._result["body"][str(key).encode('UTF-8')]=value
    
    def get_data(self):
        return json.dumps(self._result)
    
    def get_object(self):
        return self._result
