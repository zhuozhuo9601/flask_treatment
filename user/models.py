from datetime import datetime

from manage.configs import db


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now)

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s' % self.name

    def abc(self):
        return '我是测试model下面的类方法如何调用'
