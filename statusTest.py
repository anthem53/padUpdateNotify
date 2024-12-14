import mail
import db
import crawling
import log

def execute():
    try :
        log.info("서비스 시작 전 설정 테스트 시작합니다.")
        dbTest()
        crawlTest()
        log.info("설정 정상 확인")
    except Exception:
        log.error("서비스 설정에 에러가 발생하였습니다.")
        raise Exception
        

def dbTest():
    log.info("DB 연결 테스트 시작 합니다.")
    try :
        db.init_db()
        db.close()
        log.info("DB 연결이 정상적입니다.")
    except Exception as e :
        log.error("DB가 연결 실패 하였습니다.")
        raise e

    
def crawlTest():
    log.info("Crawling 연결 테스트 시작 합니다.")
    try :
        crawling.init_driver()
        log.info("Crawling 연결이 정상적입니다.")
    except Exception as e :
        log.error("Crawling 연결 실패 하였습니다.")
        raise e   


if __name__ == "__main__":
    execute()

