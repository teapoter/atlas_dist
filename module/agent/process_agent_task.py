#!-*-coding:utf8-*-
import os
import random
from comm.log import log
#from module.agent.callback_task_info import CallbackTaskInfo
from comm.ret_data import ReturnData
from comm.run_cmd import exec_cmd
from comm.config import Conf
from comm.gen_taskid import gen_taskid

try:
    import simplejson as json
except:
    import json

conf = Conf(os.getcwd()+"/conf/agent.ini")

__doc__ ="Contains Recieve api request:run()==>external api "

AGENT_API_METHOD=["script_run","cmd_run"]

class ProcessAgentTask():
    
    def __init__(self):
        self._ret_data =ReturnData()
    
    def run(self,data):
        
        log(str(data))
        return self.main_process(data)
        #return
    
    def inner_process_ret(self,data):
        """"""
        (result,header_info,body_info)=self.check_params(data)
        if isinstance(body_info["data"]["detail"],list):
            detail = body_info["data"]["detail"][0]
        elif isinstance(body_info["data"]["detail"],dict):
            detail = body_info["data"]["detail"]
        else:
            log("request content:param[detail] type need be list or dict")
            return "request content format error"
        (script_name,store_path)=self.convert_str_2_file(detail)
        
        result=exec_cmd("chmod +x "+store_path+script_name)
        log("\n".join(result))
        result = exec_cmd(store_path+script_name)
        str_result = "\n".join(result)
        log(str_result)
        return str_result
    
    def main_process(self,data):
        #step-1:
        (result,header_info,body_info)=self.check_params(data)
        if not result:
            self._ret_data.set_header(1, "params check error,please input correct formate")
            return self._ret_data
        w_dir = conf.get("TASK","agent.task.dir","/var/agent/task")
        
        try:
            result = True
            result =self._make_task_dir(w_dir)
            if not result:
                result = False
                msg = u"[ProcessTaskAPI]Create local store dir/va/agent/task failure"
            else:
                r_taskid = gen_taskid()
                w_content = json.dumps(data)
                with open(w_dir+"/"+r_taskid+".ready","w") as f:
                    f.write(w_content)
                msg = "ok"
        except Exception,e:
            log(str(e))
            result = False
            msg = str(e)
        #compose result
        if not result:
            self._ret_data.set_header(1,msg)
        else:
            self._ret_data.set_header(0, msg)
            self._ret_data.add_result("taskid",r_taskid)
        
        return self._ret_data
    
    
    
    def check_params(self,data):
        result =True
        #
        header_info = data.get("header",{})
        body_info = data.get("body",{})
        #check if need callback
        r_type = body_info.get("type","")
        if r_type.lower() == "callback":
            r_ip = header_info.get("ip","")
            r_port = header_info.get("port","")
            r_url = header_info.get("url","")
            if r_ip and r_port and r_url:
                pass
            else:
                result = False
        #check body content need contain info
        if not body_info.get("method",""):
            return False
        
        if body_info.get("method","") not in AGENT_API_METHOD:
            return False
        #check detail params info
        if body_info.get("data",""):
            pass
        else:
            return False
        if not isinstance(body_info["data"],dict):
            return False
        
        r_detail = body_info["data"].get("detail",[])
        if not  isinstance(r_detail,list):
            result = False
        if  not r_detail:
            result = False
        #
        
        return (result,header_info,body_info)
    
    def convert_str_2_file(self,content={}):
        """"""
        try:
            store_path = "/tmp/"
            script_name = content.get("scriptName","")
            script_info = content.get("scriptContent","")
            if not script_name:
                script_name = self._gen_random_filename()
            if not script_name.endswith(".sh"):
                script_name = script_name+".sh"
            
            with open(store_path+script_name,"w") as f:
                f.write(script_info)
            
        except Exception,e:
            log(str(e))
        return script_name,store_path
    
    def _gen_random_filename(self):
        """"""
        str_filename="temp_"
        chr_list =[chr(i) for i in xrange(97,123)]
        for i in xrange(0,3):
            value = random.randint(0,26)
            str_filename =str_filename+chr_list[value]
        str_filename = str_filename+".sh"
        return str_filename
    
    def _make_task_dir(self,dir):
        """function:"""
        if os.path.exists(dir):
            log("[ProcessAgentTask] /var/agent/task dir exist.continue...")
            
        else:
            shell_cmd = "mkdir -p %s"%dir
            ret_info = exec_cmd(shell_cmd)
            if ret_info:
                str_info = "\n".join(ret_info)
                log(str_info)
            if os.path.exists(dir):
                pass
            else:
                #error occur
                log("[ProcessAgentTask]mkdir /var/agent/task/ error")
                return False
        return True
    