# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  13:40 
# 文件名称   ：settings.PY
# 开发工具   ：PyCharm

import os

class Config:
    DEBUG = False
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    UPLOAD_DIR = os.path.join(STATIC_DIR, 'upload')
    ICON_DIR = os.path.join(UPLOAD_DIR, 'icon')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask010' + '?charset=utf8&autocommit=true'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'redis'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SECRET_KEY = 'guess hard to String'


class Testing(Config):
    DEBUG = True
    ENV = 'testing'

class Development(Config):
    DEBUG = True
    ENV = 'development'

class Production(Config):
    DEBUG = False
    ENV = 'production'

config = {
    'test':Testing,
    'pro':Production,
    'dev':Development
}