#coding:UTF-8

"""
应用api
@author:yubang
"""

import config

def getConfig(name):
    "获取文件内容"
    fp=open(config.PAAS_PATH+"/data/"+name+".conf","r")
    data=fp.read()
    fp.close()
    return data
