import time
import threading


def currentTime():
    return "["+ time.strftime("%Y-%m-%d %H:%M:%S") + "]"

def currentThread():
    return "["+threading.currentThread().getName()+"]"

def info(content):
    print(currentTime()  + currentThread()+ "[INFO] " + content)

def debug(content):
    print(currentTime() + currentThread()+ "[DEBUG] "  + content)

def error(content):
    print(currentTime() + currentThread()+ "[ERROR] "  + content)

def write(content):
    print(currentTime() , currentThread(), "[WRITE] ",currentThread(),content)


if __name__ == "__main__":
    debug("test")



