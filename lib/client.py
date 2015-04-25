#coding:UTF-8

"""
封装主机调用应用机的操作
2015-04-25
"""


import config
from lib.core import urlPostWithToken
from lib.webApp import buildMainServerConfig
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
    
    
