# coding=utf-8
"""
desc..
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '12/15/15'
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators


class AddTaskForm(Form):
    name = StringField(u'名称', [validators.DataRequired()])
    key = StringField(u'键名', [validators.DataRequired()])
    ctime = StringField(u'定时时间', [validators.DataRequired()])
    submit = SubmitField(u'add')


