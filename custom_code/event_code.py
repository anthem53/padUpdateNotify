from enum import Enum
class EventResultCode(Enum):
    NEW = 1
    UPDATE = 2
    EXIST = 3

# Event 최종적으로 분류했을때 각 분류한 리스트들의 Label enum
class EventTaskResultCode(Enum):
    START = 0
    CLOSE = 1
    NEED = 2
    UPDATE = 3 
    
class EventStatus(Enum):
    NOT_STARTED = "0"
    OPENED = "1"
    CLOESED = "2"
    
    