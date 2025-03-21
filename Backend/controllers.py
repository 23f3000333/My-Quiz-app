from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login',methods=['POST'])
def login_p():
    uemail=request.form.get('Email')
    upassword=request.form.get('Password')

    if not uemail or not upassword:
      flash("Enter all fields ")
      return redirect(url_for("login"))  
    user_details=Studentd.query.filter_by(uemail=uemail).first()
    if not user_details:
      flash( "Username doesn't exist, Do register first!")
      return redirect(url_for("register")) 

    if not check_password_hash(user_details.upassword, upassword):
        flash('Incorrect password')
        return redirect(url_for('login'))

    session['user_id'] = user_details.id# Storing username in session
    user = Studentd.query.get(session['user_id'])
    if user.is_admin:
      flash('Login successful')
      return redirect(url_for('admind'))  
    flash('Login successful')
    return redirect(url_for('userd'))
    

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/register',methods=['POST'])
def register_p():
    uemail=request.form.get('email')
    upassword=request.form.get('passw')
    fullname=request.form.get('fullname')
    qualification=request.form.get('qualification')
    date_of_birth=request.form.get('dob')

    if not uemail or not upassword or not fullname or not qualification:
      flash("Enter all fields") 
      return redirect(url_for('register'))

    userd=Studentd.query.filter_by(uemail=uemail).first()
    if userd:
      flash("User all ready exist") 
      return redirect(url_for('login'))
      
    password_hash = generate_password_hash(upassword)
    new_userd=Studentd(uemail=uemail,upassword=password_hash,fullname=fullname,qualification=qualification,date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d'))
    db.session.add(new_userd)
    db.session.commit()
    return redirect(url_for('login'))


# DASHBOARD FOR USER AND ADMIN
@app.route('/userdashboard')
def userd():
    user = Studentd.query.get(session['user_id']) 
    today_date = datetime.now().strftime('%Y-%m-%d') 
    # For SearchBar 
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    selected_subject_name = request.args.get('subject_name')
    selected_chapter_name = request.args.get('chapter_name')

    if selected_chapter_name:
        chapter = Chapter.query.filter_by(name=selected_chapter_name).first()
        if chapter:
            quizzes = Quiz.query.filter_by(ch_id=chapter.id).all()
        else:
            quizzes = []

    elif selected_subject_name:
        subject = Subject.query.filter_by(name=selected_subject_name).first()
        if subject:
            chapters_for_subject = Chapter.query.filter_by(sub_id=subject.id).all()
            quizzes = Quiz.query.filter(Quiz.ch_id.in_([chapter.id for chapter in chapters_for_subject])).all()
        else:
            quizzes = []

    else:
        quizzes = Quiz.query.all()
    return render_template('user.html',user=user,subjects=subjects,chapters=chapters,quizzes=quizzes,today_date=today_date,selected_subject_name=selected_subject_name,selected_chapter_name=selected_chapter_name)


@app.route('/admindashboard')
def admind():
    user = Studentd.query.get(session['user_id'])  
    subjects = Subject.query.all() 
    chapters = Chapter.query.all() 
    users = Studentd.query.all() 
    #For Searchbar
    subject_results = []
    chapter_results = []
    user_results = []
    search_type = request.args.get('search_type') 
    query = request.args.get('query')
    if query:
        try:
            if search_type == "subject_name":
                subject_results = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all() 
            elif search_type == "chapter_name":
                chapter_results = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()
            elif search_type == "user_name":
                user_results = Studentd.query.filter(Studentd.fullname.ilike(f"%{query}%")).all() 
        except ValueError:
            flash("Invalid Input Format!")
    else:
        subject_results = subjects
        chapter_results = chapters
        user_results = users
    if query and not (subject_results or chapter_results or user_results):
      flash("No such data found", "warning") 
    return render_template('admin.html',user=user,subjects=subject_results,chapters=chapter_results,users=user_results,search_type=search_type,query=query)


# SUBJECT AND CHAPTER RELATED(CRUD OPERATION)
# SUBJECT
@app.route('/sub_add')
def sub_add():
  return render_template('Admin_add/subj.html')

@app.route('/sub_add',methods=['POST'])
def sub_add_p():
    name=request.form.get('Name')
    description=request.form.get('Description')
    if not name or not description:
      flash("Enter all fields") 
    subjectd=Subject(name=name,description=description)
    db.session.add(subjectd)
    db.session.commit()
    return redirect(url_for('admind'))


# ---- SUBJECT EDIT -----
@app.route('/sub_edit/<int:id>/edit')
def sub_edit(id):
  subobj=Subject.query.get(id)
  if not subobj:
    flash("Subject doesn't exit")
  return render_template('Admin_add/Sub_edit.html',subobj=subobj)

@app.route('/sub_edit/<int:id>/edit',methods=['POST'])
def sub_edit_p(id):
    subobj=Subject.query.get(id)
    if not subobj:
      flash("Subject doesn't exit")
    name=request.form.get('Name')
    description=request.form.get('Description')
    if not name or not description :
      flash("Enter all fields")
    subobj.name=name
    subobj.description=description
    db.session.commit()
    return redirect(url_for('admind'))


# ---SUBJECT DELETE ----
@app.route('/sub_delete/<int:id>')
def sub_delete(id):
  subobj=Subject.query.get(id)
  if not subobj:
    flash("Subject doesn't exit")
  return render_template('Admin_add/Sub_delete.html',subobj=subobj)

@app.route('/sub_delete/<int:id>',methods=['POST'])
def sub_delete_p(id):
    subobj=Subject.query.get(id)
    if not subobj:
      flash("Subject doesn't exit")
    db.session.delete(subobj)
    db.session.commit()
    return redirect(url_for('admind'))
# CHAPTER
@app.route('/chap_add')
def chap_add():
  return render_template('Admin_add/chp.html')

@app.route('/chap_add',methods=['POST'])
def chap_add_p():
    name=request.form.get('Name')
    description=request.form.get('Description')
    no_of_questions=request.form.get('n_of_ques')
    sub_id=request.form.get('s_id')
    if not name or not description or not no_of_questions or not sub_id:
      flash("Enter all fields!")
    subject = Subject.query.get(sub_id)
    chapd=Chapter(name=name,description=description,no_of_questions=no_of_questions,sub_id=sub_id)
    db.session.add(chapd)
    db.session.commit()
    return redirect(url_for('admind'))

# ---- CHAPTER EDIT -----
@app.route('/chap_edit/<int:id>/edit')
def chap_edit(id):
  chapobj=Chapter.query.get(id)
  if not chapobj:
    flash("Chapter doesn't exit")
  return render_template('Admin_add/Ch_edit.html',chapobj=chapobj)

@app.route('/chap_edit/<int:id>/edit',methods=['POST'])
def chap_edit_p(id):
    chapobj=Chapter.query.get(id)
    if not chapobj:
      flash("Chapter doesn't exit")
    name=request.form.get('Name')
    description=request.form.get('Description')
    no_of_questions=request.form.get('n_of_ques')
    sub_id=request.form.get('s_id')
    if not name or not description or not no_of_questions or not sub_id:
      flash("Enter all fields")
    chapobj.name=name
    chapobj.description=description
    chapobj.no_of_questions=no_of_questions
    chapobj.sub_id=sub_id
    db.session.commit()
    return redirect(url_for('admind'))

# ---CHAPTER DELETE ----
@app.route('/chap_delete/<int:id>')
def chap_delete(id):
  chapobj=Chapter.query.get(id)
  if not chapobj:
    flash("Chapter doesn't exit")
  return render_template('Admin_add/Ch_delete.html',chapobj=chapobj)

@app.route('/chap_delete/<int:id>',methods=['POST'])
def chap_delete_p(id):
    chapobj=Chapter.query.get(id)
    if not chapobj:
      flash("Chapter doesn't exit")
    db.session.delete(chapobj)
    db.session.commit()
    return redirect(url_for('admind'))


# QUIZ AND QUESTION
# QUIZ

@app.route('/quiz')
def quize():
    chapters = Chapter.query.all()
    search_query = request.args.get('search_query', '').strip() 
    search_type = request.args.get('search_type', 'quizid')
    quizes = Quiz.query.all()
    if search_query:
        if search_type == 'quizid':
            try:
                quiz_id = int(search_query)
                quizes = [quiz for quiz in quizes if quiz.id == quiz_id]
            except ValueError:
                quizes = []
                flash("Invalid Input Format!")
        elif search_type == 'chapter_name':
            quizes = [quiz for quiz in quizes if quiz.chapter and search_query.lower() in quiz.chapter.name.lower()]

    questions = Question.query.all()
    return render_template('Admin_add/quiz.html', quizes=quizes, questions=questions, chapters=chapters, search_query=search_query, search_type=search_type)

#--QUIZADD---
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
      flash("Enter all fields" )
    quizd=Quiz(ch_id=ch_id,date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d'),time_duration=datetime.strptime(time_duration, "%H:%M").time(),remarks=remarks)
    db.session.add(quizd)
    db.session.commit()
  return redirect(url_for('quize'))


# ---QUIZ EDIT ---
@app.route('/quiz_edit/<int:id>/edit')
def quiz_edit(id):
  quizobj=Quiz.query.get(id)
  if not quizobj:
    flash("Quiz doesn't exist")
  return render_template('Admin_add/Quiz_edit.html',quizobj=quizobj)
@app.route('/quiz_edit/<int:id>/edit',methods=['POST'])
def quiz_edit_p(id):
    quizobj=Quiz.query.get(id)
    if not quizobj:
      flash("Quiz doesn't exit")
    ch_id=request.form.get('chapid')
    date_of_quiz=request.form.get('d_of_quiz')
    time_duration=request.form.get('t_dur')
    remarks=request.form.get('remarks')

    if not ch_id or not date_of_quiz or not time_duration or not remarks:
      flash("Enter all fields" )
    quizobj.ch_id=ch_id
    quizobj.date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d')
    quizobj.time_duration=datetime.strptime(time_duration, "%H:%M:%S").time()
    quizobj.remarks=remarks
    db.session.commit()
    return redirect(url_for('quize'))


# --QUIZ DELETE --
@app.route('/quiz_delete/<int:id>')
def quiz_delete(id):
  quizobj=Quiz.query.get(id)
  if not quizobj:
    flash("Quiz doesn't exit")
  return render_template('Admin_add/Quiz_delete.html',quizobj=quizobj)
@app.route('/quiz_delete/<int:id>',methods=['POST'])
def quiz_delete_p(id):
    quizobj=Quiz.query.get(id)
    if not quizobj:
      flash("Quiz doesn't exit")
    db.session.delete(quizobj)
    db.session.commit()
    return redirect(url_for('quize'))

# ---QUIZ CRUD(SHOW)----
@app.route('/quiz_show/<int:id>/show')
def quiz_show(id):
  quizobj=Quiz.query.get(id)
  chapter=Chapter.query.all()
  subject=Subject.query.all()
  if not quizobj:
    flash("Quiz doesn't exit")
  return render_template('Admin_add/quizshow.html',quizobj=quizobj,chapter=chapter,subject=subject)

# QUESTION
@app.route('/quest_add')
def questad():
  return render_template('Admin_add/questadd.html')
@app.route('/quest_add',methods=['POST'])
def questadp():
    quiz_id=request.form.get('q_id')
    question_statement=request.form.get('ques')
    option1=request.form.get('op1')
    option2=request.form.get('op2')
    option3=request.form.get('op3')
    option4=request.form.get('op4')
    correct_answer=request.form.get('corr_ans')
    if not quiz_id or not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_answer:
      flash("Enter all fields") 
    quesd=Question(quiz_id=quiz_id,question_statement=question_statement,option1=option1,option2=option2,option3=option3,option4=option4,correct_answer=correct_answer)
    db.session.add(quesd)
    db.session.commit()
    return redirect(url_for('quize'))

# QUESTION CRUD
# ---QUESTION EDIT ---
@app.route('/quest_edit/<int:id>/edit')
def quest_edit(id):
  questobj=Question.query.get(id)
  if not questobj:
    flash("Chapter doesn't exit")
  return render_template('Admin_add/Qu_edit.html',questobj=questobj)
@app.route('/quest_edit/<int:id>/edit',methods=['POST'])
def quest_edit_p(id):
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
      flash("Enter all fields")
    questobj.quiz_id=quiz_id
    questobj.question_statement=question_statement
    questobj.option1=option1
    questobj.option2=option2
    questobj.option3=option3
    questobj.option4=option4
    questobj.correct_answer=correct_answer
    db.session.commit()
    return redirect(url_for('quize'))

# --QUESTION DELETE --
@app.route('/quest_delete/<int:id>/edit')
def quest_delete(id):
  questobj=Question.query.get(id)
  if not questobj:
    flash("Chapter doesn't exit")
  return render_template('Admin_add/Qu_delete.html',questobj=questobj)
@app.route('/quest_delete/<int:id>/edit',methods=['POST'])
def quest_delete_p(id):
    questobj=Question.query.get(id)
    if not questobj:
      flash("Chapter doesn't exit")
    db.session.delete(questobj)
    db.session.commit()
    return redirect(url_for('quize'))


# StudentScore
@app.route('/stu_scores')
def stu_scores():
  user=Studentd.query.get(session['user_id'])
  score_show= []
  query = request.args.get('query') 
  search_type = request.args.get('search_type')
  quiz=None
  for score in user.uscores:
    quiz = Quiz.query.get(score.quiz_id)
    if query:
      try:
        if (search_type == "qtime" and score.timestamp.date() == datetime.strptime(query, "%Y-%m-%d").date()) or (search_type == "score_value" and score.score == int(query)):
          score_show.append((quiz,score))
      except:
        flash("Invalid Input format!")
    else:
        score_show.append((quiz,score))
        
  if query and not score_show :
      flash("No such data found", "warning" )
  return render_template('User_add/scores.html',user=user,quiz=quiz,query=query,score_show=score_show,search_type=search_type)


#QuizShow
@app.route('/stu_quiz_show/<int:id>squizs')
def stu_quiz_show(id):
  quizobj=Quiz.query.get(id)
  chapter=Chapter.query.filter_by(id=Quiz.ch_id)
  subject=Subject.query.filter_by(id=Chapter.sub_id)
  if not quizobj:
    flash("Chapter doesn't exit")
  return render_template('User_add/squizv.html',quizobj=quizobj,chapter=chapter,subject=subject)

# QUIZ ATTEMPT AND SUBMISSION
# Route to display the quiz
@app.route('/user_quiz/<int:quiz_id>/', methods=['GET', 'POST'])
@app.route('/user_quiz/<int:quiz_id>/<int:quest_no>/', methods=['GET', 'POST'])
def user_quiz(quiz_id, quest_no=0):
    user = Studentd.query.get(session['user_id'])
    quiz = Quiz.query.get(quiz_id)
    questions = quiz.questions
    if 'score' not in session:
        session['score'] = 0
    
    # Ensure question index is within range
    if quest_no >= len(questions):
        final_score = session.pop('score')  # Retrieve and remove score from session
        new_score = Score(user_id=user.id, quiz_id=quiz_id, score=final_score)
        db.session.add(new_score)
        db.session.commit()
        return redirect(url_for('userd', quiz_id=quiz_id))

    question = questions[quest_no]

    if request.method == 'POST':
        selected_option = request.form.get(f'question_{question.id}')
        if selected_option == question.correct_answer:
            session['score'] += 1 

        # Redirect to the next question
        return redirect(url_for('user_quiz', quiz_id=quiz_id, quest_no=quest_no + 1))

    return render_template('User_add/user_quiz.html', quiz=quiz, question=question, quest_no=quest_no, quiz_id=quiz_id, user=user, questions=questions)

  
# --SUMMARY---
@app.route('/summary')
def summary():
    user = Studentd.query.get(session['user_id'])
    subjects = Subject.query.all()
    scores = Score.query.all()
    highest_score_labels = []
    highest_score_values = []

    user_attempts_labels = []
    user_attempts_values = []

    for subject in subjects:
        chapters = Chapter.query.filter_by(sub_id=subject.id).all()
        quiz_ids = [quiz.id for chapter in chapters for quiz in chapter.quizes]
        subject_scores = [score.score for score in scores if score.quiz_id in quiz_ids]

        if subject_scores:
            highest_score = max(subject_scores)
            highest_score_labels.append(subject.name)  
            highest_score_values.append(highest_score)  
        user_attempts = len([score for score in scores if score.quiz_id in quiz_ids])
        user_attempts_labels.append(subject.name)  
        user_attempts_values.append(user_attempts)  

    summary_data = {
        'highest_score': {
            'labels': highest_score_labels,
            'values': highest_score_values
        },
        'user_attempts': {
            'labels': user_attempts_labels,
            'values': user_attempts_values
        }
    }

    return render_template('Admin_add/summary.html', summary_data=summary_data,user=user)
@app.route('/usum')
def user_summary():
    user = Studentd.query.get(session['user_id'])
    subjects = Subject.query.all()
    quizzes = Quiz.query.all()
    user_scores = Score.query.filter_by(user_id=user.id).all()

    subject_quiz_counts = {}
    month_quiz_counts = {}

    for subject in subjects:
        chapters = Chapter.query.filter_by(sub_id=subject.id).all()
        quiz_ids = [quiz.id for chapter in chapters for quiz in chapter.quizes]
        subject_quiz_counts[subject.name] = len(quiz_ids)
    for score in user_scores:
        month = score.timestamp.month  # Extract month from the timestamp
        month_name = datetime(2023, month, 1).strftime('%B')  # Convert month number to name
        if month_name in month_quiz_counts:
            month_quiz_counts[month_name] += 1
        else:
            month_quiz_counts[month_name] = 1

    summary_data = {
        'subject_quiz_counts': {
            'labels': list(subject_quiz_counts.keys()),  
            'values': list(subject_quiz_counts.values())  
        },
        'month_quiz_counts': {
            'labels': list(month_quiz_counts.keys()),  
            'values': list(month_quiz_counts.values())  
        }
    }

    return render_template('User_add/usum.html', summary_data=summary_data,user=user)
    

@app.route('/profile')
def profile():
  user=Studentd.query.get(session['user_id'])
  return render_template('profile.html',user=user)


@app.route('/logout')
def logout():
  session.pop('user_id')
  return redirect(url_for('home'))


@app.route('/logout/cancel')
def cancel():
  user=Studentd.query.get(session['user_id'])
  if user.is_admin:
    return redirect(url_for('admind',user=user))
  return redirect(url_for('userd',user=user))
  