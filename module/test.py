#!-*-encoding:utf8-*-
import threading
import sys
import os

class CBasicThread(threading.Thread):
    def __init__(self, name, t_id):
        threading.Thread.__init__(self)
        self.name = name
        self.t_id = t_id
    def display(self):
        print 'hello world'
                                           
                                           
    def run(self):
        print 'xxxxxxxxxxxxxxxx'
        pass
                                                                    
                                                                    
class CThread(CBasicThread):
      def __init__(self, name, t_id, num):
          super(CThread, self).__init__(name, t_id)
          self.num = num
                                                                   
      def run(self):
          self.display()
                                                                                             
                                                                                                            
if __name__ == '__main__':
    CThread('xxxx', 123, 234).start()
    CBasicThread('xxxx', 123).start()
