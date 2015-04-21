#coding:UTF-8

"""
一个封装服务器配置文件的类
@author:yubang
2015-04-20
"""


import json,os


"""
对外接口，生成php配置文件
@param aid 应用id
@param appHost 应用域名
@param appDocument 应用代码
@author:yubang
2015-04-21
"""
def buildPhpConfig(aid,appHost):
    "生成php配置文件，对外接口"
    baseObj=getBaseConfig()#获取配置文件
    
    #添加用户和用户组
    os.system("useradd -g %s %s"%(baseObj['base']['webGroup'],baseObj['base']['phpAppPrefix']+str(aid)))
    
    appSocketPath=baseObj['base']['appSocketPath']+"/"+str(aid)
    appDocument=baseObj['base']['allAppDocument']+"/"+str(aid)
    
    buildPhpFpmConfig(str(aid),appSocketPath)#生成php-fpm配置文件
    buildNginxPhpConfig(str(aid),appHost,appDocument,appSocketPath)#生成nginx映射文件
    
    #初始化应用
    buildWelcomeFile(str(aid))
    
    #平滑加载配置文件
    os.system(baseObj['nginx']['serviceReload'])
    os.system(baseObj['php-fpm']['serviceReload'])
    
    

"""
@author:yubang
2015-04-21
"""
def buildWelcomeFile(aid):
    "初始化应用目录"
    baseObj=getBaseConfig()#获取配置文件
    
    fp=open("data/index.html","r")
    html=fp.read()
    fp.close()
    
    try:
        os.makedirs(baseObj['base']['allAppDocument']+"/"+str(aid))
    except:
        pass
        
    fp=open(baseObj['base']['allAppDocument']+"/"+str(aid)+"/index.html","w")
    fp.write(html)
    fp.close()


"""
@author:yubang
2015-04-21
"""
def getBaseConfig():
    "获取基础数据"
    fp=open("data/config.conf","r")
    data=fp.read()
    fp.close()
    return json.loads(data)
    

"""
@param aid 应用id
@param appSocketPath socket位置
@author:yubang
2015-04-21
"""
def buildPhpFpmConfig(aid,appSocketPath):
    "动态生成php应用虚拟主机配置文件"
    fp=open("data/php-fpm.conf","r")
    data=fp.read()
    fp.close()
    
    baseObj=getBaseConfig()
    
    data=data.replace("{{ appId }}",aid)
    data=data.replace("{{ appSocketPath }}",appSocketPath)
    data=data.replace("{{ appPrefix }}",baseObj['base']['phpAppPrefix'])
    data=data.replace("{{ webGroup }}",baseObj['base']['webGroup'])
    
    fp=open(baseObj['php-fpm']['confPath']+"/"+aid+".conf","w")
    fp.write(data)
    fp.close()
    
    
"""
@param aid 应用id
@param appHost 应用域名
@param appDocument 应用路径
@param appSocketPath socket位置
@author:yubang
2015-04-21
"""
def buildNginxPhpConfig(aid,appHost,appDocument,appSocketPath):
    "动态生成nginx映射虚拟主机配置文件"
    fp=open("data/nginxPhp.conf","r")
    data=fp.read()
    fp.close()
    
    baseObj=getBaseConfig()
    
    data=data.replace("{{ appId }}",aid)
    data=data.replace("{{ appHost }}",appHost)
    data=data.replace("{{ appDocument }}",appDocument)
    data=data.replace("{{ appSocketPath }}",appSocketPath)
    
    fp=open(baseObj['nginx']['confPath']+"/"+aid+".conf","w")
    fp.write(data)
    fp.close()
