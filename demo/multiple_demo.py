#!-*-encoding:utf8-*-

import time
import threading
import random

class Productor(threading.Thread):
    def __init__(self,name,queue,condition):
        threading.Thread.__init__(self,name=name)
        self._queue = queue
        self._condition = condition
        self._stopevent = threading.Event()

    def run(self):
        while not self._stopevent.isSet():
            self._condition.acquire()
            print self._queue

            self._condition.notifyAll()
            self._condition.release()
            time.sleep(10)
        
    def stop(self):
        self._stopevent.set()

class Consumer(threading.Thread):
    def __init__(self,name,queue,condition):
        threading.Thread.__init__(self,name=name)
        self._queue = queue
        self._condition = condition
        self._stopevent = threading.Event()

    def run(self):
        while not self._stopevent.isSet():
            self._condition.acquire()
            print self._queue

            self._condition.notifyAll()
            self._condition.release()
            time.sleep(10)
        
    def stop(self):
        self._stopevent.set()

