from flask import Flask,render_template,request,redirect,url_for,session,flash

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
      flash("Enter all fields ")
      return redirect(url_for("login"))  
    user_details=Studentd.query.filter_by(uemail=uemail,upassword=upassword).first()
    if not user_details:
      flash( "Do register first")
      return redirect(url_for("register")) 
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
    user = Studentd.query.get(session['user_id'])  # Get logged-in user
    today_date = datetime.now().strftime('%Y-%m-%d')  # Get today's date

    # Fetch all subjects and chapters
    subjects = Subject.query.all()
    chapters = Chapter.query.all()

    # Get selected subject and chapter names from the request
    selected_subject_name = request.args.get('subject_name')
    selected_chapter_name = request.args.get('chapter_name')

    # Fetch quizzes based on selected subject and chapter names
    if selected_chapter_name:
        # Find the chapter by name
        chapter = Chapter.query.filter_by(name=selected_chapter_name).first()
        if chapter:
            quizzes = Quiz.query.filter_by(ch_id=chapter.id).all()
        else:
            quizzes = []
    elif selected_subject_name:
        # Find the subject by name
        subject = Subject.query.filter_by(name=selected_subject_name).first()
        if subject:
            # Fetch all chapters for the selected subject
            chapters_for_subject = Chapter.query.filter_by(sub_id=subject.id).all()
            # Fetch quizzes for all chapters of the selected subject
            quizzes = Quiz.query.filter(Quiz.ch_id.in_([chapter.id for chapter in chapters_for_subject])).all()
        else:
            quizzes = []
    else:
        # If no subject or chapter is selected, show all quizzes
        quizzes = Quiz.query.all()

    return render_template(
        'user.html',user=user,subjects=subjects,chapters=chapters,quizzes=quizzes,today_date=today_date,selected_subject_name=selected_subject_name,selected_chapter_name=selected_chapter_name)
@app.route('/admindashboard')
def admind():
    user = Studentd.query.get(session['user_id'])  # Get logged-in user
    subjects = Subject.query.all()  # Fetch all subjects
    chapters = Chapter.query.all()  # Fetch all chapters
    users = Studentd.query.all()  # Fetch all users

    # Initialize lists for search results
    subject_results = []
    chapter_results = []
    user_results = []

    # Get search parameters from the request
    search_type = request.args.get('search_type')  # Get search category
    query = request.args.get('query')  # Get search input

    # Perform search if a query is provided
    if query:
        try:
            if search_type == "subject_name":
                subject_results = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()  # Case-insensitive search
            elif search_type == "chapter_name":
                chapter_results = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()
            elif search_type == "user_name":
                user_results = Studentd.query.filter(Studentd.fullname.ilike(f"%{query}%")).all()  # Search users by name
        except ValueError:
            return "Invalid Input Format!", 400
    else:
        # If no query, show all subjects, chapters, and users
        subject_results = subjects
        chapter_results = chapters
        user_results = users

    # Flash message if no results are found
    if query and not (subject_results or chapter_results or user_results):
        flash("No such data found", "warning")  # Flash message for no results

    return render_template('admin.html',user=user,subjects=subject_results,chapters=chapter_results,users=user_results,search_type=search_type,query=query)
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
    subject = Subject.query.get(sub_id)
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
    chapters = Chapter.query.all()
    search_query = request.args.get('search_query', '').strip()  # Get the search query
    search_type = request.args.get('search_type', 'quizid')  # Get the search type (quizid or chapter name)

    # Initialize quizzes with all quizzes
    quizes = Quiz.query.all()

    # Filter quizzes only if a search query is provided
    if search_query:
        if search_type == 'quizid':
            try:
                quiz_id = int(search_query)
                quizes = [quiz for quiz in quizes if quiz.id == quiz_id]
            except ValueError:
                quizes = []  # If the search query is not a valid integer, return no results
        elif search_type == 'chapter_name':
            quizes = [quiz for quiz in quizes if quiz.chapter and search_query.lower() in quiz.chapter.name.lower()]

    questions = Question.query.all()
    return render_template('Admin_add/quiz.html', quizes=quizes, questions=questions, chapters=chapters, search_query=search_query, search_type=search_type)

