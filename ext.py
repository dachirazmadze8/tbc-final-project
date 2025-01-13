from flask import Flask,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config ["SECRET_KEY"]= "dachi2009"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


db =SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = None

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in to access this page.", "success")
    return redirect(url_for('login'))

