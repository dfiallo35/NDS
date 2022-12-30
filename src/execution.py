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
        self.compiled_list= list[obj]

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
                ...
            
            else:
                print(self.value(compiled))


    #todo: add conditions
    def value(self, object: obj):
        if type(object) == obj:

            #todo: add all arithmetics
            #todo: restrict arithmetics to numbers
            if object.type == 'arithmetic':
                left= self.value(object.left)
                right= self.value(object.right)

                if object.subtype == '+':
                    return left + right
                if object.subtype == '*':
                    return left * right
                if object.subtype == '/':
                    return left / right
                if object.subtype == '-':
                    return left - right
            
            if object.type == 'sarithmetic':
                if object.subtype == '+':
                    return + self.value(object.value)
                if object.subtype == '-':
                    return - self.value(object.value)
            
            elif object.type == 'xarithmetic':
                ...
            
            elif object.type == 'condition':
                left= self.conditions(self.value(object.left))
                right= self.conditions(self.value(object.right))

                if object.subtype == 'and':
                    return left and right
                if object.subtype == 'or':
                    return left or right
            
            elif object.type == 'comparation':
                left= self.value(object.left)
                right= self.value(object.right)

                if object.subtype == '==':
                    return left == right
                if object.subtype == '!=':
                    return left != right
                if object.subtype == '>':
                    print(left, right)
                    return left > right
                if object.subtype == '<':
                    return left < right
                if object.subtype == '>=':
                    return left >= right
                if object.subtype == '<=':
                    return left <= right

            
            elif object.type == 'scondition':
                if object.subtype == 'not':
                    return not self.conditions(self.value(object.value))
            
            elif object.type == 'expr':
                if object.subtype == 'list':
                    return [self.value(value) for value in object.value]
                else:
                    return self.value(object.value)
            
            elif object.get('name') and object.name in self.vars:
                return self.vars[object.name]
            
            elif object.get('name') and  object.name in self.map.mapelementsdict:
                return self.map.mapelementsdict[object.name]
            
            else:
                return object.value
        
        else:
            return object
    
    def params(self, object: obj):
        params= dict()
        params['name']= object.name
        for param in object.params:
            val= self.value(param.value)
            if type(val) == str:
                if self.vars.get(val):
                    val= self.vars[val]
                elif self.elements.get(val):
                    val= self.elements[val]
            params[param.name]= val
        return params
    
    def conditions(self, object):
        print(object)
        if type(object) == None or object == int(0) or object == str('') or object == list() or object == dict():
            return False
        else:
            return True
    
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
    
    def add_function(self):
        ...
        

    
    
a= Code()
a.compile(
    '''
    m= 2+2*4
    j= 4
    province a(extension: j, development: 20, population: 30)
    nation b(provinces: [a])
    a= 2 and 1
    '''
)
print(a.map.mapelementsdict)
print(a.vars)

