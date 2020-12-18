# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  15:20 
# 文件名称   ：__init__.py.PY
# 开发工具   ：PyCharm

from flask import g, request, abort
from exts import cache
from apps.models.user_model import User


def check_user():
    token = request.headers.get('Authorization')
    if not token:
        abort(501, msg='请先登录')
    phone = cache.get(token)
    if not phone:
        abort(501, msg='token失效，请重新登录')
    user = User.query.filter(User.phone == phone).first()
    if not user:
        abort(501, msg='用户不存在或已被删除')
    g.user = user


def login_required(func):

    def wrapper(*args, **kwargs):
        check_user()
        return func(*args, **kwargs)
    return wrapper