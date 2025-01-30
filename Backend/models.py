from flask_sqlalchemy import SQLAlchemy  
db=SQLAlchemy()
from datetime import datetime
class Studentd(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uemail=db.Column(db.String,nullable=False,unique=True)
    upassword=db.Column(db.Integer,nullable=False,unique=True)
    fullname=db.Column(db.String,nullable=False)
    qualification=db.Column(db.String,nullable=False)
    date_of_birth=db.Column(db.Date,nullable=False)
    is_admin=db.Column(db.Boolean,nullable=False,default=False)
class Subject(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    description=db.Column(db.String,unique=True,nullable=False)
class Chapter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    no_of_questions=db.Column(db.Integer,nullable=False)
    description=db.Column(db.String,unique=True,nullable=False)
class Quiz(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ch_id=db.Column(db.Integer,nullable=False,unique=True)
    date_of_quiz=db.Column(db.Date,nullable=False)
    time_duration=db.Column(db.Time,nullable=False)
    remarks=db.Column(db.String,nullable=False)
class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,nullable=False,unique=True)
    question_statement=db.Column(db.String,nullable=False)
    option_answer=db.Column(db.String,nullable=False)
