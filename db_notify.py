import db
import log

# 중복 되지 않은 항목만 추출
def getNewDatas(rawDatas):

    # 중복되지 않은 결과 저장용
    result = []

    for id, title , date, ori in rawDatas:
        # 순회후 중복되지 않은 경우 result에 추가
        if isExistNotify(id) == False:
            result.append((id,title,date,ori))
    
    # 반환
    return result

def insertRawDatas(rawDatas):
    log.info("Start Inserting Crawled data to DB")    
    
    clearData()
    for id, title, data, originText in rawDatas:
        insertData(id,title,data,originText)

    log.info("Complete Insert Data to DB")

# Insert Data to notify 
def insertData(id,title, date, originText):
    if isExistNotify(id) == True:
        return False

    sql = "INSERT INTO notify (id, title,date,origin) VALUES (%d, '%s', '%s','%s')" %(id, title, date, originText)
    db.execute(sql)

    return True

# Check item duplication. Find row with id, and If found, return True, and False
# This function is not main. So If you want to use this function, use should init db and close yourself.
def isExistNotify(id):

    sql = "SELECT 1 FROM notify WHERE id=%d" % (id)
    db.execute(sql)
    result = db.fetchall()

    if len(result) > 0 :
        return True
    else:
        return False

# clear Notify table. remove all elements in this table.
def clearData():
    sql = "DELETE FROM notify"
    db.execute(sql)

