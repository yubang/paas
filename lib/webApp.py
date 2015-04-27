#coding:UTF-8

"""
该模块用于建立虚拟主机
@author:yubang
2015-04-25
"""


from lib.app import getConfig
from lib.buildConfig import buildPhpConfig,buildStaticConfig
import os,json

"""
@param aid 应用id
@param appHost 应用域名
@param remoteSocket 需要方向代理到的远程服务器地址
@author:yubang
2015-04-25
"""
def buildMainServerConfig(aid,appHost,remoteSocket):
    "生成反响代理服务器配置文件"
    data=getConfig("mainServer")
    data=data.replace("{{ appHost }}",appHost).replace("{{ remoteSocket }}",remoteSocket).replace("{{ appId }}",str(aid))
    
    baseObj=json.loads(getConfig("config"))
    #main_作为前缀
    fp=open(baseObj['nginx']['confPath']+"/main_"+str(aid)+".conf","w")
    fp.write(data)
    fp.close()
    
    #平滑加载配置文件
    os.system(baseObj['nginx']['serviceReload'])


"""
@param aid 应用id
@param appHost 应用域名
@param appPort 应用端口
@param language 应用语言
@author:yubang
2015-04-25
"""
def buildServerConfig(aid,appHost,appPort,language):
    "动态生成容器与前端服务器配置文件"
    if language == "php":
        buildPhpConfig(aid,appHost,appPort)
    elif language == "static":
        buildStaticConfig(aid,appHost,appPort)  
