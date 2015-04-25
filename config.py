#coding:UTF-8

"""
平台自身配置文件
@author:yubang
"""

DEBUG = True
SECRET_KEY = "root"

ADMIN_USERNAME = "root"
ADMIN_PASSWORD = "root"

#mysql服务器配置
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DB = "paas"

PAAS_PATH = "/path"

#远程服务器列表（ip）用于分布式部署应用
REMOTE_SERVER=[
    '127.0.0.1',
]

#服务器安全密钥
token="root"
