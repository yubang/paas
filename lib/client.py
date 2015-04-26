#coding:UTF-8

"""
封装主机调用应用机的操作
2015-04-25
"""


import config,os
from lib.core import urlPostWithToken
from lib.webApp import buildMainServerConfig
from lib.app import getConfig
from lib.db import db,objToDict
import json


def buildApp(aid,appHost,language):
    "生成一个应用"
    #请求应用服务器生成应用
    num=0#暂时选用第一台服务器
    data={'language':language,'appHost':config.REMOTE_SERVER_PHP[num],'aid':str(aid)}
    result=urlPostWithToken(config.REMOTE_SERVER_PHP[num],"/servlet/buildApp",data)
    
    #在主服务器生成反向代理配置文件
    obj=json.loads(result)
    if obj['result'] == "ok":
        buildMainServerConfig(aid,appHost,obj['remoteSocket'])
        #把远程服务器地址写入数据库
        sql="update paas_app set remoteServer = '%s' ,remoteSocket = '%s' where id = %d"%(config.REMOTE_SERVER_PHP[num],obj['remoteSocket'],aid)
        return True
    else:
        return False
    

def startApp(aid):
    "启动app"
    
    #提取应用数据
    sql="select * from paas_app where id = %d limit 1"%(aid)
    dao=db.execute(sql)
    appData=objToDict(dao.first())
    dao.close()
    
    baseObj=json.loads(getConfig("config"))
    
    data=getConfig("mainServer")
    data=data.replace("{{ appHost }}",appData['host']).replace("{{ remoteSocket }}",appData['remoteSocket']).replace("{{ appId }}",str(aid)) 
    
    #main_作为前缀
    fp=open(baseObj['nginx']['confPath']+"/main_"+str(aid)+".conf","w")
    fp.write(data)
    fp.close()
    
    #修改状态
    sql="update paas_app set status = 1 where id =%d"%(aid)
    dao=db.execute(sql)
    dao.close()
    
    
def stopApp(aid):
    "停止app"
    baseObj=json.loads(getConfig("config"))
    path=baseObj['nginx']['confPath']+"/main_"+str(aid)+".conf"
    if os.path.exists(path):
        os.remove(path)
        
    #修改状态
    sql="update paas_app set status = 3 where id =%d"%(aid)
    dao=db.execute(sql)
    dao.close()
    
    
def developApp(aid,option):
    "部署应用，无论是不是第一次部署，主机不处理，逻辑交给应用服务器"
    #提取应用数据
    sql="select * from paas_app where id = %d limit 1"%(aid)
    dao=db.execute(sql)
    appData=objToDict(dao.first())
    dao.close()
    
    #部署过程走异步路线，所以只改变标志位
    data={'option':option,'language':appData['language'],'appHost':appData['remoteServer'],'aid':appData['id']}
    result=urlPostWithToken(appData['remoteServer'],"/servlet/developApp",data)
    
    #修改状态
    sql="update paas_app set status = 2 where id =%d"%(aid)
    dao=db.execute(sql)
    dao.close()
      
