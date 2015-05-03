#coding:UTF-8

"""
封装主机调用应用机的操作
2015-04-25
"""


import config,os
from lib.core import urlPostWithToken
from lib.webApp import buildMainServerConfig
from lib.app import getConfig,getFile
from lib.db import db,objToDict
import json


def buildApp(aid,appHost,language):
    "生成一个应用"
    #请求应用服务器生成应用
    
    #根据轮转算法选择服务器
    dao=db.execute("select count(*) from paas_app")
    r=objToDict(dao.first())
    dao.close()
    
    num=r['count(*)'] % len(config.REMOTE_SERVER_PHP)
    data={'language':language,'appHost':config.REMOTE_SERVER_PHP[num],'aid':str(aid)}
    result=urlPostWithToken(config.REMOTE_SERVER_PHP[num],"/servlet/buildApp",data)
    
    #在主服务器生成反向代理配置文件
    obj=json.loads(result)
    if obj['result'] == "ok":
        buildMainServerConfig(aid,appHost,obj['remoteSocket'])
        #把远程服务器地址写入数据库
        sql="update paas_app set remoteServer = '%s' ,remoteSocket = '%s' where id = %d"%(config.REMOTE_SERVER_PHP[num],obj['remoteSocket'],aid)
        dao=db.execute(sql)
        dao.close()
        
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
    #平滑重启服务器
    reloadServer()
    
    
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
    #平滑重启服务器
    reloadServer()
    
    
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


def reloadServer():
    "平滑重启服务器"
    baseObj=json.loads(getConfig("config"))
    os.system(baseObj['nginx']['serviceReload'])
    
    
def getAppMysql(obj):
    "获取应用的数据库信息"
    
    if obj['language'] == "static":
        return obj
    
    sql="select username as dbUsername,password as dbPassword,dbName,host as dbHost,port as dbPort from paas_db where aid = "+str(obj['id'])
    dao=db.execute(sql)
    lists=objToDict(dao.first())
    dao.close()
    
    for key in lists:
        obj[key]=lists[key]
    
    return obj


def getAppMessage(aid,language):
    "获取app用户和用户组，应用路径"
    baseObj=getBaseConfig()#获取配置文件
    
    if language == "php":
        appUser=baseObj['base']['phpAppPrefix']+str(aid)
    else:
        appUser=baseObj['base']['staticAppPrefix']+str(aid)
    appGroup=baseObj['base']['webGroup']
    appPath=baseObj['base']['allAppDocument']+"/"+str(aid)
    
    return appUser,appGroup,appPath
    
"""
@author:yubang
2015-04-21
"""
def getBaseConfig():
    "获取基础数据"
    data=getConfig("config")
    return json.loads(data)         
