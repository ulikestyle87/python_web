from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/flask_sql_demo"
    # 设置sqlalchemy自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


# 在“多”的一侧加入外键，指定“一”这一侧联结的记录
# 示例代码：一个角色可属于多个用户，每个用户只能有一个角色
# 创建数据库模型类
class User(db.Model):
    """用户表"""
    __tablename__ = "tbl_users"     # 指明数据库的表名

    id = db.Column(db.Integer,primary_key=True)     # 整型的主键会默认设置为自增的主键
    name = db.Column(db.String(64),unique=True)
    email = db.Column(db.String(128),unique=True)
    password = db.Column(db.String(128))
    # 一个角色可属于多个用户，在“多”的一侧加入一个外键
    role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id"))


class Role(db.Model):
    """用户角色表"""
    __tablename__ = "tbl_roles"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)
    # 每一个用户只能有一个角色，指定“一”这一侧联结的记录
    users = db.relationship("User", backref='role')


if __name__ == '__main__':
    # app.run(debug=True)
    # 清除数据库里的所有数据
    db.drop_all()

    # 创建所有的表
    db.create_all()

    # 创建对象
    role1 = Role(name='admin')
    # session记录对象任务
    db.session.add(role1)
    # 提交任务到数据库中
    db.session.commit()

    role2 = Role(name='staff')
    db.session.add(role2)
    db.session.commit()

    us1 = User(name='wang',email='wang@163.com',password='123456',role_id=role1.id)
    us2 = User(name='zhang',email='zhang@163.com',password='123456',role_id=role2.id)
    us3 = User(name='chen',email='chen@163.com',password='123456',role_id=role2.id)
    us4 = User(name='zhou',email='zhou@163.com',password='123456',role_id=role1.id)
    # 以列表的方式传递多条数据
    db.session.add_all([us1,us2,us3,us4])
    db.session.commit()

    # 查询所有数据
    rli = Role.query.all()
    db_rli = db.session.query(Role).all()
    print(rli)
    print(rli[0].name)

    print(db_rli)

    # 查询第一条数据
    u1 = User.query.first()
    print(u1.name)

    # 查询指定数据 get
    u3 = User.query.get(3)
    print(u3.name)

    # 分组查询
    u_group = db.session.query(User.role_id,func.count(User.role_id)).group_by(User.role_id).all()
    print(u_group)

