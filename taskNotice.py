import schedule
import threading
import time
import mail
import crawling_notice
import db_notice
import log
import sys
import traceback

def notify_job(is_debug = False):
    try:
        log.info("공지 메일 발송 이벤트가 시작 되었습니다.")
        db_notice.init()
        rawDatas = crawling_notice.crawling(is_debug);
        newDatas = db_notice.getNewDatas(rawDatas)
        if (len(newDatas) > 0 ):
            db_notice.clearData()
            db_notice.insertRawDatas(rawDatas)
            log.info("DB 삽입 완료, 메일 전송 전 ")
            mail.sendEmail(mail.generateMessage(newDatas),'퍼즐앤드래곤 신규 업데이트')
            log.info("메일 발송 이벤트가 완료 되었습니다.")
        else:
            log.info("업데이트된 내용이 없어 메일발송하지 않았습니다.")
        db_notice.close()
    except Exception as e:
        #mail.sendEmail(mail.generateErrorMessageWithText(traceback.format_exc()),"퍼즐앤드래곤 공지 업데이트 감지 에러 발생")
        log.error("에러로 인해 메일이 전송되지 않았습니다.")
        log.write(traceback.format_exc())
        db_notice.close()


if __name__ == '__main__':
    notify_job();
    