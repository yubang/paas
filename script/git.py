#coding:UTF-8

import sys,time,os

#引入上级模块
sys.path.append('../')
from lib import git
from lib.db import db,objToDict

def deal(obj):
    "处理业务"
    if obj['command'] == "clone":
        result=git.getCodeFromOsc(obj['aid'],obj['gitUrl'])
        if not result:
            return False
    elif obj['command'] == "pull":
        git.pullCode(obj['aid'])
    elif obj['command'] == "cp":
        git.getCodeFromLocation(obj['aid'])
    
    #恢复应用权限
    os.system("chown -Rv %s:%s %s"%(obj['appAccount'],obj['appGroup'],obj['appPath']))
        
    return True


def init():
    sleepSign=True
    sql="select * from paas_gitQueue limit 1"
    dao=db.execute(sql)
    obj=dao.first()
    if obj != None:
        sleepSign=False
        r=objToDict(obj)
        optionResult=deal(r)
        
        if optionResult:
            if r['executeSql'] != '':
                #执行回调sql
                dao2=db.execute(r['executeSql'])
                dao2.close()
        else:
            #发布失败
            
            dao2=db.execute("update paas_app set status = 5 where id = %d"%(r['aid']))
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
        
