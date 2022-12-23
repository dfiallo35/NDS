import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
from scipy.stats._distn_infrastructure import rv_sample

class Distribution:
    def __init__(self, distribution, scale:int=1):
        self.distribution:rv_sample = distribution
        self.scale= scale

    def randvar(self):
        '''
        Returns a random variable from the distribution
        '''
        return self.distribution.rvs(loc=1, scale=self.scale)
    
    def plot(self, *args, **kwds):
        '''
        Plots the distribution
        '''
        x= np.linspace(self.distribution.ppf(0.01), self.distribution.ppf(0.99), 100)
        fig, _= plt.subplots()
        plt.plot(x, self.distribution.pdf(x, *args, **kwds), 'r-', lw=5, alpha=0.6, label='norm pdf')
        return fig


#todo: define other distributions

class Exponential(Distribution):
    def __init__(self, scale:int=1):
        super().__init__(distribution= ss.expon, scale= scale)

    def randvar(self):
        '''
        Returns a random variable from the distribution
        '''
        return int(self.distribution.rvs(loc=1, scale=self.scale))


class Uniform(Distribution):
    def __init__(self, scale: int = 1):
        super().__init__(distribution= ss.uniform, scale= scale)
    
    def randvar(self):
        return int(self.distribution.rvs(loc=1, scale=self.scale))



# a= ss.geom
# print(a.rvs(p=0.7, size=10))

# a= Exponential(scale=10)
# print(a.randvar())


# b= ss.expon
# print(b.rvs(scale= 100))


# a= ss.rv_continuous()
# b= ss.rv_discrete(values= ([1,2,3,4], [.4,.2,.1,.3]))

# print(b.rvs())