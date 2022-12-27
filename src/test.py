from elements.elements import *
from elements.map import *
from simulation.simulation import *
from events.event import *

m = Map()
m.add_province('Matanzas', 10, 10, 120)
m.add_province('Habana', 14, 15, 240, ['Matanzas'])
m.add_province('Camaguey', 12, 12, 100, ['Matanzas', 'Habana'])
m.add_nation('Cuba', ['Matanzas', 'Habana', 'Camaguey'])
m.add_province('Florida', 10, 10, 120)
m.add_nation('USA', ['Florida'])
m.add_province('Madrid', 10, 10, 120)

m.update('Habana', development= 20)

# class population_growth(Event):
#     def __init__(self):
#         super().__init__(name='population_growth' ,distribution= Uniform(1), category= 'Social', enabled= True)
    
#     def execute(self, map: Map, **kwargs):
#         for province in map.provincedict.values():
#             province.population= province.population * 1.03

# class mortality(Event):
#     def __init__(self):
#         super().__init__(name='mortality' ,distribution= Uniform(1), category= 'Social', enabled= True)
    
#     def execute(self, map: Map, **kwargs):
#         for province in map.provincedict.values():
#             province.population= province.population * 0.99


m.add_event(name='population_growth' ,distribution= Uniform(1), category= 'Social', enabled= True, execute= lambda map, **kwargs: [setattr(province, 'population', province.population * 1.03) for province in map.provincedict.values()])
m.add_event(name='mortality' ,distribution= Uniform(1), category= 'Social', enabled= True, execute= lambda map, **kwargs: [setattr(province, 'population', province.population * 0.99) for province in map.provincedict.values()])


def Simulation_test():
    print(list(m.provincedict.values())[0].population)
    a= Simulate(m, Queue(m.event_list)).simulate(10)

    print([i.population for i in list(m.provincedict.values())])


Simulation_test()