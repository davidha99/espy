from enum import Enum, auto

class Type_t(Enum):
    TYPE_BOOLEAN = auto()
    TYPE_CHAR = auto()
    TYPE_CTE_INT = auto()
    TYPE_CTE_FLOAT = auto()
    TYPE_BANNER = auto()
    TYPE_FUNCTION = auto()
    TYPE_LIST = auto()

class Type:
    def __init__(self):
        pass