import telegram
from telegram.request import HTTPXRequest
from concurrent.futures import TimeoutError as FutureTimeoutError
from telegram.error import TimedOut, NetworkError
import configparser
import asyncio
import threading
import log
from custom_code.event_code import EventTaskResultCode

config = configparser.ConfigParser()
config.read("telegram.config")
token = config['information']["token"]
config_chat_id = config['information']["chat_id"]
bot = None
loop = None
loop_thread = None

def _loop_thread_target():
    global loop, bot
    asyncio.set_event_loop(loop)
    request = HTTPXRequest(
        connection_pool_size=5,
        connect_timeout=40.0,
        read_timeout=40.0,
        write_timeout=40.0,
        pool_timeout=10.0,
    )
    log.info("텔레그램 봇이 실행 되었습니다.")
    bot = telegram.Bot(token, request=request)
    loop.run_forever()
    # 여기까지 오면 루프 종료
    loop.close()

def start_telegram_loop():
    global loop, loop_thread
    loop = asyncio.new_event_loop()
    loop_thread = threading.Thread(target=_loop_thread_target,daemon=True)
    loop_thread.start()
    
def stop_telegram_loop():
    """프로그램 종료 시 호출"""
    global loop, loop_thread
    if loop is not None:
        loop.call_soon_threadsafe(loop.stop)
    if loop_thread is not None:
        loop_thread.join()


async def test():
    global bot
    await bot.send_message(chat_id=config_chat_id,text="Hello, Telegram!2")

async def send_async(message):
    global bot
    await bot.send_message(chat_id=config_chat_id,text=message)
    log.info("텔레그램 봇 채팅이 발송 되었습니다.")
    
def send(message):
    global loop 
    try : 
        if loop is None :
            raise RuntimeError("아직 텔레그램 Loop가 초기화 되지 않았습니다.")
        future = asyncio.run_coroutine_threadsafe(send_async(message), loop)
        return future.result(timeout=25)
    except FutureTimeoutError:
        log.error("텔레그램 전송 future 대기 시간 초과")
    except (TimedOut, NetworkError) as e:
        log.error(f"텔레그램 전송 실패: {e}")
    except Exception as e:
        log.error(e)
        return None;


def generate_notice_message(newDatas,title):
    
    result = "신규 업데이트 내용\n\n"
    
    # 신규 내용이 있는 경우 
    if len(newDatas) > 0 :
        # 해당 내용을 메일 내용에 추가
        for id, title , date, ori in newDatas:
            result = result + "%s %s %s\n" %(id, title, date)
    else : 
        result += "새로운 업데이트 내용이 없습니다."
    
    result += "\n\n\n 퍼즐앤드래곤 공식 홈페이지 사이트 : https://pad.neocyon.com/W/notice/list.aspx"
    
    return result

def  generate_event_message(result):
    msg = "일정이 변경된 이벤트 리스트\n\n\n"

    if len(result[EventTaskResultCode.START.value]) > 0 :
        msg += "● 새로 등록된 이벤트리스트\n"
        for name, link in result[EventTaskResultCode.START.value]:
            msg += "\t - %s : %s\n" % (name,link)
            
            
    if len(result[EventTaskResultCode.CLOSE.value]) > 0 :
        msg += "● 종료된 이벤트리스트\n"
        for name, link in result[EventTaskResultCode.CLOSE.value]:
            msg += "\t - %s : %s\n" % (name,link)
            
    if len(result[EventTaskResultCode.NEED.value]) > 0 :
        msg += "● 입력 필요한 이벤트리스트\n"
        for name, link in result[EventTaskResultCode.NEED.value]:
            msg += "\t - %s : %s\n" % (name,link)
    
    if (len(result[EventTaskResultCode.UPDATE.value]) > 0 ):
        msg += "● 내용이 업데이트 된 이벤트 리스트\n"
        for name,link, startDate, endDate,updateDate in result[EventTaskResultCode.UPDATE.value]:
            msg += "\t - [%s] 이벤트가 %s 에 업데이트 되었습니다.해당 이벤트 종료일은 %s 입니다. : %s\n" % (name,updateDate,endDate,link)
        
    msg += "\n\n\n 퍼즐앤드래곤 공식 홈페이지 이벤트 사이트 : https://pad.neocyon.com/W/event/list.aspx"    
    return msg

def generate_no_event_message(event:str) ->str:
    content = (
        f"별도 이벤트가 감지 되지 않아 메일은 발송하지 않았습니다."
        f""
        f"대상 이벤트 :  {event}\n\n"
    )    
    return content

def generate_error_message_with_text(errorText:str):
    content = "에러로 인해 업데이트 체크 시스템이 종료되었습니다. 확인 해주십시오.\n\n- 에러 내용\n\n"
    
    content += str(errorText)
    
    return content

if __name__ == '__main__':
    start_telegram_loop()  # init_bot과 같은 의미라면 이걸 호출
    newDatas = []
    msg = generate_notice_message(newDatas, '퍼즐앤드래곤 신규 업데이트')
    send(msg)
    
    
    # https://api.telegram.org/bot8600374599:AAEFxEkemzCQjlTADBDZsBwF7MZhN1aQwbk/getUpdates