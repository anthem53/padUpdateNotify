import db
import crawling
import log

def execute():
    try :
        log.info("서비스 시작 전 설정 테스트 시작합니다.")
        db.dbTest()
        crawling.crawlTest()
        log.info("설정 정상 확인")
    except Exception:
        log.error("서비스 설정에 에러가 발생하였습니다.")
        raise Exception

if __name__ == "__main__":
    execute()

