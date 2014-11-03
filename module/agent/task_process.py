#!-*-coding:utf8-*-
try:
    import simplejson as json
except:
    import json
     
import traceback
import os
from comm.log import log
from comm.config import Conf
from comm.run_cmd import exec_cmd

from comm.print_traceback_info import print_exc_info
from module.agent.process_agent_task import ProcessAgentTask

conf = Conf(os.getcwd()+"/conf/agent.ini")

"""
name rule:taskid.postfix 
(ex:201405147894.ready|201405147894.running|201405147894.succ|201405147894.fail)

"""

class TaskProcess():
    """function:"""
    def __init__(self):
        self._dir = conf.get("TASK", "agent.task.dir", "/var/agent/task")
        
    
    def run(self):
        
        return
    
    def _make_task_dir(self):
        """function:"""
        if os.path.exists(self._dir):
            #log("[TaskProcess] /var/agent/task dir exist.continue...")
            pass
        else:
            shell_cmd = "mkdir -p %s"%self._dir
            ret_info = exec_cmd(shell_cmd)
            if ret_info:
                str_info = "\n".join(ret_info)
                log(str_info)
            if os.path.exists(self._dir):
                pass
            else:
                #error occur
                log("[TaskProcess]mkdir /var/agent/task/ error")
                return False
        return True
    
    def read_unprocess_task(self):
        """function:"""
        try:
            if not self._make_task_dir():
                log("[TaskProcess]Create task dir /var/agent/task failure,or dir can not read/write")
                return []
            ret_list=[]
            ret_list =self.loop_pkg_dir(postfix=".ready")
        except Exception,e:
            log(traceback.print_exc())
            log(str(e))
            print_exc_info()
        return ret_list
    
    
    def loop_pkg_dir(self,postfix=""):
        #result format:{"dirPath":"/data/package/agent","fileList":[]}
        final_list =[]
        tmp_info_list=[]
        try:
            for root,dirs,files in os.walk(self._dir):
                tmp_info={"path":root,"file":[]}
                if files:
                    #add filter *.tar.gz/*.tgz/*.tar
                    for item in files:
                        if postfix in item:
                            tmp_info["file"].append(item)
                    if tmp_info["file"]:
                        final_list.append(tmp_info)
            #
            i = 0
            for index_1,item_1 in enumerate(final_list):
                for item in item_1["file"]:
                    tmp_info_list.append({"file":item,"path":item_1["path"],"index":i})
                    i =i+1
        except Exception,e:
            log(str(e))
            print_exc_info()
        return tmp_info_list
        #return final_list
        
class TaskContentParse():
    """function:parse task content detail ,get need info,execute script,
    return result,callback task result"""
    def __init__(self,path,filename):
        self._path = path
        self._filename =filename
        self._process_task_obj = ProcessAgentTask()
        
    def run(self):
        #step-1:read task file content
        content = self.read_file()
        if content:
            result = True
            info = self._process_task_obj.inner_process_ret(content)
        else:
            result = False
            info = u"[TaskContentParse]read content is null or content parse error."
        #step-2:execute content
        
        return (result,info)
    
    def __rename_file(self,str_cmd=""):
        """"""
        try:
            if str_cmd:
                ret_info =exec_cmd(str_cmd)
                if ret_info:
                    str_info = "\n".join(ret_info)
                else:
                    str_info="command already execute,but not return info."
            else:
                str_info="command content is null,please check"
        except Exception,e:
            log(str(e))
        return str_info
    
    def update_task_status(self,path="/var",file_name="",postfix=""):
        """function:"""
        try:
            #TODO
            str_cmd = ""
            name_split_list = file_name.split(".")
            if len(name_split_list) == 2:
                str_cmd = "mv %s/%s %s/%s.%s"%(path,file_name,path,name_split_list[0],postfix)
            else:
                str_cmd = "mv %s/%s %s/%s.%s"%(path,file_name,path,file_name,postfix)
            
            ret_info = self.__rename_file(str_cmd)
        except Exception,e:
            log(str(e))
        return ret_info
    
    
    def update_task_status_write_result(self,path="/var/agent/task",file_name="",postfix="",log=""):
        """function:"""
        try:
            #TODO
            #write log info
            with open(path+"/"+file_name,"a") as f:
                f.write("\n\nExecute Result:\n")
                f.write(log)
            
            #rename file 
            str_cmd = ""
            name_split_list = file_name.split(".")
            if len(name_split_list) == 2:
                str_cmd = "mv %s/%s %s/%s.%s"%(path,file_name,path,name_split_list[0],postfix)
            else:
                str_cmd = "mv %s/%s %s/%s.%s"%(path,file_name,path,file_name,postfix)
            
            ret_info = self.__rename_file(str_cmd)
        except Exception,e:
            log(str(e))
        return ret_info
    
    
    def read_file(self):
        """"""
        try:
            content = {}
            info = []
            
            with open(self._path+"/"+self._filename,"r") as f:
                info = f.readlines()
            if info:
                tmp_str = "\n".join(info)
                try:
                    content = json.loads(tmp_str)
                except Exception,e:
                    print_exc_info()
                    log(str(e))
            
        except Exception,e:
            log(str(e))
        
        return content
    