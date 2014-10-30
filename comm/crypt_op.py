#!-*-coding:utf8-*-
import bash64

def simple_encode(str_info=""):
    """"""
    return bash64.b64encode(str_info)

def simple_decode(str_info=""):
    """"""
    return base64.b64decode(str_info)