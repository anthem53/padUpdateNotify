import db
import crawling
import log
import socket
import mail

def execute():
    try :
        log.info("서비스 시작 전 설정 테스트 시작합니다.")
        internetTest()
        db.dbTest()
        crawling.crawlTest()
        mail.sendTest()
        log.info("서비스 시작 전 설정 테스트 성공")
    except Exception:
        log.error("서비스 설정에 에러가 발생하였습니다.")
        raise Exception
    
def internetTest():
    ipaddress = socket.gethostbyname(socket.gethostname())
    try : 
        if ipaddress == '127.0.0.1':
            raise Exception("Disconnect Internet")
        else:
            log.info("인터넷이 정상적으로 연결 되었습니다.")
    except Exception :
        raise Exception


if __name__ == "__main__":
    execute()

