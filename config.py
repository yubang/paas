#coding:UTF-8

"""
平台自身配置文件
@author:yubang
"""

DEBUG = True
SECRET_KEY = "root"

#后台管理帐号
ADMIN_USERNAME = "root"
ADMIN_PASSWORD = "root"

#mysql服务器配置
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DB = "paas"

PAAS_PATH = "/home/yubang/project/paas"

#远程服务器列表（ip）用于分布式部署应用
REMOTE_SERVER_PHP=[
    '127.0.0.1',
]

#服务器安全密钥
clientToken="root"
servletToken="root"

#主服务域名
API_HOST="127.0.0.5"


#应用服务器端口
APP_SERVER_PORT=8080
