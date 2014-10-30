#!-*-coding:utf8-*-
import sys
import traceback

def print_exc_info():
    #step-0:
    tb = sys.exc_info()[2]
    while tb.tb_next:
        tb = tb.tb_next
    stack =[]
    #step-1:
    f = tb.tb_frame
    while f:
        stack.append(f)
        f=f.f_back
    #step-2:
    stack.reverse()
    traceback.print_exc()
    
    print "Locals by frame:"
    for frame in stack:
        print
        print "Frame %s in %s at line %s"%(frame.f_code.co_name,
                                           frame.f_code.co_filename,
                                           frame.f_lineno)
        for key,value in frame.f_locals.items():
            print "\t%20s = " %key,
            try:
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"
                
def print_error(data=[]):
    ret_value =[]
    for item in data:
        ret_value.append("0"*(4-len(item))+item)
                
    return ret_value

if __name__ =='__main__':
    
    data =["9","4",1,"2"]
    try:
        print_error(data)
    except:
        print_exc_info()
