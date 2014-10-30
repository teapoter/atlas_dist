#!-*-coding:utf8-*-
from comm.ret_data import ReturnData
from comm.log import log
from comm.setting import *
import random


#from api.agent.agent_api import AgentAPI
from module.agent.process_agent_task import ProcessAgentTask
from module.server.process_server_task import ProcessServerTask

class API(object):
    
    def __init__(self):
        self._ret_data = ReturnData()
    
    #@staticmethod
    def run(self,content):
        try:
            log(type(content))
            #for i in range(random.randint(0,100)):
            #    log(i)
            #    self._ret_data.add_result(str("key_"+str(i)), i)
            #TODO:process command execute
            ret_obj = AgentAPI().run(content)
            return ret_obj.get_data()
        except Exception,e:
            print str(e)
            log(str(e))
            self._ret_data.add_result("msg","error")
        return self._ret_data.get_data()
        
        
        def callback(self,content):
            #process callback 
            try:
                log(type(content))
                #for i in range(random.randint(0,100)):
                #    log(i)
                #    self._ret_data.add_result(str("key_"+str(i)), i)
                #TODO:process command execute
                
                #return ret_obj.get_data()
            except Exception,e:
                print str(e)
                log(str(e))
                self._ret_data.add_result("msg","error")
            return self._ret_data.get_data()
            
class AgentAPI():
    """function:main process agent http request content"""
    def __init__(self):
        #self._ret_data = ReturnData()
        pass
    
    def run(self,content):
        #check params
        
        #write info into local sqlite
        obj = ProcessAgentTask()
        
        #return task info 
        return obj.run(content)
        #
        #return self._ret_data
class ServerAPI():
    """function:"""
    def __init__(self):
        #self._ret_data =ReturnData()
        pass
    def run(self,content):
        obj = ProcessServerTask()
        return obj.run(content)
        #return self._ret_data