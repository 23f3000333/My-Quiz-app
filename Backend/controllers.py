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

# -------------------------------------------------DASHBOARD FOR USER AND ADMIN----------------------------------------------------------------------
@app.route('/userdashboard')
def userd():
  quizess=Quiz.query.all()
  return render_template('user.html',quizess=quizess)
@app.route('/admindashboard')
def admind():
  subjects=Subject.query.all()
  chapters = Chapter.query.filter_by(sub_id=Subject.id).all()
  return render_template('admin.html', subjects=subjects,chapters=chapters)
# -------------------------------------------SUBJECT AND CHAPTER RELATED(CRUD OPERATION)--------------------------------------------
# ------------------------------------------------------SUBJECT--------------------------------------------------------------
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
# -------------------------------------------------CHAPTER-------------------------------------------------------------------
@app.route('/chap_add')
def chap_add():
  return render_template('Admin_add/chp.html')
@app.route('/chap_add',methods=['POST'])
def chap_add_p():
  if request.method =='POST':
    name=request.form.get('Name')
    description=request.form.get('Description')
    no_of_questions=request.form.get('n_of_ques')
    sub_id=request.form.get('s_id')
    if not name or not description or not no_of_questions or not sub_id:
      return "Enter all fields" # here flash messsages will work 
    chapd=Chapter(name=name,description=description,no_of_questions=no_of_questions,sub_id=sub_id)
    db.session.add(chapd)
    db.session.commit()
  return redirect(url_for('admind'))
# -----------------CHAPTER EDIT ------------------------------
@app.route('/chap_edit/<int:id>/edit')
def chap_edit(id):
  chapobj=Chapter.query.get(id)
  if not chapobj:
    return "Chapter doesn't exit"#Flash message is required here
  return render_template('Admin_add/Ch_edit.html',chapobj=chapobj)
@app.route('/chap_edit/<int:id>/edit',methods=['POST'])
def chap_edit_p(id):
  if request.method =='POST':
    chapobj=Chapter.query.get(id)
    if not chapobj:
      return "Chapter doesn't exit"#Flash message is required here
    name=request.form.get('Name')
    description=request.form.get('Description')
    no_of_questions=request.form.get('n_of_ques')
    sub_id=request.form.get('s_id')
    if not name or not description or not no_of_questions or not sub_id:
      return "Enter all fields" # here flash messsages will work 
    chapobj.name=name
    chapobj.description=description
    chapobj.no_of_questions=no_of_questions
    chapobj.sub_id=sub_id
    db.session.commit()
  return redirect(url_for('admind'))
# -----------------CHAPTER DELETE ------------------------------
@app.route('/chap_delete/<int:id>/edit')
def chap_delete(id):
  chapobj=Chapter.query.get(id)
  if not chapobj:
    return "Chapter doesn't exit"#Flash message is required here
  return render_template('Admin_add/Ch_delete.html',chapobj=chapobj)
@app.route('/chap_delete/<int:id>/edit',methods=['POST'])
def chap_delete_p(id):
  if request.method =='POST':
    chapobj=Chapter.query.get(id)
    if not chapobj:
      return "Chapter doesn't exit"#Flash message is required here
    db.session.delete(chapobj)
    db.session.commit()
  return redirect(url_for('admind'))


# QUIZ CRUD OPERATION
@app.route('/quiz')
def quize():
  chapters=Chapter.query.all()
  quizes=Quiz.query.filter_by(ch_id=Chapter.id)
  questions=Question.query.all()
  return render_template('Admin_add/quiz.html',quizes=quizes,questions=questions,chapters=chapters)
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
    option1=request.form.get('op1')
    option2=request.form.get('op2')
    option3=request.form.get('op3')
    option4=request.form.get('op4')
    correct_answer=request.form.get('corr_ans')
    if not quiz_id or not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_answer:
      return "Enter all fields" # here flash messsages will work 
    quesd=Question(quiz_id=quiz_id,question_statement=question_statement,option1=option1,option2=option2,option3=option3,option4=option4,correct_answer=correct_answer)
    db.session.add(quesd)
    db.session.commit()
  return redirect(url_for('quize'))
@app.route('/quizshow')
def quizshow():
  return render_template('Admin_add/quizshow.html')
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
@app.route('/stu_quiz_show')
def stu_quiz_show():
  return render_template('User_add/viewscore.html')
