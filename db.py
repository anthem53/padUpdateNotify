import pymysql
import log

# Global DB variable
conn = None;
cur = None

# Init db variable, conn and cur
def init_db():
    global conn, cur
    log.currentTime()
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

def execute(sql,values=None):
    global conn,cur
    try :
        if (values == None):
            cur.execute(sql)
        else:
            cur.execute(sql,values)
        conn.commit()
    except Exception as e:
        log.info("DB.execute  Exception")
        log.write(e)
    

def fetchall():
    global conn, cur
    return cur.fetchall()


# close connection.
def close():
    global conn, cur
    log.info("DB connection이 종료됩니다.")
    try :
        cur.close()
        conn.close()
    except Exception as e:
        log.info("DB Connection이 이미 종료 되었습니다.")
        log.write(e)

if __name__ == "__main__":
    init_db()
    #insertData(2,"3","2000-1-1","-")
    close()
