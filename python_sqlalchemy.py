# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/28  16:36 
# 文件名称   ：python_sqlalchemy.PY
# 开发工具   ：PyCharm

import random
import faker

from sqlalchemy import create_engine, Table, Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/blog?charset=utf8')

Base = declarative_base()


# 用户表
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    user_articles_list = relationship('Article', backref='author')
    userinfo = relationship('UserInfo', backref='user', uselist=False)

    def __repr__(self):
        return f"{self.username}"

# 用户信息详情表  （与用户表一对一关系）
class UserInfo(Base):
    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True)
    name = Column(String(11))
    qq = Column(String(11))
    phone = Column(String(11))
    link = Column(String(64))

    user_id = Column(Integer, ForeignKey('user.id'))


# 文章表（与用户表多对一关系）
class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    cate_id = Column(Integer, ForeignKey('category.id'))
    article_tags_list = relationship('Tag', secondary='article_tag', backref='article')

    def __repr__(self):
        return f"{self.title}"


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)
    category_articles_list = relationship('Article', backref='category')

    def __repr__(self):
        return f"{self.name}"

article_tag = Table(
    'article_tag',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)

    def __repr__(self):
        return f"{self.name}"


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    faker = faker.Factory.create()
    Session = sessionmaker(bind=engine)
    session = Session()

    faker_users = [
        User(username=faker.name(),
             password=faker.word(),
             email=faker.email(),)
        for i in range(10)
    ]
    session.add_all(faker_users)

    faker_categories = [Category(name=faker.word()) for i in range(5)]
    session.add_all(faker_categories)

    faker_tags = [Tag(name=faker.word()) for i in range(10)]
    session.add_all(faker_tags)

    for i in range(20):
        article = Article(
            title=faker.sentence(),
            content=' '.join(faker.sentences(nb=random.randint(10,20))),
            author=random.choice(faker_users),
            category=random.choice(faker_categories)
        )
        for tag in random.sample(faker_tags, random.randint(2,5)):
            article.article_tags_list.append(tag)
        session.add(article)

    session.commit()