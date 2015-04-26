#coding:UTF-8

"""
API模块，用于对外调用
2015-04-25
"""

from flask import Blueprint,request
from lib.db import db,sqlDeal,objToDict
from lib import client

app=Blueprint("api",__name__)


@app.route("/git/<apiKey>/<secretKey>",methods=['POST'])
def git(apiKey,secretKey):
    "用于git调用通知有新代码"
    sql="select aid from paas_app_token where apiKey = '%s' AND secretKey = '%s'"%(sqlDeal(apiKey),sqlDeal(secretKey))
    dao=db.execute(sql)
    r=objToDict(dao.first())
    dao.close()
    
    aid=r['aid']
    client.developApp(aid,'develop')
    
    return "ok"
