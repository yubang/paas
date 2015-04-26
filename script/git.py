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
    sleepSign=True
    sql="select * from paas_gitQueue limit 1"
    dao=db.execute(sql)
    obj=dao.first()
    if obj != None:
        sleepSign=False
        r=objToDict(obj)
        deal(r)
        
        if r['executeSql'] != '':
            #执行回调sql
            dao2=db.execute(r['executeSql'])
            dao2.close()
        
        sql="delete from paas_gitQueue where id = %d"%(r['id'])
        dao2=db.execute(sql)
        dao2.close()
        
    dao.close()
    
    if sleepSign:
        print 'sleep 1s'
        time.sleep(1)
    
if __name__ == "__main__":
    while True:
        init()
        
