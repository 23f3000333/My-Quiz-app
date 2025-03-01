from flask import Flask,render_template,request,redirect,url_for,session

from flask import current_app as app
from .models import *
@app.route('/')
def home():
  if 'user' in session:
    return render_template('index.html')
  else:
    return redirect(url_for ('login'))
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
    user_details=Studentd.query.filter_by(uemail=uemail,upassword=upassword).first()
    if not user_details:
      return "Do register first"
  # Password checking is not done yet
    session['user_id'] = user_details.id# Storing username in session
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
  today_date=datetime.now().strftime('%Y-%m-%d')
  user=Studentd.query.get(session['user_id'])
  return render_template('user.html',quizess=quizess,today_date=today_date,user=user)
@app.route('/admindashboard')
def admind():
  subjects=Subject.query.all()
  user=Studentd.query.get(session['user_id'])
  return render_template('admin.html', subjects=subjects,user=user,Chapter=Chapter)
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


# ----------------------------------QUIZ AND QUESTION-----------------------------------------------
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

# ____________________________________________________________QUIZ CRUD(SHOW)
@app.route('/quiz_show/<int:id>/show')
def quiz_show(id):
  quizobj=Quiz.query.get(id)
  chapter=Chapter.query.all()
  subject=Subject.query.all()
  if not quizobj:
    return "Chapter doesn't exit"
  return render_template('Admin_add/quizshow.html',quizobj=quizobj,chapter=chapter,subject=subject)

# _____________________________________QUESTION
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
# ______________________________________________________________QUESTION CRUD
# -----------------QUESTION EDIT ------------------------------
@app.route('/quest_edit/<int:id>/edit')
def quest_edit(id):
  questobj=Question.query.get(id)
  if not questobj:
    return "Chapter doesn't exit"#Flash message is required here
  return render_template('Admin_add/Qu_edit.html',questobj=questobj)
@app.route('/quest_edit/<int:id>/edit',methods=['POST'])
def quest_edit_p(id):
  if request.method =='POST':
    questobj=Question.query.get(id)
    if not questobj:
      return "Chapter doesn't exit"#Flash message is required here
    quiz_id=request.form.get('q_id')
    question_statement=request.form.get('ques')
    option1=request.form.get('op1')
    option2=request.form.get('op2')
    option3=request.form.get('op3')
    option4=request.form.get('op4')
    correct_answer=request.form.get('corr_ans')
    if not quiz_id or not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_answer:
      return "Enter all fields" # here flash messsages will work 
    questobj.quiz_id=quiz_id
    questobj.question_statement=question_statement
    questobj.option1=option1
    questobj.option2=option2
    questobj.option3=option3
    questobj.option4=option4
    questobj.correct_answer=correct_answer
    db.session.commit()
  return redirect(url_for('quize'))
# -----------------QUESTION DELETE ------------------------------
@app.route('/quest_delete/<int:id>/edit')
def quest_delete(id):
  questobj=Question.query.get(id)
  if not questobj:
    return "Chapter doesn't exit"
  return render_template('Admin_add/Qu_delete.html',questobj=questobj)
@app.route('/quest_delete/<int:id>/edit',methods=['POST'])
def quest_delete_p(id):
  if request.method =='POST':
    questobj=Question.query.get(id)
    if not questobj:
      return "Chapter doesn't exit"
    db.session.delete(questobj)
    db.session.commit()
  return redirect(url_for('userd'))
# ___________________________________________________________StudentScore
@app.route('/stu_scores')
def stu_scores():
  user=Studentd.query.get(session['user_id'])
  score_show= []
  query = request.args.get('query')  # Get score from search bar
  search_type = request.args.get('search_type')  # Get search type (Score ID or Score Value)
  for score in user.uscores:
    quiz = Quiz.query.get(score.quiz_id)
    if query:
      try:
        if (search_type == "qtime" and score.timestamp.date() == datetime.strptime(query, "%Y-%m-%d").date()) or (search_type == "score_value" and score.score == int(query)):
          score_show.append((quiz,score))
      except:
        return "Invalid Input format!"
    else:
        score_show.append((quiz,score))# idhr elif not query lgayenge tih data jb nhi hogi toh wo sara data show nahi kregi instead wo kewal head part show kregi table ka lekin else me data nahi hota h phir vhi pura data show krta h ab ye clear hoga flash message lgane ke baad
        
  if query and not score_show:
      return "No such data found", "warning" # Flash message will be here 
  return render_template('User_add/scores.html',user=user,quiz=quiz,query=query,score_show=score_show,search_type=search_type)



@app.route('/stu_quiz_show/<int:id>squizs')
def stu_quiz_show(id):
  quizobj=Quiz.query.get(id)
  chapter=Chapter.query.filter_by(id=Quiz.ch_id)
  subject=Subject.query.filter_by(id=Chapter.sub_id)
  if not quizobj:
    return "Chapter doesn't exit"
  return render_template('User_add/squizv.html',quizobj=quizobj,chapter=chapter,subject=subject)

# ______________________________________________________________QUIZ ATTEMPT AND SUBMISSION
# Route to display the quiz
@app.route('/user_quiz/<int:quiz_id>/', methods=['GET', 'POST'])
@app.route('/user_quiz/<int:quiz_id>/<int:quest_no>/', methods=['GET', 'POST'])
def user_quiz(quiz_id, quest_no=0):
    user = Studentd.query.get(session['user_id'])
    quiz = Quiz.query.get(quiz_id)
    questions = quiz.questions

    # Ensure question index is within range
    if quest_no >= len(questions):
        return redirect(url_for('userd', quiz_id=quiz_id))

    question = questions[quest_no]
    score = 0

    if request.method == 'POST':
        selected_option = request.form.get(f'question_{question.id}')
        if selected_option == question.correct_answer:
            score = score + 1

        new_score = Score(user_id=user.id, quiz_id=quiz_id, score=score)
        db.session.add(new_score)
        db.session.commit()

        # Redirect to the next question
        if quest_no + 1 < len(questions):
            return redirect(url_for('user_quiz', quiz_id=quiz_id, quest_no=quest_no + 1))
        else:
            return redirect(url_for('userd', quiz_id=quiz_id))

    return render_template('User_add/user_quiz.html', quiz=quiz, question=question, quest_no=quest_no, quiz_id=quiz_id, user=user, questions=questions)
  
# ------------------------SUMMARY---------------------------------------------
@app.route('/summary')
def summary():
    summary_data = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        'values': [65, 59, 80, 81, 56, 55, 40]
    }
    return render_template('Admin_add/summary.html', summary_data=summary_data)  
    
   