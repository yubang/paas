#coding:UTF-8

"""
后台管理面板
@author:yubang
2015-04-21
"""

from flask import Blueprint,render_template,request,redirect,session,g
import config,time,hashlib
from lib.db import db,sqlDeal,objToDict

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
  
    
@app.route("/account",methods=['GET','POST'])   
def account():
    "管理员登录"
    if request.method == "GET":
        return render_template("admin/account.html")
    else:
        username = request.form.get("username","")
        password = request.form.get("password","")
        
        if config.ADMIN_USERNAME == username and config.ADMIN_PASSWORD == password:
            session['admin']=time.time()
            
        return redirect("/admin")
        

@app.route("/userManager")        
def userManager():
    "用户管理面板"
    sql="select * from paas_account where status != 3 order by id desc"
    dao=db.execute(sql)
    g.lists=map(objToDict,dao.fetchall())
    dao.close()
    return render_template("admin/userManager.html")
    
    
@app.route("/appManager")        
def appManager():
    "应用管理面板"
    return render_template("admin/appManager.html")
    
    
@app.route("/userAdd",methods=['GET','POST'])  
def userAdd():
    if request.method == "GET":
        g.title=u"添加信息"
        g.obj={}
        return render_template("admin/userAdd.html")
    else:
        username=request.form.get("username",None)
        password=request.form.get("password",None)
        status=request.form.get("status",None)
        realname=request.form.get("realname",None)
        college=request.form.get("college",None)
        specialty=request.form.get("specialty",None)
        
        #加密密码
        password=hashlib.md5(password).hexdigest()
        
        #把用户写入数据库
        args=map(sqlDeal,(username,password,status,realname,college,specialty))
        
        sql="insert into paas_account(username,password,status,realname,college,specialty) values('%s','%s','%s','%s','%s','%s')"%tuple(args)
        dao=db.execute(sql)
        dao.close()
        
        return redirect("/admin/userManager") 
        
        
@app.route("/userMessage",methods=['GET','POST'])        
def userMessage():
    "修改用户信息"
    
    uid=request.args.get("id",None)
    
    if request.method == "GET":
        g.title=u"修改信息"
        
        dao=db.execute("select * from paas_account where id = %s limit 1"%(sqlDeal(uid)))
        g.obj=objToDict(dao.fetchone())
        dao.close()
        return render_template("admin/userAdd.html")
    else:
        
        username=request.form.get("username",None)
        password=request.form.get("password",None)
        status=request.form.get("status",None)
        realname=request.form.get("realname",None)
        college=request.form.get("college",None)
        specialty=request.form.get("specialty",None)
        
        if password == "":
            args=map(sqlDeal,(username,status,realname,college,specialty,uid))
            sql="update paas_account set username = '%s',status = '%s',realname = '%s',college = '%s',specialty='%s' where id = %s"%tuple(args)
        else:
            #加密密码
            password=hashlib.md5(password).hexdigest()
            args=map(sqlDeal,(username,password,status,realname,college,specialty,uid))
            sql="update paas_account set username = '%s',password = '%s',status = '%s',realname = '%s',college = '%s',specialty='%s' where id = %s"%tuple(args)
            
        #修改用户信息
        dao=db.execute(sql)
        dao.close()
        
        return redirect("/admin/userManager")
        
@app.route("/deleteUser")
def deleteUser():
    "删除用户"
    uid=request.args.get("id",None)
    sql="update paas_account set status = 3 where id = "+sqlDeal(uid)
    dao=db.execute(sql)
    dao.close()
    return redirect("/admin/userManager")
             
