from elements.map import Map
from elements.elements import *
from compiler.compiler import *

#todo: generar codigo de funciones
#todo: elementos desconocidos no dan error

class Code:
    def __init__(self) -> None:
        self.map= Map()
        self.vars= dict()
    
    @property
    def elements(self):
        return self.map.mapelementsdict
    
    @property
    def events(self):
        return self.map.eventdict

    def compile(self, code: str):
        '''
        Compiles the code and then executes it
        :param code: the code to compile
        '''
        self.execute(compile(code), inside=0)
    
    def execute(self, compiled_list, vars: dict={}, inside: int=0):
        '''
        Execute the code
        '''
        #todo: and inside_vars to vars verification and 
        inside_vars= {}

        for compiled in compiled_list:
            
            #ELEMENTS
            #Creates a new element
            if compiled.type == 'element':
                if compiled.name not in self.vars and self.real_value(compiled.name) not in self.events:
                    self.add_element(compiled.subtype, self.params(compiled))
                else:
                    raise Exception(f'Error: {compiled.name} is already used')
            

            #VARS
            #Create a new var. For inside_vars, it is only created if it does not exist in vars
            elif compiled.type == 'var':
                if self.real_value(compiled.name) not in self.elements and self.real_value(compiled.name) not in self.events:
                    if inside:
                        if self.vars.get(compiled.name):
                            raise Exception(f'Error: {compiled.name} is already a var name')
                        else:
                            inside_vars[compiled.name]= self.value(compiled.value)
                    else:
                        self.vars[compiled.name]= self.value(compiled.value)
                else:
                    raise Exception(f'Error: {compiled.name} is already used')
            

            #ELEMENT VARS
            #Updates a var of an element
            elif compiled.type == 'element var':
                if self.real_value(compiled.name) in self.elements:

                    if self.elements[self.real_value(compiled.name)].data.get(self.real_value(compiled.var)):
                        self.elements[self.real_value(compiled.name)].data[self.real_value(compiled.var)] = self.real_value(self.value(compiled.value))
                    
                    else:
                        raise Exception(f'Error: var {compiled.var} does not exist in element {compiled.name}')
                
                else:
                    raise Exception(f'Error: {compiled.name} is not a element name')
            

            #FUNCTIONS
            #Execute a function
            elif compiled.type == 'func':
                #todo: add functions
                if compiled.subtype == 'show':
                    print('>>',self.value(compiled.value))
                self.add_function(compiled)
            

            #FUNCTIONS
            #Creates a new function
            elif compiled.type == 'function':
                if compiled.subtype == 'event':
                    if self.real_value(compiled.name) not in self.elements and compiled.name not in self.vars:
                        self.map.add_event(*self.real_value_list(self.params(compiled)), execution= self.execute, code= compiled.script)
                    else:
                        raise Exception(f'Error: {compiled.name} is already used')
            
            #EXECUTION
            #Execute a event
            elif compiled.type == 'execution':
                if self.events.get(self.real_value(compiled.name)):
                    self.events[self.real_value(compiled.name)].execute(*self.real_value_list(self.params(compiled)))
                else:
                    raise Exception(f'Error: event {compiled.name} does not exist')
            
            else:
                raise Exception('Error: unknown type')



    def value(self, obj: pobj):
        if type(obj) == pobj:
            
            if obj.type == 'expr':
                if obj.subtype == 'number':
                    return number(obj.value)
                
                elif obj.subtype == 'time':
                    return time(int(obj.value[:-1]), obj.value[-1])

                elif obj.subtype == 'string':
                    return string(obj.value)

                elif obj.subtype == 'bool':
                    if obj.value == 'true':
                        return boolean(True)
                    return boolean(False)

                elif obj.subtype == 'list':
                    return array([self.value(value) for value in obj.value])

                elif obj.subtype == 'name':
                    if obj.value in self.vars:
                        return self.vars[obj.value]
                    elif self.real_value(obj.value) in self.elements:
                        return self.elements[self.real_value(obj.value)]
                    else:
                        raise Exception(f'Name {obj.value} not found')

                elif obj.subtype == 'arrow':
                    if self.real_value(obj.name) in self.elements:
                        if self.elements[self.real_value(obj.name)].data.get(self.real_value(obj.var)):
                            return self.elements[obj.name].data[obj.var]
                        else:
                            raise Exception(f'Error: var {obj.var} does not exist in element {obj.name}')
                    else:
                        raise Exception(f'Error: {obj.name} is not a element name')
            
            elif obj.type == 'arithmetic':
                left= self.value(obj.left)
                right= self.value(obj.right)
                
                if self.same_type(left, right):
                    try:
                        if obj.subtype == '+':
                            return left + right
                        if obj.subtype == '*':
                            return left * right
                        if obj.subtype == '/':
                            return left / right
                        if obj.subtype == '-':
                            return left - right
                        if obj.subtype == '%':
                            return left % right
                        if obj.subtype == '**':
                            return left**right
                    except:
                        raise Exception(f'Error: {left.type} does not support "{obj.subtype}" operation')
                else:
                    raise Exception('Error: Cant do arithmetic with different types')
            
            if obj.type == 'uarithmetic':
                try:
                    if obj.subtype == '+':
                        return + self.value(obj.value)
                    if obj.subtype == '-':
                        return - self.value(obj.value)
                except:
                    raise Exception(f'Error: {self.value(obj.value).type} does not support "{obj.subtype}" unary operation')
            
            #todo
            elif obj.type == 'xarithmetic':
                ...
            
            elif obj.type == 'condition':
                left= self.conditions(self.value(obj.left))
                right= self.conditions(self.value(obj.right))
                
                try:
                    if obj.subtype == 'and':
                        return left & right
                    if obj.subtype == 'or':
                        return left | right
                    if obj.subtype == 'xor':
                        return left ^ right
                except:
                    raise Exception(f'Error: {left.type} does not support "{obj.subtype}" operation')
            
            elif obj.type == 'comparation':
                left= self.value(obj.left)
                right= self.value(obj.right)

                if self.same_type(left, right):
                    try:
                        if obj.subtype == '==':
                            return left == right
                        if obj.subtype == '!=':
                            return left != right
                        if obj.subtype == '>':
                            return left > right
                        if obj.subtype == '<':
                            return left < right
                        if obj.subtype == '>=':
                            return left >= right
                        if obj.subtype == '<=':
                            return left <= right
                    except:
                        raise Exception(f'Error: "{left.type}" does not support "{obj.subtype}" operation')
                else:
                    raise Exception(f'Error: "{obj.subtype}" not supported between instances of "{left.type}" and "{right.type}"')
            
            elif obj.type == 'scondition':
                if obj.subtype == 'not':
                    return ~self.value(obj.value)
            
            else:
                #check: an error can be raised here
                raise Exception(f'Error: ------------------')
                return obj.value
        else:
            raise Exception('The object is not recognized')
    
    def real_value(self, obj: Element):
        if type(obj) == number:
            try:
                return int(obj.val)
            except:
                return float(obj.val)
        
        elif type(obj) == time:
            return int(obj.days)

        elif type(obj) == string:
            return str(obj.val)

        elif type(obj) == boolean:
            return bool(obj.val)

        elif type(obj) == array:
            return list(obj.val)
        
        else:
            return obj
    
    def real_value_list(self, obj: list):
        return [self.real_value(value) for value in obj]

    
    def params(self, obj: pobj):
        #todo: params to list
        params= []
        params.append(obj.name)
        
        for param in obj.params:
            if param.get('value'):
                if param.subtype == 'exe param':
                    val= self.value(param.value)
                if param.subtype == 'func param':
                    val= self.value(param.value)
            params.append(val)
        return params

    
    
    def conditions(self, obj):
        if (obj == number(0)).value or (obj == string('')).value or (obj == array([])).value or (obj == boolean(False)).value:
            return boolean(False)
        else:
            return boolean(True)
    
    #todo: verification of args
    def add_element(self, element: str, args):
        '''
        Add an element to the map
        :param element: the element to add
        '''
        elements={
            'nation': self.map.add_nation,
            'province': self.map.add_province,
            'sea': self.map.add_sea,
            'neutral': self.map.add_neutral,
            'trait': self.map.add_trait,
            'category': self.map.add_category,
        }
        if element in elements:
            elements[element](*self.real_value_list(args))
        else:
            raise Exception('The element is not recognized')
    
    
    def add_function(self, obj: pobj):
        ...
    
    def same_type(self, a, b):
        return type(a) == type(b)
        
    
a= Code()
a.compile(
    '''
    event a(1, 'w', true, 'y', [])(){
        b=2
        show(b)
    }
    a()

    

    # province Havana(extension: 10, development: 20, population: 30)
    # show(Havana->extension)
    # Havana->extension: 20
    # show(Havana->extension)

    # a=1
    # event c(distribution: 1, category: 'a', enabled: true)(){
    #     b=2
    #     d=2
    #     show(a)
    #     # c(c: 2)
    # }

    # c(c:2)
    # a=2
    # event d(c: number, d: number){
    #     b=2
    #     d=2
    #     show(a)
    # }
    # d(c:2)
    '''
)
print('map', a.map.mapelementsdict)
print('vars', a.vars)
print('events', a.events)

