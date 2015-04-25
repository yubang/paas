#coding:UTF-8

from flask import Flask
from app.admin import app as adminApp
from app.servlet import app as servletApp
import config

app=Flask(__name__)
app.secret_key=config.SECRET_KEY
app.register_blueprint(adminApp,url_prefix="/admin")
app.register_blueprint(servletApp,url_prefix="/servlet")

@app.route("/")
def index():
    from lib.client import buildApp
    print buildApp(5,'127.0.0.7',"php")
    return "debug"
    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
