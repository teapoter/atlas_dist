#!-*-encoding:utf8-*-
# @author:jackson
# @summary:
#import random
#import os
import threading
#import time
import random

class ThreadHelper(threading.Thread):
    
    def __init__(self,obj,name=""):
        super(ThreadHelper,self).__init__(name=name if name else self.gen_random_name())
        self._obj = obj
        self._result = None
    def run(self):
        print "[Start Run as Thread]%s"%str(self._obj)
        self._result = self._obj.run()
        
    def get_result(self):
        return self._result
    
    def gen_random_name(self):
        """function:"""
        char_list =[chr(i) for i in xrange(97,123)]
        file_str =""
        for i in xrange(0,5):
            tmp =random.randint(0,23)
            file_str = file_str+char_list[tmp]
        return file_str