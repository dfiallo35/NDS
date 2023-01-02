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

m.add_category('Social')
m.add_trait('Comunist')


# def declare_war(map, **kwargs):
#     map.nations['Cuba'].declare_war('USA')
#     return {'enable': ['war']}

def population_growth(map, **kwargs):
    for province in map.provincedict.values():
        province.population= province.population * 1.03
    return {'enable': ['mortality']}
m.add_event(name='population_growth' ,distribution= Uniform(1), category= 'Social', enabled= True, execution= population_growth, type= 'unique')

def mortality(map, **kwargs):
    for province in map.provincedict.values():
        province.population= province.population * 0.99
    return {'disable:': ['population_growth']}
m.add_event(name='mortality' ,distribution= Uniform(1), category= 'Social', enabled= False, execution= mortality, type= 'unique')



def Simulation_test():
    print('init',[i.population for i in list(m.provincedict.values())])
    a= Simulate(m, Queue(m.event_list)).simulate(10)

    print('end', [i.population for i in list(m.provincedict.values())])


Simulation_test()