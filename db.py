import pymysql

conn = None;
cur = None


#cur.execute("INSERT INTO  notify VALUES (1,'TESTTitle','2000-01-01','origin text')")

#conn.commit()

def init_db():
    global conn, cur
    conn = pymysql.connect (host="127.0.0.1", user="root", password="1234",db="padNotify",charset="utf8")
    cur = conn.cursor()

def insertData(id,title, date, originText):
    global conn, cur

    if checkDup(id) == True:
        return False

    sql = "INSERT INTO notify (id, title,date,origin) VALUES (%d, '%s', '%s','%s')" %(id, title, date, originText)
    print(sql)
    cur.execute(sql)
    conn.commit();

    return True

def checkDup(id):
    global conn, cur
    sql = "SELECT 1 FROM notify WHERE id=%d" % (id)
    cur.execute(sql)
    result = cur.fetchall()

    if len(result) > 0 :
        return True
    else:
        return False

def clearData():
    global conn, cur

    sql = "DELETE FROM notify"
    cur.execute(sql)
    conn.commit()

def close():
    global conn, cur
    cur.close()
    conn.close()


#checkDup(1)

if __name__ == "__main__":
    init_db()
    #insertData(2,"3","2000-1-1","-")
    insertData(44982, '[극악] 칭호 배포 관련 안내', '2024-06-12','4498 [극악] 칭호 배포  관련 안내 2024-06-12')
