#coding:UTF-8


"""
核心业务模块
@author:yubang
2014-04-24
"""

import config
import httplib

def urlPostWithToken(host,path,data):
    "封装带有token的post请求"
    data['token']=config.servletToken
    

