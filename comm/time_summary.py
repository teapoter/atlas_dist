#!-*-encoding:utf8-*-
# @author:jackson
# @time:2014-08-07 16:00:00
# @summary:decorator time eclipse
import time

def time2stamp(timestr,format_type='%Y-%m-%d %H:%M:%S'):
    return time.mktime(time.strptime(timestr, format_type))

def stamp2time(stamp,format_type='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format_type,time.localtime(stamp))


def timer_elasped(func):
        
    def _decorator(*args,**kwargs):
        now_time = time.time()
        print "Now Time:",now_time,"Func Name:",func.__name__
        result = func(*args,**kwargs)
        end_time = time.time()
        print "End Time:",end_time,"Func Name:",func.__name__
        print "Elasped Time:",(end_time-now_time)
        return result
    return _decorator
                                                           
@timer_elasped
def demo():
    print "Hello"
    time.sleep(2)
                                                        
if __name__ =='__main__':
    demo()
    stamp_2_time = stamp2time(time.time())
