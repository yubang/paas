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
    num=0
    data={'language':language,'appHost':config.REMOTE_SERVER_PHP[num],'aid':str(aid)}
    result=urlPostWithToken(config.REMOTE_SERVER_PHP[num],"/servlet/buildApp",data)
    
    #在主服务器生成反向代理配置文件
    obj=json.loads(result)
    if obj['result'] == "ok":
        buildMainServerConfig(aid,appHost,obj['remoteSocket'])
        return True
    else:
        return False
    
