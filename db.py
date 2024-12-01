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

    conn = pymysql.connect (host="127.0.0.1", user=configInfo["id"], password=configInfo["password"],db="padNotify",charset="utf8")
    cur = conn.cursor()

def execute(sql):
    global conn,cur

    cur.execute(sql)
    conn.commit()

def fetchall():
    global conn, cur

    return cur.fetchall()

# Insert Data to notify 
def insertData(id,title, date, originText):
    global conn, cur

    if checkDup(id) == True:
        return False

    sql = "INSERT INTO notify (id, title,date,origin) VALUES (%d, '%s', '%s','%s')" %(id, title, date, originText)
    #print(sql)
    cur.execute(sql)
    conn.commit();

    return True

# Check item duplication. Find row with id, and If found, return True, and False
def checkDup(id):
    global conn, cur
    sql = "SELECT 1 FROM notify WHERE id=%d" % (id)
    cur.execute(sql)
    result = cur.fetchall()

    if len(result) > 0 :
        return True
    else:
        return False

# clear Notify table. remove all elements in this table.
def clearData():
    global conn, cur

    sql = "DELETE FROM notify"
    cur.execute(sql)
    conn.commit()

# close connection.
def close():
    global conn, cur
    cur.close()
    conn.close()


if __name__ == "__main__":
    init_db()
    #insertData(2,"3","2000-1-1","-")
    insertData(44982, '[극악] 칭호 배포 관련 안내', '2024-06-12','4498 [극악] 칭호 배포  관련 안내 2024-06-12')
