import os
import sys
import logging


class Config(object):  # 默认配置
    DEBUG = False

    # get attribute
    def __getitem__(self, key):
        return self.__getattribute__(key)


# 测试环境
class TestingConfig(Config):
    headers_post = {
        "Content-Type": "application/json",
        "autograph": "12345678",
        "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
        "access_token": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJTVVQwMl91Z2NfMTUwNjU0IiwiaWF0IjoxNTk2MDAzMzMwLCJzdWIiOiJ7XCJtZWRpYUlkXCI6XCIxNTA2NTRcIixcIm1lZGlhVHlwZVwiOlwidWdjXCIsXCJzb3VyY2VUeXBlXCI6XCJTVVQwMlwifSIsImV4cCI6MzE5MjAwNjY2MX0.hvdY1XbdTYobdXIxlGc5fJOrOsJ0c6hebL4LmJeY0Pc",
    }
    headers_get = {
        "autograph": "12345678",
        "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
        "access_token": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJTVVQwMl91Z2NfMTUwNjU0IiwiaWF0IjoxNTk2MDAzMzMwLCJzdWIiOiJ7XCJtZWRpYUlkXCI6XCIxNTA2NTRcIixcIm1lZGlhVHlwZVwiOlwidWdjXCIsXCJzb3VyY2VUeXBlXCI6XCJTVVQwMlwifSIsImV4cCI6MzE5MjAwNjY2MX0.hvdY1XbdTYobdXIxlGc5fJOrOsJ0c6hebL4LmJeY0Pc",
    }
    headers_delete={}
    headers_put={}


# 开发环境
class DevelopmentConfig(Config):
    headers_post = {
    }
    headers_get = {}
    headers_delete = {}
    headers_put = {}


# 生产环境
class ProductionConfig(Config):
    headers_post = {
    }
    headers_get = {}
    headers_delete = {}
    headers_put = {}


# 环境映射关系
mapping = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'pro': ProductionConfig,
}


print(sys.argv)
if 'dev' in sys.argv:
    env = 'dev'
elif 'test' in sys.argv:
    env = 'test'
elif 'pro' in sys.argv:
    env = 'pro'
else:
    # exit("参数错误,必须传环境变量!比如: python xx.py dev|pro|default")
    env = 'test'

import pdb
print(pdb.set_trace())

APP_ENV = os.environ.get('APP_ENV', env).lower()
print(APP_ENV)
config = mapping[APP_ENV]()  # 实例化对应的环境
print(config)
logging.warning('现在使用的配置是: {}'.format(env))


