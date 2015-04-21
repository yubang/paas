#coding:UTF-8

"""
应用api
@author:yubang
"""

def getConfig(name):
    "获取文件内容"
    fp=open("data/"+name+".conf","r")
    data=fp.read()
    fp.close()
    return data
