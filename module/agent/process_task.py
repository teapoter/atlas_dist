#!-*-coding:utf8-*-
import os
import sys

from comm.ret_data import ReturnData
#from module.agent.download_file import DownLoadFile

class MainAgentProcess():
    
    def __init__(self):
        self._ret_data = ReturnData()
    
    def run(self,content):
        #step-1:check params
        #DownLoadFile().download_from_remote(pkg_path="", pkg_name="manual.tar.gz", md5_info="956eb64566c79f483920fa3aa3b0a03c")
        #step-2:write info into db or file
        return self._ret_data
        