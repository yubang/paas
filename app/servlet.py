#coding:UTF-8


"""
应用部署模块
该模块只需实现单机应用维护，分布式实现在clinet模块分发
@author:yubang
2015-04-25
"""

from flask import Blueprint,request,session

app=Blueprint("servlet",__name__)


def buildApp():
    "创建应用"
    pass
    
def updateApp():
    "更新应用"
    pass
    
def deleteApp():
    "删除应用"
    pass
    
def rebootApp():
    "重启应用"
    pass
    
def startApp():
    "启动应用"
    pass

def stopApp():
    "停止应用"
    pass
    
def reBuildApp():
    "重构应用"
    pass
