from elements.map import Map
from elements.elements import *
from compiler.compiler import *

#todo: get the execution list
#todo: generar codigo de funciones
#todo: terminar value method

#fix: var and elements names cant be de same

class Code:
    def __init__(self) -> None:
        self.elements= dict()
        self.vars= dict()

        self.execution_list = list()
        self.compiled_list= list[pobj]

        self.map= Map()

    def compile(self, code: str):
        self.compiled_list= compile(code)
        for compiled in self.compiled_list:

            #ELEMENTS
            if compiled.type == 'element':
                self.add_element(compiled.subtype, **self.params(compiled))
            
            #VARS
            elif compiled.type == 'var':
                self.add_var(compiled.name, self.value(compiled.value))
            
            #FUNCTIONS
            elif compiled.type == 'function':
                if compiled.subtype == 'show':
                    print('>>',self.value(compiled.value))
                self.add_function(compiled)
            
            else:
                raise Exception('Error: unknown type')


    #todo: add conditions
    def value(self, obj: pobj):
        if type(obj) == pobj:
            
            if obj.type == 'expr':

                if obj.subtype == 'number':
                    return number(obj.value)
                
                #todo: add time
                if obj.subtype == 'time':
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
                    elif obj.value in self.map.mapelementsdict:
                        return self.map.mapelementsdict[obj.value]
                    else:
                        raise Exception(f'Name {obj.value} not found')
            
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
    
    def params(self, obj: pobj):
        params= dict()
        params['name']= obj.name
        for param in obj.params:
            val= self.value(param.value)
            if type(val) == str:
                if self.vars.get(val):
                    val= self.vars[val]
                elif self.elements.get(val):
                    val= self.elements[val]
            params[param.name]= val
        return params
    
    def conditions(self, obj):
        if (obj == number(0)).value or (obj == string('')).value or (obj == array([])).value or (obj == boolean(False)).value:
            return boolean(False)
        else:
            return boolean(True)
    
    def add_element(self, element: str, **kwargs):
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
        }
        if element in elements:
            elements[element](**kwargs)
        else:
            raise Exception('The element is not recognized')
    
    #todo: dynamic var type
    def add_var(self, name: str, value):
        '''
        Add a variable to the code
        :param name: the name of the variable
        :param value: the value of the variable
        '''
        self.vars[name]= value
    
    def add_function(self, obj: pobj):
        ...
    
    def same_type(self, a, b):
        return type(a) == type(b)
        
    
a= Code()
a.compile(
    '''
    province a(extension: 10, development: 20, population: 30)
    show(a)
    '''
)
print(a.map.mapelementsdict)
print(a.vars)

