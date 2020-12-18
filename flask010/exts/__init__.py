# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  13:49 
# 文件名称   ：__init__.py.PY
# 开发工具   ：PyCharm
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_cors import CORS

db = SQLAlchemy()
cache = Cache()
cors = CORS()
