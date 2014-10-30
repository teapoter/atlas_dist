#!-*-encoding:utf8-*-

from wsgiref.simple_server import make_server

def simple_app(environ,start_response):
    print "Remote Path:",environ.get("REMOTE_ADDR")
    print "Path Info:",environ.get("PATH_INFO")
    status='200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status,response_headers)
    return [u"This is hello wsgi app".encode('utf8')]

httpd = make_server('',9000,simple_app)
print "server on port 9000"
httpd.serve_forever()
