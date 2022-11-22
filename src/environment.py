from errors import EspyNameError

'''
Environment.py
Descripción: Definición de clases y métodos usadas para la administración 
             y acceso de memoria en compilación
Autores: David Hernández    |   A01383543
         Bernardo García    |   A00570682
'''

# Variable global para el guardado de variables globales
_global_environment  = None

'''
    Clase: Parameter
    Descripción: Almacena los parametros de una función
    Atributos: parameters : Diccionario de listas[num, num]
'''
class Parameter:
    def __init__(self):
        self.parameters = {}
    
    def set_new_parameter(self, name, memory_idx, value=None) -> None:
        self.parameters[name] = [memory_idx, value]
    
    # Función para buscar y asignar el valor a un parámetro
    # Regresa: val
    def set_parameter_value(self, name, value) -> None:
        try:
            self.parameters[name][1] = value
        except KeyError:
            raise EspyNameError("Parameter %s is not defined" % name)
    
    # Función para buscar un parámetro
    # Regresa: parametro
    def parameter_lookup(self, name) -> int:
        try:
            return self.parameters[name]
        except KeyError:
            raise EspyNameError("Parameter %s is not defined" % name)

'''
    Clase: Symbol
    Descripción: Almacena los atributos de una variable
    Atributos: 
        - name : string
        - memory_idx : num
        - value : num, ID, list
        - label : string
        - parameters : Parameter
'''
class Symbol:
    def __init__(self, name=None, memory_idx=None, value=None, label=None, params=None, size=None) -> None:
        self.name = name
        self.memory_idx = memory_idx 
        self.value = value
        self.label = label
        self.params = params
        self.size = size

'''
    Clase: Environment
    Descripción: Almacena las variables declaradas de cada contexto (scope)
    Atributos: 
        - name : string
        - environment : Diccionario de Symbols
'''
class Environment:
    def __init__(self, name = None) -> None:
        self.environment = {} 
        self.name = name 
    
    def add_entry(self, name, symbol) -> None:
        self.environment[name] = symbol

'''
    Clase: Environment Stack
    Descripción: Almacena los distintos alcances (scopes) del programa
    Atributos: 
        - stack : Pila de Environments
'''
class Environment_Stack:
    def __init__(self) -> None:
        self.stack = []

    def scope_enter(self, name = None) -> None:
        '''
        Agregar un nuevo Environment a la pila
        '''
        new_environment = Environment(name)
        self.stack.append(new_environment)
        

    def scope_exit(self) -> None:
        '''
        Elimina el mas reciente Environment
        '''
        self.stack.pop()

    def scope_pop(self) -> Environment:
        '''
        Regresa y elimina el más reciente Environment
        '''
        return self.stack.pop()

    def scope_level(self) -> int:
        '''
        Regresa el numero de Environments de la pila
        '''
        return len(self.stack)

    def scope_bind(self, name, sym=None, memory_idx=None) -> None:
        '''
        Agrega un Symbol al Environment más reciente, asignando su nombre con la estructura
        '''
        if sym is None:
            sym = Symbol(name, memory_idx)
        topmost_scope = self.stack[-1]
        topmost_scope.add_entry(name, sym)

    def scope_lookup(self, name) -> Symbol:
        '''
        Busca de arriba hacia abajo de la pila por el Symbol con el mismo nombre <name>
        '''
        for scope in reversed(self.stack):
            if name in scope.environment.keys() and scope.environment[name].value is not None:
                return scope.environment[name]
        return None

    def scope_func_lookup(self, name) -> Symbol:
        '''
        Busca de arriba hacia abajo de la pila por Symbol con el mismo nombre <name>. Su implementación es
        relacionada a la busqueda de funciones (no guardan un valor (value)).
        '''
        for scope in reversed(self.stack):
            if name in scope.environment.keys():
                return scope.environment[name]
        return None

    def scope_lookup_current(self, name) -> Symbol:
        '''
        Busca el nombre de una variable dentro del Environment más reciente. Su implementación es relacionada
        a la búsqueda de Symbols ya definidos dentro del mismo Environment
        '''
        topmost_scope = self.stack[-1]
        if name in topmost_scope.environment.keys():
            return topmost_scope.environment[name]
        return None

    def func_lookup_param(self, func_name, param_name):
        '''
        Busca el parámetro de una función específica
        '''
        # Buscar el Symbol de la función con el nombre otorgado
        function = self.scope_func_lookup(func_name)
        
        # Regresa el parámetro que se busca. De no existir ninguno, regresa None.
        if function.params is None:
            return None
        else:
            return function.params.parameter_lookup(param_name)

    def get_len_all_parameters(self):
        '''
        Regresa el número de parametros totales que tiene la Environment más reciente
        '''
        total_params = 0
        topmost_scope = self.stack[-1]
        for func in topmost_scope.environment.values():
            if func.params is not None:
                total_params += len(func.params.parameters)
        return total_params        

    def insert_environment(self, global_env):
        '''
        Agrega un Environment ya existente al stack
        '''
        self.stack.append(global_env)
    
    def function_bind(self, func_name, label):
        '''
        Agrega una nueva funcion con su Symbol correspondiente al Environment más reciente
        '''
        symbol = Symbol(name=func_name, label=label, params=None)
        topmost_scope = self.stack[-1]
        topmost_scope.add_entry(func_name, symbol)
    
    def parameter_bind(self, func_name, param_name, memory_idx, value=None):
        '''
        Agrega un nuevo parametro al Symbol correspondiente
        '''
        # Buscar la información de la función en el último Environment
        function = self.scope_lookup_current(func_name)
        
        # Crear un nuevo parámetro si la función no tiene aún
        if function.params is None:
            function.params = Parameter()

        # Asignar valor de nuevo parámetro
        function.params.set_new_parameter(param_name, memory_idx, value)

'''
    Clase: Global Environment
    Descripción: Diseño Singleton para obtener la instancia global del contexto de variables globales
'''
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

