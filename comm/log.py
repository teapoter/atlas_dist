#!-*-coding:utf8-*-
# @author:jackson
# @summary: logging info by days
import logging
import logging.handlers
import os
import sys
import time
#import inspect

from comm.setting import *

#def get_funcname():
#    return inspect.stack()

class CLog(object):
    
    INSTANCE = None
    ENCODE="utf-8"
    LEVEL_MAP = {
                 "DEBUG":logging.DEBUG,
                 "INFO":logging.INFO,
                 "WARNING":logging.WARNING,
                 "ERROR":logging.ERROR,
                 "CRITICAL":logging.CRITICAL
                 }
    @staticmethod
    def instance():
        if CLog.INSTANCE is None:
            CLog.INSTANCE = CLog()
        return CLog.INSTANCE
    
    def __init__(self):
        print "first init..."
        self._file=get_logfile()
        self._dir=get_logdir()
        #self._level=get_loglevel()
        self._level = self._transfor_level()
        self._proj=get_projname()
        self._handler = None
        self._logger = self.init()
    
    def _transfor_level(self):
        #print "transfor"
        self._level = get_loglevel()
        if self.LEVEL_MAP.has_key(self._level.upper()):
            self._level = self.LEVEL_MAP[self._level.upper()]
        else:
            self._level = self.LEVEL_MAP["DEBUG"]
        return self._level
    
    def init(self):
        '''function:'''
        #print self._dir
        #print self._file
        #print self._level
        formatter =logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        self._handler = logging.handlers.TimedRotatingFileHandler(self._dir+"/"+self._file+".log","D")
        #self._handler = logging.FileHandler(self._dir+"/"+self._file+".log")
        self._handler.setFormatter(formatter)
        
        logger = logging.getLogger(self._proj)
        logger.setLevel(self._level)
        logger.addHandler(self._handler)
        
        return logger
    
    def write(self,content):
        #print "sss:",content
        f =sys._getframe().f_back.f_back.f_back
        if f is None:
            f= sys._getframe().f_back.f_back
        extra_msg = '[%s:%s:%3d]'%(os.path.basename(f.f_code.co_filename),f.f_code.co_name,f.f_lineno)
        
        msg = str((extra_msg+str(content)).encode(self.ENCODE))
        self._logger.log(self._level, msg)
        self._handler.flush()
    
def log(msg):
    CLog.instance().write(msg)

