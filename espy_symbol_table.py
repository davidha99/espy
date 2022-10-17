from enum import Enum, auto
from espy_types import *

class Symbol_t(Enum):
    SYMBOL_LOCAL = auto()
    SYMBOL_PARAM = auto()
    SYMBOL_GLOBAL = auto() # este tal vez no se usa

class Symbol:
    def __init__(self, kind : Symbol_t, type : Type, name : str, which=0) -> None:
        self.kind = kind
        self.type = type
        self.name = name
        self.which = which

class Symbol_Table:
    def __init__(self, table_name) -> None:
        self.table_name = table_name
        self.symbol_table = {}

    def add_entry(self, kind, type, name):
        symbol = Symbol(kind, type, name)
        self.symbol_table[name] = symbol
    
    def add_entry(self, name, symbol):
        self.symbol_table[name] = symbol

class Stack_ST:
    def __init__(self) -> None:
        self.stack = []

    def scope_enter(self, name):
        '''
        Causes a new symbol table to be pushed on the top of the stack, representing a new scope
        '''
        new_table = Symbol_Table(table_name=name)
        self.stack.append(new_table)
        

    def scope_exit(self) -> None:
        '''
        Causes the topmost symbol table to be removed
        '''
        self.stack.pop()

    def scope_level(self):
        '''
        Returns the number of symbol tables in the current stack (this is helpful to know whether 
        we are at the global scope or not)
        '''
        return len(self.stack)

    def scope_bind(self, name, sym):
        '''
        Adds an entry to the topmost symbol table of the stack, mapping <name> to the symbol structure <sym>.
        '''
        topmost = self.stack[-1]
        topmost.add_entry(name, sym)
        self.stack[-1] = topmost

    def scope_lookup(self, name):
        '''
        Searches the stack of symbol tables from top to bottom, looking for the first entry that matches 
        <name> exactly. If no match is found, it returns null
        '''
        for table in reversed(self.stack):
            if name in table.keys():
                return table[name]
        return None

    def scope_lookup_current(self, name):
        '''
        Works like scope lookup except that it only searches the topmost table. This is used to determine 
        whether a symbol has already been defined in the current scope.
        '''
        topmost_table = self.stack[-1]
        if name in topmost_table.keys():
            return topmost_table[name]
        return None


