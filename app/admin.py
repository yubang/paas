#coding:UTF-8

"""
后台管理面板
2015-04-21
"""

from flask import Blueprint,render_template,request,redirect,session

app=Blueprint("admin",__name__)

def checkUser(fn):
    "检测管理员是否已经登录"
    def deal(*args,**kwds):
        if session.has_key("admin"):
            return fn()
        else:
            return redirect("/admin/account")
    return deal
    
    
@app.route("/")
@checkUser
def index():
    "主界面"
    return render_template("admin/index.html")
  
    
@app.route("/account")   
def account():
    "管理员登录"
    if request.method == "GET":
        return render_template("admin/account.html")
    else:
        return ""
