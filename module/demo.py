#!-*-coding:utf8-*-
import threading

class Test():
    def __init__(self):
        pass
    def run(self):
        print "test demo"


class Demo(threading.Thread):
    def __init__(self,data,class_obj):
        threading.Thread.__init__(self,name="demo")
        self._data = data
        self._obj = class_obj

    def run(self):
        obj = self._obj()
        obj.run()


if __name__ =='__main__':
    demo = Demo("dddd",Test)
    demo.start()
    #result =[]
    #for i in xrange(10):
    #    "index-""+str(i)=i
    #    result.append()
    #    print i
