#coding:UTF-8


"""
paas的数据库管理模块
@author:yubang
2014-04-24
"""


from lib.db import db


"""
@param dbName 数据库名称
@param username 用户名
@param password 密码
return 运行结果
"""
def buildDb(dbName,username,password):
    "新建一个数据库"
    try:
        #创建数据库
        sql="create database %s"%(dbName)
        dao=db.execute(sql)
        dao.close()
        #创建用户
        sql="CREATE USER %s IDENTIFIED BY '%s'"%(username,password)
        dao=db.execute(sql)
        dao.close()
        #用户授权
        sql="GRANT ALL ON %s.* TO %s"%(dbName,username)
        dao=db.execute(sql)
        dao.close()
        return True
    except:
        return False
        
        
