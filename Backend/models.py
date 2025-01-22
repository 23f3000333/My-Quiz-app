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
