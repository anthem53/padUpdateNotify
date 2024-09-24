import db
import crawling_impl

# 중복 되지 않은 항목만 추출
def getNewDatas():

    # 크롤링 한 데이터들
    newDatas = crawling_impl.crawling()

    # 중복되지 않은 결과 저장용
    result = []


    db.init_db()
    for id, title , date, ori in newDatas:
        # 순회후 중복되지 않은 경우 result에 추가
        if db.checkDup(int(id)) == False:
            result.append((id,title,date,ori))
    db.close()

    # 반환
    return result



