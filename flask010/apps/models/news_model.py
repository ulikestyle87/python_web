# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  15:21 
# 文件名称   ：news_model.PY
# 开发工具   ：PyCharm
from apps.models import BaseModel
from exts import db
import time


# 第三张表（多对多）news_tag
news_tag =db.Table(
    'news_tag',
    BaseModel.metadata,
    db.Column('news_id', db.ForeignKey('news.id'), primary_key=True),
    db.Column('tag_id', db.ForeignKey('tag.id'), primary_key=True)
)


# 标签表
class Tag(BaseModel):
    __tablename__ = 'tag'
    tname = db.Column(db.String(10), nullable=False)

    def __init__(self, json):
        self.tname = json['tname']

    def __repr__(self):
        return self.tname

    def to_json(self):
        json = {
            'id':int(self.id),
            'date_time':self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_delete':self.is_delete,
            'tname':self.tname
        }
        return json

    def from_json(self,json):
        self.id = int(json['id'])
        self.tname = json['tname']
        self.date_time = json['date_time'].strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.is_delete = json['is_delete']
        return self


# 新闻表
class News(BaseModel):
    __tablename__ = 'news'
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    news_tag_lists = db.relationship('Tag', backref=db.backref('news_tag_lists'), secondary='news_tag')
    news_comment_lists = db.relationship('Comment', backref=db.backref('news_comment_lists'))

    def __init__(self, json):
        self.title = json['title']
        self.desc = json['desc']
        self.content = json['content']
        self.category_id = int(json['category_id'])
        self.user_id = int(json['user_id'])

    def __repr__(self):
        return self.title

    def to_json(self):
        json = {
            'id':int(self.id),
            'date_time':self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_delete':self.is_delete,
            'title':self.title,
            'desc':self.desc,
            'content':self.content,
            'user_id':int(self.user_id),
            'category_id':int(self.category_id),
            'news_tag_lists':Tag.query.get(int(self.id)).to_json() if Tag.query.get(int(self.id)) else [],
            'news_comment_lists':Comment.query.get(int(self.id)).to_json() if Comment.query.get(int(self.id)) else []
        }
        return json

    def from_json(self, json):
        self.id = int(json['id'])
        self.date_time = json['date_time'].strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.is_delete = json['is_delete']
        self.title = json['title']
        self.desc = json['desc']
        self.content = json['content']
        self.user_id = int(json['user_id'])
        self.category_id = int(json['category_id'])
        self.news_comment_lists = json['news_comment_lists']
        self.news_tag_lists = json['news_tag_lists']
        return self


# 分类表
class Category(BaseModel):
    __tablename__ = 'category'
    cname = db.Column(db.String(50), nullable=False)
    category_news_lists = db.relationship('News', backref=db.backref('category_news_lists'))

    def __init__(self, json):
        self.cname = json['cname']

    def __repr__(self):
        return self.cname

    def to_json(self):
        json = {
            'id':int(self.id),
            'date_time':self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_delete':self.is_delete,
            'cname':self.cname,
            # 'category_news_lists':self.category_news_lists
            'category_news_lists':News.query.get(int(self.id)).to_json() if News.query.get(int(self.id)) else []
        }
        return json

    def from_json(self, json):
        self.id = int(json['id'])
        self.date_time = json['date_time'].strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.is_delete = json['is_delete']
        self.cname = json['cname']
        self.category_news_lists = json['category_news_lists']
        return self


# 评论表
class Comment(BaseModel):
    __tablename__ = 'comment'
    content = db.Column(db.Text, nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_reply_lists = db.relationship('Reply', backref=db.backref('comment_reply_lists'))

    def __init__(self, json):
        self.content = json['content']
        self.news_id = int(json['news_id'])
        self.user_id = int(json['user_id'])

    def __repr__(self):
        return self.id

    def to_json(self):
        json = {
            'id':int(self.id),
            'date_time':self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_delete':self.is_delete,
            'content':self.content,
            'news_id':self.news_id,
            'user_id':self.user_id,
            'comment_reply_lists':Reply.query.get(int(self.id)).to_json() if Reply.query.get(int(self.id)) else []
        }
        return json

    def from_json(self, json):
        self.id = int(json['id'])
        self.date_time = json['date_time'].strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.is_delete = json['is_delete']
        self.content = json['content']
        self.news_id = int(json['news_id'])
        self.user_id = int(json['user_id'])
        self.comment_reply_lists = json['comment_reply_lists']
        return self


# 回复表
class Reply(BaseModel):
    __tablename__ = 'reply'
    content = db.Column(db.Text, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, json):
        self.comment_id = int(json['comment_id'])
        self.user_id = int(json['user_id'])
        self.content = json['content']

    def __repr__(self):
        return self.id

    def to_json(self):
        json = {
            'id':int(self.id),
            'content':self.content,
            'comment_id':int(self.comment_id),
            'user_id':int(self.user_id),
            'date_time':self.date_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return json

    def from_json(self,json):
        self.id = int(json['id'])
        self.date_time = json['date_time'].strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.is_delete = json['is_delete']
        self.content = json['content']
        self.user_id = int(json['user_id'])
        self.comment_id = int(json['comment_id'])
        return self




