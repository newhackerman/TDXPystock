# -*- coding: utf-8 -*-
from functools import wraps
import time

def time_counts(fn):
    @wraps(fn)
    def mesasure_time(*args,**kwargs):
        t1=time.time()
        result=fn(*args,**kwargs)
        t2=time.time()
        print('<-- '+fn.__name__+' _执行耗时: '+str(round((t2-t1),3))+' seconds -->')
        return result
    return mesasure_time


if __name__ == '__main__':
    @time_counts
    def add(a, b):
        print('{}+{}={}'.format(a, b, a + b))
        return a + b
    add(5,6)
