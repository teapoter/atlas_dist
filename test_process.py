#!-*-coding:utf8-*-
import multiprocessing
import time

def func(msg):
    for i in xrange(3):
        print msg
        time.sleep(1)
    return "done:"+msg
if __name__ =='__main__':
    #p = multiprocessing.Process(target=func,args=("hello",))
    p = multiprocessing.Pool(processes=4)
    result =[]
    for i in xrange(10):
        msg ="hello: %s" %str(i)
        result.append(p.apply_async(func,(msg,)))
    p.close()
    #p.start()
    p.join()
    for res in result:
        print res.get()
    print "sub-process done"

