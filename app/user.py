#coding:UTF-8


"""
用户模块
2015-04-26
"""


from flask import Blueprint,request,g,render_template,session,redirect,abort,json
from lib.db import db,objToDict,sqlDeal
from lib import client
import config

from functools import wraps
import hashlib


app=Blueprint("user",__name__)


def checkUser(fn):
    "权限检查"
    @wraps(fn)
    def deal(*args,**kwds):
        if session.has_key("user"):
            return fn(*args,**kwds)
        else:
            return redirect("/user/account")
    return deal


@app.route("/")
@checkUser
def index():
    "主页面"
    g.apiHost=config.API_HOST
    
    sql="select paas_app_token.apiKey,paas_app_token.secretKey,paas_app.status,paas_app.id,paas_app.gitUrl,paas_app.host,paas_app.remoteServer,paas_app.title,paas_app.description,paas_app.language,paas_account.username from paas_app_token,paas_app,paas_account where paas_app.status != 4 AND paas_app.uid = paas_account.id AND  paas_app_token.aid=paas_app.id  AND paas_app.uid = %d order by paas_app.id desc"%(session['user'])
    dao=db.execute(sql)
    g.lists=map(objToDict,dao.fetchall())
    #显示数据库信息
    g.lists=map(client.getAppMysql,g.lists)
    dao.close()
    
    dao=db.execute("select * from paas_account where id = %d limit 1"%(session['user']))
    g.user=objToDict(dao.first())
    dao.close()
    
    return render_template("user/index.html")
    
@app.route("/api")
@checkUser
def api():
    "Ajax Api"
    g.apiHost=config.API_HOST
    
    sql="select paas_app.status,paas_app.id,paas_app.title,paas_app.language,paas_account.username from paas_app_token,paas_app,paas_account where paas_app.status != 4 AND paas_app.uid = paas_account.id AND  paas_app_token.aid=paas_app.id  AND paas_app.uid = %d order by paas_app.id desc"%(session['user'])
    dao=db.execute(sql)
    obj=map(objToDict,dao.fetchall())
    dao.close()
    
    return json.dumps(obj)

@app.route("/account",methods=['GET','POST'])
def account():
    "用户请登录"
    if request.method == "GET":
        return render_template("user/account.html")
    else:
        username=request.form.get("username",None)
        password=hashlib.md5(request.form.get("password",None)).hexdigest()
        sql="select * from paas_account where username = '%s' AND password = '%s' limit 1"%(sqlDeal(username),sqlDeal(password))
        dao=db.execute(sql)
        obj=dao.first()
        if obj != None:
            obj=objToDict(obj)
            session['user']=obj['id']
            r=True
        else:
            r=False
        dao.close()
        
        if r:
            return redirect("/user/")
        else:
            return redirect("/user/account")


@app.route("/exit")
def exitAccount():
    "用户退出"
    if session.has_key("user"):
        del session['user']
    return redirect("/user/account")
    
    
@app.route("/optionApp/<option>",methods=['POST'])
@checkUser        
def optionApp(option):
    "操作应用"
    aid=int(request.form.get("aid",None))
    
    #防止操作别人的应用
    sql="select count(*) from paas_app where uid = %d"%(session['user'])
    dao=db.execute(sql)
    r=objToDict(dao.first())
    dao.close()
    if r['count(*)']==0:
        return abort(403)
    
    if option == "start":
        #启动应用
        client.startApp(aid)
        return "ok"
    elif option == "stop":
        #停止应用
        client.stopApp(aid)
        return "ok"
    elif option == "reboot":
        #重启应用
        client.developApp(aid,"reboot")
        return "ok"
    elif option == "develop":
        #部署应用
        client.developApp(aid,"develop")
        return "ok"
