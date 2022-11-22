from errors import EspyNameError

_global_environment  = None

class Parameter:
    def __init__(self):
        self.parameters = {}
    
    def set_new_parameter(self, name, memory_idx, value=None) -> None:
        self.parameters[name] = [memory_idx, value]
    
    def set_parameter_value(self, name, value) -> None:
        try:
            # Look for the paramater in the parameters dictionary {name: (memory_idx, value)}
            # Set the value of the parameter (memory_idx, value)
            self.parameters[name][1] = value
        except KeyError:
            raise EspyNameError("Parameter %s is not defined" % name)
    
    def parameter_lookup(self, name) -> int:
        try:
            # Look for the paramater in the parameters dictionary {name: (memory_idx, value)}
            # Return the information of the parameter [memory_idx, value]
            return self.parameters[name]
        except KeyError:
            raise EspyNameError("Parameter %s is not defined" % name)

class Symbol:

    # Name: name of the symbol
    # Memory_idx: memory index of the symbol when the symbol is a variable
    # Value: value of the symbol when the symbol is a variable
    # Label: label of the symbol when the symbol is a function
    # Parameters: dictionary of parameters of the symbol when the symbol is a function
    def __init__(self, name=None, memory_idx=None, value=None, label=None, params=None, size=None) -> None:
        self.name = name
        self.memory_idx = memory_idx 
        self.value = value
        self.label = label
        self.params = params
        self.size = size

class Environment:
    def __init__(self, name = None) -> None:
        self.environment = {} 
        self.name = name 
    
    def add_entry(self, name, symbol) -> None:
        self.environment[name] = symbol

class Environment_Stack:
    def __init__(self) -> None:
        self.stack = []

    def scope_enter(self, name = None) -> None:
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

    def scope_pop(self) -> Environment:
        '''
        Returns the topmost environment. Used to save global environment
        '''
        return self.stack.pop()

    def scope_level(self) -> int:
        '''
        Returns the number of environments in the current stack (this is helpful to know whether 
        we are at the global scope or not)
        '''
        return len(self.stack)

    def scope_bind(self, name, sym=None, memory_idx=None) -> None:
        '''
        Adds an entry to the topmost environment of the stack, mapping <name> to the symbol structure <sym>.
        '''
        if sym is None:
            sym = Symbol(name, memory_idx)
        topmost_scope = self.stack[-1]
        topmost_scope.add_entry(name, sym)

    def scope_lookup(self, name) -> Symbol:
        '''
        Searches the stack of environments from top to bottom, looking for the first entry that matches 
        <name> exactly. If no match is found, it returns null
        '''
        for scope in reversed(self.stack):
            if name in scope.environment.keys() and scope.environment[name].value is not None:
                return scope.environment[name]
        return None

    def scope_func_lookup(self, name) -> Symbol:
        '''
        Searches the stack of environments from top to bottom, looking for the first entry that matches function name
        exactly. If no match is found, it returns null
        '''
        for scope in reversed(self.stack):
            if name in scope.environment.keys():
                return scope.environment[name]
        return None

    def scope_lookup_current(self, name) -> Symbol:
        '''
        Works like scope lookup except that it only searches the topmost environment. This is used to determine 
        whether a symbol has already been defined in the current scope.
        '''
        topmost_scope = self.stack[-1]
        if name in topmost_scope.environment.keys():
            return topmost_scope.environment[name]
        return None

    def func_lookup_param(self, func_name, param_name):
        '''
        Search for the parameter of a given function
        '''
        # Search for the function symbol information in the stack of environments
        function = self.scope_func_lookup(func_name)
        
        # Create new Parameter object if the function has no parameters yet
        if function.params is None:
            return None
        else:
            return function.params.parameter_lookup(param_name)

    def get_len_all_parameters(self):
        '''
        Get all parameters of a given function
        '''
        total_params = 0
        topmost_scope = self.stack[-1]
        for func in topmost_scope.environment.values():
            if func.params is not None:
                total_params += len(func.params.parameters)
        return total_params

        

    def insert_environment(self, global_env):
        '''
        Function to insert global environment every parse running
        '''
        self.stack.append(global_env)
    
    def function_bind(self, func_name, label):
        '''
        Bind the symbol as a function in current environment
        '''
        symbol = Symbol(name=func_name, label=label, params=None)
        topmost_scope = self.stack[-1]
        topmost_scope.add_entry(func_name, symbol)
    
    def parameter_bind(self, func_name, param_name, memory_idx, value=None):
        '''
        Bind the symbol as a parameter of a given function
        '''
        # Search for the function symbol information in the stack of environments
        function = self.scope_lookup_current(func_name)
        
        # Create new Parameter object if the function has no parameters yet
        if function.params is None:
            function.params = Parameter()

        function.params.set_new_parameter(param_name, memory_idx, value)

#Singleton Class for global environment
class Global_Environment:
    @staticmethod
    def get_instance():
        global _global_environment
        if _global_environment is None:
            _global_environment = Environment()
        return _global_environment
    def set_instance(value):
        global _global_environment
        _global_environment = value

