import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
from scipy.stats._distn_infrastructure import rv_sample

#todo: definir bien el uso de las distribuciones.
class Distribution:
    def __init__(self, distribution, scale:int=1):
        self.distribution:rv_sample = distribution
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
    
    def generate_distribution(data: list, bins:int=100, **kwargs):
        '''
        Generates a distribution from a list of data
        '''
        if type(data) != list and type(data) != np.ndarray:
            raise TypeError('Error: Data must be a list or a numpy array')
        if len(data) == 0:
            raise ValueError(f'Error: Data cannot be empty')
        
        hist_dist = ss.rv_histogram(np.histogram(data, bins=100))
        dist= Distribution(hist_dist, **kwargs)
        dist.__dict__['data']= data
        return dist
    
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



# Discrete distributions

class Poisson(Distribution):
    def __init__(self, scale: int=1):
        super().__init__(distribution=ss.poisson, scale=scale)

    def randvar(self):
        return int(self.distribution.rvs(loc=1, scale=self.scale))


class Bernoulli(Distribution):
    def __init__(self, scale: int=1):
        super().__init__(distribution=ss.bernoulli, scale=scale)

    def randvar(self):
        return int(self.distribution.rvs(loc=1, scale=self.scale))


class Binomial(Distribution):
    def __init__(self, scale: int=1): 
        super().__init__(distribution=ss.binom, scale=scale)
        
    def randvar(self):
        return int(self.distribution.rvs(loc=1, scale=self.scale))
    

# Multivariate distributions

class Multinomial(Distribution):
    def __init__(self, scale: int=1): 
        super().__init__(distribution=ss.multinomial, scale=scale)
    
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