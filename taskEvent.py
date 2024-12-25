import schedule
import threading
import time
import mail
import crawling_event
import db_event
import db 
import log
from datetime import date
import sys


def notify_event_job(is_debug = False):
    START = 0
    CLOSE = 1
    NEED = 2
    try:
        log.info("퍼즐앤드래곤 이벤트 크롤링이 시작되었습니다.")
        db_event.init()
        
        # 기존 DB에 있는 event의 이름 목록 조회
        oldEventDateNameList = db_event.selectEventNameList()

        # event 크롤링 
        crawledEventList = crawling_event.crawling(oldEventDateNameList) 
        #crawledEventList = [['서비스 12주년 기념 스페셜 세트 판매!', 'https://pad.neocyon.com/W/event/view.aspx?id=2235', datetime.date(2024, 12, 16), datetime.date(2025, 1, 12)], ['대감사제! 앙케이트 슈퍼 갓 페스티벌 개최 결정!', 'None', 'None', 'None'], ['레어 에그 ~트리 카니발~', 'None', 'None', 'None'], ['그라비티 네오싸이언 설문조사', 'https://pad.neocyon.com/Poll.aspx?PollGroupSeq=206', None, None], ['겅호 콜라보 외전 캐릭터가 기간한정으로 등장!', 'None', 'None', 'None'], ['서비스 12주년 기념 이벤트!', 'None', 'None', 'None'], ['퍼즐앤드래곤 대감사제', 'None', 'None', 'None'], ['[마법석 100개+대감사제 세트 [12월]] 판매!', 'None', 'None', 'None'], ['[대감사제 스페셜 세트] 판매!', 'None', 'None', 'None']]
    
        # crawledEventList elemnet  [title , targetUrl , startDate, endDate ]
        crawledEventNameList = [elem[0] for elem  in crawledEventList]

        # 만약 새로운 놈들이라면 일단 DB 넣기
        for (name,link, startDate, endDate) in crawledEventList:
            if is_debug == True:
                print((name,link, startDate, endDate))
            if link != None:
                db_event.insertEvent((name,link,startDate,endDate,"0"))
                

        # 업데이트된 DB 조회
        eventDataNameList = db_event.selectEventList()

        #결과 반영할 것 
        #START = 0 , CLOSE = 1, NEED = 2
        result = [[],[],[]]

        # 돌면서 이벤트 검증.
        for (name,link,status ,startDate, endDate,updateDate) in eventDataNameList:
            # 날짜 등록 x 시 result에 넣기. 그래도 status는 1로 변경
            if startDate == None or endDate == None:
                result[NEED].append((name,link))
                db_event.updateEventStatus(name,"1")
            # open인데 status = 1인 경우는 새로 추가된 경우. 따라서 넣기
            elif isOpenDate(startDate,endDate) == True and status == '0':
                result[START].append((name,link))
                db_event.updateEventStatus(name,"1")
            # status는 1인데 close는 이제 이벤트가 끝난거. 역시 통보
            elif isOpenDate(startDate,endDate) == False and status == '1':
                result[CLOSE].append((name,link))
                db_event.updateEventStatus(name,"0")
            elif status == "0":
                pass
                #print("TEST")
                #result[CLOSE].append((name,link))
            else :
                #print("NoResult")
                pass
            
            if name not in crawledEventNameList:
                db_event.deleteEvent(name)
                
        if len(result[START]) > 0 or len(result[CLOSE]) > 0 or len(result[NEED]) > 0:
            log.info("변동된 이벤트가 있어 메일 발송을 시작하였습니다.")
            mail.sendEmail(mail.generateEventMessage(result),"퍼즐앤드래곤 이벤트 일정 변경 알림")
            log.info("변동된 이벤트에 대한 메일 발송 완료하였습니다.")
        else : 
            log.info("변동된 이벤트가 없습니다.")
            
        if len(result[NEED]) > 0:
            writeNeedEvent(result[NEED])
        
        db_event.close()
        log.info("퍼즐앤드래곤 이벤트 크롤링 작업이 종료되었습니다.")
    except Exception as e:
        mail.sendEmail(mail.generateErrorMessageWithText(str(e)),"퍼즐앤드래곤 업데이트 감지 시스템 에러 발생")
        log.error("에러로 인해 메일이 전송되지 않았습니다.")
        log.write(e)
        db_event.close()


def isOpenDate(startDate,endDate):
    if (startDate == None or endDate == None):
        return False
    curDate= date.today()
    return startDate <= curDate and curDate <= endDate

def isWillOpen(startDate):
    if (startDate == None):
        return False
    curDate= date.today()
    return curDate < startDate;

def writeNeedEvent(needList):
    f = open("needEvent.txt",'w',encoding='utf-8')
    f.write("크롤링 시간 : "+log.currentTime()+"\n\n")
    f.write("● 입력 필요한 이벤트리스트\n")
    for name, link in needList:
        f.write("\t - %s : %s\n" % (name,link))
        
def schedule_event_notify():
    log.info("이벤트 크롤링 스케줄이 시작되었습니다.")
    #schedule.every().day.at("18:30").do(notify_event_job)
    schedule.every(1).minutes.do(notify_event_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def getTaskJobThread():
    return threading.Thread(target=schedule_event_notify)

if __name__ == '__main__':
    writeNeedEvent([("test","www.naver.com"),("test2","www.daum.net")])
    quit()
    if len(sys.argv) < 2:
        notify_event_job();
    else :
        notify_thread = getTaskJobThread()
        notify_thread.start()
    
