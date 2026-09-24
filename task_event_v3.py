import mail
import crawling_event_only
import db_event
import log
from datetime import date, datetime
import traceback
import telegram_notify as tn

from custom_code.event_code import EventResultCode, EventTaskResultCode , EventStatus
from model.event import Event


def notify_event_job(is_debug = False):
    try:
        log.info("퍼즐앤드래곤 이벤트 크롤링이 시작되었습니다.")
        db_event.init()
        
        # 크롤링해서 현황을 저장. 순수 데이터 존재 여부를 통해 추가/수정/삭제 결징 및 진행.
        add_set, update_set, delete_set = sync_crawl_event(is_debug)
        
        
        # 크롤링한 결과를 바탕으로 DB 다시 조회해서 각 이벤트별로 메일 발송 여부에 대한 최종 결과 산출
        result = classify_event(add_set, update_set, delete_set,is_debug)
            
        # 알림 결과에 따
        if is_result_empty(result) == False:
            log.info("변동된 이벤트가 있어 메일 발송을 시작하였습니다.")
            if is_debug == False:           
                mail.sendEmail(mail.generate_event_message(result),"퍼즐앤드래곤 이벤트 일정 변경 알림")
                tn.send(tn.generate_event_message(result))
                log.info("변동된 이벤트에 대한 메일 발송 완료하였습니다.")
            else:
                log.info("디버그 모드로 실행중이라 실제 메일 발송은 하지 않았습니다.")
                tn.send(tn.generate_event_message(result))
        else :
            tn.send(tn.generate_no_event_message("EVENT")) 
            log.info("변동된 이벤트가 없습니다.")
            
        db_event.close()
        log.info("퍼즐앤드래곤 이벤트 크롤링 작업이 종료되었습니다.")
    except Exception as e:
        if is_debug == False:
            mail.sendEmail(mail.generate_error_message_with_text(traceback.format_exc()),"퍼즐앤드래곤 이벤트 업데이트 감지 에러 발생")
            tn.send(tn.generate_error_message_with_text(traceback.format_exc()))
            log.error("에러로 인해 메일이 전송되지 않았습니다.")
        else: pass
        log.write(traceback.format_exc())
        db_event.close()

def sync_crawl_event(is_debug=False):
    # 기존 DB에 있는 event의 이름 목록 조회
    old_event_name_date_map = db_event.select_event_name_date_map(is_debug)
    
    # 제목에 정해놓은 단어가 있으면 크롤링 대상에서 제거 진행.
    exception_word_list = load_exception_word_config()
    
    # event 크롤링 
    crawled_event_list = crawling_event_only.crawling(exception_word_list) 
    #crawled_event_list = [['서비스 12주년 기념 스페셜 세트 판매!', 'https://pad.neocyon.com/W/event/view.aspx?id=2235', datetime.date(2024, 12, 16), datetime.date(2025, 1, 12)], ['대감사제! 앙케이트 슈퍼 갓 페스티벌 개최 결정!', 'None', 'None', 'None'], ['레어 에그 ~트리 카니발~', 'None', 'None', 'None'], ['그라비티 네오싸이언 설문조사', 'https://pad.neocyon.com/Poll.aspx?PollGroupSeq=206', None, None], ['겅호 콜라보 외전 캐릭터가 기간한정으로 등장!', 'None', 'None', 'None'], ['서비스 12주년 기념 이벤트!', 'None', 'None', 'None'], ['퍼즐앤드래곤 대감사제', 'None', 'None', 'None'], ['[마법석 100개+대감사제 세트 [12월]] 판매!', 'None', 'None', 'None'], ['[대감사제 스페셜 세트] 판매!', 'None', 'None', 'None']]


    # crawled_event_list elemnet  [title , targetUrl , start_date, end_date ]
    # DB 검증시 존재 유무 확인 위함.
    crawled_event_name_list = [elem[0] for elem  in crawled_event_list]
    # 업데이트 된 녀석들 정리
    add_set = set()
    update_set = set()
    delete_set = set()
    event_list = db_event.selectEventList(is_debug)
    event_name_set = set([name for name,link,status ,start_date, end_date,update_date in event_list])
    event_dict = dict()
    for event in event_list:
        name,link,status ,start_date, end_date,update_date = event;
        event_dict[name] = event
        
    # 돌면서 이벤트 검증.
    #for (name,link,status ,start_date, end_date,update_date) in eventList:
    # 만약 새로운 놈들이라면 일단 DB 넣기
    for crawled_event in crawled_event_list:
        name,link, start_date, end_date,update_date = crawled_event 
        crawled_event = tuple(crawled_event)
        if name not in event_name_set:
            add_set.add(crawled_event)
        else :
            old_name,old_link,old_status ,old_start_date, old_end_date,old_update_date = event_dict[name]
            if (update_date != old_update_date ) or (link != old_link) or (start_date != old_start_date) or (end_date != old_end_date) :
                update_set.add(crawled_event)
    for event in event_list :
        name,link,status ,start_date, end_date,update_date = event
        event = tuple(event)
        if name not in crawled_event_name_list:
            delete_set.add(event)
    
    # 없는거 제거        
    for event in delete_set:
        name,link,status ,start_date, end_date,update_date = event
        db_event.deleteEvent(name, is_debug);
    
    # 있는거 추가
    for added_event in add_set:
        name,link, start_date, end_date,update_date = added_event 
        event = Event(name=name,link=link,status=EventStatus.NOT_STARTED.value,startDate=start_date,endDate=end_date,updateDate=update_date);
        db_event.insertEvent(event,is_debug)
    # 다른거 업데이트 
    for updated_event in update_set:
        name,link, start_date, end_date,update_date = updated_event 
        db_event.update_event_v3(name=name, link=link, status=None, start_date=start_date, end_date=end_date,update_date=update_date, is_debug=is_debug)
        
    return add_set, update_set, delete_set

