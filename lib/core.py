#coding:UTF-8


"""
核心业务模块
@author:yubang
2014-04-24
"""

import config
import httplib,urllib

def urlPostWithToken(host,path,data):
    "封装带有token的post请求"
    
    data['token']=config.servletToken
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"} 
    
    con=httplib.HTTPConnection(host,config.APP_SERVER_PORT)
    con.request("POST",path,urllib.urlencode(data),headers)
    response=con.getresponse()
    html=response.read()
    con.close()
    return html
    

