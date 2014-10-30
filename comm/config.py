#!-*-coding:utf8-*-

import ConfigParser

class Conf:
    def __init__(self,conf_file):
        self._conf_file=conf_file
        self._oconf=ConfigParser.ConfigParser()
        self._oconf.read(self._conf_file)
    
    def get(self,section,key,default=""):
        try:
            return self._oconf.get(section,key)
        except Exception,e:
            print str(e)
            return default
        
    def gets(self):
        confs={}
        sections = self._oconf.sections()
        for k in range(len(sections)):
            confs[sections[k]]={}
            for sk,sv in self.oconf.items(sections[k]):
                confs[sections[k]][sk]=sv
        return confs
    
    def get_single(self,section=""):
        confs={}
        if section:
            for sk,sv in self._oconf.items(section):
                confs[sk]=sv
        return confs
    
    def get_int(self,section,key,default=0):
        try:
            return int(self._oconf.get(section,key))
        except Exception,e:
            print str(e)
            return default

