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
    # Relationship with Chapters
    chapters=db.relationship('Chapter',backref='subject',lazy=True)

class Chapter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    sub_id=db.Column(db.Integer,db.ForeignKey('subject.id'))
    name=db.Column(db.String,unique=True,nullable=False)
    no_of_questions=db.Column(db.Integer,nullable=False)
    description=db.Column(db.String,unique=True,nullable=False)
    quizes=db.relationship('Quiz',backref='chapter',lazy=True)
class Quiz(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ch_id=db.Column(db.Integer,db.ForeignKey('chapter.id'))
    date_of_quiz=db.Column(db.Date,nullable=False)
    time_duration=db.Column(db.Time,nullable=False)
    remarks=db.Column(db.String,nullable=False)
    questions=db.relationship('Question',backref='quiz',lazy=True)

class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id'))
    question_statement=db.Column(db.String,nullable=False)
    option1=db.Column(db.String,nullable=False)
    option2=db.Column(db.String,nullable=False)
    option3=db.Column(db.String,nullable=False)
    option4=db.Column(db.String,nullable=False)
    correct_answer=db.Column(db.String,nullable=False)


