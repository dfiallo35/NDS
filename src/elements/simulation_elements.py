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
    
    def __init__(self, name: str, dist: str, scale:int=1):
        super().__init__(name)
        self.distribution:rv_generic = ss.__dict__[dist]
        self.scale= scale
    
    def rvs(self, **kwargs):
        return self.distribution.rvs(**kwargs)
    
    def pdf(self, x, **kwargs):
        return self.distribution.pdf(x, **kwargs)

    def randvar(self, loc:int=0):
        '''
        Returns a random variable from the distribution
        '''
        return int(self.distribution.rvs(scale=self.scale, loc=loc))
    
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
    def __init__(self, name: str, distribution: Distribution, category: Category, execution, code=None, enabled: bool= True, type: str= None, decisions: list=[], args: list=[]):
        super().__init__(name)
        self.category= category
        self.distribution= distribution
        self.enabled= enabled
        self.type= type
        self.execution= execution
        self.code= code
        self.decisions= decisions
        
        self.args= args

    
    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the event is enabled
        '''
        return self.enabled
    
    # def __str__(self) -> str:
    #     return f'{self.name} - {self.category}'

    def execute(self, *args, **kwargs):
        '''
        Execute the event
        '''
        if self.type == 'unique':
            self.enabled= False

            #fix: args input
        if self.code:
            if args:
                return self.execution(compiled_list=self.code, inside=1, vars= {k:v for k,v in zip(self.args, args)})
            else:
                return self.execution(compiled_list=self.code, inside=1)
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