from elements.elements import *

import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
from inspect import getmembers as gm
from scipy.stats._distn_infrastructure import rv_generic




class Distribution(Element):
    distributions= {name:val for (name, val) in gm(ss, lambda x: isinstance(x, rv_generic))}
    
    def __init__(self, name: str, dist, *args, **kwargs):
        super().__init__(name)
        if isinstance(dist, str):
            self.distribution:rv_generic = Distribution.distributions[dist]
        else:
            self.distribution:rv_generic = dist
        self.args= args
        self.kwargs= kwargs
    
    def rvs(dist, *args, **kwargs):
        d= dist.distribution.rvs(*args, **kwargs)
        if isinstance(d, list) or isinstance(d, np.ndarray):
            return [float(i) for i in d]
        else:
            return float(d)
    
    
    def irvs(dist, *args, **kwargs):
        d= dist.distribution.rvs(*args, **kwargs)
        if isinstance(d, list) or isinstance(d, np.ndarray):
            return [int(i) for i in d]
        else:
            return int(d)
    
    def pdf(self, x, *args, **kwargs):
        return self.distribution.pdf(x, *args, **kwargs)

    def randvar(self, loc:int=0):
        '''
        Returns a random variable from the distribution
        '''
        d= self.distribution.rvs(loc=loc, *self.args, **self.kwargs)
        if isinstance(d, list) or isinstance(d, np.ndarray):
            return [int(i) for i in d]
        else:
            return int(d)
    
    def generate_distribution(name: str, data: list, bins:int=100, **kwargs):
        '''
        Generates a distribution from a list of data
        '''
        if type(data) != list and type(data) != np.ndarray:
            raise TypeError('Error: Data must be a list or a numpy array')
        if len(data) == 0:
            raise ValueError(f'Error: Data cannot be empty')
        
        hist_dist = ss.rv_histogram(np.histogram(data, bins=100))
        dist= Distribution(name, hist_dist, **kwargs)
        dist.__dict__['data']= data
        return dist
    
    #fix: plot
    def plot(self, *args, **kwds):
        '''
        Plots the distribution
        '''
        x= np.linspace(self.distribution.ppf(0.01), self.distribution.ppf(0.99), 100)
        fig, _= plt.subplots()
        plt.plot(x, self.distribution.pdf(x, *args, **kwds), 'r-', lw=5, alpha=0.6, label='norm pdf')
        return fig


class Category(Element):
    def __init__(self, name: str):
        super().__init__(name)
        self.decisions= list()
    
    def add_decision(self, decision):
        self.decisions.append(decision)
    
    def __str__(self) -> str:
        return f'{self.name}'

class Event(Element):
    def __init__(self, name: str, execution, code=None):
        super().__init__(name)
        self.execution= execution
        self.code= code

    def __str__(self) -> str:
        return f'{self.name}'

    def execute(self, *args, **kwargs):
        '''
        Execute the event
        '''
        if not self.code:
            return self.execution(*args, **kwargs)
        
        else:
            self.execution(code=self.code, inside=1)


class Function(Event):
    def __init__(self, name: str, execution, code=None, params: list=[]):
        super().__init__(name, execution, code)
        self.execution= execution
        self.code= code
        self.params= params

    
    
    def __str__(self) -> str:
        return f'{self.name}'

    def execute(self, *args, **kwargs):
        '''
        Execute the event
        '''
        if not self.code:
            return self.execution(*args, **kwargs)
        
        else:
            for i in kwargs:
                if i not in self.params:
                    raise ValueError(f'Error: {i} is not in the arguments')
                else:
                    self.params.remove(i)
            params= {**{k:v for k,v in zip(self.params, args)}, **kwargs}
            return self.execution(code=self.code, inside=1, vars= params)


class SimulationEvent(Event):
    def __init__(self, name: str, dist: Distribution, category: Category, execution, code=None, enabled: bool= True, decisions: list=[]):
        super().__init__(name, execution, code)
        self.category= category
        self.distribution= dist
        self.enabled= enabled
        self.decisions= decisions

    
    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the event is enabled
        '''
        return self.enabled
    
    def __str__(self) -> str:
        return f'{self.name}'


    def next(self) -> float:
        '''
        Returns the time of the next execution of the event
        '''
        return self.distribution.randvar()



class DecisionEvent(Event):
    def __init__(self, name: str, category: Category, execution, code=None, params: list=[]):
        super().__init__(name, execution, code)
        self.category= category
        self.params= params
        self.enabled= True
        self.nation= None
    
    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the event is enabled
        '''
        return self.enabled
    
    def copy(self):
        return DecisionEvent(self.name, self.category, self.execution, self.code, self.params)
    
    def __str__(self) -> str:
        return f'{self.name}'

    def execute(self, *args, **kwargs):
        '''
        Execute the event
        '''
        if not self.nation:
            raise ValueError('Error: Nation not defined')
        
        if not self.code:
            self.execution(self.nation)
        else: 
            params= {self.params[0]: self.nation}
            self.execution(vars=params,code=self.code, inside=1)
    
    def add_nation(self, nation):
        self.nation= nation
    
    def get_event(self, nation):
        event: DecisionEvent= copy(self)
        event.add_nation(nation)
        return event



class Decision(Element):
    def __init__(self, name: str, cond, event: Event, execution, params: list=[]):
        super().__init__(name)
        self.cond= cond
        self.event= event
        self.execution= execution

        self.params= params
    
    def condition(self, *args, **kwargs):
        '''
        Returns the condition of the decision
        '''
        if self.cond:
            for i in kwargs:
                if i not in self.params:
                    raise ValueError(f'Error: {i} is not in the arguments')
                else:
                    self.params.remove(i)
            params= {**{k:v for k,v in zip(self.params, args)}, **kwargs}
            return self.execution(code=[self.cond], inside=1, vars= params)
        else:
            return self.execution(*args, **kwargs)

