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
        
    os.system("git clone %s %s"%(gitUrl,codePath))
    
    #迁移clone下来的代码
    os.system("mv -fv %s %s"%(codePath,appPath))
    
