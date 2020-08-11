# 导入Flask类
import os

from flask import Flask

#Flask类接收一个参数__name__
from flask import render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from manage.configs import db
from operation.tenance import opera
from user.user_center import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(opera,url_prefix='/opera')

# "mysql+pymysql://root:zsh123@127.0.0.1:3306/basic12"
# '数据库类型://数据库登录名:数据库登录密码@数据库的地址:数据库的端口/数据库的名字'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@127.0.0.1:3306/flask_zhuo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

# 通过Manager管理app
manager = Manager(app)

# - 使用Migrate,关联app,db
Migrate(app, db)

from user.models import Student
# 给manager添加操作命令,使用MigrateCommand
manager.add_command("db", MigrateCommand)

# 装饰器的作用是将路由映射到视图函数index
@app.route('/')
def index():
    return render_template('index.html')

# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    manager.run()