# _________________________________________________________QUIZADD
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
            score = score + 1 # Abhi ke lliye use store krrhe h value directly in score kuch problem hua to ushko session me store krna h as deepseek bhi direct sessionme store kr rha thaa
        # Redirect to the next question
        if quest_no + 1 < len(questions):
          return redirect(url_for('user_quiz', quiz_id=quiz_id, quest_no=quest_no + 1))
        else:
          new_score = Score(user_id=user.id, quiz_id=quiz_id, score=score)
          db.session.add(new_score)
          db.session.commit()
          return redirect(url_for('userd', quiz_id=quiz_id))

    return render_template('User_add/user_quiz.html', quiz=quiz, question=question, quest_no=quest_no, quiz_id=quiz_id, user=user, questions=questions)
  
# ------------------------SUMMARY---------------------------------------------
@app.route('/summary')
def summary():
    # Fetch all subjects
    subjects = Subject.query.all()

    # Fetch all scores
    scores = Score.query.all()

    # Prepare data for the charts
    highest_score_labels = []
    highest_score_values = []

    user_attempts_labels = []
    user_attempts_values = []

    for subject in subjects:
        # Fetch all chapters for the current subject
        chapters = Chapter.query.filter_by(sub_id=subject.id).all()

        # Fetch all quizzes for these chapters
        quiz_ids = [quiz.id for chapter in chapters for quiz in chapter.quizes]

        # Find scores for these quizzes
        subject_scores = [score.score for score in scores if score.quiz_id in quiz_ids]

        # If scores exist for the subject, find the highest score
        if subject_scores:
            highest_score = max(subject_scores)
            highest_score_labels.append(subject.name)  # Subject name
            highest_score_values.append(highest_score)  # Highest score

        # Calculate the number of user attempts for the subject
        user_attempts = len([score for score in scores if score.quiz_id in quiz_ids])
        user_attempts_labels.append(subject.name)  # Subject name
        user_attempts_values.append(user_attempts)  # Number of attempts

    # Prepare data for the template
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

    return render_template('Admin_add/summary.html', summary_data=summary_data)
@app.route('/usum')
def user_summary():
    user = Studentd.query.get(session['user_id'])
    # Fetch all subjects
    subjects = Subject.query.all()

    # Fetch all quizzes
    quizzes = Quiz.query.all()

    # Fetch all scores for the current user
    user_scores = Score.query.filter_by(user_id=user.id).all()

    # Prepare data for the charts
    subject_quiz_counts = {}
    month_quiz_counts = {}

    # Calculate subject-wise number of quizzes
    for subject in subjects:
        # Fetch all chapters for the current subject
        chapters = Chapter.query.filter_by(sub_id=subject.id).all()

        # Fetch all quizzes for these chapters
        quiz_ids = [quiz.id for chapter in chapters for quiz in chapter.quizes]

        # Count the number of quizzes for the subject
        subject_quiz_counts[subject.name] = len(quiz_ids)

    # Calculate month-wise number of quizzes attempted by the user
    for score in user_scores:
        month = score.timestamp.month  # Extract month from the timestamp
        month_name = datetime(2023, month, 1).strftime('%B')  # Convert month number to name
        if month_name in month_quiz_counts:
            month_quiz_counts[month_name] += 1
        else:
            month_quiz_counts[month_name] = 1

    # Prepare data for the template
    summary_data = {
        'subject_quiz_counts': {
            'labels': list(subject_quiz_counts.keys()),  # Subject names
            'values': list(subject_quiz_counts.values())  # Number of quizzes
        },
        'month_quiz_counts': {
            'labels': list(month_quiz_counts.keys()),  # Month names
            'values': list(month_quiz_counts.values())  # Number of attempts
        }
    }

    return render_template('User_add/usum.html', summary_data=summary_data)

@app.route('/profile')
def profile():
  user=Studentd.query.get(session['user_id'])
  return render_template('profile.html',user=user)
@app.route('/logout')
def logout():
  session.pop('user_id')
  return redirect(url_for('home'))