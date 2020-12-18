# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  13:50 
# 文件名称   ：__init__.py.PY
# 开发工具   ：PyCharm
from flask import Flask
from exts import db
from exts import cache
from exts import cors
from apps.views.user_view import bp_user
from apps.views.news_view import bp_news


def create_app(configName):
    app = Flask(__name__)
    app.config.from_object(configName)

    app.register_blueprint(bp_user)
    app.register_blueprint(bp_news)

    db.init_app(app)
    cache.init_app(app)
    cors.init_app(app=app, supports_credentials=True)


    print(app.url_map)
    return app