# coding=utf-8
"""
beanstald job
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
import time
import json
import logging
from beanstalkc import Connection


class JobService(object):
    """
    beanstalkd job service
    watching the appointed tube.
    """
    def __init__(self, host, port, tube):
        self.__host = host
        self.__port = port
        self.__tube = tube
    
    def connect(self):
        while True:
            try:
                self.__bs = Connection(self.__host, self.__port)
                print 'connected to %s:%s' % (self.__host, self.__port)
                self.__bs.watch(self.__tube)
                print 'watching %s' % self.__bs.watching()
                if not self.__bs is None:
                    return
            except:
                time.sleep(1)

    def process(self, job):
        """overwrite
        Realize your functions
        """
        pass

    def finish(self, job):
        job.delete()
    
    def start(self):
        self.connect()
        while True:
            try:
                job = self.__bs.reserve()
                print '>>[new job]', job, job.body
                self.process(job)
                self.finish(job)
            except Exception as ex:
                logging.error('job process exception', exc_info=ex)
                self.connect()


class JobWorkerClient(object):
    """
    job client.
    """
    def __init__(self, host, port, tube=None):
        self.__host = host
        self.__port = port
        self.__tube = tube    
        self.__bs = None
        
    def _ensure_connect(self):
        if self.__bs is None:
            print 'beanstalkc client connecting ...'
            self.__bs = Connection(self.__host, self.__port)
            print 'beanstalkc client connected to %s:%s:[%s]' % (self.__host, self.__port, self.__tube)
            if not self.__tube is None:
                self.__bs.use(self.__tube)
                print 'beanstalkc client using %s' % self.__bs.using()
        
    def put(self,obj):
        self._ensure_connect()
        self.__bs.put(json.dumps(obj))
    
    def use_put(self, tube, obj):
        self._ensure_connect()
        self.__bs.use(tube)
        self.__bs.put(json.dumps(obj))
    
    def use(self, tube):
        self._ensure_connect()
        self.__bs.use(tube)
        self.__tube = tube
    
    def close(self):
        try:
            self.__bs.close()
        except:
            pass
