from elements.elements import *
from elements.map import *
from simulation.simulation import *
from ia.planning_decisions import *
# from ia.test_planning import*

m = Map()
# m.add_province('Matanzas', 10, 10, 120)
# m.add_province('Habana', 14, 15, 240, ['Matanzas'])
# m.add_province('Camaguey', 12, 12, 100, ['Matanzas', 'Habana'])
m.add_nation('Cuba',10, 10) #['Matanzas', 'Habana', 'Camaguey'])
# m.add_province('Florida', 10, 10, 120)
m.add_nation('USA',10, 10)#, ['Florida'])
# m.add_province('Madrid', 10, 10, 120)

m.add_category('Social')
m.add_category('Economic')
m.add_trait('Comunist')


# def mortality(map, **kwargs):
#     for nation in map.provincedict.values():
#         nation.population= nation.population * 0.99
# m.add_simulation_event(name="mortality",dist=Distribution(name="uniform",dist="uniform",scale=100),cat= 'Social',enabled=True,dec=[],execution=mortality)

# def decrease_industrialization(map, **kwargs):
#     for nation in map.provincedict.values():
#         if(nation.data.get("industrialization")):
#             nation.data["industrialization"]-= 1
# m.add_simulation_event(name="decrease_industrialization",dist=Distribution("uniform","uniform",scale=100),cat= 'Economic',enabled=True,dec=[],execution=decrease_industrialization)


# def industrialization_increases( state,**kargs):
#     # new_state=deepcopy(state)
#     state.change_data("economic_resources",-1000) 
#     state.change_data("industrialization",3)
#     # return new_state
# m.add_simulation_event(name="industrialization_increases",dist=Distribution("uniform","uniform"),cat= 'Economic',enabled=False,dec=[],execution=industrialization_increases)
# precond_industrialization =lambda state, **kwargs: state.get_nation_data("economic_resources")>1000
# m.add_decision(name="industrialization_increases_dec",event=m.events["industrialization_increases"],cond=None,execution=precond_industrialization)


# def average_living_standard_increases( state,**kargs):
#     # new_state=deepcopy(state)
#     state.change_data("economic_resources",-20000)
#     state.change_data("average_living_standard",1)
#     # return new_state
# m.add_simulation_event(name="average_living_standard_increases",dist=Distribution("uniform","uniform"),cat= 'Social',enabled=False,dec=[],execution=average_living_standard_increases)
# precond_average_living_standard=lambda state, **kwargs: state.get_nation_data("economic_resources")>20000
# m.add_decision(name="average_living_standard_increases_dec",event=m.events["average_living_standard_increases"],cond=None,execution=precond_average_living_standard)


# def tourism_increases( state,**kargs):
#     # new_state=deepcopy(state)
#     state.change_data("economic_resources",-5000)
#     state.change_data("tourism",1)
#     # return new_state
# m.add_simulation_event(name="tourism_increases",dist=Distribution("uniform","uniform"),cat= 'Economic',enabled=False,dec=[],execution=tourism_increases)
# precond_tourism=lambda state, **kwargs: state.get_nation_data("economic_resources")>5000
# m.add_decision(name="tourism_increases_dec",event=m.events["tourism_increases"],cond=None,execution=precond_tourism)







def mortality(map, **kwargs):
    for nation in map.provincedict.values():
        nation.population= nation.population * 0.99
m.add_simulation_event(name="mortality",dist=Distribution(name="uniform",dist="uniform",scale=10000),cat= 'Social',enabled=True,dec=[],execution=mortality)

def decrease_industrialization(map, **kwargs):
    for nation in map.nationdict.values():
        if(nation.data.get("industrialization")):
            nation.data["industrialization"]*=0.9
m.add_simulation_event(name="decrease_industrialization",dist=Distribution("expon","expon",scale=10000),cat= 'Economic',enabled=True,dec=[],execution=decrease_industrialization)


def industrialization_increases( state,**kargs):
    # state.change_data("economic_resources",-1000) 
    # state.change_data("industrialization",10)
    
    state.data["economic_resources"]-=2000
    state.data["industrialization"]*=1.1
m.add_decision_event(name="industrialization_increases",cat= 'Economic',execution=industrialization_increases,params=["a"])
precond_industrialization =lambda state, **kwargs: state.get_nation_data("economic_resources")>1000
m.add_decision(name="industrialization_increases_dec",event=m.events["industrialization_increases"],cond=None,execution=precond_industrialization)


def average_living_standard_increases( state,**kargs):
    # state.change_data("economic_resources",-2000)
    # state.change_data("average_living_standard",3)
    state.data["economic_resources"]-=2000
    state.data["average_living_standard"]*=1.1
m.add_decision_event(name="average_living_standard_increases",cat= 'Social',execution=average_living_standard_increases,params=["a"])
precond_average_living_standard=lambda state, **kwargs: state.get_nation_data("economic_resources")>20000
m.add_decision(name="average_living_standard_increases_dec",event=m.events["average_living_standard_increases"],cond=None,execution=precond_average_living_standard)


def tourism_increases( state,**kargs):
    state.data["economic_resources"]-=5000
    state.data["tourism"]*=1.1
    # state.change_data("economic_resources",-5000)
    # state.change_data("tourism",3)
m.add_decision_event(name="tourism_increases",cat= 'Economic',execution=tourism_increases,params=["a"])
precond_tourism=lambda state, **kwargs: state.get_nation_data("economic_resources")>5000
m.add_decision(name="tourism_increases_dec",event=m.events["tourism_increases"],cond=None,execution=precond_tourism)


for nation in m.nationdict.values():
    # for nation in nation.values():
        nation.data["economic_resources"]=100000
        nation.data["industrialization"] =3
        nation.data["average_living_standard"]=3
        nation.data["tourism"]=3


def Simulation_test():
    # print('init',[i.population for i in list(m.provincedict.values())])
    for i in m.nationdict.values():
        print_nation(i)
    a= Simulate(m, Pqueue(m.event_enabled_list)).simulate(10)
    for i in m.nationdict.values():
        print_nation(i)
    # print('end', [i.population for i in list(m.provincedict.values())])

def print_nation(nation):
    print(nation.name,nation.get_nation_all_data())
    # for nation in nation.provinces.values():
    #     print(nation.name,nation.data)
    # print()

Simulation_test()