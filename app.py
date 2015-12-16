# coding=utf-8
"""
desc..
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '12/15/15'
import datetime
import redis
from flask import Flask, render_template, request, redirect, jsonify
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from forms import AddTaskForm


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='...',
    BEANSTALKD_HOST='127.0.0.1',
    BEANSTALKD_PORT='11300',
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI='mysql://root:!qaz2wsx@192.168.0.120/cron'
)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

rd = redis.Redis(password='2015yunlianxiQAZWSX')

# 键空间通知（keyspace notification）
subKey = '__keyevent@0__:expired'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    redis_key = db.Column(db.String(128), unique=True)
    start_time = db.Column(db.DateTime)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, redis_key, start_time):
        self.name = name
        self.redis_key = redis_key
        start_time = ':'.join(start_time.split(':')[:2])
        self.start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        # self.seconds as key expire seconds
        self.seconds = int((self.start_time - datetime.datetime.now()).total_seconds())

    def __repr__(self):
        return '<Task name:%r, key:%r>' % (self.name, self.redis_key)


@app.route('/')
def task_list():
    tasks = Task.query.order_by(Task.start_time.desc())
    task_lists = []
    for obj in tasks:
        dic = {}
        dic['id'] = obj.id
        dic['name'] = obj.name
        dic['redis_key'] = obj.redis_key
        dic['start_time'] = obj.start_time
        dic['expired'] = 0 if rd.exists(obj.redis_key) else 1
        dic['create_date'] = obj.create_date
        task_lists.append(dic)
        # todo: task执行结果回调
    return render_template('index.html', tasks=task_lists)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    task_id = request.args.get('tid')
    ori_task = Task.query.filter(Task.id == task_id).first()
    form = AddTaskForm()
    if ori_task:
        form = AddTaskForm(name=ori_task.name, key=ori_task.redis_key, ctime=ori_task.start_time)

    if request.method == 'POST' and form.validate():
        tid = request.values.get('tid')
        str_key = form.key.data
        task = Task(form.name.data, str_key, form.ctime.data)
        if tid:
            # update
            tsObj = Task.query.filter(Task.id == tid).first()
            ori_str_key = tsObj.redis_key
            rd.delete(ori_str_key)
            tsObj.redis_key = str_key
            tsObj.name = form.name.data
            tsObj.start_time = form.ctime.data
            db.session.commit()
        else:
            db.session.add(task)

        rd.setex(str_key, 1, task.seconds)
        return redirect('/')
    return render_template('add.html', form=form)


@app.route('/del/<tid>')
def del_task(tid):
    task = Task.query.filter(Task.id == tid).first()
    str_key = task.redis_key
    db.session.delete(task)
    rd.delete(str_key)
    return redirect('/')


if __name__ == '__main__':
    app.run()