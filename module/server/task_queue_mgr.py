#!-*-coding:utf8-*-
import threading
import time
import traceback
import random
from comm.log import log
from module.agent.callback_task_info import CallbackTaskInfo
from module.agent.process_agent_task import ProcessAgentTask

from Queue import Queue

class TaskProcessThreadPool():
    #main run process
    def __init__(self):
        self.queue = Queue()
        self._cond = threading.Condition()
        
    def run(self):
        
        return


class AgentConsumer(threading.Thread):
    """"""
    def __init__(self,index,queue,condition):
    #def __init__(self,index,queue,condition,class_obj):
        """"""
        threading.Thread.__init__(self,name=str(index))
        self._cond = condition
        self._queue = queue
        #self._class_obj = class_obj
        self._stopevent = threading.Event()
        self._callback_obj = CallbackTaskInfo()
        
    def run(self):
        
        while not self._stopevent.is_set():
            self._cond.acquire()
            while self._queue.empty():
                self._cond.wait()
            fetch_data = self._queue.get()
            #process data
            #update task status
            self._cond.release()
            #obj = self._class_obj()
            obj = ProcessAgentTask()
            ret_result = obj.run(fetch_data)
            #add callback result
            log(str(ret_result))
            #self._callback_obj.run(ret_result)
            #time.sleep
            sleep_interval = random.randint(0,10)
            time.sleep(sleep_interval)
    
    def stop(self):
        self._stopevent.set()
        
class AgentProducter(threading.Thread):
    """"""
    def __init__(self,name,queue,condition):
        threading.Thread.__init__(self,name=name)
        self._queue = queue
        self._cond = condition
        self._stopevent = threading.Event()
    
    def run(self):
        while not self._stopevent.is_set():
            self._cond.acquire()
            #if need,clear data
            #add unprocess data into queue
            #
            xx = random.randint(0,30)
            for i in xrange(xx):
                self._queue.put(i)
            
            self._cond.notifyAll()
            self._cond.release()
            
            sleep_interval = random.randint(0,20)
            time.sleep(sleep_interval)
    
    def stop(self):
        self._stopevent.set()

class AgentFactory():
    def __init__(self,name,queue,condition,num):
        self._name = name
        self._cond = condition
        self._queue = queue
        self._num = num
        
        self._productor = AgentProducter(self._name,self._queue,self._cond)
        self._consumer_list=[]
        for i in xrange(self._num):
            self._consumer_list.append(AgentConsumer(i,self._queue,self._cond))
            
    def start(self):
        #
        self._productor.setDaemon(True)
        self._productor.start()
        for consumer in self._consumer_list:
            consumer.setDaemon(True)
            consumer.start()
    
    def stop(self):
        #
        self._productor.stop()
        for consumer in self._consumer_list:
            consumer.stop()