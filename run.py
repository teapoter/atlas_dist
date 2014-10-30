#-*-coding:utf8-*-
# @time:
"""Demo Server Entrance"""
import traceback
import random
import time
import os,sys

from multiprocessing  import Process
from multiprocessing import Queue
from threading import Thread

from comm.thread_helper import ThreadHelper

from comm.daemon import Daemon
from process import ThreadingHttpServer,MyRequestHandler
from process import ThreadingUDPServer,UDPRequestHandler
from comm.setting import get_svrport,get_type

from comm.log import log
#from process import DaemonTaskHandler
#from module.cron.host_info_collector import ReportHostInfo
from module.cron.host_info_collector import HostBasicInfo
from module.cron.pkg_info_coll import PkgInfoMgr
from module.agent.daemon_task_service import AgentTaskFactory


class UDPSvr(Daemon):
    """function:support udp api"""
    def run(self):
        try:
            #server = HTTPServer(('', 8000), MyRequestHandler)
            port = get_svrport()
            
            server = ThreadingUDPServer(('',port),UDPRequestHandler)
            print 'started httpserver...'
            server.serve_forever()

        except KeyboardInterrupt:
            server.socket.close()

class TaskTiming(Daemon):
    
    def run(self):
        try:
            #server = HTTPServer(('', 8000), MyRequestHandler)
            port = get_svrport()
            type = get_type()
            if type.lower() == "http":
                server = ThreadingHttpServer(('',port),MyRequestHandler)
            elif type.lower() == "udp":
                server = ThreadingUDPServer(('',port),UDPRequestHandler)
            else:
                #default
                server = ThreadingUDPServer(('',port),UDPRequestHandler)
            print 'started httpserver...'
            server.serve_forever()

        except KeyboardInterrupt:
            server.socket.close()

#def run_process(func, router_obj):
#    #process
#    instance = func(router_obj)
#    instance.run()

def start_run_process(cls,process_list,router_obj):
    
    if not isinstance(cls,list):
        cls = [cls]
        
    for c in cls:
        t = ThreadHelper(c(router_obj))
        process_list.append(t)
        t.setDaemon(True)
        t.start()
#    for c in cls:
#        p= Process(target = run_process,args = (c,router_obj),name = c.__name__)
#        process_list.append(p)
#        p.start()
    return process_list

def terminate_all(process_list=[]):
    for p in process_list:
        #p.terminate()
        p.join()
    sys.exit(222)

def main_run():
    #HostBasicInfo().run()
    thread_obj_list =[]
    
    obj = ThreadHelper(HostBasicInfo())
    #obj.setDaemon(True)
    #obj.start()
    thread_obj_list.append(obj)
    
    for item in thread_obj_list:
        item.setDaemon(True)
        item.start()
        
    while 1:
        result_list = [item.isAlive() for item in thread_obj_list]
        if True not in result_list:
            log("exist task not run over,con")
            break
        time.sleep(5)
    #DaemonTaskHandler().run()
    #ReportHostInfo().run()
def pkg_run():
    #collector pkg info and restore into db
    PkgInfoMgr().run()
    
class PkgInfoDemo(Daemon):
    #execute info collector daemon process
    def run(self):
        try:
            while 1:
                pkg_run()
        except KeyboardInterrupt:
            log("[Keyboard]PkgInfoDemo stop")
            pass

class TimingDemo(Daemon):
    """function:"""
    def run(self):
        try:
            router_obj = None
            process_list =[]
            start_run_process([PkgInfoMgr,HostBasicInfo,AgentTaskFactory],process_list,router_obj)
            while 1:
                #main_run()
                time.sleep(2)
                for p in process_list:
                    if not p.is_alive():
                        #log("process [%s]is dead,pid:%s,exit code:%s"%(p.name,p.pid,p.exitcode))
                        log("error............")
                        p.join()
                        process_list.remove(p)
                        if len(process_list)<4:
                            terminate_all(process_list)
                            break
                        else:
                            log("exist more pid info,need terminate.")
                            terminate_all(process_list)
                
                #log("sleep time:%d"%(time.sleep(random.randint(0,10))))
                #log("Random number:%d"%(random.randint(0,100)))
                
        except KeyboardInterrupt:
            log("[Keyboard]TimingDaemon stop")
            terminate_all(process_list)
            
        except Exception,e:
            log(str(e))
            log(traceback.print_exc())
            terminate_all(process_list)

if __name__=='__main__':
#
    if len(sys.argv)>2:
        print "Run Path:",os.getcwd()
    #test_daemon = TestDaemon(os.getcwd()+'/var/s.pid')
        if sys.argv[2] == "server":
            daemonS = TaskTiming(os.getcwd()+'/var/server.pid')
#            #daemonS = UDPSvr(os.getcwd()+'/var/udp_svr.pid')
#            #daemonS = TaskTiming(os.getcwd()+'/var/api.pid')
#        elif sys.argv[2] == "http_svr":
#            daemonS = TaskTiming(os.getcwd()+'/var/http_svr.pid')
        elif sys.argv[2] == "agent":
            daemonS =TimingDemo(os.getcwd()+'/var/agent.pid')
        elif sys.argv[2] == "pkgmgr":
            daemonS = PkgInfoDemo(os.getcwd()+'/var/pkgmgr.pid')
        
        else:
            print "unkown server"
            sys.exit(2)
        
        if 'start' == sys.argv[1]:
            daemonS.start()
        elif 'stop'== sys.argv[1]:
            daemonS.stop()
        elif 'restart' == sys.argv[1]:
            daemonS.restart()
        else:
            print "unkown command!"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usag:%s start|stop|restart"%(sys.argv[0])
        sys.exit(2)
