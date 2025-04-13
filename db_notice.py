import db
import log

def init():
    db.init_db(getConnName())
    
def close ():
    db.close(getConnName())

# 중복 되지 않은 항목만 추출
def getNewDatas(rawDatas):

    # 중복되지 않은 결과 저장용
    result = []

    for id, title , date, ori in rawDatas:
        # 순회후 중복되지 않은 경우 result에 추가
        if isExistNotify(id,title) == False:
            result.append((id,title,date,ori))
    
    # 반환
    return result

def insertRawDatas(rawDatas):
    log.info("Start Inserting Crawled data to DB")    
    
    for id, title, data, originText in rawDatas:
        insertData(id,title,data,originText)

    log.info("Complete Insert Data to DB")

# Insert Data to notify 
def insertData(id,title, date, originText):
    if isExistNotify(id,title) == True:
        return False

    sql = "INSERT INTO notify (id, title,date,origin) VALUES (%s, %s, %s,%s)"
    db.execute(getConnName(),sql,(id, title, date, originText))

    return True

# Check item duplication. Find row with id, and If found, return True, and False
# This function is not main. So If you want to use this function, use should init db and close yourself.
def isExistNotify(id, title):

    sql = "SELECT 1 FROM notify WHERE id=%s AND title=%s"
    db.execute(getConnName(),sql,(id,title))
    result = db.fetchall(getConnName())

    if len(result) > 0 :
        return True
    else:
        return False

# clear Notify table. remove all elements in this table.
def clearData():
    log.info("Delete All Notify Data")
    sql = "DELETE FROM notify"
    db.execute(getConnName(),sql)


def getConnName():
    return "Notice"

import crawling_notice
if __name__ == "__main__":
    init()
    
    db.close(getConnName())