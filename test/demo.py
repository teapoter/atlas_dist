#!-*-coding:utf8-*-

def fun():
    try:
        raise "errr"
    except:
        print "dddd"

def func():
    try:
        fun()
    except:
        print "ttt"

class Demo():
    def __init__(self):
        pass
    def run(self):
        pass

if __name__ == '__main__':
    demo = Demo()
    print getattr(Demo,'run')
