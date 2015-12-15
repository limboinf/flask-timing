# flask-timing
Timing job with flask, redis, beanstalkd

## 定时任务的选择方案

- *Unix, crontab: 适合shell,python小脚本，较少修改的任务，如mysql备份脚本，Nginx日志切割脚本; 使用简单，不足之处就是管理和控制不友好。
- threading.Timer&sched模块: 线程且阻塞的方式，适合但脚本终端执行
- [APScheduler](https://apscheduler.readthedocs.org/en/latest/), Python任务调度模块,功能强大，适合一些常用，稳定的定时任务，完全可以替代crontab;但缺点就是缺乏web interface
- [Celery](http://www.celeryproject.org/): 功能最强大，但对于我来说太重了，我一般用于配合做tornado异步的api接口和消息队列

造一个简单的web interface定时任务, 原理就是redis键空间通知(keyspace notification)

>键空间通知使得客户端可以通过订阅频道或模式， 来接收那些以某种方式改动了 Redis 数据集的事件。

以下是一些键空间通知发送的事件的例子：

- 所有修改键的命令。
- 所有接收到 LPUSH 命令的键。
- 0 号数据库中所有已过期的键。

事件通过 Redis 的订阅与发布功能（pub/sub）来进行分发， 因此所有支持订阅与发布功能的客户端都可以在无须做任何修改的情况下， 直接使用键空间通知功能。

## 使用

安装redis后，修改redis.conf文件或者直接使用`CONFIG SET`命令来开启键空间通知功能

    # vim redis.conf
    notify-keyspace-events ExA

    # or
    redis-cli config set notify-keyspace-events ExA

clone该项目：

    git clone https://github.com/BeginMan/flask-timing.git
    cd flask-timing
    pip install -r requirements.txt

    # run app
    python app.py

    # run scheduler
    python dispath.py

## demo效果：

![](https://raw.githubusercontent.com/BeginMan/flask-timing/master/flask-corn-demo1.png)

![](https://raw.githubusercontent.com/BeginMan/flask-timing/master/flask-corn-demo2.png)

## 功能：

- 新建基于时间的任务，该时间到达后任务立马执行
- 修改任务
- 删除任务
- 分布式任务处理

## todo:

- [ ] 更灵活的时间调度,类crontab，如：每N分钟,每N小时,每天几点,每月几号几时
- [ ] 任务运行次数，处理结果反馈与同步
- [ ] 页面任务倒计时

