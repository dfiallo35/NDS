from elements.map import Map
from elements.compiler_objects import *
from elements.simulation_elements import *

from compiler.lexer import *
from compiler.parser import *
from compiler.parser_obj import *
from simulation.simulation import *
# from ia.expert_system.expert_system import *

import pandas as pd


class Code:
    def __init__(self):
        self.map= Map()
        self.vars= dict()

        self.plots= []
        self.dataframes= []
    
    @property
    def elements(self):
        return self.map.all
    
    @property
    def events(self):
        return self.map.events

    def compile(self, code: str):
        '''
        Compiles the code and then executes it
        :param code: the code to compile
        '''
        parsed_code= NDSParser().parse(NDSLexer().tokenize(code))
        self.semantic_check(parsed_code)
        self.execute(parsed_code, vars={}, inside=0)
    
    #fix
    def semantic_check(self, code):
        elements= {
            'nation': {'min':4},
            'sea': {'args':2},
            'trait': {'args':0},
            'category': {'args':0},
            'dec event': {'params':1, 'args':1},
            'sim event': {'args':4},
            # 'decision': 2,
            'distribution': {'min':1},
        }

        #fix
        funcs= {
            'type': {'args':1},
            'pos': {'args':2},
            'size': {'args':1},
            'simulate': {'args':1},
            'plot': {'args':3},
            'dataframe': {'args':2},
        }

        for line in code:
            if line.type == 'element':
                if elements.get(line.subtype):
                    if elements[line.subtype].get('min') and len(line.args) < elements[line.subtype]['min']:
                        el= elements[line.subtype]['min']
                        raise Exception(f'Error: The element {line.subtype} needs at least {el} parameters')

                    if elements[line.subtype].get('args') and len(line.args) != elements[line.subtype]['args']:
                        el= elements[line.subtype]['args']
                        raise Exception(f'Error: The element {line.subtype} needs {el} arguments')
                    
                    if elements[line.subtype].get('params') and len(line.params) != elements[line.subtype]['params']:
                        el= elements[line.subtype]['params']
                        raise Exception(f'Error: The element {line.subtype} needs {el} parameters')
            
            if line.type == 'func':                
                if funcs.get(line.subtype):
                    if funcs[line.subtype].get('min') and len(line.args) < funcs[line.subtype]['min']:
                        f= funcs[line.subtype]['min']
                        raise Exception(f'Error: The element {line.subtype} needs at least {f} parameters')

                    if funcs[line.subtype].get('args') and len(line.args) != funcs[line.subtype]['args']:
                        f= funcs[line.subtype]['args']
                        raise Exception(f'Error: The element {line.subtype} needs {f} arguments')
                    
                    if funcs[line.subtype].get('max') and len(line.params) > funcs[line.subtype]['max']:
                        f= funcs[line.subtype]['max']
                        raise Exception(f'Error: The element {line.subtype} accepts at most {f} parameters')
    


    def execute(self, code, vars: dict={}, inside: int=0):
        '''
        Execute the code
        :param code: the compiled code
        :param vars: internal variables
        :param inside: the level of inside. To control the vars and recursion
        '''
        
        #Convert variables to the types used in the code
        inside_vars= {**{k:self.to_object(v) for k,v in vars.items()}}

        #Iterate over the compiled code
        for line in code:

            #ELEMENTS
            if line.type == 'element':
                self.map.alredy_exist(self.to_python(line.name))

                if line.name in self.vars or line.name in inside_vars:
                    raise Exception(f'The element {line.name} already exist')

                elif line.subtype == 'dec event':
                    params= self.extra_params(line.params)
                    args, kwargs= self.args_names(line, inside_vars, inside)
                    if args:
                        self.map.add_decision_event(self.to_python(line.name), cat=args[0], execution=self.execute, code=line.script, params=params)
                    elif kwargs:
                        self.map.add_decision_event(self.to_python(line.name), cat=kwargs['cat'], execution=self.execute, code=line.script, params=params)
                
                elif line.subtype == 'function':
                    self.map.add_function(self.to_python(line.name), execution=self.execute, code=line.script, params=self.extra_params(line.params))

                elif line.subtype == 'sim event':
                    args, kwargs= self.args_names(line, inside_vars, inside)
                    args= self.to_python([line.name, *args])
                    kwargs= self.to_python({**kwargs, **{'execution': self.execute, 'code': line.script}})
                    self.map.add_simulation_event(*self.to_python(args), **self.to_python(kwargs))


                elif line.subtype == 'decision':
                    args, kwargs= self.args_names(line, inside_vars, inside)
                    args= self.to_python([line.name, *args])
                    kwargs= self.to_python({**kwargs, **{'execution': self.execute, 'cond': ParserObj(type='cond', cond=line.condition), 'params': self.extra_params(line.params)}})
                    self.map.add_decision(*self.to_python(args), **self.to_python(kwargs))


                else:
                    element= self.to_python(line.subtype)
                    args, kwargs= self.args_names(line, inside_vars, inside)
                    args= self.to_python([line.name, *args])
                    kwargs= self.to_python(kwargs)

                    elements={
                        'nation': self.map.add_nation,
                        'sea': self.map.add_sea,
                        'trait': self.map.add_trait,
                        'category': self.map.add_category,
                        'distribution': self.map.add_distribution,
                    }
                    if element in elements:
                        elements[element](*args, **kwargs)
                    else:
                        raise Exception('The element is not recognized')
            

            #VARS
            #Create a new var. For inside_vars, the vars are created in the moment of the execution
            elif line.type == 'var':
                if line.subtype == 'element':

                    if line.get('op'):
                        if line.op == '++':
                            self.map.update(element=self.to_python(self.value(line.name, inside_vars, inside)),
                                        data={'add':{self.to_python(line.var): self.to_python(self.value(line.value, inside_vars, inside))}})
                        
                        elif line.op == '--':
                            self.map.update(element=self.to_python(self.value(line.name, inside_vars, inside)),
                                        data={'delete':{self.to_python(line.var): self.to_python(self.value(line.value, inside_vars, inside))}})
                    
                    else:

                        self.map.update(element=self.to_python(self.value(line.name, inside_vars, inside)),
                                    data={'update':{self.to_python(line.var): self.to_python(self.value(line.value, inside_vars, inside))}})
                
                elif line.subtype == 'expr':
                    self.map.alredy_exist(self.to_python(line.name))

                    if inside:
                        if self.vars.get(line.name):
                            self.vars[line.name]= self.value(line.value, inside_vars, inside)
                        else:
                            inside_vars[line.name]= self.value(line.value, inside_vars, inside)
                    else:
                        self.vars[line.name]= self.value(line.value, inside_vars, inside)
                
                else:
                    raise Exception('Error: the var type is not recognized')                
            

            elif line.type == 'function':
                self.execute([line.value], inside_vars, inside+1)

            #FUNCTIONS
            #Execute a function
            elif line.type == 'func':

                if line.subtype == 'show':
                    params= self.args(line, inside_vars, inside)
                    print('>>', *params)


                elif line.subtype == 'type':
                    params= self.args(line, inside_vars, inside)
                    return self.to_object(type(self.value(params[0], inside_vars, inside)).__name__)    
                

                elif line.subtype == 'pos':
                    params= self.args(line, inside_vars, inside)
                    if not type(params[0]) == array:
                        raise Exception('Error: pos() only accepts lists as first parameter')
                    if not type(params[1]) == integer:
                        raise Exception('Error: pos() only accepts integers as second parameter')
                        
                    return self.to_object(params[0].value[params[1].value])  


                elif line.subtype == 'size':
                    params= self.args(line, inside_vars, inside)
                    if not type(self.to_python(params[0])) == list:
                        raise Exception('Error: size() only accepts lists')

                    return self.to_object(len(params[0]))
                        

                elif line.subtype == 'rvs':
                    args, kwargs= self.args_names(line, inside_vars, inside)
                    args= self.to_python(args)
                    kwargs= self.to_python(kwargs)
                    if not isinstance(args[0], Distribution) and not kwargs.get('dist'):
                        raise Exception('Error: rvs() only accepts distributions as first parameter')
                    else:
                        return self.to_object(Distribution.rvs(*args, **kwargs))
                
                elif line.subtype == 'irvs':
                    args, kwargs= self.args_names(line, inside_vars, inside)
                    args= self.to_python(args)
                    kwargs= self.to_python(kwargs)

                    if not isinstance(args[0], Distribution) and not kwargs.get('dist'):
                        raise Exception('Error: irvs() only accepts distributions as first parameter')
                    else:
                        return self.to_object(Distribution.irvs(*args, **kwargs))
                
                elif line.subtype == 'gen_dist':
                    ...
                
                
                elif line.subtype == 'simulate':
                    params= self.args(line, inside_vars, inside)
                    if not type(params[0]) == time:
                        raise Exception('Error: simulate() only accepts time')
                    sim= Simulate(self.map, Pqueue(self.map.event_enabled_list))
                    sim.simulate(self.to_python(params[0]))
                

                elif line.subtype == 'plot':
                    params= self.args(line, inside_vars, inside)
                    if self.to_python(params[2]) not in ['line', 'area', 'bar']:
                        raise Exception('Error: plot() only acept line, area or bar as third parameter')

                    if isinstance(params[0], Nation) and not isinstance(params[1], array):
                        if params[0].name not in self.elements:
                            raise Exception('Error: the element is not recognized')
                        self.map.get_data(self.to_python(params[0]), self.to_python(params[1]))
                        
                        self.plots.append(
                            (self.to_python(params[2]),
                            pd.DataFrame(
                                self.map.log.get_nation_data(self.to_python(params[0].name), self.to_python(params[1])),
                                columns=[self.to_python(params[1])]
                            )
                            )
                        )

                    elif isinstance(params[0], array) and not isinstance(params[1], array):
                        gn= []
                        columns= []

                        for nat in self.to_python(params[0]):
                            if isinstance(nat, Nation):
                                if nat.name not in self.elements:
                                    raise Exception('Error: the element is not recognized')
                                self.map.get_data(self.to_python(nat), self.to_python(params[1]))
                                
                                gn.append(self.map.log.get_nation_data(self.to_python(nat.name), self.to_python(params[1])))
                                columns.append(nat.name)
                        
                        self.plots.append(
                            (self.to_python(params[2]),
                            pd.DataFrame(
                                [list(i) for i in list(zip(*gn))],
                                columns=columns
                            )
                            )
                        )

                    elif not isinstance(params[0], array) and isinstance(params[1], array):
                        if params[0].name not in self.elements:
                            raise Exception('Error: the element is not recognized')
                        gn= []
                        columns= []

                        for data in self.to_python(params[1]):
                            self.map.get_data(self.to_python(params[0]), self.to_python(data))
                            
                            gn.append(self.map.log.get_nation_data(self.to_python(params[0].name), self.to_python(data)))
                            columns.append(self.to_python(data))
                        
                        self.plots.append(
                            (self.to_python(params[2]),
                            pd.DataFrame(
                                [list(i) for i in list(zip(*gn))],
                                columns=columns
                            )
                            )
                        )
                    
                    else:
                        raise Exception('Error: plot() only accepts nations or arrays as first and second parameters')

                
                elif line.subtype == 'dataframe':
                    params= self.args(line, inside_vars, inside)

                    if isinstance(params[0], Nation) and not isinstance(params[1], array):
                        if params[0].name not in self.elements:
                            raise Exception('Error: the element is not recognized')
                        self.map.get_data(self.to_python(params[0]), self.to_python(params[1]))
                        
                        self.dataframes.append(
                            pd.DataFrame(
                                self.map.log.get_nation_data(self.to_python(params[0].name), self.to_python(params[1])),
                                columns=[self.to_python(params[1])]
                            )
                        )

                    elif isinstance(params[0], array) and not isinstance(params[1], array):
                        gn= []
                        columns= []

                        for nat in self.to_python(params[0]):
                            if isinstance(nat, Nation):
                                if nat.name not in self.elements:
                                    raise Exception('Error: the element is not recognized')
                                self.map.get_data(self.to_python(nat), self.to_python(params[1]))
                                
                                gn.append(self.map.log.get_nation_data(self.to_python(nat.name), self.to_python(params[1])))
                                columns.append(nat.name)
                        
                        self.dataframes.append(
                            pd.DataFrame(
                                [list(i) for i in list(zip(*gn))],
                                columns=columns
                            )
                        )

                    elif not isinstance(params[0], array) and isinstance(params[1], array):
                        if params[0].name not in self.elements:
                            raise Exception('Error: the element is not recognized')
                        gn= []
                        columns= []

                        for data in self.to_python(params[1]):
                            self.map.get_data(self.to_python(params[0]), self.to_python(data))
                            
                            gn.append(self.map.log.get_nation_data(self.to_python(params[0].name), self.to_python(data)))
                            columns.append(self.to_python(data))
                        
                        self.dataframes.append(
                            pd.DataFrame(
                                [list(i) for i in list(zip(*gn))],
                                columns=columns
                            )
                        )
                    
                    else:
                        raise Exception('Error: dataframe() only accepts nations or arrays as first and second parameters')
                        
                
            
            #LOOPS
            #Execute a loop
            elif line.type == 'loop':
                if line.subtype == 'while':
                    while self.to_python(self.value(line.condition, inside_vars, inside)):
                        val= self.execute(line.script, vars= inside_vars, inside=inside+1)
                        if self.to_python(val) != None:
                            return val
                
                elif line.subtype == 'repeat':           
                    init= self.value(line.init, inside_vars, inside)
                    end= self.value(line.end, inside_vars, inside)
                    
                    if type(init) != integer or type(end) != integer:
                        raise Exception('Error: for() only accepts integers as parameters')

                    for i in range(self.to_python(init), self.to_python(end) + 1):
                        val= self.execute(line.script,
                                        vars= {line.var: i, **inside_vars},
                                        inside=inside+1)
                        if self.to_python(val) != None:
                            return val
                
                elif line.subtype == 'foreach':   
                    param= self.value(line.param)
                    if type(param) != array:
                        raise Exception('Error: for() only accepts lists as parameter')

                    for i in self.to_python(param):
                        val= self.execute(line.script,
                                        vars= {line.var: i, **inside_vars},
                                        inside=inside+1)
                        if self.to_python(val) != None:
                            return val

                else:
                    raise Exception('Error: unknown loop')
            
            
            elif line.type == 'conditional':
                if line.subtype == 'if':
                    if self.to_python(self.value(line.condition, inside_vars, inside)):
                        val= self.execute(line.script, vars= inside_vars, inside=inside+1)
                        if self.to_python(val) != None:
                            return val
                
                elif line.subtype == 'if else':
                    if self.to_python(self.value(line.condition, inside_vars, inside)):
                        val= self.execute(line.script, vars= inside_vars, inside=inside+1)   
                    else:
                        val= self.execute(line.else_script, vars= inside_vars, inside=inside+1)
                    if self.to_python(val) != None:
                            return val
                
                else:
                    raise Exception('Error: unknown conditional')
                
            

            #EXECUTION
            #Execute a event
            elif line.type == 'execution':
                if self.events.get(self.to_python(line.name)):
                    args, kwargs= self.args_names(line, inside_vars, inside)
                    args= self.to_python(args)
                    kwargs= self.to_python(kwargs)
                    ex= self.to_object(self.events[line.name].execute(*args, **kwargs))
                    if self.to_python(ex) != None:
                        return ex
                    
                else:
                    raise Exception(f'Error: event {line.name} does not exist')
            

            elif line.type == 'out':
                if line.subtype == 'return':
                    return self.value(line.value, inside_vars, inside)
                
                elif line.subtype == 'enable':
                    param= self.value(line.value, inside_vars, inside)

                    if type(param) == array:
                        for i in params:
                            if type(i) != Event:
                                raise Exception('Error: enable only accepts events')
                            self.map.enable(i)
                    elif type(param) == Event:
                        self.map.enable(param)
                    
                    else:
                        raise Exception('Error: enable only accepts events')
                
                elif line.subtype == 'disable':
                    param= self.value(line.value, inside_vars, inside)
                    if type(param) == array:
                        for i in params:
                            if type(i) != Event:
                                raise Exception('Error: disable only accepts events')
                            self.map.disable(i)
                    elif type(param) == Event:
                        self.map.disable(param)
                    
                    else:
                        raise Exception('Error: disable only accepts events')


            elif line.type == 'cond':
                return self.value(line.cond, inside_vars, inside+1)

            else:
                raise Exception('Error: unknown type')



    def value(self, obj: ParserObj, inside_vars: dict={}, inside: int=0):
        '''
        Converts the parser object to a code object. Do arithmetics, comparisons, get vars, etc.
        :param obj: the parser object
        :param inside_vars: the vars inside the function
        :param inside: the level of inside
        :return: the code object
        '''
        if type(obj) == ParserObj:
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
                        return self.elements[obj.value]

                    else:
                        raise Exception(f'Name {obj.value} not found')

                #fix
                elif obj.subtype == 'arrow':
                    if obj.get('params'):
                        return self.to_object(self.map.get_data(self.to_python(self.value(obj.name, inside_vars, inside)),
                                            self.to_python(obj.var),
                                            self.to_python(self.args(obj, inside_vars, inside))))
                    
                    if isinstance(self.value(obj.name, inside_vars, inside), Map):
                        return self.to_object(self.map.map_data(self.to_python(obj.var)))

                    else:
                        return self.to_object(self.map.get_data(self.to_python(self.value(obj.name, inside_vars, inside)),
                                            self.to_python(obj.var)))
            
            if obj.type == 'type':
                if obj.value == 'event':
                    return Event
                elif obj.value == 'decision':
                    return Decision
                elif obj.value == 'distribution':
                    return Distribution
                elif obj.value == 'trait':
                    return Trait
                elif obj.value == 'nation':
                    return Nation
                elif obj.value == 'sea':
                    return Sea
                else:
                    return None
                

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
            

            elif obj.type == 'ucondition':
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
        
        elif type(obj) == decimal:
            return float(obj.val)
        
        elif type(obj) == time:
            return int(obj.days)

        elif type(obj) == string:
            return str(obj.val)

        elif type(obj) == boolean:
            return bool(obj.val)

        elif type(obj) == array:
            return list(obj.val)
        
        elif type(obj) == list:
            return [self.to_python(i) for i in obj]
        
        elif type(obj) == dict:
            return {key: self.to_python(value) for key, value in obj.items()}

        else:
            return obj
    
    
    def to_object(self, obj):
        '''
        Converts the real types to the code types
        :param obj: The object to convert
        :return The object converted
        '''
        if type(obj) == str and obj in self.vars:
            return self.vars[obj]
        elif type(obj) == str and obj in self.elements:
            return self.elements[obj]
        elif type(obj) == list:
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
        elif obj == None:
            return None
        else:
            raise Exception(f'Error: The object {obj} is not recognized')


    def args(self, obj: ParserObj, inside_vars: dict={}, inside: int=0):
        params= []
        for param in obj.args:
            params.append(self.value(param.value, inside_vars, inside))
        return params

    def args_names(self, obj: ParserObj, inside_vars: dict={}, inside: int=0):
        params_list= []
        params_dict= {}
        for param in obj.args:
            if param.get('name'):
                params_dict[param.name]= self.value(param.value, inside_vars, inside)
            else:
                if params_dict:
                    raise Exception('Error: You cannot exist a named parameter after an unnamed parameter')
                params_list.append(self.value(param.value, inside_vars, inside))
        
        return params_list, params_dict

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
        if isinstance(obj, integer) and (obj == integer(0)).value:
            return boolean(False)
        elif isinstance(obj, decimal) and (obj == decimal(0.0)).value:
            return boolean(False)
        elif isinstance(obj, string) and (obj == string('')).value:
            return boolean(False)
        elif isinstance(obj, array) and (obj == array([])).value:
            return boolean(False)
        elif isinstance(obj, boolean) and (obj == boolean(False)).value:
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


