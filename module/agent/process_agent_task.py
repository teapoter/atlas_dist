#!-*-coding:utf8-*-
import random
from comm.log import log
#from module.agent.callback_task_info import CallbackTaskInfo
from comm.ret_data import ReturnData
from comm.run_cmd import exec_cmd

class ProcessAgentTask():
    
    def __init__(self):
        self._ret_data =ReturnData()
    
    def run(self,data):
        
        log(str(data))
        return self.main_process(data)
        #return
    
    def main_process(self,data):
        #step-1:
        (result,header_info,body_info)=self.check_params(data)
        detail = body_info["data"]["detail"][0]
        (script_name,store_path)=self.convert_str_2_file(detail)
        
        result=exec_cmd("chmod +x "+store_path+script_name)
        log("\n".join(result))
        result = exec_cmd(store_path+script_name)
        str_result = "\n".join(result)
        log(str_result)
        
        self._ret_data.set_header(0, "success")
        self._ret_data.add_result("result",str_result)
        
        return self._ret_data
    
    def check_params(self,data):
        result =True
        #
        header_info = data.get("header",{})
        body_info = data.get("body",{})
        
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
    
    def write_local_info(self):
        #
        
        return