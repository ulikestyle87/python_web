# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  15:20 
# 文件名称   ：__init__.py.PY
# 开发工具   ：PyCharm

from exts import db
import time


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_delete = db.Column(db.Boolean, default=False)
    date_time = db.Column(db.DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))