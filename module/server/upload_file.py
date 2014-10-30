#!-*-encoding:utf8-*-
# @summary:upload file from local to remote host
# @author:jackson
import os
import traceback
from comm.config import Conf
from comm.log import log

conf = Conf(os.getcwd()+"/conf/server.ini")

local_dir = conf.get("UPLOAD","svr.local.dir", "/data/package/")
remote_dir = conf.get("UPLOAD","agent.remote.dir","/tmp/")
agent_user=conf.get("UPLOAD","agent.user","")
agent_pwd = conf.get("UPLOAD","agent.password","")

transfor_tool_dir = os.getcwd()+"/transfor_tools/"

def new_upload_file(ip,file_name):
    """"""
    try:
        os.chmod(transfor_tool_dir+"/*.exp",755)
        lines = os.popen(transfor_tool_dir+"upload.exp %s %s %s %s %s"%(agent_user,ip,agent_pwd,local_dir+file_name,remote_dir+file_name)).readlines()
        strLines = " ".join(lines)
        if strLines.find("rsync error") !=-1:
                log("[Upload file [%s] fail]"%str(file_name))
                return False
        if strLines.find("Password error") !=-1:
            log("[Upload file [%s] fail,password error]"%str(file_name))
            return False
        if strLines.find("Timeout") !=-1:
            log("[Upload file [%s] fail,Timeout]"%str(file_name))
            return False
        if strLines.find("No such file or directory") !=-1:
            log("[Upload file [%s] fail,No such file or directory]"%str(file_name))
            return False
        
    except Exception,e:
        log(str(e))
        log(str(traceback.print_exc()))
        return False
    
    return True
def local_check_upload_file_avilable(filename,md5sum_str=""):
    """check file md5 info"""
    try:
        lines = os.popen("md5sum %s"%str(filename)).readlines()
        if not lines:
            log("[Check Upload file failure]no such file or directory,upload failure")
            return False
        #check assistance
        info_str = lines[0]
        info_list = info_str.split(None)
        md5_info = info_list[0]
        if md5_info != md5sum_str:
            log("[Check Upload file]check md5sum info failure")
            return False
        return True
    except KeyError,e:
        log("[Check Upload file]return list is null")
        log(str(e))
        return False
    except Exception,e:
        log(str(e))
        log(str(traceback.print_exc()))
        return False

