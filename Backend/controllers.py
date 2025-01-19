from flask import Flask,render_template,request
from flask import current_app as app
from .models import *
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login')
def loging():
    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
  return render_template('register.html')



@app.route('/userdashboard')
def userd():
   return render_template('user.html')
@app.route('/admindashboard')
def admid():
   return render_template('admin.html')