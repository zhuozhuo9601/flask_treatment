import json

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from manage.configs import db
from user.models import Student

user_bp=Blueprint('user',__name__)
# @user_bp.route('/add', methods=['POST'])
# def userValue():
#     # 测试json数据
#     a = request.json
#     print(a)
#     return a


# @user_bp.route('/delete/<username>', methods=['GET'])
# # 测试路由传参
# def userDelete(username):
#     username = username
#     print(username)
#     return username

@user_bp.route('/index', methods=['GET'])
def user_index():
    datas = Student.query.all()
    return render_template('ment.html', datas=datas)

@user_bp.route('/add/', methods=['POST'])
def user_add():
    # print(request.method)  # 获取访问方式 GET
    # print(request.url)  # 获取url http://127.0.0.1:5000/req?id=1&name=wl
    # print(request.cookies)  # 获取cookies {}
    # print(request.path)  # 获取访问路径 /req
    # print(request.args)  # 获取url传过来的值  ImmutableMultiDict([('id', '1'), ('name', 'wl')])
    # print(request.args.get("id"))  # get获取id  1
    # print(request.args["name"])  # 索引获取name wl
    # print(request.args.to_dict())  # 获取到一个字典 {'id': '1', 'name': 'wl'}
    # a = request.args.to_dict()
    # print(a)
    # 获取表单数据
    if request.method == 'POST':
        user_dict = request.form.to_dict()
        name = user_dict['username']
        time = user_dict['time']
        user = Student(name=name, time=time, age=20)
        db.session.add(user)
        db.session.commit()
    else:
        return redirect(url_for('user.user_index'))
    return redirect(url_for('user.user_index'))

@user_bp.route('/update/', methods=['POST'])
def user_update():
    if request.method == 'POST':
        update_dict = request.form.to_dict()
        id = update_dict['updateid']
        name = update_dict['updatename']
        time = update_dict['updatetime']
        student = Student.query.get(id)
        student.name = name
        student.time = time
        db.session.commit()
    else:
        return redirect(url_for('user.user_index'))
    return redirect(url_for('user.user_index'))


@user_bp.route('/delete/', methods=['POST'])
def user_delete():
    data = {}
    if request.method == 'POST':
        id = json.loads(request.get_data().decode())
        if id:
            user = Student.query.get(id)
            db.session.delete(user)
            db.session.commit()
            data['code'] = '200'
            data['msg'] = '删除成功'
        else:
            data['code'] = '500'
            data['msg'] = '删除失败'
    else:
        data['code'] = '500'
        data['msg'] = '删除失败'
    return jsonify(data)