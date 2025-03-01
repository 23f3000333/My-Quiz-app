from flask import Flask
from Backend.models import *
from datetime import date,time

def setup_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///quiz_app.sqlite3'
    db.init_app(app)
    app.app_context().push()
    app.debug=True
    return app
app=setup_app()
from Backend.controllers import *
if __name__== '__main__':
    app.run(debug=True)
with app.app_context():
    db.create_all()
    admin=Studentd.query.filter_by(is_admin=True).first()
    if not admin:
        admin=Studentd(uemail="admin@iitm.ac.in",upassword=123456,fullname="admin",qualification="admin",date_of_birth=date(1995,7,14),is_admin=True)
        db.session.add(admin)
        db.session.commit()