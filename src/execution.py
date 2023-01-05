from elements.map import Map
from elements.compiler_objects import *
from elements.simulation_elements import *

from compiler.compiler import *
from simulation.simulation import *

#todo: generar codigo de funciones

class Code:
    def __init__(self) -> None:
        self.map= Map()
        self.vars= dict()
    
    @property
    def elements(self):
        return self.map.all
    
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
        :param compiled_list: the compiled code
        :param vars: internal variables
        :param inside: the level of inside. To control the vars and recursion
        '''
        
        #Convert variables to the types used in the code
        inside_vars= {**self.real_vars_to_code(vars)}

        #Iterate over the compiled code
        for compiled in compiled_list:
            #ELEMENTS
            #Creates a new element
            if compiled.type == 'element':
                if compiled.name not in self.vars and self.real_value(compiled.name) not in self.events:
                    self.add_element(self.real_value(compiled.subtype), self.params(compiled, inside_vars, inside))
                else:
                    raise Exception(f'Error: {compiled.name} is already used')
            

            #VARS
            #Create a new var. For inside_vars, the vars are created in the moment of the execution
            elif compiled.type == 'var':
                if self.real_value(compiled.name) not in self.elements and self.real_value(compiled.name) not in self.events:
                    if inside:
                        if self.vars.get(compiled.name):
                            self.vars[compiled.name]= self.value(compiled.value, inside_vars, inside)
                        else:
                            inside_vars[compiled.name]= self.value(compiled.value, inside_vars, inside)
                    else:
                        self.vars[compiled.name]= self.value(compiled.value, inside_vars, inside)
                else:
                    raise Exception(f'Error: {compiled.name} is already used')


            #ELEMENT VARS
            #Updates a var of an element
            elif compiled.type == 'element var':
                if compiled.get('op'):
                    if compiled.op == '++':
                        self.map.update(element=self.real_value(compiled.name), data={'add':{self.real_value(compiled.var): self.real_value(self.value(compiled.value, inside_vars, inside))}})
                    elif compiled.op == '--':
                        self.map.update(element=self.real_value(compiled.name), data={'delete':{self.real_value(compiled.var): self.real_value(self.value(compiled.value, inside_vars, inside))}})
                else:    
                    self.map.update(element=self.real_value(compiled.name), data={'update':{self.real_value(compiled.var): self.real_value(self.value(compiled.value, inside_vars, inside))}})
            

            #todo: working here
            #FUNCTIONS
            #Execute a function
            elif compiled.type == 'func':
                #todo: add functions
                if compiled.subtype == 'show':
                    print('>>', *self.func_params(compiled, inside_vars, inside))
                
                if compiled.subtype == 'simulate':
                    #todo: init events
                    sim= Simulate(self.map, )
                    sim.simulate()
                
            
            #LOOPS
            #Execute a loop
            elif compiled.type == 'loop':

                if compiled.subtype == 'while':
                    while self.real_value(self.value(compiled.condition, inside_vars, inside)):
                        val= self.execute(compiled.script, vars= inside_vars, inside=inside+1)
                        if self.real_value(val) != None:
                            return val
                
                elif compiled.subtype == 'repeat':
                    for i in range(self.real_value(self.value(compiled.start, inside_vars, inside)), self.real_value(self.value(compiled.end, inside_vars, inside))):
                        val= self.execute(compiled.script, vars= {compiled.var: i, **inside_vars}, inside=inside+1)
                        if self.real_value(val) != None:
                            return val
                
                elif compiled.subtype == 'if':
                    if self.real_value(self.value(compiled.condition, inside_vars, inside)):
                        val= self.execute(compiled.script, vars= inside_vars, inside=inside+1)
                        if self.real_value(val) != None:
                            return val
                
                elif compiled.subtype == 'if else':
                    if self.real_value(self.value(compiled.condition, inside_vars, inside)):
                        val= self.execute(compiled.script, vars= inside_vars, inside=inside+1)   
                    else:
                        val= self.execute(compiled.else_script, vars= inside_vars, inside=inside+1)
                    if self.real_value(val) != None:
                            return val
                
                else:
                    raise Exception('Error: unknown loop type')

            
            #FUNCTIONS
            #Creates a new function
            elif compiled.type == 'function':
                # self.add_function(compiled)
                if compiled.subtype == 'event':
                    if self.real_value(compiled.name) not in self.elements and compiled.name not in self.vars:
                        self.map.add_event(*self.real_value_list(self.params(compiled, inside_vars, inside)), execution= self.execute, code= compiled.script, args=self.extra_params(compiled.args))
                    else:
                        raise Exception(f'Error: {compiled.name} is already used')
                
                if compiled.subtype == 'distribution':
                    if self.real_value(compiled.name) not in self.elements and compiled.name not in self.vars and compiled.name not in inside_vars:
                        self.map.add_distribution(*self.real_value_list(self.params(compiled, inside_vars, inside)), execution= self.execute, code= compiled.script, args=self.extra_params(compiled.args))
                    else:
                        raise Exception(f'Error: {compiled.name} is already used')
            
            #EXECUTION
            #Execute a event
            elif compiled.type == 'execution':
                if self.events.get(self.real_value(compiled.name)):
                    return self.events[self.real_value(compiled.name)].execute(*self.real_value_list(self.params(compiled, inside_vars, inside))[1:])
                else:
                    raise Exception(f'Error: event {compiled.name} does not exist')
            
            elif compiled.type == 'return':
                return self.value(compiled.value, inside_vars, inside)


            else:
                raise Exception('Error: unknown type')



    def value(self, obj: pobj, inside_vars: dict={}, inside: int=0):
        '''
        Converts the parser object to a code object. Do arithmetics, comparisons, get vars, etc.
        :param obj: the parser object
        :param inside_vars: the vars inside the function
        :param inside: the level of inside
        :return: the code object
        '''
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
                    return array([self.value(value, inside_vars, inside) for value in obj.value])

                elif obj.subtype == 'name':

                    if inside:
                        if obj.value in inside_vars:
                            return inside_vars[obj.value]
                    
                    elif obj.value in self.vars:
                        return self.vars[obj.value]

                    elif self.real_value(obj.value) in self.elements:
                        return self.elements[self.real_value(obj.value)].name

                    else:
                        raise Exception(f'Name {obj.value} not found')

                elif obj.subtype == 'arrow':
                    return self.real_to_code(self.map.get_data(self.real_value(obj.name), self.real_value(obj.var)))
            
            elif obj.type == 'arithmetic':
                left= self.value(obj.left, inside_vars, inside)
                right= self.value(obj.right, inside_vars, inside)
                
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
                        return + self.value(obj.value, inside_vars, inside)
                    if obj.subtype == '-':
                        return - self.value(obj.value, inside_vars, inside)
                except:
                    raise Exception(f'Error: {self.value(obj.value, inside_vars, inside).type} does not support "{obj.subtype}" unary operation')
            
            #todo
            elif obj.type == 'xarithmetic':
                ...
            
            elif obj.type == 'condition':
                left= self.conditions(self.value(obj.left, inside_vars, inside))
                right= self.conditions(self.value(obj.right, inside_vars, inside))
                
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
                left= self.value(obj.left, inside_vars, inside)
                right= self.value(obj.right, inside_vars, inside)

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
                    return ~self.value(obj.value, inside_vars, inside)
            
            elif obj.type == 'func' or obj.type == 'execution':
                return self.execute([obj], inside_vars, inside+1)

            
            else:
                raise Exception(f'Error: {obj.type} is not a valid type')
        else:
            raise Exception('The object is not recognized')
    


    def real_value(self, obj: Element):
        '''
        Returns the real value of an object(the values for functions outside the code)
        :param obj: The object to get the real value
        :return The real value of the object
        '''
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
        '''
        Returns the real value of a list of objects
        :param obj: The list of objects to get the real value
        :return The real value of the list of objects
        '''
        return [self.real_value(value) for value in obj]
    
    def real_vars_to_code(self, vars: dict):
        '''
        Converts the real types to the code types
        :param vars: The dict of variables
        :return The dict of values
        '''
        new_dict= {}
        for key in vars:
            if type(vars[key]) == list:
                new_dict[key] = array(vars[key])
            elif type(vars[key]) == str:
                new_dict[key] = string(vars[key])
            elif type(vars[key]) == int or type(vars[key]) == float:
                new_dict[key] = number(vars[key])
            elif type(vars[key]) == bool:
                new_dict[key] = boolean(vars[key])
            else:
                new_dict[key] = vars[key]
        return new_dict
    
    def real_to_code(self, obj):
        '''
        Converts the real types to the code types
        :param obj: The object to convert
        :return The object converted
        '''
        if type(obj) == list:
            return array(obj)
        elif type(obj) == str:
            return string(obj)
        elif type(obj) == int or type(obj) == float:
            return number(obj)
        elif type(obj) == bool:
            return boolean(obj)
        else:
            return obj

    def func_params(self, obj: pobj, inside_vars: dict={}, inside: int=0):
        params= []

        for param in obj.params:
            params.append(self.value(param.value, inside_vars, inside))
        return params
    
    def params(self, obj: pobj, inside_vars: dict={}, inside: int=0):
        '''
        Returns the params of a function
        :param obj: The function
        :param inside_vars: The variables inside the function
        :param inside: The number of functions inside the function
        :return The params of the function
        '''
        params= []
        params.append(obj.name)
        for param in obj.params:
            if param.get('value'):
                if param.subtype == 'exe param':
                    val= self.value(param.value, inside_vars, inside)
                if param.subtype == 'func param':
                    val= self.value(param.value, inside_vars, inside)
            params.append(val)
        return params


    def extra_params(self, extra: list):
        '''
        Returns the extra params of a function
        :param extra: The extra params of the function
        '''
        return [self.real_value(i.value) for i in extra]
        
    
    def conditions(self, obj: Element):
        '''
        Do dynamic conditions
        :param obj: The object to do the conditions
        :return The object with the conditions
        '''
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
    
    
    def same_type(self, a, b):
        '''
        Returns if the types of the objects are the same
        :param a: The first object
        :param b: The second object
        :return True if the types are the same, False if not
        '''
        return type(a) == type(b)
        
    
a= Code()
a.compile(
    '''

    province Havana(10, 20, 30)
    province Mayabeque(10, 20, 30)
    show(Havana->population)
    Havana->population: 20
    show(Havana->population)

    trait crazy()

    nation Cuba([Mayabeque], [crazy])
    Cuba->provinces: ++Havana
    Cuba->provinces: --Mayabeque
    show(Cuba->provinces)


    category socialism()
    event fib(1, socialism, true, 'y', [])(n: number){
        if(n == 0){
            return 0
        }
        if(n ==1){
            return 1
        }
        else{
            return fib(n-1) + fib(n-2)
        }
    }
    show(fib(10))
    

    '''
)
print('map', a.elements)
print('vars', a.vars)
print('events', a.events)

