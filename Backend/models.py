from flask_sqlalchemy import SQLAlchemy 
db=SQLAlchemy()
class Studntd(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uemail=db.Column(db.String,nullable=False,unique=True)
    upassword=db.Column(db.Integer,nullable=False,unique=True)
    fullname=db.Column(db.String,nullable=False)
    qualification=db.Column(db.String,nullable=False)
    date_of_birth=db.Column(db.Date,nullable=False)