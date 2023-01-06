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

# m.update('Habana')

m.add_category('Social')
m.add_category('Economic')
m.add_trait('Comunist')


def population_growth(map, **kwargs):
    for province in map.provincedict.values():
        province.population= province.population * 1.03
    return {'enable': ['mortality']}
m.add_event(name='population_growth' ,distribution= Uniform(1), category= 'Social', enabled= True, execution= population_growth, type= 'unique', decisions=[])

def mortality(map, **kwargs):
    for province in map.provincedict.values():
        province.population= province.population * 0.99
    return {'disable:': ['population_growth']}
m.add_event(name='mortality' ,distribution= Uniform(1), category= 'Social', enabled= False, execution= mortality, type= 'unique', decisions=[])


def decrease_industrialization(map, **kwargs):
    for province in map.provincedict.values():
        if(province.data.get("industrialization")):
            province.data["industrialization"]-= 1
    return {'disable:': ['decrease_industrialization']}
m.add_event(name='decrease_industrialization' ,distribution= Uniform(1), category= 'Economic', enabled= False, execution= decrease_industrialization, type= 'unique', decisions=[])



def Simulation_test():
    print('init',[i.population for i in list(m.provincedict.values())])
    a= Simulate(m, Pqueue(m.event_list)).simulate(10)

    print('end', [i.population for i in list(m.provincedict.values())])




def decide_simulation_test(nation:Nation):
    
    a = Simulate(m, Pqueue(m.event_list))

    actions=[Decision(action="increase_industrialization",preconds=precond_industrialization , effects=effects_industrialization),
            Decision(action="increase_average_living_standard",preconds=precond_average_living_standard ,effects=effects_average_living_standard),
            Decision(action="increase_tourism",preconds=precond_tourism ,effects=effects_tourism)]
    
    m.decisions=actions
    # m.nationdict["Cuba"].__dict__={}
    # m.nationdict["Cuba"].data["industrialization"]=0
    # m.nationdict["Cuba"].data["average_living_standard"]=0
    # m.nationdict["Cuba"].data["tourism"]=0

    for province in m.nationdict["Cuba"].provinces.values():
        province.data["economic_resources"]=100000
        province.data["industrialization"] =3
        province.data["average_living_standard"]=3
        province.data["tourism"]=3
        # m.nationdict["Cuba"].data["industrialization"]+=province.data["industrialization"]
        # m.nationdict["Cuba"].data["average_living_standard"]+=province.data["industrialization"]
        # m.nationdict["Cuba"].data["tourism"]+=province.data["industrialization"]

    # a.decide(nation, Event("decrease_industrialization",Exponential(1),m.categorydict['Economic'],decrease_industrialization), 0)
    b= a.decide(m, m.eventdict["decrease_industrialization"], 0)
    d=2
    return b
    # print('init',[i.population for i in list(m.provincedict.values())])
    # a= Simulate(m, Queue(m.event_list)).simulate(10)



# Simulation_test()

# print(decide_simulation_test(m.nationdict["Cuba"]))
a=decide_simulation_test(m.nationdict["Cuba"])
print(a)
print("papas")
for j in a.values():
    print( [i["action"].action if i["action"] else None for i in get_path(j)])





# for i in a:
#     print( [i["action"].action if i["action"] else None for i in get_path(i)])

# print( [i["action"].action if i["action"] else None for i in get_path(decide_simulation_test(m.nationdict["Cuba"]))])


# distributions= {name:val for (name, val) in gm(ss, lambda x: isinstance(x, rv_generic))}

# print(distributions.keys())