from datetime import datetime

from manage.configs import db


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now)