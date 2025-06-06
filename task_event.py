import mail
import crawling_event
import db_event
import log
from datetime import date
import traceback

from custom_code.event_code import EventResultCode, EventTaskResultCode , EventStatus
from model.event import Event


def notify_event_job(is_debug = False):
    try:
        log.info("퍼즐앤드래곤 이벤트 크롤링이 시작되었습니다.")
        db_event.init()
        
        # 기존 DB에 있는 event의 이름 목록 조회
        old_event_name_date_map = db_event.selectEventNameDateList(is_debug)
        
        exception_word_list = load_exception_word_config()
        
        # event 크롤링 
        crawled_event_list = crawling_event.crawling(old_event_name_date_map,exception_word_list) 
        #crawled_event_list = [['서비스 12주년 기념 스페셜 세트 판매!', 'https://pad.neocyon.com/W/event/view.aspx?id=2235', datetime.date(2024, 12, 16), datetime.date(2025, 1, 12)], ['대감사제! 앙케이트 슈퍼 갓 페스티벌 개최 결정!', 'None', 'None', 'None'], ['레어 에그 ~트리 카니발~', 'None', 'None', 'None'], ['그라비티 네오싸이언 설문조사', 'https://pad.neocyon.com/Poll.aspx?PollGroupSeq=206', None, None], ['겅호 콜라보 외전 캐릭터가 기간한정으로 등장!', 'None', 'None', 'None'], ['서비스 12주년 기념 이벤트!', 'None', 'None', 'None'], ['퍼즐앤드래곤 대감사제', 'None', 'None', 'None'], ['[마법석 100개+대감사제 세트 [12월]] 판매!', 'None', 'None', 'None'], ['[대감사제 스페셜 세트] 판매!', 'None', 'None', 'None']]
    
        # crawled_event_list elemnet  [title , targetUrl , start_date, end_date ]
        # DB 검증시 존재 유무 확인 위함.
        crawled_event_name_list = [elem[0] for elem  in crawled_event_list]
        
        updateList = set()
        
        # 만약 새로운 놈들이라면 일단 DB 넣기
        for (name,link, start_date, end_date,update_date,eventResultCode) in crawled_event_list:
            if is_debug == True:
                print((name,link, start_date, end_date))
            if eventResultCode == EventResultCode.NEW:
                db_event.insertEvent(Event(name,link,EventStatus.NOT_STARTED.value ,start_date, end_date,update_date),is_debug)
            elif eventResultCode == EventResultCode.UPDATE:
                db_event.update_event(name,link, end_date,update_date,is_debug)
                db_event.updateEventStatus(name,EventStatus.OPENED.value,is_debug)
                updateList.add(name)
            else:
                pass
                
         #결과 반영할 것 
        #START = 0 , CLOSE = 1, NEED = 2, UPDATE= 3
        result = [[] for _ in range(len(EventTaskResultCode.__members__.items()))]

        # 업데이트된 DB 조회
        eventList = db_event.selectEventList(is_debug)
        
        # 돌면서 이벤트 검증.
        for (name,link,status ,start_date, end_date,update_date) in eventList:
            # 날짜 등록 x 시 result에 넣기. 그래도 status는 0로 유지.
            if start_date == None or end_date == None:
                result[EventTaskResultCode.NEED.value].append((name,link))
            # DB에 있는데 크롤링 안되면 일단 종료된 것. 삭제와 동시에 종료 이벤트 진행.
            elif name not in crawled_event_name_list:
                db_event.deleteEvent(name,is_debug)
                result[EventTaskResultCode.CLOSE.value].append((name,link))
            # 크롤링한 이벤트의 시작날짜, 종료날짜가 오늘인 경우. 시작, 종료 이벤트 둘다 진행 및 종료 처리.
            elif is_instant_event(start_date, end_date):
                result[EventTaskResultCode.START.value].append((name,link))
                result[EventTaskResultCode.CLOSE.value].append((name,link))
                db_event.updateEventStatus(name,EventStatus.CLOESED.value,is_debug)
            # open인데 status = 0인 경우는 새로 추가된 경우. 따라서 넣기
            elif isOpenDate(start_date,end_date) == True and status == EventStatus.NOT_STARTED.value:
                result[EventTaskResultCode.START.value].append((name,link))
                db_event.updateEventStatus(name,EventStatus.OPENED.value,is_debug)
            # status는 1인데 close는 이제 이벤트가 끝난거. 역시 통보
            elif isOpenDate(start_date,end_date) == False and status == EventStatus.OPENED.value:
                result[EventTaskResultCode.CLOSE.value].append((name,link))
                db_event.updateEventStatus(name,EventStatus.CLOESED.value,is_debug)
            elif isOpenDate(start_date,end_date) == False and status == EventStatus.NOT_STARTED.value:
                log.info("이벤트 '%s'는 홈페이지에 등록 되었으나, 아직 시작하지 않았습니다." % (name))
                pass
            else :
                pass
            
            if name in updateList :
                result[EventTaskResultCode.UPDATE.value].append((name,link,start_date, end_date,update_date))
           
        
        if is_result_empty(result) == False:
            log.info("변동된 이벤트가 있어 메일 발송을 시작하였습니다.")
            if is_debug == False:           
                mail.sendEmail(mail.generate_event_message(result),"퍼즐앤드래곤 이벤트 일정 변경 알림")
                log.info("변동된 이벤트에 대한 메일 발송 완료하였습니다.")
            else:
                log.info("디버그 모드로 실행중이라 실제 메일 발송은 하지 않았습니다.")
        else : 
            log.info("변동된 이벤트가 없습니다.")
            
        db_event.close()
        log.info("퍼즐앤드래곤 이벤트 크롤링 작업이 종료되었습니다.")
    except Exception as e:
        if is_debug == False:
            mail.sendEmail(mail.generate_error_message_with_text(traceback.format_exc()),"퍼즐앤드래곤 이벤트 업데이트 감지 에러 발생")
            log.error("에러로 인해 메일이 전송되지 않았습니다.")
        else: pass
        log.write(traceback.format_exc())
        db_event.close()

def is_result_empty(result):
    for subList in result:
        if len(subList) > 0:
            return False
    return True    

def load_exception_word_config(isDebug = False):
    try :
        wordList = []
        f = open("exceptionWord.config","r", encoding='UTF8')
        while True:
            line = f.readline()
            for rawWord in line.split(",") :
                if rawWord.strip() != "":
                    wordList.append(rawWord.strip())
            if not line :
                break
        return wordList       
    except Exception as e:
        if isDebug == True:
            log.write(traceback.format_exc())
        else: pass
        return []
    

# start_date 포함 이후 시간이자 end_date 시간은 아닌 경우 까지만 판단
# end_date 포함 할 경우 끝나고 다음 날 알림이 오는데 좀 늦어서 end_date 날은 포함하지 않도록 설정.
def isOpenDate(start_date,end_date):
    if start_date == None or end_date == None:
        return False
    curDate= date.today()
    return start_date <= curDate and curDate < end_date


def is_instant_event(start_date,end_date):
    cur_date= date.today()
    return start_date == end_date and start_date == cur_date
    

if __name__ == '__main__':
    notify_event_job(True)
