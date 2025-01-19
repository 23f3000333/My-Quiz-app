from flask import Flask
from Backend.models import db 
def setup_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///quiz_app.sqlite3'
    db.init_app(app)
    app.app_context().push()
    app.debug=True
    return app
app=setup_app()
from Backend.controllers import *
# app=Flask(__name__)
if __name__== '__main__':
    app.run(debug=True)