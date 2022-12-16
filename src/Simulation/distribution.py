import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
from scipy.stats._distn_infrastructure import rv_sample

class Distribution:
    def __init__(self, distribution, scale:int=1):
        self.distribution:rv_sample = distribution
        self.scale= scale

    def randvar(self):
        return self.distribution.rvs(loc=1, scale=self.scale)
    
    def plot(self, *args, **kwds):
        x= np.linspace(self.distribution.ppf(0.01), self.distribution.ppf(0.99), 100)
        fig, _= plt.subplots()
        plt.plot(x, self.distribution.pdf(x, *args, **kwds), 'r-', lw=5, alpha=0.6, label='norm pdf')
        return fig
    

class Exponential(Distribution):
    def __init__(self, scale:int=1):
        super().__init__(distribution= ss.expon, scale= scale)

    def randvar(self):
        return int(self.distribution.rvs(loc=1, scale=self.scale))
