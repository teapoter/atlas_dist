#!-*-coding:utf8-*-

import os
#import subprocess

def exec_cmd(cmd):
    try:
        info = os.popen(cmd).readlines()
        ret_list =[item.strip() for item in info]
        return ret_list
    except:
        raise Exception("exec cmd error")
        return []
    
    
def get_local_ip():
    #get  inner ip info,not cbs ip
    try:
        cmd ="/sbin/ip route |grep src|grep -v eth0|awk '{print $NF}' "
        info_list = exec_cmd(cmd)
    except :
        raise Exception("[RunCmd]Get local ip info error")
    
    if info_list:
        return info_list[0]
    else:
        return ""