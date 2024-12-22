import pymysql
import log


# Global DB variable
conn = None
cur = None
connMap = dict()

# Init db variable, conn and cur
def init_db(connName):
    global connMap
    
    if (connName in connMap):
        raise Exception("중복된 커넥션 이름이 존재합니다. Task의 connection 이름을 점검해주십시오.  " + connName)
    
    configInfo = dict()
    f= open("db.config",'r')

    while True:
        line = f.readline().strip()
        if line =="":
            break
        else:
            parsed = line.split("=")
            configInfo[parsed[0]] = parsed[1]

    conn = pymysql.connect (host=configInfo["host"], user=configInfo["id"], password=configInfo["password"],db="padNotify",charset="utf8")
    cur = conn.cursor()
    
    connMap[connName] = (conn,cur)

def execute(connName,sql,values=None):
    conn,cur = getConnInfo(connName)
    try :
        if (values == None):
            cur.execute(sql)
        else:
            cur.execute(sql,values)
        conn.commit()
    except Exception as e:
        log.info("DB.execute  Exception")
        log.write(e)
    

def fetchall(connName):
    conn,cur = getConnInfo(connName)
    return cur.fetchall()


# close connection.
def close(connName):
    log.info("DB connection이 종료됩니다. " + connName)
    try :
        conn,cur = getConnInfo(connName)
        del connMap[connName]
        cur.close()
        conn.close()
    except Exception as e:
        log.info("DB Connection이 이미 종료 되었습니다. " + connName)
        log.write(e)
        
def getConnInfo(connName):
    global connMap
    if connName in connMap :
        return connMap[connName]
    else :
        raise Exception("해당 커넥션은 초기화되지 않았습니다. "+ connName)
    

if __name__ == "__main__":
    init_db("test")
    #insertData(2,"3","2000-1-1","-")
    close("test")
