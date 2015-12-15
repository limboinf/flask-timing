# coding=utf-8
"""
Deal with tasks via beanstalkd and redis Pub/Sub

    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '12/15/15'
import json
import logging
import app
import job

job_client = job.JobWorkerClient('127.0.0.1', 11300)


def sub():
    """
    主调度，通过订阅键空间通知事件来执行响应的Task
    """
    ps = app.rd.pubsub()
    ps.psubscribe(app.subKey)
    for i in ps.listen():
        if i['type'] == 'pmessage' or 'message':
            redis_key = i['data']
            # 匹配 redis key 处理你的定时任务
            # do something

            try:
                job_client.use_put('taskWorkers',
                                   {'cmd': 'task-1', 'args': json.dumps({})})
            except Exception as ex:
                logging.error(ex)


if __name__ == '__main__':
    sub()