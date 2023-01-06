from elements.map import Map
from elements.compiler_objects import *
from elements.simulation_elements import *

from compiler.compiler import *
from simulation.simulation import *

#fix: None
#todo: generar codigo de funciones

#todo: params with param name
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
        inside_vars= {**{k:self.to_object(v) for k,v in vars.items()}}

        #Iterate over the compiled code
        for compiled in compiled_list:

            #ELEMENTS
            #Creates a new element
            #todo: verification of args
            if compiled.type == 'element':
                if compiled.subtype == 'map':
                    raise Exception('Error: map can not be created')

                if compiled.name not in self.vars and self.to_python(compiled.name) not in self.events:
                    element= self.to_python(compiled.subtype)
                    args= self.elements_params(compiled, inside_vars, inside)
                    elements={
                        'nation': self.map.add_nation,
                        'province': self.map.add_province,
                        'sea': self.map.add_sea,
                        'neutral': self.map.add_neutral,
                        'trait': self.map.add_trait,
                        'category': self.map.add_category,
                        'distribution': self.map.add_distribution,
                    }

                    if element in elements:
                        elements[element](*self.to_python_list(args))
                    else:
                        raise Exception('The element is not recognized')

                else:
                    raise Exception(f'Error: {compiled.name} is already used')
            

            #VARS
            #Create a new var. For inside_vars, the vars are created in the moment of the execution
            elif compiled.type == 'var':
                if compiled.subtype == 'element':
                    if compiled.get('op'):
                        if compiled.op == '++':
                            self.map.update(element=self.to_python(compiled.name), data={'add':{self.to_python(compiled.var): self.to_python(self.value(compiled.value, inside_vars, inside))}})
                        elif compiled.op == '--':
                            self.map.update(element=self.to_python(compiled.name), data={'delete':{self.to_python(compiled.var): self.to_python(self.value(compiled.value, inside_vars, inside))}})
                    else:    
                        self.map.update(element=self.to_python(compiled.name), data={'update':{self.to_python(compiled.var): self.to_python(self.value(compiled.value, inside_vars, inside))}})
                
                elif compiled.subtype == 'expr':
                    if self.to_python(compiled.name) not in self.elements and self.to_python(compiled.name) not in self.events:
                        if inside:
                            if self.vars.get(compiled.name):
                                self.vars[compiled.name]= self.value(compiled.value, inside_vars, inside)
                            else:
                                inside_vars[compiled.name]= self.value(compiled.value, inside_vars, inside)
                        else:
                            self.vars[compiled.name]= self.value(compiled.value, inside_vars, inside)
                    else:
                        raise Exception(f'Error: {compiled.name} is already used')
                
                else:
                    raise Exception('Error: the var type is not recognized')                
            

            #FUNCTIONS
            #Execute a function
            elif compiled.type == 'func':
                #todo: add functions

                #todo: show for class is str
                if compiled.subtype == 'show':
                    params= self.params(compiled, inside_vars, inside)
                    print('>>', *params)
                
                elif compiled.subtype == 'type':
                    params= self.params(compiled, inside_vars, inside)
                    if len(params) == 1:
                        return self.to_object(type(self.value(params[0])).__name__)
                    else:
                        raise Exception('Error: type() only accepts one parameter')
                
                elif compiled.subtype == 'pos':
                    params= self.params(compiled, inside_vars, inside)
                    if len(params) == 2:
                        if type(params[0]) == array:
                            if type(params[1]) == integer:
                                return self.to_object(params[0].value[params[1].value])
                            else:
                                raise Exception('Error: pos() only accepts integers as second parameter')
                        else:
                            raise Exception('Error: pos() only accepts lists as first parameter')
                    else:
                        raise Exception('Error: pos() only accepts two parameters')

                elif compiled.subtype == 'size':
                    params= self.params(compiled, inside_vars, inside)
                    if len(params) == 1:
                        if type(self.to_python(params[0])) == list:
                            return self.to_object(len(params[0]))
                        else:
                            raise Exception('Error: size() only accepts lists')
                    else:
                        raise Exception('Error: size() only accepts one parameter')
                
                
                elif compiled.subtype == 'simulate':
                    #todo: init events
                    params= self.params(compiled, inside_vars, inside)
                    if len(params) == 1:
                        if type(params[0]) == time:
                            sim= Simulate(self.map, Pqueue(self.map.event_list))
                            sim.simulate(self.to_python(params[0]))
                        else:
                            raise Exception('Error: simulate() only accepts time')
                    else:
                        raise Exception('Error: simulate() only accepts one parameter')
                
            
            #LOOPS
            #Execute a loop
            elif compiled.type == 'loop':

                if compiled.subtype == 'while':
                    while self.to_python(self.value(compiled.condition, inside_vars, inside)):
                        val= self.execute(compiled.script, vars= inside_vars, inside=inside+1)
                        if self.to_python(val) != None:
                            return val
                
                elif compiled.subtype == 'for':
                    if len(compiled.params) > 2 or len(compiled.params) < 1:
                        raise Exception('Error: for() only accepts two or one parameters')
                    
                    params= self.params(compiled, inside_vars, inside)
                    if len(params) == 2:
                        if type(self.value(params[0], inside_vars, inside)) != integer or type(self.value(params[1], inside_vars, inside)) != integer:
                            raise Exception('Error: for() only accepts integers as parameters')

                        for i in range(self.to_python(self.value(params[0], inside_vars, inside)), self.to_python(self.value(params[1], inside_vars, inside)) + 1):
                            val= self.execute(compiled.script, vars= {compiled.var: i, **inside_vars}, inside=inside+1)
                            if self.to_python(val) != None:
                                return val
                    else:
                        if type(self.value(params[0], inside_vars, inside)) != array:
                            raise Exception('Error: for() only accepts lists as parameter')

                        for i in self.to_python(self.value(params[0], inside_vars, inside)):
                            val= self.execute(compiled.script, vars= {compiled.var: i, **inside_vars}, inside=inside+1)
                            if self.to_python(val) != None:
                                return val
                
                elif compiled.subtype == 'if':
                    if self.to_python(self.value(compiled.condition, inside_vars, inside)):
                        val= self.execute(compiled.script, vars= inside_vars, inside=inside+1)
                        if self.to_python(val) != None:
                            return val
                
                elif compiled.subtype == 'if else':
                    if self.to_python(self.value(compiled.condition, inside_vars, inside)):
                        val= self.execute(compiled.script, vars= inside_vars, inside=inside+1)   
                    else:
                        val= self.execute(compiled.else_script, vars= inside_vars, inside=inside+1)
                    if self.to_python(val) != None:
                            return val
                
                else:
                    raise Exception('Error: unknown loop type')

            
            #FUNCTIONS
            #Creates a new function
            elif compiled.type == 'function':
                # self.add_function(compiled)
                if compiled.subtype == 'event':
                    if self.to_python(compiled.name) not in self.elements and compiled.name not in self.vars and compiled.name not in inside_vars:
                        self.map.add_event(*self.to_python_list(self.elements_params(compiled, inside_vars, inside)), execution= self.execute, code= compiled.script, args=self.extra_params(compiled.args))
                    else:
                        raise Exception(f'Error: {compiled.name} is already used')
                
                if compiled.subtype == 'distribution':
                    if self.to_python(compiled.name) not in self.elements and compiled.name not in self.vars and compiled.name not in inside_vars:
                        self.map.add_distribution(*self.to_python_list(self.elements_params(compiled, inside_vars, inside)), execution= self.execute, code= compiled.script, args=self.extra_params(compiled.args))
                    else:
                        raise Exception(f'Error: {compiled.name} is already used')
            
            #EXECUTION
            #Execute a event
            elif compiled.type == 'execution':
                if self.events.get(self.to_python(compiled.name)):
                    return self.events[self.to_python(compiled.name)].execute(*self.to_python_list(self.params(compiled, inside_vars, inside)))
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
                if obj.subtype == 'integer':
                    return integer(obj.value)
                
                elif obj.subtype == 'decimal':
                    return decimal(obj.value)
                
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

                    if obj.value == 'map':
                        return self.map
                    
                    elif inside and (obj.value in inside_vars):
                        return inside_vars[obj.value]

                    elif obj.value in self.vars:
                        return self.vars[obj.value]
                    
                    
                    elif obj.value in self.elements:
                        return self.elements[obj.value].name

                    else:
                        raise Exception(f'Name {obj.value} not found')

                elif obj.subtype == 'arrow':
                    if obj.get('params'):
                        return self.to_object(self.map.get_data(self.to_python(self.value(obj.name)), self.to_python(obj.var), self.to_python(self.params(obj))))
                    if obj.name == 'map':
                        return self.to_object(self.map.get_map_data(self.to_python(obj.var)))
                    else:
                        return self.to_object(self.map.get_data(self.to_python(self.value(obj.name)), self.to_python(obj.var)))
            

            elif obj.type == 'arithmetic':
                left= self.value(obj.left, inside_vars, inside)
                right= self.value(obj.right, inside_vars, inside)
                
                try:
                    if obj.subtype == '+':
                        return left + right
                    if obj.subtype == '*':
                        return left * right
                    if obj.subtype == '//':
                        return left // right
                    if obj.subtype == '/':
                        return left / right
                    if obj.subtype == '-':
                        return left - right
                    if obj.subtype == '%':
                        return left % right
                    if obj.subtype == '**':
                        return left**right
                except:
                    raise Exception(f'Error: {left.type} and {right.type} does not support "{obj.subtype}" operation')
            
            if obj.type == 'uarithmetic':
                try:
                    if obj.subtype == '+':
                        return + self.value(obj.value, inside_vars, inside)
                    if obj.subtype == '-':
                        return - self.value(obj.value, inside_vars, inside)
                except:
                    raise Exception(f'Error: {self.value(obj.value, inside_vars, inside).type} does not support "{obj.subtype}" unary operation')
            
            
            elif obj.type == 'condition':
                left= self.dynamic_conditions(self.value(obj.left, inside_vars, inside))
                right= self.dynamic_conditions(self.value(obj.right, inside_vars, inside))
                
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
        
        elif isinstance(obj, object):
            return obj
        
        elif obj in inside_vars:
            return inside_vars[obj]
        
        elif obj in self.vars:
            return self.vars[obj]

        elif self.elements.get(obj):
            return self.elements[obj]
        
        elif isinstance(obj, Map):
            return obj

        else:
            raise Exception('The object is not recognized')
    


    def to_python(self, obj: Element):
        '''
        Returns the real value of an object(the values for functions outside the code)
        :param obj: The object to get the real value
        :return The real value of the object
        '''
        if type(obj) == integer:
            return int(obj.val)
        
        elif type(obj) == float:
            return decimal(obj.val)
        
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
    

    def to_python_list(self, obj: list):
        '''
        Returns the real value of a list of objects
        :param obj: The list of objects to get the real value
        :return The real value of the list of objects
        '''
        return [self.to_python(value) for value in obj]
    
    
    def to_object(self, obj):
        '''
        Converts the real types to the code types
        :param obj: The object to convert
        :return The object converted
        '''
        if type(obj) == list:
            return array(obj)
        elif type(obj) == str:
            return string(obj)
        elif type(obj) == int:
            return integer(obj)
        elif type(obj) == float:
            return decimal(obj)
        elif type(obj) == bool:
            return boolean(obj)
        elif type(obj) == dict:
            return array([self.to_object(value) for _, value in obj.items()])
        elif isinstance(obj, object) or isinstance(obj, Element):
            return obj
        else:
            raise Exception(f'Error: The object {obj} is not recognized')


    def params(self, obj: pobj, inside_vars: dict={}, inside: int=0):
        params= []
        for param in obj.params:
            params.append(self.value(param.value, inside_vars, inside))
        return params
    
    def elements_params(self, obj: pobj, inside_vars: dict={}, inside: int=0):
        '''
        Returns the params of a function
        :param obj: The function
        :param inside_vars: The variables inside the function
        :param inside: The number of functions inside the function
        :return The params of the function
        '''
        params= []
        params.append(obj.name)
        params += self.params(obj, inside_vars, inside)
        return params


    def extra_params(self, extra: list):
        '''
        Returns the extra params of a function
        :param extra: The extra params of the function
        '''
        return [self.to_python(i.value) for i in extra]
        
    
    def dynamic_conditions(self, obj: Element):
        '''
        Do dynamic conditions
        :param obj: The object to do the conditions
        :return The object with the conditions
        '''
        if (obj == integer(0)).value or obj == decimal(0.0).value or (obj == string('')).value or (obj == array([])).value or (obj == boolean(False)).value:
            return boolean(False)
        else:
            return boolean(True)    
    
    
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
    category socialism()
    category capitalism()

    province Havana(100, 10, 10345)    
    province Mayabeque(236, 10, 204)
    province New_York(2056, 20, 103856)
    province California(341, 30, 402175)

    nation Cuba([Havana, Mayabeque], [socialism])
    nation USA([New_York, California], [capitalism])
    

    # event population_growth(expon, socialism, true, '', [])(){
    #     for(prov, map->provinces){
    #         prov->population: 
    #     }
    # }

    # simulate(10d)

    # nation Cuba([Mayabeque], [crazy])
    # Cuba->provinces: ++Havana
    # Cuba->provinces: --Mayabeque
    # show(Cuba->provinces)


    category socialism()
    # event fib(1, socialism, true, 'y', [])(n: number){
    #     if(n == 0){
    #         return 0
    #     }
    #     if(n ==1){
    #         return 1
    #     }
    #     else{
    #         return fib(n-1) + fib(n-2)
    #     }
    # }
    # show(fib(10))
    

    # event a (1, socialism, true, 'y', [])(n: number){
    #     show(n)
    # }
    # b= a(10)
    # c= 2+b

    '''
)
# print('map', a.elements)
# print('vars', a.vars)
# print('events', a.events)

