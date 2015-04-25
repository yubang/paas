#coding:UTF-8

import sys,time

#引入上级模块
sys.path.append('../')
from lib import git
from lib.db import db,objToDict

def deal(obj):
    "处理业务"
    if obj['command'] == "clone":
        git.getCodeFromOsc(obj['aid'],obj['gitUrl'])
    elif obj['command'] == "pull":
        git.pullCode(obj['aid'])
    elif obj['command'] == "cp":
        git.getCodeFromLocation(obj['aid'])


def init():
    sql="select * from paas_gitQueue limit 1"
    dao=db.execute(sql)
    obj=dao.first()
    if obj != None:
        r=objToDict(obj)
        deal(r)
        sql="delete from paas_gitQueue where id = %d"%(r['id'])
        dao2=db.execute(sql)
        dao2.close()
    dao.close()
    
    
if __name__ == "__main__":
    while True:
        init()
        time.sleep(1)
