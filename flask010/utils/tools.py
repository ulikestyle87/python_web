# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  16:45 
# 文件名称   ：tools.PY
# 开发工具   ：PyCharm

from flask import Flask, make_response, jsonify

class Tools:
    """
    工具类
    """
    @staticmethod
    def str_null(getenv):
        if getenv is None or getenv == '' or getenv == "":
            return True
        return False

    @staticmethod
    def generate_cors_response(jsondata):
        response = make_response(jsonify(jsondata))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-methods'] = 'PUT, POST, GET, DELETE, OPTIONS, HEAD'
        response.headers['Access-Control-Allow-Headers'] = 'x-www-request, Content-type'
        return response
