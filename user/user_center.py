import json

import datetime
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from manage.configs import db
from user.models import Student, sj, School, Subject

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
    """
    进入首页
    :return:
    """
    datas = Student.query.all()
    # 测试调用模型类方法
    # 必须有model对象，然后对象直接调用方法
    # a = Student.query.get(1)
    # print(a.abc())
    data_list = []
    for value in datas:
        data_dict = {}
        subject_name = value.sub_student
        school_name = value.sch_student[0].name
        data_dict['subject_name'] = subject_name
        data_dict['school_name'] = school_name
        data_dict['student_name'] = value.name
        data_dict['id'] = value.id
        data_list.append(data_dict)
    return render_template('ment.html', datas=data_list)

@user_bp.route('/add/', methods=['POST'])
def user_add():
    """
    添加
    :return:
    """
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
        time = datetime.datetime.now()
        user_dict = request.form.to_dict()
        name = user_dict['username']
        select_sub = user_dict['select_sub']
        select_sch = user_dict['select_sch']
        user = Student(name=name, time=time, age=20)
        school = School.query.get(select_sch)
        subject = Subject.query.get(select_sub)
        school.stu_school.append(user)
        subject.stu_subject.append(user)
        db.session.add(user)
        db.session.commit()
    else:
        return redirect(url_for('user.user_index'))
    return redirect(url_for('user.user_index'))

@user_bp.route('/update/', methods=['POST'])
def user_update():
    """
    修改
    :return:
    """
    if request.method == 'POST':
        update_dict = request.form.to_dict()
        id = update_dict['updateid']
        name = update_dict['updatename']
        update_sub = update_dict['update_sub']
        update_sch = update_dict['update_sch']
        student = Student.query.get(id)
        school = School.query.get(update_sch)
        subject = Subject.query.get(update_sub)
        student.name = name
        student.sch_student[0] = school
        student.sub_student[0] = subject
        db.session.commit()
    else:
        return redirect(url_for('user.user_index'))
    return redirect(url_for('user.user_index'))


@user_bp.route('/delete/', methods=['POST'])
def user_delete():
    """
    删除
    :return:
    """
    data = {}
    if request.method == 'POST':
        try:
            delete_dict = json.loads(request.get_data().decode())
            if delete_dict:
                id = delete_dict.get('del_id')
                school_name = delete_dict.get('school_list')
                subject_list = delete_dict.get('subject')
                user = Student.query.get(id)
                school = School.query.filter(School.name==school_name).first()
                school.stu_school.remove(user)
                for sub in subject_list:
                    if sub:
                        sub_obj = Subject.query.filter(Subject.name==sub).first()
                        sub_obj.stu_subject.remove(user)
                # db.session.delete(user)
                db.session.commit()
                try:
                    db.session.delete(user)
                    db.session.commit()
                except Exception as e:
                    pass
                data['code'] = '200'
                data['msg'] = '删除成功'
        except Exception as e:
            data['code'] = '500'
            data['msg'] = '删除失败'
    else:
        data['code'] = '500'
        data['msg'] = '删除失败'
    return jsonify(data)

@user_bp.route('/add_select/', methods=['POST'])
def add_select():
    """
    返回添加下拉框所需要的课程和学校
    :return:
    """
    school = School.query.all()
    subject = Subject.query.all()
    select_list = []
    for sch in school:
        school_dict = {}
        school_dict['id'] = 'school'
        school_dict['school_id'] = sch.id
        school_dict['sch_name'] = sch.name
        select_list.append(school_dict)
    for sub in subject:
        subject_dict = {}
        subject_dict['id'] = 'subject'
        subject_dict['subject_id'] = sub.id
        subject_dict['sub_name'] = sub.name
        select_list.append(subject_dict)
    return jsonify(select_list)


@user_bp.route('/subject/', methods=['GET'])
def subject_index():
    subjects = Subject.query.all()
    sub_datas = []
    for sub in subjects:
        sub_dict = {}
        stu_list = []
        sch_list = []
        sub_dict['sub'] = sub.name
        sub_dict['id'] = sub.id
        for stu in sub.stu_subject:
            stu_name = stu.name
            stu_list.append(stu_name)
            sub_dict['stu_name'] = stu_list
        for sch in sub.sch_subject:
            sch_name = sch.name
            sch_list.append(sch_name)
            sub_dict['sch_name'] = sch_list
        sub_datas.append(sub_dict)
    return render_template('subject.html', sub_datas=sub_datas)