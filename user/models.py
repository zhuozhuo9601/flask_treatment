from datetime import datetime

from manage.configs import db

# python manager.py db init  初始化出migrations的文件，只调用一次
#
# python manager.py db migrate  生成迁移文件
#
# python manager.py db upgrade 执行迁移文件中的升级
#
# python manager.py db downgrade 执行迁移文件中的降级
#
# python manager.py db --help 帮助文档


# 第一个参数 stu_sc 是表名,student_id是字段名
# 学生学校多对多关联表
sc = db.Table('stu_school',
              # 创建两个列，分别设置链接的外键
              db.Column('student_id', db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), primary_key=True),
              db.Column('school_id', db.Integer, db.ForeignKey('schools.id', ondelete='CASCADE'), primary_key=True))

# 学生课程多对多关联表
sj = db.Table('stu_subject',
              # 创建两个列，分别设置链接的外键
              db.Column('student_id', db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), primary_key=True),
              db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True))

# 学校课程多对多关联表
ss = db.Table('sub_school',
              # 创建两个列，分别设置链接的外键
              db.Column('school_id', db.Integer, db.ForeignKey('schools.id', ondelete='CASCADE'), primary_key=True),
              db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True))

# 学生表
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now)
    student_many1 = db.relationship('School', secondary=sc,
                              backref='stu_school',
                              lazy='dynamic')
    student_many2 = db.relationship('Subject', secondary=sj,
                              backref='stu_subject',
                              lazy='dynamic')
    # repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s' % self.name

    def abc(self):
        return '我是测试model下面的类方法如何调用'


# 学校表
class School(db.Model):
    __tablename__ = "schools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    school_many1 = db.relationship('Subject', secondary=ss,
                                    backref='sch_subject',
                                    lazy='dynamic')
    school_many2 = db.relationship('Student', secondary=sc,
                                    backref='sch_student',
                                    lazy='dynamic')

# 课程表
class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    subject_many1 = db.relationship('Student', secondary=sj,
                                    backref='sub_student',
                                    lazy='dynamic')
    subject_many2 = db.relationship('School', secondary=ss,
                                   backref='sub_school',
                                   lazy='dynamic')