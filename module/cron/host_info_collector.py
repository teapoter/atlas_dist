#!-*-encoding:utf8-*-
import random
import os
import time
from comm.log import log
from module.report_info import ReportInfo
from comm.run_cmd import exec_cmd
try:
    import simplejson as json
except:
    import json


class BasicInfo(object):
    
    def __init__(self):
        pass
    
    def run(self):
        
        return

    def get_hostname(self):
        """"""
        try:
            hostname_ver_list =os.popen('hostname').read()
            
            if isinstance(hostname_ver_list,(list,)) and hostname_ver_list:
                hostname_ver_str = hostname_ver_list[0].strip('\n')
            else:
                hostname_ver_str = hostname_ver_list.strip('\n')
        except Exception,e:
            hostname_ver_str ="unkown"
            log(str(e))
        return hostname_ver_str
    
    def get_kernel_ver(self):
        """"""
        try:
            kernel_ver_list =os.popen('uname -r').read()
            
            if isinstance(kernel_ver_list,(list,)) and kernel_ver_list:
                ker_ver_str = kernel_ver_list[0].strip('\n')
            else:
                ker_ver_str = kernel_ver_list.strip('\n')
        except Exception,e:
            ker_ver_str ="unkown"
            log(str(e))
        return ker_ver_str
    
    def get_libvirt_ver(self):
        """"""
        try:
            lib_ver_list = os.popen('rpm -qa|grep libvirt').read()
            #log(type(lib_ver_list))
            if isinstance(lib_ver_list,(list,)) and lib_ver_list:
                lib_ver_str = lib_ver_list[0].strip('\n')
            else:
                lib_ver_str = lib_ver_list.strip('\n')
        except Exception,e:
            lib_ver_str ="unkown"
            log(str(e))
        return  lib_ver_str
    
    def get_qemu_ver(self):
        """"""
        try:
            qemu_ver_list = os.popen('rpm -qa|grep qemu').read()
            #log(type(lib_ver_list))
            if isinstance(qemu_ver_list,(list,)) and qemu_ver_list:
                qemu_ver_str = qemu_ver_list[0].strip('\n')
            else:
                qemu_ver_str = qemu_ver_list.strip('\n')
        except Exception,e:
            qemu_ver_str ="unkown"
            log(str(e))
        return  qemu_ver_str
    
    def get_disk_usage(self):
        """"""
        ret_list=[]
        disk_usage_list = exec_cmd("/bin/df -PTh")
        for index,item in enumerate(disk_usage_list):
            if item.startswith("Filesystem"):
                #filter start header
                continue
            try:
                (device,fstype,total,used,available,percentage,mount)=item.split(None)
                ret_list.append({
                             "device":device,
                             "fstyp":fstype,
                             "total":total,
                             "used":used,
                             "available":available,
                             "percentage":percentage,
                             "mount":mount
                             })
            except Exception,e:
                log(str(e))
        return ret_list
    
    def get_hardware_info(self):
        """"""
        
        return
    
class HostBasicInfo(BasicInfo):
    
    def __init__(self,router_obj):
        super(HostBasicInfo,self).__init__()
        self._router_obj = router_obj
        self._info ={}
        
    def run(self):
        
        while 1:
            try:
                interval_sec = random.randint(30,60)
                time.sleep(interval_sec)
                log("[HostBasicInfo]report interval [%s] "%str(interval_sec))
                self._compose()
                ReportInfo().run(self._info)
            except Exception,e:
                log(str(e))
            #log("dddddd")
        #return self.get_result()
    
    def _compose(self):
        
        self._info["libvirt"]=self.get_libvirt_ver()
        self._info["qemu"] = self.get_qemu_ver()
        self._info["kernel"] = self.get_kernel_ver()
        self._info["hostname"] = self.get_hostname()
        self._info["diskUsage"]=self.get_disk_usage()
        log(json.dumps(self._info))
        
    def get_result(self):
        return self._info
    

#class ReportHostInfo():
#    """"""
#    def __init__(self):
#        self._host_obj = HostBasicInfo()
#        self._report_obj = ReportInfo()
#        
#    def run(self):
#        try:
#            time.sleep(10)
#            log("repprttt ")
#            host_info =self.host_obj.run()
#            self._report_obj.run(host_info)
#        except Exception,e:
#            log(str(e))
#        return
