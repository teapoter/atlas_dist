#!-*-coding:utf8-*-
# @author:jackson
# @time:2014-10-17 16:00:00
# @summary:

import random
import os
import time
from comm.log import log
from comm.config import Conf

from comm.run_cmd import exec_cmd
from comm.run_cmd import get_local_ip
from comm.time_summary import stamp2time
try:
    import simplejson as json
except:
    import json
    
import traceback

from module.sql import Sql
    
conf = Conf(os.getcwd()+'/conf/server.ini')
local_dir = conf.get("UPLOAD", "svr.local.dir", "/data/package")

#get config connect db info,as global variable
db_ip=conf.get("DBServer","db.svr.ip","")
db_port=conf.get_int("DBServer","db.svr.port",3306)
db_user=conf.get("DBServer","db.svr.user","root")
db_pwd=conf.get("DBServer","db.svr.pwd","root")
db_name=conf.get("DBServer","db.name","")

class PkgInfoMgr(object):
    
    def __init__(self,router_obj):
        self._router_obj = router_obj
        #pass
        
    def run(self):
        while 1:
            #step-0:sleep info
            interval_sec = random.randint(60,120)
            time.sleep(interval_sec)
            #step-1:
            pkg_list = self.loop_pkg_dir()
            log(str(pkg_list))
            md5_info_list = self.calc_md5_info(pkg_list)
            
            fsvr_info = self.fsvr_ip()
            log("*&"*30)
            log(str(md5_info_list))
            self.write_info_into_db(fsvr_info,fsvr_info, md5_info_list)
            log("info success...")
            #return
    
    def loop_pkg_dir(self):
        #result format:{"dirPath":"/data/package/agent","fileList":[]}
        final_list =[]
        for root,dirs,files in os.walk(local_dir):
            tmp_info={"dirPath":root,"fileList":[]}
            if files:
                #add filter *.tar.gz/*.tgz/*.tar
                for item in files:
                    if ".tar" in item  or ".tgz" in item:
                        tmp_info["fileList"].append(item)
                if tmp_info["fileList"]:
                    final_list.append(tmp_info)
        
        return final_list
    
    def fsvr_ip(self):
        #get local ip info
        return get_local_ip()
    
    def calc_md5_info(self,file_info=[]):
        #calculate
        md5_info=[]
        for index,item in enumerate(file_info):
            for file_item in item["fileList"]:
                result_info= exec_cmd('md5sum '+item["dirPath"]+'/'+file_item)
                if result_info:
                    info = result_info[0].split()
                    md5_info.append({"storePath":item["dirPath"],"fileName":file_item,"md5Info":info[0]})
        
        return md5_info
    
    def write_info_into_db(self,ip_info="",file_svr="",info_list=[]):
        """"""
        try:
            if not db_ip or not db_user or not db_pwd or not db_name:
                log("DB Config info miss[host:%s,user:%s,pwd:%s,dbname:%s]"%(db_ip,db_user,db_pwd,db_name))
                return False
            
            tamp_2_time = stamp2time(time.time())
            sql = Sql(host=db_ip,port = db_port,user=db_user,passwd=db_pwd,dbname=db_name)
            for index,item in enumerate(info_list):
                sql_str = "replace into package_info(`fileServer`,`storePath`,`fileName`,`md5Info`,`updateTime`,`flag`)\
                 values ('%s','%s','%s','%s','%s','%s')"%(file_svr,item.get("storePath",""),item.get("fileName",""),
                                                    item.get("md5Info",""),tamp_2_time,0)
                log(sql_str)
                sql.execute(sql_str)
            sql.close()

        except Exception,e:
            log(str(e))
            return False
        return True
    