def classify_event(add_set, update_set, delete_set,is_debug):
    
    # added_event_name_set = set([name for name,link, start_date, end_date,update_date in add_set])
    updated_event_name_set = set([name for name,link, start_date, end_date,update_date in update_set])
    deleted_event_name_set = set([name for name,link, status, start_date, end_date,update_date in delete_set])

    result = [[] for _ in range(len(EventTaskResultCode.__members__.items()))]
    
    for name,link, status, start_date, end_date,update_date in delete_set:
        if status != EventStatus.CLOESED.value:
            result[EventTaskResultCode.CLOSE.value].append((name,link))
    
    # 업데이트된 DB 조회
    event_list = db_event.selectEventList(is_debug)
    # 돌면서 이벤트 검증.
    for (name,link,status ,start_date, end_date,update_date) in event_list:
        
        # 날짜 등록 x 시 result에 넣기. 그래도 status는 0로 유지.
        if start_date == None or end_date == None:
            result[EventTaskResultCode.NEED.value].append((name,link))
        elif name in updated_event_name_set :
            result[EventTaskResultCode.UPDATE.value].append((name,link,start_date, end_date,update_date))
        # 크롤링한 이벤트의 시작날짜, 종료날짜가 오늘인 경우. 시작, 종료 이벤트 둘다 진행 및 종료 처리.
        elif is_instant_event(start_date, end_date):
            result[EventTaskResultCode.START.value].append((name,link))
            result[EventTaskResultCode.CLOSE.value].append((name,link))
            db_event.update_event_v3(name=name, status=EventStatus.CLOESED.value,is_debug=is_debug)
        # open인데 status = 0인 경우는 새로 추가된 경우. 따라서 넣기
        elif is_open_date(start_date,end_date) == True and status == EventStatus.NOT_STARTED.value:
            result[EventTaskResultCode.START.value].append((name,link))
            db_event.update_event_v3(name=name, status=EventStatus.OPENED.value,is_debug=is_debug)
        # status는 1인데 close는 이제 이벤트가 끝난거. 역시 통보
        elif is_open_date(start_date,end_date) == False and status == EventStatus.OPENED.value:
            result[EventTaskResultCode.CLOSE.value].append((name,link))
            db_event.update_event_v3(name=name, status=EventStatus.CLOESED.value,is_debug=is_debug)
        elif is_open_date(start_date,end_date) == False and status == EventStatus.NOT_STARTED.value:
            result[EventTaskResultCode.NOT_YET.value].append((name,link))
            log.info("이벤트 '%s'는 홈페이지에 등록 되었으나, 아직 시작하지 않았습니다." % (name))
        else :
            pass
    return result

def find_event_result_code(crawled_event,event_name_date_map):
    name = crawled_event[0]
    publised_date = crawled_event[4]
    if name in event_name_date_map:
        if publised_date == event_name_date_map[name]:
            return EventResultCode.EXIST
        else : 
            return EventResultCode.UPDATE
    else :
        return EventResultCode.NEW

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
def is_open_date(start_date,end_date):
    if start_date == None or end_date == None:
        return False
    curDate= date.today()
    return start_date <= curDate and curDate < end_date

def is_close_date(end_date):
    if end_date == None:
        return False
    if (type(end_date) is str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    curDate= date.today()
    return curDate >= end_date


def is_instant_event(start_date,end_date):
    cur_date= date.today()
    return start_date == end_date and start_date == cur_date
    

if __name__ == '__main__':
    tn.start_telegram_loop()
    notify_event_job(True)
