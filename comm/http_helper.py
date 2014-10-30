# -*- coding: utf-8 -*-

try:
    import simplejson as json
except:
    import json
import traceback
import httplib
#import urllib
#import urllib2
from comm.output import *
from comm.config import Conf
from comm.log import log
#from modules.dba.comm_db_opt import get_api_list

class HttpHelper():
    
    def __init__(self):
        pass
        #self._timeout = config.get_int("DEFAULT", "http.timeout",10)
        self._timeout = 30
        #self._dbread = dbread 
    
    def call_callback_api (self ,host_and_port,url,params):
        #print "call external api:",host_and_port,url,params
        #output("###############################################")
        #output("external request is :%s\n"%str(params))
        ret_flag = True
        data = ""
        headers = {"Content-type": "application/x-www-form-urlencoded",
                     "Accept": "text/plain"}
        try:
            if isinstance(params,(str,unicode)):
                req_data = params
                
            elif isinstance(params,(dict,list,tuple)):
                req_data = json.dumps(params)

            conn = httplib.HTTPConnection(host_and_port,timeout= self._timeout)
            conn.request("POST",url,req_data, headers)
            response = conn.getresponse()
            #output("[external api]response:(%s,%s)"%(str(response.status),str(response.reason)))
            data = json.loads(response.read())
        except Exception,e:
            log(traceback.print_exc())
            ret_flag = False
            if hasattr(e,"reason"):
                data = e.reason
            elif hasattr(e,"message"):
                data = e.message
            else:
                data = "urlopen error: unknown reson."
        #output("\nresponse is :%s\n"%str(data))
        #output("###############################################")
        conn.close()
        return ret_flag,data

if __name__=='__main__':
    
    httphelper = HttpHelper()
    httphelper.call_cc_api("10.12.22.187","")