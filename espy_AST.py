from enum import Enum, auto
from espy_types import *

class Declaration:
    def __init__(self, name : str, type, value, code, next) -> None:
        self.name = name
        self.type = type
        self.value = value
        self.code = code
        self.next = next

class Statement_t(Enum):
    STMT_DECL = auto()
    STMT_EXPR = auto()
    STMT_IF_ELSE = auto()
    STMT_DISPLAY = auto()
    STMT_ = auto()

class Statement:
    def __init__(self) -> None:
        pass
