#coding:UTF-8

from flask import Flask
from app.admin import app as adminApp
from app.servlet import app as servletApp
from app.api import app as apiApp
import config

app=Flask(__name__)
app.secret_key=config.SECRET_KEY
app.register_blueprint(adminApp,url_prefix="/admin")
app.register_blueprint(servletApp,url_prefix="/servlet")
app.register_blueprint(apiApp,url_prefix="/api")


@app.route("/")
def index():
    from lib.db import db,objToDict
    dao=db.execute("select count(*) from paas_app where remoteServer = '%s'"%("127.0.0.1"))
    r=objToDict(dao.first())
    dao.close()
    print r
    return "debug"
    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
