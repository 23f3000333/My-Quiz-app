from flask import Flask,render_template,request,redirect,url_for
from flask import current_app as app
from .models import *
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login',methods=['POST'])
def login_p():
  if request.method=="POST":
    uemail=request.form.get('Email')
    upassword=request.form.get('Password')
    if not uemail or not upassword:
      return "Enter all fields "
    user_details=Studentd.query.filter_by(uemail=uemail).first()
    if not user_details:
      return "Do register first"
  # Password checking is not done yet
    c_for_admin=(uemail=="admin@iitm.ac.in")
    if c_for_admin:
      return redirect(url_for('admind'))
  return redirect(url_for('userd'))
@app.route('/register')
def register():
  return render_template('register.html')
@app.route('/register',methods=['POST'])
def register_p():
  if request.method =='POST':
    uemail=request.form.get('email')
    upassword=request.form.get('passw')
    fullname=request.form.get('fullname')
    qualification=request.form.get('qualification')
    date_of_birth=request.form.get('dob')
    if not uemail or not upassword or not fullname or not qualification:
      return "Enter all fields" # here flash messsages will work 
    userd=Studentd.query.filter_by(uemail=uemail).first()
    if userd:
      return "user already exist"
    new_userd=Studentd(uemail=uemail,upassword=upassword,fullname=fullname,qualification=qualification,date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d'))
    db.session.add(new_userd)
    db.session.commit()
  return redirect(url_for('login'))




@app.route('/userdashboard')
def userd():
   return render_template('user.html')
@app.route('/admindashboard')
def admind():
   return render_template('admin.html')