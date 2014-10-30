#encoding=utf-8
'''
@author:Jackson 
基于BaseHTTPServer的http server实现，包括get，post方法，get参数接收，post参数接收。
'''
from SocketServer import ThreadingMixIn

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import UDPServer,BaseRequestHandler

import io,shutil  
import urllib,time
import getopt,string
try:
    import simplejson as json
except:
    import json
#import random

from comm.setting import *

from comm.log import log
from comm.ret_data import ReturnData
from server.rpc_service import RPC_DICT

#from module.cron.host_info_collector import ReportHostInfo
from module.cron.host_info_collector import HostBasicInfo

from module.udp_svr.process_upd_report_info import process_udp_report_info

class DaemonTaskHandler(object):
    """function:"""
    def __init__(self):
        pass
    def run(self):
        #log("dddddd")
        HostBasicInfo().run()
        return


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.process(2)

    def do_POST(self):
        self.process(1)
        
    def process(self,type):
        
        content =""
        if type==1:#post方法，接收post参数
            datas = self.rfile.read(int(self.headers['content-length']))
            datas = urllib.unquote(datas).decode("utf-8", 'ignore')#指定编码方式
            #print datas
            try:
                req_content=json.loads(datas)
                print "requeset content:",req_content
                #resp=json.dumps(req_content)
                (result,resp_result)=self._dispather(req_content)
                #(result,resp_result)=self._dispather(resp)
                #log(resp)
            except Exception,e:
                log(str(e))
                print str(e)
                resp="Error"
            content =resp_result 
            #process request
            #指定返回编码
            enc="UTF-8" 
            #content="Ok"
            content = content.encode(enc)          
            f = io.BytesIO()  
            f.write(content)  
            f.seek(0)  
            self.send_response(200)  
            self.send_header("Content-type", "text/html; charset=%s" % enc)  
            self.send_header("Content-Length", str(len(content)))  
            self.end_headers()  
            shutil.copyfileobj(f,self.wfile)
            
    def _dispather(self,content):
        print "enter path:",self.path
        print "ip:",self.client_address
        #parse path info
        path_list=[]
        for item in self.path.split('/'):
            if item:
                path_list.append(item)
        #
        if len(path_list) !=3:
            result = False
            msg = u"[Process]Miss Path Info,error path format"
        else:
            result = True
            msg = self._run_obj(path_list, content)
        
        return (result,msg)
    
    def _run_obj(self,path,content):
        ''''''
        app=path[0]
        log("path:%s"%str(path))
        log(get_projname())
        if app == get_projname():
            pass
        else:
            ret_data = ReturnData()
            ret_data.set_header(code=1000, msg="[Process]Get obj path info error")
            log(ret_data.get_data())
            return ret_data.get_data()
        
        if isinstance(path,list):
            
            try:
                classname=RPC_DICT[path[1]]
                class_obj=classname()
                method = path[2]
                obj = getattr(class_obj,method)
                #log(obj)
                return obj(content)
            except Exception,e:
                print str(e)
                ret_data = ReturnData()
                ret_data.set_header(code=1000, msg="[Process]Get obj info error")
                log(ret_data.get_data())
                return ret_data.get_data()
        else:
            ret_data = ReturnData()
            ret_data.set_header(code=1000, msg="[Process]Path info error")
            return ret_data.get_data()
         
class ThreadingHttpServer(ThreadingMixIn,HTTPServer):
    pass

##########################################################
class ThreadingUDPServer(ThreadingMixIn,UDPServer):
    pass

class UDPRequestHandler(BaseRequestHandler):
    """process udp report info"""
    def handle(self):
        """"""
        try:
            data = self.request[0].strip()
            ip = self.client_address[0].strip()
            port = self.client_address[1]
            #log("[recv info data]:%s"%str(data))
            log("[recv info address]:%s,%s"%(str(ip),str(port)))
            #TODO:process data
            #socket = self.request[1]
            #log("[recv info socket]:%s"%str(socket))
            process_udp_report_info(ip,json.loads(data))
            #process success
        except Exception,e:
            log(str(e))
        #return

def transDicts(params):
    dicts={}
    if len(params)==0:
        return
    params = params.split('&')
    for param in params:
        dicts[param.split('=')[0]]=param.split('=')[1]
    return dicts
       
if __name__=='__main__':
    
    try:
        #server = HTTPServer(('', 8000), MyRequestHandler)
        server = ThreadingHttpServer(('',8000),MyRequestHandler)
        print 'started httpserver...'
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
    
    pass
