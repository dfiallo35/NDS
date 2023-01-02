from elements.elements import *
from elements.map import *
from simulation.simulation import *
from ia.planning_decisions import *
from ia.test_planning import*

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
m.add_category('Economic')
m.add_trait('Comunist')


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


def decrease_industrialization(map, **kwargs):
    for province in map.provincedict.values():
        province.data["industrialization"]-= 1
    return {'disable:': ['decrease_industrialization']}
m.add_event(name='decrease_industrialization' ,distribution= Uniform(1), category= 'Economic', enabled= False, execution= decrease_industrialization, type= 'unique')



def Simulation_test():
    print('init',[i.population for i in list(m.provincedict.values())])
    a= Simulate(m, Queue(m.event_list)).simulate(10)

    print('end', [i.population for i in list(m.provincedict.values())])




def decide_simulation_test(nation):
    a = Simulate(m, Queue(m.event_list))

    actions=[Decision(action="increase_industrialization",preconds=precond_industrialization ,effects=effects_industrialization),
            Decision(action="increase_average_living_standard",preconds=precond_average_living_standard ,effects=effects_average_living_standard),
            Decision(action="increase_tourism",preconds=precond_tourism ,effects=effects_tourism)]
    
    m.decisions=actions
    
    a.decide(nation, decrease_industrialization, 0)

    # print('init',[i.population for i in list(m.provincedict.values())])
    # a= Simulate(m, Queue(m.event_list)).simulate(10)



# Simulation_test()

print(decide_simulation_test(m.nationdict["Cuba"]))