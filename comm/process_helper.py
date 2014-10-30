#!-*-encoding:utf8-*-
# @author:jackson
# @summary:
import multiprocessing

class ProcessHelper(multiprocessing.Process):

    def run(self):
        print "In %s"%self.name
        return


if __name__=='__main__':
    jobs=[]
    for i in range(5):
        p=ProcessHelper()
        jobs.append(p)
        p.start()

    for j in jobs:
        j.join()
