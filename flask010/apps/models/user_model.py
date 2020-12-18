# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  15:21 
# 文件名称   ：user_model.PY
# 开发工具   ：PyCharm
import time

from exts import db
from apps.models import BaseModel
from apps.models.news_model import News, Comment, Reply


class User(BaseModel):
    __tablename__ = 'user'
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(50))
    icon = db.Column(db.String(256))

    user_news_lists = db.relationship('News', backref=db.backref('user_news_lists'))
    user_comment_lists = db.relationship('Comment', backref=db.backref('user_comment_lists'))
    user_reply_lists = db.relationship('Reply', backref=db.backref('user_reply_lists'))

    def __repr__(self):
        return self.username

    def __init__(self, json):
        self.username = json['username']
        self.password = json['password']
        self.phone = json['phone']
        self.email = json['email']

    def to_json(self):
        json = {
            'id':int(self.id),
            'date_time':self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'username':self.username,
            # 'password':self.password,
            # 'phone':self.phone,
            'email':self.email,
            'icon':self.icon,
            # 'is_delete':self.is_delete,
            'user_news_lists':News.query.get(int(self.id)).to_json() if News.query.get(int(self.id)) else [],
            'user_comment_lists':Comment.query.get(int(self.id)).to_json() if Comment.query.get(int(self.id)) else [],
            'user_reply_lists':Reply.query.get(int(self.id)).to_json() if Reply.query.get(int(self.id)) else []
        }

        return json

    def from_json(self, json):
        self.id = int(json['id'])
        self.date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.username = json['username']
        self.password = json['password']
        self.phone = json['phone']
        self.email = json['email']
        self.icon = json['icon']
        self.is_delete = json['is_delete']
        self.user_news_lists = json['user_news_lists']
        self.user_comment_lists = json['user_comment_lists']
        self.user_reply_lists = json['user_reply_lists']
        return self