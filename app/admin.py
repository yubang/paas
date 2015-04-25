#coding:UTF-8

"""
后台管理面板
@author:yubang
2015-04-21
"""

from flask import Blueprint,render_template,request,redirect,session,g
import config,time,hashlib
from lib.db import db,sqlDeal,objToDict,Session
from lib.models import AppModel

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
    
    sql="select paas_app.id,paas_app.gitUrl,paas_app.host,paas_app.remoteServer,paas_app.title,paas_app.description,paas_app.language,paas_account.username from paas_app left join paas_account on paas_app.uid = paas_account.id where paas_app.status != 4 order by paas_app.id desc"
    dao=db.execute(sql)
    g.lists=map(objToDict,dao.fetchall())
    dao.close()
    
    return render_template("admin/appManager.html")
    
    
@app.route("/userAdd",methods=['GET','POST'])  
def userAdd():
    "添加用户"
    if request.method == "GET":
        g.add=True
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
        g.add=False
        
        dao=db.execute("select * from paas_account where id = %s limit 1"%(sqlDeal(uid)))
        g.obj=objToDict(dao.fetchone())
        dao.close()
        return render_template("admin/userAdd.html")
    else:
        
        password=request.form.get("password",None)
        status=request.form.get("status",None)
        realname=request.form.get("realname",None)
        college=request.form.get("college",None)
        specialty=request.form.get("specialty",None)
        
        if password == "":
            args=map(sqlDeal,(status,realname,college,specialty,uid))
            sql="update paas_account set status = '%s',realname = '%s',college = '%s',specialty='%s' where id = %s"%tuple(args)
        else:
            #加密密码
            password=hashlib.md5(password).hexdigest()
            args=map(sqlDeal,(password,status,realname,college,specialty,uid))
            sql="update paas_account set password = '%s',status = '%s',realname = '%s',college = '%s',specialty='%s' where id = %s"%tuple(args)
            
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


@app.route("/addApp",methods=['GET','POST'])
def addApp():
    "添加应用"
    if request.method == "GET":
        g.add=True
        g.obj={}
        
        sql="select * from paas_account where status != 3"
        dao=db.execute(sql)
        g.users=map(objToDict,dao.fetchall())
        dao.close()
        
        return render_template("admin/addApp.html")
    else:
        uid=request.form.get("uid",None)
        title=request.form.get("title",None)
        description=request.form.get("description",None)
        language=request.form.get("language",None)
        host=request.form.get("host",None)
        gitUrl=request.form.get("gitUrl",None)
        #处理git地址，防止注入恶意代码
        gitUrl=gitUrl.replace(" ","")
        
        #添加应用信息
        session=Session()
        obj=AppModel(title,description,uid,language,host,gitUrl,-1)
        session.add(obj)
        session.commit()
        
        #为应用创建一个数据库
        
        
        return redirect("/admin/appManager")   
        
        
@app.route("/deleteApp")        
def deleteApp():
    "删除应用"
    uid=request.args.get("id",None)
    sql="update paas_app set status = 4 where id = "+sqlDeal(uid)
    dao=db.execute(sql)
    dao.close()
    return redirect("/admin/appManager")
    

@app.route("/editApp")    
def editApp():
    "编辑应用"
    aid=request.args.get("id",None)
    if request.method == "GET":
        g.add=False
        
        sql="select * from paas_app where id = %s limit 1"%(sqlDeal(aid))
        dao=db.execute(sql)
        g.obj=objToDict(dao.first())
        dao.close()
        
        sql="select * from paas_account where status != 3"
        dao=db.execute(sql)
        g.users=map(objToDict,dao.fetchall())
        dao.close()
        
        return render_template("admin/addApp.html")         
