#coding:UTF-8

"""
封装数据库对象
2015-04-24
"""

from sqlalchemy import Table,MetaData,Column
from sqlalchemy.sql.sqltypes import TIMESTAMP,Integer,String
from sqlalchemy.orm import mapper
from lib.db import db

metaData=MetaData(db)
AppTable=Table('paas_app',metaData,
    Column('id',Integer,primary_key=True),
    Column('title',String(50)),
    Column('description',String(200)),
    Column('uid',Integer),
    Column('language',String(10)),
    Column('host',String(255)),
    Column('gitUrl',String(255)),
    Column('status',Integer),
    Column('remoteServer',String(255)),
    Column('remoteSocket',String(255)),
    Column('createTime',TIMESTAMP),
)

class AppModel(object):
    def __init__(self,title,description,uid,language,host,gitUrl,status):
        self.title=title
        self.description=description
        self.uid=uid
        self.language=language
        self.host=host
        self.gitUrl=gitUrl
        self.status=status
        self.remoteServer=""
        self.remoteSocket=""
    
mapper(AppModel,AppTable)
