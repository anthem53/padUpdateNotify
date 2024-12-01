import schedule
import threading
import time
import mail
import crawling_event
import db_notify
import log


def notify_event_job(is_debug = False):
    try:
        log.info("퍼즐앤드래곤 이벤트 크롤링이 시작되었습니다.")
        rawEventDatas = crawling_event.crawling()
        print(rawEventDatas,sep="\n") 
        #TODO rawEventData와 DB 정보 비교해서 newEventDatas 확인. 
        if (len(newEventDatas) > 0) :
            #TODO 신규 이벤트 존재할 경우, 해당 이벤트가 진행중인지를 기간으로 확인후 진행 중인 경우 mail 항목에 넣기
            # DB에 넣기
            pass
        
        #TODO  DB 조회후 종료된 이벤트 확인
        # DB내 이벤트의 status를 참고. 해당 status가 open이면서  기간이 끝난 경우 한정
        # 해당 status가 close 라면 이벤트 확인에 스킵.
        
        
        log.info("퍼즐앤드래곤 이벤트 크롤링 작업이 종료되었습니다.")
    except Exception as e:
        mail.sendEmail(mail.generateErrorMessage())
        log.error("에러로 인해 메일이 전송되지 않았습니다.")
        log.write(e)
        
        
def schedule_notify():
    log.info("스케줄이 시작되었습니다.")
    schedule.every().day.at("19:00").do(notify_event_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def getTaskJobThread():
    return threading.Thread(target=schedule_notify)

if __name__ == '__main__':
    notify_event_job(True)
    '''
    if len(sys.argv) < 2:
        notify_job();
    else :
        notify_thread = threading.Thread(target=schedule_notify)
        notify_thread.start()
    '''
