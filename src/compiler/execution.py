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
        semantic_elements= {
            'nation': {'min':4},
            'sea': {'args':2},
            'trait': {'args':0},
            'category': {'args':0},
            'dec event': {'params':1, 'args':1},
            'sim event': {'args':4},
            'decision': {'args':1, 'params': 1},
            'distribution': {'min':1},
        }

        #fix
        semantic_funcs= {
            'type': {'args':1},
            'pos': {'args':2},
            'size': {'args':1},
            'simulate': {'args':1},
            'plot': {'args':3},
            'dataframe': {'args':2},
        }

        for line in code:
            if line.type == 'element':
                if semantic_elements.get(line.subtype):
                    if semantic_elements[line.subtype].get('min') and len(line.args) < semantic_elements[line.subtype]['min']:
                        el= semantic_elements[line.subtype]['min']
                        raise Exception(f'Error: The element {line.subtype} needs at least {el} parameters')

                    if semantic_elements[line.subtype].get('args') and len(line.args) != semantic_elements[line.subtype]['args']:
                        el= semantic_elements[line.subtype]['args']
                        raise Exception(f'Error: The element {line.subtype} needs {el} arguments')
                    
                    if semantic_elements[line.subtype].get('params') and len(line.params) != semantic_elements[line.subtype]['params']:
                        el= semantic_elements[line.subtype]['params']
                        raise Exception(f'Error: The element {line.subtype} needs {el} parameters')
            
            if line.type == 'func':                
                if semantic_funcs.get(line.subtype):
                    if semantic_funcs[line.subtype].get('min') and len(line.args) < semantic_funcs[line.subtype]['min']:
                        f= semantic_funcs[line.subtype]['min']
                        raise Exception(f'Error: The element {line.subtype} needs at least {f} parameters')

                    if semantic_funcs[line.subtype].get('args') and len(line.args) != semantic_funcs[line.subtype]['args']:
                        f= semantic_funcs[line.subtype]['args']
                        raise Exception(f'Error: The element {line.subtype} needs {f} arguments')
                    
                    if semantic_funcs[line.subtype].get('max') and len(line.params) > semantic_funcs[line.subtype]['max']:
                        f= semantic_funcs[line.subtype]['max']
                        raise Exception(f'Error: The element {line.subtype} accepts at most {f} parameters')
    

    
    #ELEMENTS
    def generate_decision_event(self, line, inside_vars, inside):
        params= self.extra_params(line.params)
        args, kwargs= self.args_names(line, inside_vars, inside)
        if args:
            self.map.add_decision_event(self.to_python(line.name), cat=args[0], execution=self.execute, code=line.script, params=params)
        elif kwargs:
            self.map.add_decision_event(self.to_python(line.name), cat=kwargs['cat'], execution=self.execute, code=line.script, params=params)
    
    def generate_function(self, line, inside_vars, inside):
        self.map.add_function(self.to_python(line.name), execution=self.execute, code=line.script, params=self.extra_params(line.params))
    
    def generate_simulation_event(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python([line.name, *args])
        kwargs= self.to_python({**kwargs, **{'execution': self.execute, 'code': line.script}})
        self.map.add_simulation_event(*self.to_python(args), **self.to_python(kwargs))

    def generate_decision(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python([line.name, *args])
        kwargs= self.to_python({**kwargs, **{'execution': self.execute, 'cond': ParserObj(type='cond', cond=line.condition), 'params': self.extra_params(line.params)}})
        self.map.add_decision(*self.to_python(args), **self.to_python(kwargs))
    
    def generate_nation(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python([line.name, *args])
        kwargs= self.to_python(kwargs)
        self.map.add_nation(*self.to_python(args), **self.to_python(kwargs))
    
    def generate_sea(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python([line.name, *args])
        kwargs= self.to_python(kwargs)
        self.map.add_sea(*self.to_python(args), **self.to_python(kwargs))
    
    def generate_trait(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python([line.name, *args])
        kwargs= self.to_python(kwargs)
        self.map.add_trait(*self.to_python(args), **self.to_python(kwargs))
    
    def generate_category(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python([line.name, *args])
        kwargs= self.to_python(kwargs)
        self.map.add_category(*self.to_python(args), **self.to_python(kwargs))
    
    def generate_distribution(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python([line.name, *args])
        kwargs= self.to_python(kwargs)
        self.map.add_distribution(*self.to_python(args), **self.to_python(kwargs))

    elements_types={
        'dec event': generate_decision_event,
        'function': generate_function,
        'sim event': generate_simulation_event,
        'decision': generate_decision,
        'nation': generate_nation,
        'sea': generate_sea,
        'trait': generate_trait,
        'category': generate_category,
        'distribution': generate_distribution,
    }

    def code_element(self, line, inside_vars, inside):
        self.map.alredy_exist(self.to_python(line.name))
        if line.name in self.vars or line.name in inside_vars:
            raise Exception(f'The element {line.name} already exist')
        
        if line.subtype in self.elements_types:
            self.elements_types[line.subtype](self, line, inside_vars, inside)
        else:
            raise Exception(f'The element {line.subtype} does not exist')



    #VARS
    def code_var(self, line, inside_vars, inside):
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



    #FUNCTION
    def code_function(self, line, inside_vars, inside):
        self.execute([line.value], inside_vars, inside+1)
    

    
    #FUNC
    def func_show(self, line, inside_vars, inside):
        params= self.args(line, inside_vars, inside)
        print('>>', *params)
    
    #fix return
    def func_type(self, line, inside_vars, inside):
        params= self.args(line, inside_vars, inside)
        return ('ret', self.to_object(type(self.value(params[0], inside_vars, inside)).__name__))
    
    #fix return
    def func_pos(self, line, inside_vars, inside):
        params= self.args(line, inside_vars, inside)
        if not type(params[0]) == array:
            raise Exception('Error: pos() only accepts lists as first parameter')
        if not type(params[1]) == integer:
            raise Exception('Error: pos() only accepts integers as second parameter')
            
        return ('ret', self.to_object(params[0].value[params[1].value]))
    
    #fix return
    def func_size(self, line, inside_vars, inside):
        params= self.args(line, inside_vars, inside)
        if not type(self.to_python(params[0])) == list:
            raise Exception('Error: size() only accepts lists')

        return ('ret', self.to_object(len(params[0])))
    
    #fix return
    def func_rvs(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python(args)
        kwargs= self.to_python(kwargs)
        if not isinstance(args[0], Distribution) and not kwargs.get('dist'):
            raise Exception('Error: rvs() only accepts distributions as first parameter')
        else:
            return ('ret', self.to_object(Distribution.rvs(*args, **kwargs)))
    
    #fix return
    def func_irvs(self, line, inside_vars, inside):
        args, kwargs= self.args_names(line, inside_vars, inside)
        args= self.to_python(args)
        kwargs= self.to_python(kwargs)

        if not isinstance(args[0], Distribution) and not kwargs.get('dist'):
            raise Exception('Error: irvs() only accepts distributions as first parameter')
        else:
            return ('ret', self.to_object(Distribution.irvs(*args, **kwargs)))

    def func_gen_dist(self, line, inside_vars, inside):
        ...
    
    def func_simulate(self, line, inside_vars, inside):
        params= self.args(line, inside_vars, inside)
        if not type(params[0]) == time:
            raise Exception('Error: simulate() only accepts time')
        sim= Simulate(self.map, Pqueue(self.map.event_enabled_list))
        sim.simulate(self.to_python(params[0]))
    
    def func_plot(self, line, inside_vars, inside):
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

    
    def func_dataframe(self, line, inside_vars, inside):
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


    func_types={
        'show': func_show,
        'type': func_type,
        'pos': func_pos,
        'size': func_size,
        'rvs': func_rvs,
        'irvs': func_irvs,
        'gen_dist': func_gen_dist,
        'simulate': func_simulate,
        'plot': func_plot,
        'dataframe': func_dataframe,
    }

    #fix return
    def code_func(self, line, inside_vars, inside):
        if line.subtype not in self.func_types:
            raise Exception('Error: the function is not recognized')

        c= self.func_types[line.subtype](self, line, inside_vars, inside)
        if isinstance(c, tuple):
            return c
    

    #fix return
    #LOOPS
    def loop_while(self, line, inside_vars, inside):
        while self.to_python(self.value(line.condition, inside_vars, inside)):
            val= self.execute(line.script, vars= inside_vars, inside=inside+1)
            if self.to_python(val) != None:
                return ('ret', val)
    
    #fix return
    def loop_repeat(self, line, inside_vars, inside):
        init= self.value(line.init, inside_vars, inside)
        end= self.value(line.end, inside_vars, inside)
        
        if type(init) != integer or type(end) != integer:
            raise Exception('Error: for() only accepts integers as parameters')

        for i in range(self.to_python(init), self.to_python(end) + 1):
            val= self.execute(line.script,
                            vars= {line.var: i, **inside_vars},
                            inside=inside+1)
            if self.to_python(val) != None:
                return ('ret', val)
    
    #fix return
    def loop_foreach(self, line, inside_vars, inside):
        param= self.value(line.param)
        if type(param) != array:
            raise Exception('Error: for() only accepts lists as parameter')

        for i in self.to_python(param):
            val= self.execute(line.script,
                            vars= {line.var: i, **inside_vars},
                            inside=inside+1)
            if self.to_python(val) != None:
                return ('ret', val)
    
    loops_types={
        'while': loop_while,
        'repeat': loop_repeat,
        'foreach': loop_foreach,
    }
    def code_loops(self, line, inside_vars, inside):
        if line.subtype not in self.loops_types:
            raise Exception('Error: the loop is not recognized')

        c= self.loops_types[line.subtype](self, line, inside_vars, inside)
        if isinstance(c, tuple):
            return c
    

    #fix return
    #CONDITIONALS
    def code_conditional(self, line, inside_vars, inside):
        if line.subtype == 'if':
                    if self.to_python(self.value(line.condition, inside_vars, inside)):
                        val= self.execute(line.script, vars= inside_vars, inside=inside+1)
                        if self.to_python(val) != None:
                            return ('ret', val)
                
        elif line.subtype == 'if else':
            if self.to_python(self.value(line.condition, inside_vars, inside)):
                val= self.execute(line.script, vars= inside_vars, inside=inside+1)   
            else:
                val= self.execute(line.else_script, vars= inside_vars, inside=inside+1)
            if self.to_python(val) != None:
                    return ('ret', val)
        
        else:
            raise Exception('Error: unknown conditional')


    #fix return
    #EXECUTION
    def code_execution(self, line, inside_vars, inside):
        if self.events.get(self.to_python(line.name)):
            args, kwargs= self.args_names(line, inside_vars, inside)
            args= self.to_python(args)
            kwargs= self.to_python(kwargs)
            ex= self.to_object(self.events[line.name].execute(*args, **kwargs))
            if self.to_python(ex) != None:
                return ('ret', ex)
            
        else:
            raise Exception(f'Error: event {line.name} does not exist')
    

    #fix return
    #OUT
    def out_return(self, line, inside_vars, inside):
        return ('ret', self.value(line.value, inside_vars, inside))
    
    def out_enable(self, line, inside_vars, inside):
        params= self.value(line.value, inside_vars, inside)

        if type(params) == array:
            for i in params:
                if type(i) != Event:
                    raise Exception('Error: enable only accepts events')
                self.map.enable(i)
        elif type(params) == Event:
            self.map.enable(params)
        
        else:
            raise Exception('Error: enable only accepts events')
    
    def out_disable(self, line, inside_vars, inside):
        params= self.value(line.value, inside_vars, inside)
        if type(params) == array:
            for i in params:
                if type(i) != Event:
                    raise Exception('Error: disable only accepts events')
                self.map.disable(i)
        elif type(params) == Event:
            self.map.disable(params)
        
        else:
            raise Exception('Error: disable only accepts events')


    out_types={
        'return': out_return,
        'enable': out_enable,
        'disable': out_disable,
    }
    def code_out(self, line, inside_vars, inside):
        if line.subtype not in self.out_types:
            raise Exception('Error: the out is not recognized')
        
        c= self.out_types[line.subtype](self, line, inside_vars, inside)
        if isinstance(c, tuple):
            return c
    

    #fix return
    #COND
    def code_cond(self, line, inside_vars, inside):
        return ('ret', self.value(line.cond, inside_vars, inside+1))


    code_types={
        'element': code_element,
        'var': code_var,
        'function': code_function,
        'func': code_func,
        'loop': code_loops,
        'conditional': code_conditional,
        'execution': code_execution,
        'out': code_out,
        'cond': code_cond,
    }



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
            if line.type not in self.code_types:
                raise Exception('Error: unknown type')
                
            c= self.code_types[line.type](self, line, inside_vars, inside)
            if isinstance(c, tuple):
                return c[1]





    #EXPR
    def expr_interger(self, obj, inside_vars, inside):
        return integer(obj.value)
    
    def expr_decimal(self, obj, inside_vars, inside):
        return decimal(obj.value)
    
    def expr_time(self, obj, inside_vars, inside):
        return time(int(obj.value[:-1]), obj.value[-1])
    
    def expr_string(self, obj, inside_vars, inside):
        return string(obj.value)
    
    def expr_bool(self, obj, inside_vars, inside):
        if obj.value == 'true':
            return boolean(True)
        return boolean(False)
    
    def expr_list(self, obj, inside_vars, inside):
        return array([self.value(value, inside_vars, inside) for value in obj.value])
    
    def expr_name(self, obj, inside_vars, inside):
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
    
    def expr_arrow(self, obj, inside_vars, inside):
        if obj.get('params'):
            return self.to_object(self.map.get_data(self.to_python(self.value(obj.name, inside_vars, inside)),
                                self.to_python(obj.var),
                                self.to_python(self.args(obj, inside_vars, inside))))
        
        if isinstance(self.value(obj.name, inside_vars, inside), Map):
            return self.to_object(self.map.map_data(self.to_python(obj.var)))

        else:
            return self.to_object(self.map.get_data(self.to_python(self.value(obj.name, inside_vars, inside)),
                                self.to_python(obj.var)))


    expr_types={
        'integer': expr_interger,
        'decimal': expr_decimal,
        'time': expr_time,
        'string': expr_string,
        'bool': expr_bool,
        'list': expr_list,
        'name': expr_name,
        'arrow': expr_arrow,
    }

    def code_expr(self, obj, inside_vars, inside):
        if obj.subtype not in self.expr_types:
            raise Exception('Error: unknown type')
        
        return self.expr_types[obj.subtype](self, obj, inside_vars, inside)
    

    #ARITHMETICS
    def arithmetic_sum(self, left, right):
        return left + right
    
    def arithmetic_sub(self, left, right):
        return left - right
    
    def arithmetic_mul(self, left, right):
        return left * right
    
    def arithmetic_div(self, left, right):
        return left / right
    
    def arithmetic_mod(self, left, right):
        return left % right
    
    def arithmetic_pow(self, left, right):
        return left**right
    
    def arithmetic_floor_div(self, left, right):
        return left // right
    


    arithmetic_types={
        '+': arithmetic_sum,
        '-': arithmetic_sub,
        '*': arithmetic_mul,
        '/': arithmetic_div,
        '%': arithmetic_mod,
        '**': arithmetic_pow,
        '//': arithmetic_floor_div,
    }
    def code_arithmetic(self, obj, inside_vars, inside):
        left= self.value(obj.left, inside_vars, inside)
        right= self.value(obj.right, inside_vars, inside)
        
        if obj.subtype not in self.arithmetic_types:
            raise Exception('Error: unknown type')
        
        try:
            return self.arithmetic_types[obj.subtype](self, left, right)
        except:
            raise Exception(f'Error: {left.type} and {right.type} does not support "{obj.subtype}" operation')
            

    #UNARY ARITHMETICS
    def unary_arithmetic_sum(self, value):
        return value
    
    def unary_arithmetic_sub(self, value):
        return -value
    
    unary_arithmetic_types={
        '+': unary_arithmetic_sum,
        '-': unary_arithmetic_sub,
    }
    
    def code_unary_arithmetic(self, obj, inside_vars, inside):
        value= self.value(obj.value, inside_vars, inside)
        
        if obj.subtype not in self.arithmetic_types:
            raise Exception('Error: unknown type')
        
        try:
            return self.arithmetic_types[obj.subtype](self, value)
        except:
            raise Exception(f'Error: {value.type} does not support "{obj.subtype}" operation')
        

    #CONDITIONS
    def condition_and(self, left, right):
        return left and right
    
    def condition_or(self, left, right):
        return left or right
    
    def condition_xor(self, left, right):
        return left ^ right
    

    condition_types={
        'and': condition_and,
        'or': condition_or,
        'xor': condition_xor,
    }

    def code_condition(self, obj, inside_vars, inside):
        left= self.dynamic_conditions(self.value(obj.left, inside_vars, inside))
        right= self.dynamic_conditions(self.value(obj.right, inside_vars, inside))
        
        if obj.subtype not in self.condition_types:
            raise Exception('Error: unknown type')
        
        try:
            return self.condition_types[obj.subtype](self, left, right)
        except:
            raise Exception(f'Error: {left.type} and {right.type} does not support "{obj.subtype}" operation')



    #COMPARISONS
    def comparison_equal(self, left, right):
        return left == right
    
    def comparison_not_equal(self, left, right):
        return left != right
    
    def comparison_less(self, left, right):
        return left < right
    
    def comparison_less_equal(self, left, right):
        return left <= right
    
    def comparison_greater(self, left, right):
        return left > right
    
    def comparison_greater_equal(self, left, right):
        return left >= right
    
    comparison_types= {
        '==': comparison_equal,
        '!=': comparison_not_equal,
        '<': comparison_less,
        '<=': comparison_less_equal,
        '>': comparison_greater,
        '>=': comparison_greater_equal,
    }

    def code_comparison(self, obj, inside_vars, inside):
        left= self.value(obj.left, inside_vars, inside)
        right= self.value(obj.right, inside_vars, inside)
        
        if obj.subtype not in self.comparison_types:
            raise Exception('Error: unknown type')
            
        try:
            return self.comparison_types[obj.subtype](self, left, right)
        except:
            raise Exception(f'Error: {left.type} and {right.type} does not support "{obj.subtype}" operation')


    #UNARY CONDITIONS
    def code_unary_condition(self, obj, inside_vars, inside):
        if obj.subtype == 'not':
            return ~self.value(obj.value, inside_vars, inside)
    

    #EXECUTION
    def code_execution(self, obj, inside_vars, inside):
        return self.execute([obj], inside_vars, inside+1)
    

    #TYPES
    def code_type(self, obj, inside_vars, inside):
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
    
    value_types={
        'expr': code_expr,
        'arithmetic': code_arithmetic,
        'uarithmetic': code_unary_arithmetic,
        'condition': code_condition,
        'comparation': code_comparison,
        'ucondition': code_unary_condition,
        'execution': code_execution,
        'func': code_execution,
        'type': code_type,
    }


    def value(self, obj: ParserObj, inside_vars: dict={}, inside: int=0):
        '''
        Converts the parser object to a code object. Do arithmetics, comparisons, get vars, etc.
        :param obj: the parser object
        :param inside_vars: the vars inside the function
        :param inside: the level of inside
        :return: the code object
        '''
        if type(obj) == ParserObj:
            if obj.type not in self.value_types:
                raise Exception('Error: unknown type')
            
            return self.value_types[obj.type](self, obj, inside_vars, inside)

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




    to_python_types={
        integer: lambda x: int(x.val),
        decimal: lambda x: float(x.val),
        time: lambda x: int(x.days),
        string: lambda x: str(x.val),
        boolean: lambda x: bool(x.val),
        array: lambda x: list(x.val),
    }

    def to_python(self, obj: Element):
        '''
        Returns the real value of an object(the values for functions outside the code)
        :param obj: The object to get the real value
        :return The real value of the object
        '''
        if self.to_python_types.get(type(obj)):
            return self.to_python_types[type(obj)](obj)
        
        elif type(obj) == list:
            return [self.to_python(i) for i in obj]
        
        elif type(obj) == dict:
            return {key: self.to_python(value) for key, value in obj.items()}

        else:
            return obj
    
    
    to_object_types={
        list: lambda x: array(x),
        str: lambda x: string(x),
        int: lambda x: integer(x),
        float: lambda x: decimal(x),
        bool: lambda x: boolean(x),
    }

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
        if self.to_object_types.get(type(obj)):
            return self.to_object_types[type(obj)](obj)
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


