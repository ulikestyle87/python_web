# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  15:21 
# 文件名称   ：user_view.PY
# 开发工具   ：PyCharm
import random
import uuid

from flask import Blueprint, request
from utils.tools import Tools
from apps.models.user_model import User
from exts import db, cache
from werkzeug.security import generate_password_hash, check_password_hash


bp_user = Blueprint('user', __name__, url_prefix='/user')


# 用户注册
@bp_user.route('/register', endpoint='register', methods=['GET','POST'])
def bp_user_register():
    data = request.get_json()
    if not data and data is None:
        return Tools.generate_cors_response({"code":200, "msg":'缺少必要参数'})
    if not data.get('username'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入用户名'})
    if not data.get('password'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入密码'})
    data['password'] = generate_password_hash(data.get('password'))
    if not data.get('phone'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入手机号码'})
    if not data.get('email'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入email'})

    user = User(data)
    db.session.add(user)
    db.session.commit()
    return Tools.generate_cors_response({'code':200, 'msg':'恭喜你，注册成功！'})


# 用户登录
@bp_user.route('/login', endpoint='login', methods=['POST'])
def bp_user_login():
    data = request.get_json()
    if not data and data is None:
        return Tools.generate_cors_response({'code':200, 'msg':'缺少必要参数'})
    if not data.get('username'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入用户名'})
    if not data.get('phone'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入手机号码'})
    if not data.get('password'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入密码'})
    user = User.query.filter(User.phone==data.get('phone')).first()
    if user and user.username==data.get('username') and check_password_hash(user.password, data.get('password')):
        token = str(uuid.uuid4()).replace('-','') + str(random.randint(100, 999))
        cache.set(token, data.get('phone'), timeout=6000)
        return Tools.generate_cors_response({'code':200, 'msg':'登录成功', 'token':token})
    return Tools.generate_cors_response({'code':200, 'msg':'登录失败'})


# 用户展示
@bp_user.route('/show_user', endpoint='/show_user')
def bp_user_show_user():
    users = User.query.filter(User.is_delete==False).all()
    data_list = list()
    for user in users:
        data_list.append(user.to_json())
    return Tools.generate_cors_response({'code':200, 'msg':'用户信息显示成功', 'user_list':data_list})