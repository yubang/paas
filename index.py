#coding:UTF-8

from flask import Flask
from app.admin import app as adminApp
from lib.buildConfig import buildPhpConfig
from lib.git import getCodeFromOsc
import config

app=Flask(__name__)
app.secret_key=config.SECRET_KEY
app.register_blueprint(adminApp,url_prefix="/admin")

@app.route("/")
def index():
    return "debug"
    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
