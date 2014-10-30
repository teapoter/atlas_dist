#!-*-coding:utf8-*-
import os
import sys
import threading
from Queue import Queue
import time
import random
import traceback
from comm.log import log

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
    
    def run(self):
        while not self._stopEvent.isSet():
            self._cond.acquire()
            while not self._queue.empty():
                self._cond.wait()
            #self._queue.queue.clear()
            #TODO:add item into queue
            for i in xrange(10):
                log("loop times:%d"%i)
                self._queue.put(random.randint(100,200))
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
            log(self.getName())
            log(fetch_data)
            self._cond.notifyAll()
            self._cond.release()
            time.sleep(3)
    
    def stop(self):
        self._stopEvent.set()
        