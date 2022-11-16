class Symbol:
    def __init__(self, name=None, memory_idx=None, value=None) -> None:
        self.name = name
        self.memory_idx = memory_idx
        self.value = value

class Environment:
    def __init__(self, name = None) -> None:
        self.environment = {}
        self.name = name

    # def add_entry(self, name, memory_idx):
    #     symbol = Symbol(name, memory_idx)
    #     self.environment[name] = symbol
    
    def add_entry(self, name, symbol):
        self.environment[name] = symbol

class Environment_Stack:
    def __init__(self) -> None:
        self.stack = []

    def scope_enter(self, name = None):
        '''
        Causes a new environment to be pushed on the top of the stack, representing a new scope
        '''
        new_environment = Environment(name)
        self.stack.append(new_environment)
        

    def scope_exit(self) -> None:
        '''
        Causes the topmost environment to be removed
        '''
        self.stack.pop()

    def scope_level(self):
        '''
        Returns the number of environments in the current stack (this is helpful to know whether 
        we are at the global scope or not)
        '''
        return len(self.stack)

    def scope_bind(self, name, sym=None, memory_idx=None):
        '''
        Adds an entry to the topmost environment of the stack, mapping <name> to the symbol structure <sym>.
        '''
        if sym is None:
            sym = Symbol(name, memory_idx)
        topmost_scope = self.stack[-1]
        topmost_scope.add_entry(name, sym)

    def scope_lookup(self, name):
        '''
        Searches the stack of environments from top to bottom, looking for the first entry that matches 
        <name> exactly. If no match is found, it returns null
        '''
        for scope in reversed(self.stack):
            if name in scope.environment.keys():
                return scope.environment[name]
        return None

    def scope_lookup_current(self, name):
        '''
        Works like scope lookup except that it only searches the topmost environment. This is used to determine 
        whether a symbol has already been defined in the current scope.
        '''
        topmost_scope = self.stack[-1]
        if name in topmost_scope.environment.keys():
            return topmost_scope.environment[name]
        return None


