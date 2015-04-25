#coding:UTF-8


"""
paas平台数据库模块
2014-04-24
@author:yubang
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

#mysql://用户名：密码@主机：端口/数据库?charset=UTF8
command="mysql://%s:%s@%s:%s/%s?charset=UTF8"%(config.MYSQL_USERNAME,config.MYSQL_PASSWORD,config.MYSQL_HOST,config.MYSQL_PORT,config.MYSQL_DB)
db=create_engine(command,echo=config.DEBUG)

Session = sessionmaker(bind=db)

def sqlDeal(text):
    "处理字段，防止sql注入"
    return text.replace("'","\\'").replace("\"","\\\"")

def objToDict(obj):
    "代理类转成字典"
    r=dict(obj.items())
    return r

