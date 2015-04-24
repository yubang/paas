#coding:UTF-8


"""
paas平台数据库模块
2014-04-24
@author:yubang
"""

from sqlalchemy import create_engine
import config

#mysql://用户名：密码@主机：端口/数据库?charset=UTF8
command="mysql://%s:%s@%s:%s/%s?charset=UTF8"%(config.MYSQL_USERNAME,config.MYSQL_PASSWORD,config.MYSQL_HOST,config.MYSQL_PORT,config.MYSQL_DB)
db=create_engine(command,echo=config.DEBUG)

