#coding:UTF-8

"""
API模块，用于对外调用
2015-04-25
"""

from flask import Blueprint,request,jsonify
from lib.db import db,sqlDeal,objToDict
from lib import client

app=Blueprint("api",__name__)

def getAppFromToken(apiKey,secretKey):
    "获取应用信息"
    sql="select aid from paas_app_token where apiKey = '%s' AND secretKey = '%s'"%(sqlDeal(apiKey),sqlDeal(secretKey))
    dao=db.execute(sql)
    r=objToDict(dao.first())
    dao.close()
    return r
    

@app.route("/git/<apiKey>/<secretKey>",methods=['POST'])
def git(apiKey,secretKey):
    "用于git调用通知有新代码"
    
    r=getAppFromToken(apiKey,secretKey)
    
    aid=r['aid']
    client.developApp(aid,'develop')
    
    return "ok"
    

@app.route("/app/<apiKey>/<secretKey>",methods=['GET','POST'])    
def appMessage(apiKey,secretKey):
    "获取应用状态"
    
    r=getAppFromToken(apiKey,secretKey)
    sql="select * from paas_app where id = %d limit 1"%(r['aid'])
    dao=db.execute(sql)
    obj=objToDict(dao.first())
    dao.close()
    
    obj['createTime']=obj['createTime'].strftime("%Y-%m-%d")
    return jsonify(obj)
    
