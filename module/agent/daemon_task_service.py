#!-*-coding:utf8-*-
import os
import sys
import threading
from Queue import Queue
import time
import random
import traceback
from comm.log import log

from module.agent.task_process import TaskProcess
from module.agent.task_process import TaskContentParse
#from comm.ret_data import ReturnData
#from module.agent.download_file import DownLoadFile
CONSUMER_NUM=3
NAME = "Agent-Server"

class AgentTaskFactory(object):
    
    def __init__(self,route_obj):
        self._name = NAME
        self._queue = Queue()
        self._cond = threading.Condition()
        self._fetch_obj = AgentTaskFetch(self._name+"-fetch-data",self._queue,self._cond)
        self._process_obj=[]
        self._process_obj.append(self._fetch_obj)
        for x in xrange(CONSUMER_NUM):
            self._process_obj.append(AgentTaskProcess(self._name+"-process-thread-"+str(x),
                                                      self._queue,self._cond))

    def run(self):
        while 1:
            try:
                for item in self._process_obj:
                    if item.is_alive():
                        continue
                    else:
                        log("thread restart:%s"%str(item.getName()))
                        item.setDaemon(True)
                        item.start()
                time.sleep(5)
                #self._fetch_obj.setDaemon(True)
                #self._fetch_obj.start()
            except:
                log("error occur,need stop")
                self.stop()
    
    def stop(self):
        #self._fetch_obj.stop()
        for item in self._process_obj:
            item.stop()

class AgentTaskFetch(threading.Thread):
    
    def __init__(self,name,queue,condition):
        #self._ret_data = ReturnData()
        threading.Thread.__init__(self,name=name)
        self._queue = queue
        self._cond = condition
        self._stopEvent = threading.Event()
        self._task_fetch = TaskProcess()
    
    def run(self):
        while not self._stopEvent.isSet():
            self._cond.acquire()
            while not self._queue.empty():
                self._cond.wait()
            ret_list = self._task_fetch.read_unprocess_task()
            for item in ret_list:
                self._queue.put(item)
            #self._queue.queue.clear()
            #TODO:add item into queue
            #for i in xrange(10):
            #    log("loop times:%d"%i)
            #    self._queue.put(random.randint(100,200))
            log("[AgentTaskFetch]queue info:%s"%str(self._queue))
            self._cond.notifyAll()
            self._cond.release()
            
            time.sleep(5)
        #step-1:check params
        #DownLoadFile().download_from_remote(pkg_path="", pkg_name="manual.tar.gz", md5_info="956eb64566c79f483920fa3aa3b0a03c")
        #step-2:write info into db or file
        
    def stop(self):
        self._stopEvent.set()

class AgentTaskProcess(threading.Thread):
    
    def __init__(self,name,queue,condition):
        threading.Thread.__init__(self,name = name)
        self._queue = queue
        self._cond = condition
        self._stopEvent = threading.Event()
        
        
    def run(self):
        while not self._stopEvent.isSet():
            self._cond.acquire()
            while self._queue.empty():
                self._cond.wait()
            fetch_data = self._queue.get()
            p_path = fetch_data.get("path","")
            p_file = fetch_data.get("file","")
            #for 
            prefix_file = p_file.split('.')[0]
            
            result = False
            process_obj = None
            if p_path  and p_file:
                #midify file name==>means task status
                tmp_file = prefix_file+".running"
                process_obj = TaskContentParse(p_path,p_file)
                process_obj.update_task_status(p_path, p_file, "running")
                #final execute obj
                process_obj = TaskContentParse(p_path,tmp_file)
                result = True
            #log(self.getName())
            #log(fetch_data)
            self._cond.notifyAll()
            self._cond.release()
            
            #start run 
            if result:
                (resp_result,resp_content) = process_obj.run()
                if resp_result:
                    process_obj.update_task_status_write_result(p_path, tmp_file, "success",resp_content)
                else:
                    process_obj.update_task_status_write_result(p_path, tmp_file, "failure",resp_content)
            
            time.sleep(3)
    
    def stop(self):
        self._stopEvent.set()
        