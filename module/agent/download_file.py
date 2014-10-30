#!-*-coding:utf8-*-
# @author:jackson
# @summary:agent download file from remote host
import os
import subprocess
import hashlib
import base64

from comm.log import log
from comm.config import Conf

conf = Conf(os.getcwd()+'/conf/agent.ini')
p_ip = conf.get("DOWNLOAD", "pkg.svr.ip", "")
p_dir = conf.get("DOWNLOAD", "pkg.svr.dir", "/data/package")
p_user = conf.get("DOWNLOAD", "pkg.svr.user", "root")
p_password = conf.get("DOWNLOAD","pkg.svr.password","")



class DownLoadFile(object):
    
    def __init__(self):
        self._local_dir = "/tmp"
    
    def download_from_remote(self,pkg_path="",pkg_name="",md5_info=""):
        """"""
        #step-0:before download,check file is exist or not
        check_result = self.check_download(pkg_name, md5_info)
        if check_result:
            log("file or package already exist")
            return True
        log("No file")
        #step-1:start download
        user_info = p_user+" "+p_ip+" "+p_password+" "+p_dir+"/"+pkg_path+"/"+pkg_name +" "+self._local_dir+"/"+pkg_name
        cmd_str = os.getcwd()+'/transfor_tools/download.exp '+user_info
        log(cmd_str)
        exe_info = self.execute_cmd(cmd_str)
        log(exe_info[0])
        log(exe_info[1])
        #step-2:start check
        result = self.check_download(pkg_name, md5_info)
        return result
    
    def check_download(self,pkg_name,md5_info):
        #step-1:ls
        ls_cmd = "ls -a "+self._local_dir+"/"+pkg_name
        log(ls_cmd)
        info = self.execute_cmd(ls_cmd)
        if info[0]:
            if info[0].find("No such file or directory") !=-1:
                #find ,download failure
                return False
        else:
            log(info[1])
            return False
        #step-2:check md5 info
        result = self.__check_md5_info(pkg_name, md5_info)
        
        return result
        #return True
    
    def __check_md5_info(self,pkg_name,md5_info):
        """"""
        md5_cmd = "md5sum "+self._local_dir+"/"+pkg_name
        info = self.execute_cmd(md5_cmd)
        if info[0]:
            tmp = info[0].split()
            #start compare,if equal,return True
            if tmp[0] == md5_info:
                log("md5sum info success")
                return True
        else:
            log(info[1])
        return False
    
    def download_from_ftp(self):
        
        return
    
    def execute_cmd(self,cmd_str):
        try:
            
            obj = subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            info = obj.communicate()
        except Exception,e:
            log(str(e))
            info = ("","")
            
        return info