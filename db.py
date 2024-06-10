import pymysql

conn = None;
conn = pymysql.connect (host="127.0.0.1", user="root", password="12345",db="padNotify",charset="utf8")

cur = conn.cursor()

#cur.execute("INSERT INTO  notify VALUES (1,'TESTTitle','2000-01-01','origin text')")

#conn.commit()

def init_db():
    global conn
    conn = pymysql.connect (host="127.0.0.1", user="root", password="12345",db="padNotify",charset="utf8")
    cur = conn.cursor()

def insertData(id,title, date, originText):
    global conn, cur

    if checkDup(id) == True:
        return False

    sql = "INSERT INTO notify VALUES (%d, %s, %s,%s)" %(id, title, date, originText)
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

#checkDup(1)
