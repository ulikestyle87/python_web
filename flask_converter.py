# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/7/15  8:35 
# 文件名称   ：flask_converter.PY
# 开发工具   ：PyCharm

from flask import Flask
from werkzeug.routing import BaseConverter


app = Flask(__name__)


# 1、定义自己的类转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(RegexConverter, self).__init__(url_map)
        # 将正则表达式的参数保存到对象的属性中，flask会去使用整个属性来进行路由的正则匹配
        self.regex = regex


# 2、将定义好的类转化器添加到flask的应用中
app.url_map.converters['reg'] = RegexConverter


@app.route("/send/<reg(r'1[35678]\d{9}'):mobile>")
def send_msn(mobile):
    return "send msn to %s" % mobile


if __name__ == '__main__':
    # url_map 可以查看整个flask中的路由信息
    print(app.url_map)
    app.run(debug=True)