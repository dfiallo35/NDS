from elements.elements import *
from elements.map import *
from simulation import *
from events import *

m = Map()
m.add_province('Matanzas', 10, 10, 120)
m.add_province('Habana', 14, 15, 240, ['Matanzas'])
m.add_province('Camaguey', 12, 12, 100, ['Matanzas', 'Habana'])
m.add_nation('Cuba', ['Matanzas', 'Habana', 'Camaguey'])
m.add_province('Florida', 10, 10, 120)
m.add_nation('USA', ['Florida'])
m.add_province('Madrid', 10, 10, 120)

m.update('Habana', development= 20)

class population_growth(Event):
    def __init__(self):
        self.distribution= Exponential(1)
        self.enabled= True
    
    def execute(self, map: Map, **kwargs):
        for province in map.provincedict.values():
            province.population= province.population * 1.01








def Simulation_test():

    print(list(m.provincedict.values())[0].population)
    a= Simulate(m, Queue(population_growth())).simulate(10)

    print(list(m.provincedict.values())[0].population)


Simulation_test()