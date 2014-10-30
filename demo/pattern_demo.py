#!-*-encoding:utf8-*-
import re

def _check_format(ip):
    '''function:check ip validate'''
    r_pattern =r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    result = re.match(r_pattern,ip)
    print result
    if result is None:
        return False 
    else:
        return True 


if __name__ =='__main__':
    r_ip = "10.101.10.1"
    print _check_format(r_ip)
    r_ip="q.a.12.10"
    print _check_format(r_ip)
    r_ip="20147455666"
    print _check_format(r_ip)
    r_ip="104.14247.12.13"
