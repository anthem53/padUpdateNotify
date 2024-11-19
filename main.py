import sys
import task
import atexit
import log

def endFunction():
    log.info("프로그램이 특정 이유로 종료 되었습니다.");

atexit.register(endFunction)

if __name__ == '__main__':
    if len(sys.argv) < 2: 
        task.notify_job();
    else :
        notify_thread = task.getTaskJobThread()
        notify_thread.start()

