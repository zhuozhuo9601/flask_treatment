from flask import Blueprint
from flask import render_template
from flask import request

from user.models import Student

user_bp=Blueprint('user',__name__)
@user_bp.route('/add', methods=['POST'])
def userValue():
    # 测试json数据
    a = request.json
    print(a)
    return a


@user_bp.route('/delete/<username>', methods=['GET'])
# 测试路由传参
def userDelete(username):
    username = username
    print(username)
    return username

@user_bp.route('/index', methods=['GET'])
def user_index():
    datas = Student.query.all()
    return render_template('ment.html', datas=datas)