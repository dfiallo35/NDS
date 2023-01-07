from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
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
        if isinstance(d, list) or isinstance(dist, np.ndarray):
            return [float(i) for i in d]
        else:
            return float(d)
    
    
    def irvs(dist, *args, **kwargs):
        d= dist.distribution.rvs(*args, **kwargs)
        if isinstance(d, list) or isinstance(dist, np.ndarray):
            return [int(i) for i in d]
        else:
            return int(d)
    
    def pdf(self, x, *args, **kwargs):
        return self.distribution.pdf(x, *args, **kwargs)

    def randvar(self, loc:int=0):
        '''
        Returns a random variable from the distribution
        '''
        return int(self.distribution.rvs(loc=loc, *self.args, **self.kwargs))
    
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
    def __init__(self, name: str, dist: Distribution, category: Category, execution, code=None, enabled: bool= True, decisions: list=[], params: list=[]):
        super().__init__(name)
        self.category= category
        self.distribution= dist
        self.enabled= enabled
        self.execution= execution
        self.code= code
        self.decisions= decisions
        
        self.params= params

    
    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the event is enabled
        '''
        return self.enabled
    
    def __str__(self) -> str:
        return f'{self.name}'

    def execute(self, *args, **kwargs):
        '''
        Execute the event
        '''
        if self.code:
            
            if not self.params:
                self.execution(compiled_list=self.code, inside=1)
            
            else:
                for i in kwargs:
                    if i not in self.params:
                        raise ValueError(f'Error: {i} is not in the arguments')
                    else:
                        self.params.remove(i)
                params= {**{k:v for k,v in zip(self.params, args)}, **kwargs}
                return self.execution(compiled_list=self.code, inside=1, vars= params)
        else:
            if args:
                return self.execution(*args)
            else:
                return self.execution()


    def next(self) -> float:
        '''
        Returns the time of the next execution of the event
        '''
        return self.distribution.randvar()
    
    def __str__(self) -> str:
        return f'{self.name}'


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
        for i in kwargs:
            if i not in self.params:
                raise ValueError(f'Error: {i} is not in the arguments')
            else:
                self.params.remove(i)
        params= {**{k:v for k,v in zip(self.params, args)}, **kwargs}
        return self.execution(compiled_list=self.cond, inside=1, vars= params)

