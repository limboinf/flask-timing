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

key_to_funcs = {
    'send_yidong_msm': 'func1',
    'clean_data': 'func2',
}


def sub():
    """
    主调度，通过订阅键空间通知事件来执行响应的Task

    匹配 redis key 处理你的定时任务
    如带参数有如下两种方式：
        1. redis key 设计成这样: strKey@param1@param2@param3..., 以`@`分隔参数
        2. 参数写入数据库中，查询数据获取对应的参数

    """
    ps = app.rd.pubsub()
    ps.psubscribe(app.subKey)
    for i in ps.listen():
        if i['type'] == 'pmessage' or 'message':
            redis_key = i['data']
            print '>>>>>', redis_key
            # 匹配 redis key 处理你的定时任务
            # do something

            # try:
            #     job_client.use_put('taskWorkers',
            #                        {'cmd': 'task-1', 'args': json.dumps({})})
            # except Exception as ex:
            #     logging.error(ex)


if __name__ == '__main__':
    sub()