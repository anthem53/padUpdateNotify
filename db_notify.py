import db
import crawling_impl

# 중복 되지 않은 항목만 추출
def getNewDatas():

    newDatas = crawling_impl.crawling()
    result = []

    db.init_db()
    for id, title , date, ori in newDatas:

        if db.checkDup(int(id)) == False:
            result.append((id,title,date,ori))
    db.close()

    return result



