#!-*-coding:utf8-*-
import os
import time
from comm.log import log
from comm.run_cmd import get_local_ip
from comm.http_helper import HttpHelper

local_ip = get_local_ip()

class CallbackTaskInfo():
    """"""
    def __init__(self):
        self._http_obj = HttpHelper()
        pass
    
    def run(self,dict_info={}):
        #step-1:check info integrate or not
        c_method = dict_info.get("method","")
        c_taskid=dict_info.get("taskid","")
        c_detail = dict_info.get("detail",[])
        c_ip = dict_info.get("ip","")
        c_port = dict_info.get("port","")
        c_url = dict_info.get("url","")
        #
        if not c_method or not c_taskid or not c_detail:
            code = 1
            msg = u"[CallbackTaskInfo]error,miss params[method or taskid or detail] or params is null."
            return (False,code,msg)
        #step-2:
        self.callback_result(method = c_method,taskid=c_taskid,detail=c_detail,ip=c_ip,port=c_port,url=c_url)
        return
    
    def callback_result(self,**kwargs):
        #step-1:compose request
        callback_req = self._compose_req(**kwargs)
        loop_times =1
        while 1:
            (result,resp_info)=self._http_obj.call_callback_api(kwargs.get("host")+":"+str(kwargs.get("port")),
                                                            kwargs.get("url"),callback_req)
            if result:
                break
            loop_times=loop_times+1
            if loop_times >500:
                log("[CallbackTaskInfo]loop too many times,failure,exit")
                break
            time.sleep(5)
            log(str(resp_info))
        else:
            log("[CallbackTaskInfo]callback failure.")
        #no add judge result
        return True
    
    def _compose_req(self,**kwargs):
        """
        """
        req_info = {
                    "header":{
                              "version":"V1.0",
                              "type":"Json",
                              "time":kwargs.get("time",0),
                              "ip": kwargs.get("ip","") if kwargs.get("ip","") else local_ip
                              },
                    "body":{
                            "method":kwargs.get("method",""),
                            "type": kwargs.get("type","") if kwargs.get("type","") else "callback",
                            "detail":kwargs.get("detail",[]),
                            "taskid":kwargs.get("taskid","")
                            }
                    }
        return req_info