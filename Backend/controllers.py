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
  quizess=Quiz.query.all()
  return render_template('user.html',quizess=quizess)
@app.route('/admindashboard')
def admind():
  subjects=Subject.query.all()
  chapters=Chapter.query.all()
  return render_template('admin.html', subjects=subjects,chapters=chapters)
@app.route('/sub_add')
def sub_add():
  return render_template('Admin_add/subj.html')
@app.route('/sub_add',methods=['POST'])
def sub_add_p():
  if request.method =='POST':
    name=request.form.get('Name')
    description=request.form.get('Description')
    if not name or not description:
      return "Enter all fields" # here flash messsages will work 
    subjectd=Subject(name=name,description=description)
    db.session.add(subjectd)
    db.session.commit()
  return redirect(url_for('admind'))
@app.route('/chap_add')
def chap_add():
  return render_template('Admin_add/chp.html')
@app.route('/chap_add',methods=['POST'])
def chap_add_p():
  if request.method =='POST':
    name=request.form.get('Name')
    description=request.form.get('Description')
    no_of_questions=request.form.get('n_of_ques')
    if not name or not description or not no_of_questions:
      return "Enter all fields" # here flash messsages will work 
    chapd=Chapter(name=name,description=description,no_of_questions=no_of_questions)
    db.session.add(chapd)
    db.session.commit()
  return redirect(url_for('admind'))
@app.route('/quiz')
def quize():
  quizes=Quiz.query.all()
  questions=Question.query.all()
  return render_template('Admin_add/quiz.html',quizes=quizes,questions=questions)
@app.route('/quiz_add')
def quizad():
  return render_template('Admin_add/quizadd.html')
@app.route('/quiz_add',methods=['POST'])
def quizadp():
  if request.method =='POST':
    ch_id=request.form.get('chapid')
    date_of_quiz=request.form.get('d_of_quiz')
    time_duration=request.form.get('t_dur')
    remarks=request.form.get('remarks')

    if not ch_id or not date_of_quiz or not time_duration or not remarks:
      return "Enter all fields" # here flash messsages will work 
    quizd=Quiz(ch_id=ch_id,date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d'),time_duration=datetime.strptime(time_duration, "%H:%M").time(),remarks=remarks)
    db.session.add(quizd)
    db.session.commit()
  return redirect(url_for('quize'))


@app.route('/quest_add')
def questad():
  return render_template('Admin_add/questadd.html')
@app.route('/quest_add',methods=['POST'])
def questadp():
  if request.method =='POST':
    quiz_id=request.form.get('q_id')
    question_statement=request.form.get('ques')
    option_answer=request.form.get('answer')
    if not quiz_id or not question_statement or not option_answer :
      return "Enter all fields" # here flash messsages will work 
    quesd=Question(quiz_id=quiz_id,question_statement=question_statement,option_answer=option_answer)
    db.session.add(quesd)
    db.session.commit()
  return redirect(url_for('quize'))
# @app.route('/summary')
# def summary():
#     summary_data = {
#         'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
#         'values': [65, 59, 80, 81, 56, 55, 40]
#     }
#     return render_template('Admin_add/summary.html', summary_data=summary_data)
@app.route('/stu_scores')
def stu_scores():
  return render_template('User_add/scores.html')