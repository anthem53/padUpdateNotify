import pymysql


# Global DB variable
conn = None;
cur = None


#cur.execute("INSERT INTO  notify VALUES (1,'TESTTitle','2000-01-01','origin text')")

#conn.commit()


# Init db variable, conn and cur
def init_db():
    global conn, cur
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
        print("DB.execute  Exception")
        print(e)
    

def fetchall():
    global conn, cur

    return cur.fetchall()


# close connection.
def close():
    global conn, cur
    cur.close()
    conn.close()


if __name__ == "__main__":
    init_db()
    #insertData(2,"3","2000-1-1","-")
    close()
