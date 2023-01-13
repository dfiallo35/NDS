from elements.simulation_elements import *

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





# a= ss.uniform
# print(a.rvs(loc=0))
# print(a.rvs(loc=0))





# data = 
# print(data)
# hist = np.histogram(data, bins=100)
# print(hist)
# hist_dist = Distribution.generate_distribution(ss.expon.rvs(size=10000000, loc=0, random_state=123), scale=10)
# print(hist_dist.randvar(loc=50))

# import matplotlib.pyplot as plt
# X = np.linspace(-5.0, 5.0, 100)
# fig, ax = plt.subplots()
# ax.set_title("PDF from Template")
# ax.hist(hist_dist.data, density=True, bins=30)
# ax.plot(X, hist_dist.pdf(X), label='PDF')
# ax.legend()
# plt.savefig("hist_dist.png")
# hist_dist.plot().savefig("hist_dist.png")

# print(b.rvs())




# a= ss.poisson
# print(a.rvs(mu= 2, size=10))

# a= ss.expon
# print(a.rvs(loc=100, scale=2))