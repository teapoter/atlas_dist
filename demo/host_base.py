#!-*-encoding:utf8-*-

import os

class HostBase(object):
    def __init__(self):
        pass
    def run(self):
        #self._get_meminfo()
        self._get_meminfo_2()
        #self._get_cpuinfo()
    def _get_meminfo(self):
        result = {}
        with open('/proc/meminfo','r') as f:
            tmp = f.readlines()
            for index,item in enumerate(tmp):
                tmp_list=item.split(":")
                if len(tmp_list)>=2:
                    if tmp_list[0].lower() in ("memtotal","memfree"):
                        result[tmp_list[0].lower()]=float(tmp_list[1].strip().split(' ')[0])
            #print tmp
        print result
        return result
    def _get_meminfo_2(self):
        result = {}
        tmp = os.popen('cat /proc/meminfo|grep "Mem"|awk -F: \'{print $1 $2}\'')
        tmp_read = tmp.read()
        print tmp_read
        print type(tmp_read)
        tmp_list = tmp_read.split('\n')
        for index,item in enumerate(tmp_list):
            tmp_filter =[]
            tmp_filter=[i for i in  item.split(' ') if i]
            if tmp_filter:
                result[tmp_filter[0].lower()]=int(tmp_filter[1])
            print tmp_filter
        print result
        return {"host_meminfo":result}    
if __name__ =='__main__':
    hostbase = HostBase()
    hostbase.run()
