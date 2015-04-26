#coding:UTF-8

"""
拉取代码模块
第一阶段兼容osc
@author:yubang
2015-04-21
"""


from lib import app
import json,os


def getCodeFromOsc(aid,gitUrl):
    "从osc上拉取代码"
    baseObj=json.loads(app.getConfig("config"))
    codePath=baseObj['base']['codePath']+"/"+str(aid)
    appPath=baseObj['base']['allAppDocument']
    
    if not os.path.exists(codePath):
        os.makedirs(codePath)
    
    os.system("rm -Rvf %s"%(codePath))
        
    out=os.popen("git clone %s %s"%(gitUrl,codePath))
    log=out.read()
    if log.find("Receiving objects: 100%") == -1:
        return False
    
    #迁移clone下来的代码
    getCodeFromLocation(aid)
    
    return True
    

def pullCode(aid):
    "更新代码仓库的代码"
    baseObj=json.loads(app.getConfig("config"))
    codePath=baseObj['base']['codePath']+"/"+str(aid)
    appPath=baseObj['base']['allAppDocument']
    os.system("cd %s"%(codePath))
    os.system("git pull")
    getCodeFromLocation(aid)


def getCodeFromLocation(aid):
    "从本地代码仓库拉取代码"
    baseObj=json.loads(app.getConfig("config"))
    codePath=baseObj['base']['codePath']+"/"+str(aid)
    appPath=baseObj['base']['allAppDocument']
    os.system("rm -Rvf %s"%(appPath+"/"+str(aid)))
    os.system("cp -Rfv %s %s"%(codePath,appPath))
    
    
def checkLocationCode(aid):
    "检测本地是否有克隆好的代码"
    baseObj=json.loads(app.getConfig("config"))
    codePath=baseObj['base']['codePath']+"/"+str(aid)
    if os.path.exists(codePath):
        return True
    else:
        return False
