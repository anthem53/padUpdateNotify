import time


def currentTime():
    return "["+ time.strftime("%Y-%m-%d %H:%M:%S") + "] "

def info(content):
    print(currentTime() + "[INFO] " + content)

def debug(content):
    print(currentTime() + "[DEBUG] " + content)

def error(content):
    print(currentTime() + "[ERROR] " + content)

def write(content):
    print(currentTime() , content)




