#!-*-encoding:utf8-*-
try:
    import simplejson as json
except:
    import json
#import urllib
import urllib2
import os
import datetime
import socket

from comm.log import log

from comm.config import Conf

def report_info(func):
    
    def decorate(*args,**kwargs):
        
        return
    
    return decorate


class ReportInfo():
    
    def __init__(self):
        self._conf = Conf(os.getcwd()+'/conf/agent.ini')
        self._get_conf() 
    def _get_conf(self):
        self._report_type = self._conf.get("REPORT","report.type","udp")
        self._host_ip = self._conf.get("REPORT","host.svr.ip","")
        self._host_port = self._conf.get("REPORT","host.svr.port","9999")
        self._host_url = self._conf.get("REPORT","host.svr.url","/demo/run/api")
    def run(self,info):
        """"""
        #log("44444444444")
        try:
            if self._report_type.lower() == "udp":
                self.udp_report(self.standard_format(info))
            elif self._report_type.lower() == "http":
                (code,result)=self.timout_report(self.standard_format(info))
            else:
                #default udp
                self.udp_report(self.standard_format(info))
            code = 0
            result = "success"
        except Exception,e:
            log(str(e))
            code = 1
            result = "[ReportInfo] run error"
        return (code,result)
    
    def standard_format(self,info):
        request_format={
                        "header":{
                                  "version":"V1.0",
                                  "time":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                  },
                        "body":{
                                "data":info
                                }
                        }
        return request_format
    
    def udp_report(self,info):
        """function:support upd report info"""
        try:
            s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,20)
            s.sendto(json.dumps(info),(self._host_ip,int(self._host_port)))
        except Exception,e:
            log("udp report error:%s"%str(e))
        return
    
    def timout_report(self,info):
        """function:support http timeout report info"""
        try:
            code = 0
            ret = ""
            url = "http://"+self._host_ip+":"+self._host_port+self._host_url
            log(str(url))
            f = urllib2.urlopen(url=url,
                                data = json.dumps(info),timeout=10)
        except Exception,e:
            if hasattr(e,"reason"):
                ret = e.reason
            else:
                ret = e.message
            code = 1
            
        else:
            ret = f.read()
        log(str(ret))
        if code ==1:
            return (code,ret)
    
        try:
            result = json.loads(ret)
        except Exception,e:
            log(str(e))
            log("")
            code = 1
            
        return (code,result)
