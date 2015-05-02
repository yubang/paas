#coding:UTF-8

from flask import Flask,render_template
from app.admin import app as adminApp
from app.servlet import app as servletApp
from app.user import app as userApp
from app.api import app as apiApp
import config

app=Flask(__name__)
app.secret_key=config.SECRET_KEY
app.register_blueprint(adminApp,url_prefix="/admin")
app.register_blueprint(servletApp,url_prefix="/servlet")
app.register_blueprint(apiApp,url_prefix="/api")
app.register_blueprint(userApp,url_prefix="/user")

@app.route("/")
def index():
    return render_template("index.html")
    

