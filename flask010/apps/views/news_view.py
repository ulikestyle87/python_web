# -*- coding: utf-8 -*-
# 开发人员   ：黎工
# 开发时间   ：2020/12/3  15:21 
# 文件名称   ：news_view.PY
# 开发工具   ：PyCharm

from flask import Blueprint, request, g
from apps.models.news_model import Tag, News, Category, Comment, Reply, news_tag
from utils.tools import Tools
from exts import db
from apps.views import login_required

bp_news = Blueprint('news', __name__, url_prefix='/news')


# 添加标签
@bp_news.route('/add_tag', endpoint='add_tag', methods=['POST'])
def bp_news_add_tag():
    data = request.get_json()
    if not data and data is None:
        return Tools.generate_cors_response({'code':200, 'msg':'缺少必要参数'})
    if not data.get('tname'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入标签名称'})

    tag = Tag(data)
    db.session.add(tag)
    db.session.commit()
    return Tools.generate_cors_response({'code':200, 'msg':'标签添加成功'})


# 添加分类
@bp_news.route('/add_cate', endpoint='add_cate', methods=['POST'])
def bp_news_add_category():
    data = request.get_json()
    if not data and data is None:
        return Tools.generate_cors_response({'code':200, 'msg':'缺少必要参数'})
    if not data.get('cname'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入分类名称'})
    category = Category(data)
    db.session.add(category)
    db.session.commit()
    return Tools.generate_cors_response({'code':200, 'msg':'分类添加成功'})


# 添加新闻
@bp_news.route('/add_news', endpoint='add_news', methods=['POST'])
@login_required
def bp_news_add_news():

    data = request.get_json()
    if not data and data is None:
        return Tools.generate_cors_response({'code':200, 'msg':'缺少必要参数'})
    if not data.get('title'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入新闻标题'})
    if not data.get('desc'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入新闻描述'})
    if not data.get('content'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入新闻内容'})
    if not data.get('category_id'):
        return Tools.generate_cors_response({'code':200, 'msg':'请输入分类ID'})
    data['user_id'] = g.user.id

    news = News(data)
    if not data.get('tag_id'):
        db.session.add(news)
        db.session.commit()
        return Tools.generate_cors_response({'code': 200, 'msg': '新闻添加成功', 'news': news.to_json()})

    # 给该条新闻添加标签
    for t in data.get('tag_id'):
        tag = Tag.query.get(t)
        news.news_tag_lists.append(tag)
    db.session.add(news)
    db.session.commit()
    return Tools.generate_cors_response({'code':200, 'msg':'带标签新闻添加成功', 'news':news.to_json()})


# 展示新闻
@bp_news.route('/every_news', endpoint='every_news')
def bp_news_every_news():
    news = News.query.filter(News.is_delete==False).all()
    news_list = list()
    for n in news:
        news_list.append(n.to_json())
    return Tools.generate_cors_response({'code':200, 'msg':'新闻内容请求成功', 'news_list':news_list})


# 添加评论
@bp_news.route('/add_comment', endpoint='add_comment', methods=['POST'])
@login_required
def bp_news_add_comment():
    data = request.get_json()
    if not data and data is None:
        return Tools.generate_cors_response({'code':200, 'msg':'缺少必要参数'})
    if not data.get('content'):
        return Tools.generate_cors_response({'code':200, 'msg':'请填写评论内容'})
    if not data.get('news_id'):
        return Tools.generate_cors_response({'code':200, 'msg':'请填写评论新闻ID'})
    data['user_id'] = g.user.id

    comment = Comment(data)
    db.session.add(comment)
    db.session.commit()
    return Tools.generate_cors_response({'code':200, 'msg':'评论添加成功', 'comment':comment.to_json()})


# 展示评论
@bp_news.route('/every_comment', endpoint='every_comment')
def bp_news_show_comment():
    comments = Comment.query.filter(Comment.is_delete==False).all()
    comment_list = list()
    for comment in comments:
        comment_list.append(comment.to_json())
    return Tools.generate_cors_response({'code':200, 'msg':'请求评论内容成功', 'comment_list':comment_list})


# 添加回复
@bp_news.route('/add_reply', endpoint='add_reply', methods=['POST'])
@login_required
def bp_news_add_reply():
    data = request.get_json()
    if not data and data is None:
        return Tools.generate_cors_response({'code':200, 'msg':'缺少必要参数'})
    if not data.get('content'):
        return Tools.generate_cors_response(({'code':200, 'msg':'请填写回复内容'}))
    if not data.get('comment_id'):
        return Tools.generate_cors_response({'code':200, 'msg':'请填写需回复的评论ID'})
    data['user_id'] = g.user.id

    reply = Reply(data)
    db.session.add(reply)
    db.session.commit()
    return Tools.generate_cors_response({'code':200, 'msg':'回复添加成功', 'reply':reply.to_json()})


# 展示回复
@bp_news.route('/every_reply', endpoint='every_reply')
def bp_news_show_reply():
    replys = Reply.query.filter(Reply.is_delete==False).all()
    reply_list = list()
    for reply in replys:
        reply_list.append(reply.to_json())
    return Tools.generate_cors_response({'code':200, 'msg':'请求回复内容成功', 'reply_list':reply_list})