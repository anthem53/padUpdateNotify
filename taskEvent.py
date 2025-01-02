import schedule
import threading
import time
import mail
import crawling_event
import db_event
import log
from datetime import date
import sys
import traceback

from customCode.event_code import EventResultCode, EventTaskResultCode , EventStatus

from model.event import Event


def notify_event_job(is_debug = False):
    try:
        log.info("퍼즐앤드래곤 이벤트 크롤링이 시작되었습니다.")
        db_event.init()
        
        # 기존 DB에 있는 event의 이름 목록 조회
        oldEventNameDateMap = db_event.selectEventNameDateList()

        # event 크롤링 
        crawledEventList = crawling_event.crawling(oldEventNameDateMap) 
        #crawledEventList = [['서비스 12주년 기념 스페셜 세트 판매!', 'https://pad.neocyon.com/W/event/view.aspx?id=2235', datetime.date(2024, 12, 16), datetime.date(2025, 1, 12)], ['대감사제! 앙케이트 슈퍼 갓 페스티벌 개최 결정!', 'None', 'None', 'None'], ['레어 에그 ~트리 카니발~', 'None', 'None', 'None'], ['그라비티 네오싸이언 설문조사', 'https://pad.neocyon.com/Poll.aspx?PollGroupSeq=206', None, None], ['겅호 콜라보 외전 캐릭터가 기간한정으로 등장!', 'None', 'None', 'None'], ['서비스 12주년 기념 이벤트!', 'None', 'None', 'None'], ['퍼즐앤드래곤 대감사제', 'None', 'None', 'None'], ['[마법석 100개+대감사제 세트 [12월]] 판매!', 'None', 'None', 'None'], ['[대감사제 스페셜 세트] 판매!', 'None', 'None', 'None']]
    
        # crawledEventList elemnet  [title , targetUrl , startDate, endDate ]
        # DB 검증시 존재 유무 확인 위함.
        crawledEventNameList = [elem[0] for elem  in crawledEventList]
        
        updateList = set()
        
        # 만약 새로운 놈들이라면 일단 DB 넣기
        for (name,link, startDate, endDate,updateDate,eventResultCode) in crawledEventList:
            if is_debug == True:
                print((name,link, startDate, endDate))
            if eventResultCode == EventResultCode.NEW:
                db_event.insertEvent(Event(name,link,EventStatus.DISABLE.value ,startDate, endDate,updateDate))
            elif eventResultCode == EventResultCode.UPDATE:
                db_event.updateEventDate(name,endDate,updateDate)
                updateList.add(name)
            else:
                pass
                
         #결과 반영할 것 
        #START = 0 , CLOSE = 1, NEED = 2, UPDATE= 3
        result = [[] for _ in range(len(EventTaskResultCode.__members__.items()))]

        # 업데이트된 DB 조회
        eventList = db_event.selectEventList()
        
        # 돌면서 이벤트 검증.
        for (name,link,status ,startDate, endDate,updateDate) in eventList:
            # 날짜 등록 x 시 result에 넣기. 그래도 status는 0로 유지.
            if startDate == None or endDate == None:
                result[EventTaskResultCode.NEED.value].append((name,link))
            # open인데 status = 1인 경우는 새로 추가된 경우. 따라서 넣기
            elif isOpenDate(startDate,endDate) == True and status == '0':
                result[EventTaskResultCode.START.value].append((name,link))
                db_event.updateEventStatus(name,"1")
            # status는 1인데 close는 이제 이벤트가 끝난거. 역시 통보
            elif isOpenDate(startDate,endDate) == False and status == '1':
                result[EventTaskResultCode.CLOSE.value].append((name,link))
                db_event.updateEventStatus(name,"0")
            elif isOpenDate(startDate,endDate) == False and status == '0':
                log.info("이벤트 '%s'는 홈페이지에 등록 되었으나, 아직 시작하지 않았습니다." % (name))
                pass
            else :
                pass
            
            if name in updateList :
                result[EventTaskResultCode.UPDATE.value].append((name,link,startDate, endDate,updateDate))
            
            if name not in crawledEventNameList:
                db_event.deleteEvent(name)
                
        if isResultEmpty(result) == False:
            log.info("변동된 이벤트가 있어 메일 발송을 시작하였습니다.")
            mail.sendEmail(mail.generateEventMessage(result),"퍼즐앤드래곤 이벤트 일정 변경 알림")
            log.info("변동된 이벤트에 대한 메일 발송 완료하였습니다.")
        else : 
            log.info("변동된 이벤트가 없습니다.")
            
        if len(result[EventTaskResultCode.NEED.value]) > 0:
            writeNeedEvent(result[EventTaskResultCode.NEED.value])
        
        db_event.close()
        log.info("퍼즐앤드래곤 이벤트 크롤링 작업이 종료되었습니다.")
    except Exception as e:
        mail.sendEmail(mail.generateErrorMessageWithText(traceback.format_exc()),"퍼즐앤드래곤 이벤트 업데이트 감지 에러 발생")
        log.error("에러로 인해 메일이 전송되지 않았습니다.")
        log.write(traceback.format_exc())
        db_event.close()

def isResultEmpty(result):
    for subList in result:
        if len(subList) > 0:
            return False
    return True    

def isOpenDate(startDate,endDate):
    if (startDate == None or endDate == None):
        return False
    curDate= date.today()
    return startDate <= curDate and curDate <= endDate

def writeNeedEvent(needList):
    html_text = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page Title</title>
        </head>
        <body style="margin-left: 30vw; margin-top:5vw">
            <h1>%s</h1>\n""" % ("퍼즐앤드래곤 이벤트 크롤링 시간 : <br>"+log.currentTime())
    
    for name, link in needList:
        html_text += '''            <div><span>%s : </span>  <a href='%s'>링크</a></div>\n''' % (name,link)
        
    html_text += """
        </body>
        </html>
    """
    f = open("needEvent.html",'w',encoding='utf-8')
    print(html_text)
    f.write(html_text)
        
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
    
    if len(sys.argv) < 2:
        notify_event_job();
    else :
        notify_thread = getTaskJobThread()
        notify_thread.start()
    
