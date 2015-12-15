# coding=utf-8
"""
beanstalkd Job分布式处理
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__author__ = 'fang'
import os
import json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import job


class TalkWorker(job.JobService):
    def process(self, job):
        if not job:
            return

        data = json.loads(job.body)
        if isinstance(data, dict) and "cmd" in data:
            cmd = data['cmd']

            if cmd == 'yourCmd' and 'args' in data:
                args = data['args']
                # apply(func, (arg1, arg2,...argn))
            #
            # if cmd == 'yourCmd2' and 'args' in data:
            #     args = data['args']
            #     # apply(func, (arg1, arg2,...argn))
            # ............


if __name__ == '__main__':
    worker = TalkWorker('127.0.0.1', 11300, 'taskWorkers')
    worker.start()

