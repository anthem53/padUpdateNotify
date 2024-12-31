from enum import Enum
class EventResultCode(Enum):
    NEW = 1
    UPDATE = 2
    EXIST = 3


class EventTaskResultCode(Enum):
    START = 0
    CLOSE = 1
    NEED = 2
    UPDATE = 3 