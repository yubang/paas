#coding:UTF-8


"""
应用部署模块
该模块只需实现单机应用维护，分布式实现在clinet模块分发
@author:yubang
2015-04-25
"""

from flask import Blueprint,request,session,abort
from lib.webApp import buildServerConfig
from lib.db import db,objToDict,sqlDeal
from lib import git

from functools import wraps
import json,config


app=Blueprint("servlet",__name__)


def checkToken(fn):
    "检测调用者是否合法"
    @wraps(fn)
    def deal(*args,**kwds):
        token=request.form.get("token",None)
        if token == config.servletToken:
            return fn()
        else:
            return abort(404)    
    return deal

@app.route('/buildApp',methods=['POST'])
@checkToken
def buildApp():
    "创建应用"
    try:
        aid=request.form.get("aid",None)
        appHost=request.form.get("appHost",None)
        language=request.form.get("language",None)
        
        #确定应用端口号
        dao=db.execute("select count(*) from paas_app where remoteServer = '%s'"%(appHost))
        r=objToDict(dao.first())
        dao.close()
        appPort=10001+int(r['count(*)'])
        
        
        buildServerConfig(aid,appHost,appPort,language)
        return json.dumps({"result":"ok","remoteSocket":"http://"+appHost+":"+str(appPort)})
    except:
        return json.dumps({"result":"fail"})


@app.route("/developApp",methods=['POST'])    
def develop():
    "发布应用"
    
    #提取应用信息
    aid=int(request.form.get("aid",None))
    sql="select * from paas_app where id = %d limit 1"%(aid)
    dao=db.execute(sql)
    appData=objToDict(dao.first())
    dao.close()
    
    #把任务交给后台队列
    option=request.form.get("option",None)
    if option == "reboot":
        gitUrl=""
        command="cp"
    elif option == "develop":
        gitUrl=appData['gitUrl']
        if git.checkLocationCode(aid):
            command="pull"
        else:
            command="clone"
            
    executeSql="update paas_app set status = 1 where id = %d"%(aid)
    
    sql="insert into paas_gitQueue(aid,command,gitUrl,executeSql) values(%d,'%s','%s','%s')"%(aid,command,gitUrl,sqlDeal(executeSql))
    dao=db.execute(sql)
    dao.close()
    
    return "ok"
