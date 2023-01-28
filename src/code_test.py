from elements.elements import *
from elements.map import *
from simulation.simulation import *
from ia.planning.planning_decisions import *
# from ia.test_planning import*

m = Map()
m.add_nation('Cuba',10, 10)
m.add_nation('USA',100, 100)

m.add_category('Social')
m.add_category('Economic')
m.add_trait('Comunist')


def mortality(map, **kwargs):
    for nation in map.nationdict.values():
        nation.population= nation.population * 0.99
m.add_simulation_event(name="mortality",dist=Distribution(name="uniform",dist="uniform",scale=10000),cat= 'Social',enabled=True,dec=[],execution=mortality)

def decrease_industrialization(map, **kwargs):
    for nation in map.nationdict.values():
        if(nation.data.get("industrialization")):
            nation.data["industrialization"]*=0.9
m.add_simulation_event(name="decrease_industrialization",dist=Distribution("expon","expon",scale=10, size=100),cat= 'Economic',enabled=True,dec=[],execution=decrease_industrialization)

def bloqueo_effect(map, **kwargs):
    for nation in map.nationdict.values():
        if nation.name!="Cuba":
            continue
        if(nation.data.get("industrialization")):
            nation.data["industrialization"]*=0.9
        if(nation.data.get("average_living_standard")):
            nation.data["average_living_standard"]*=0.9
        if(nation.data.get("tourism")):
            nation.data["tourism"]*=0.9
m.add_simulation_event(name="bloqueo_effect",dist=Distribution("expon","expon",scale=10000),cat= 'Economic',enabled=True,dec=[],execution=bloqueo_effect)


def industrialization_increases( state,**kargs):
    state.data["economic_resources"] = state.data["economic_resources"] - 2000
    state.data["industrialization"] *= 1.2
m.add_decision_event(name="industrialization_increases",cat= 'Economic',execution=industrialization_increases,params=["a"])
precond_industrialization =lambda state, **kwargs: state.get_nation_data("economic_resources")>1000
m.add_decision(name="industrialization_increases_dec",event=m.events["industrialization_increases"],cond=None,execution=precond_industrialization)



def average_living_standard_increases( state,**kargs):
    state.data["economic_resources"]=state.data["economic_resources"]-2000
    state.data["average_living_standard"]*=1.2
m.add_decision_event(name="average_living_standard_increases",cat= 'Social',execution=average_living_standard_increases,params=["a"])
precond_average_living_standard=lambda state, **kwargs: state.get_nation_data("economic_resources")>20000
m.add_decision(name="average_living_standard_increases_dec",event=m.events["average_living_standard_increases"],cond=None,execution=precond_average_living_standard)


def tourism_increases( state,**kargs):
    state.data["economic_resources"]=state.data["economic_resources"]-5000
    state.data["tourism"]*=1.2
m.add_decision_event(name="tourism_increases",cat= 'Economic',execution=tourism_increases,params=["a"])
precond_tourism=lambda state, **kwargs: state.get_nation_data("economic_resources")>5000
m.add_decision(name="tourism_increases_dec",event=m.events["tourism_increases"],cond=None,execution=precond_tourism)


for nation in m.nationdict.values():
        nation.data["economic_resources"]=100000
        nation.data["industrialization"] =3
        nation.data["average_living_standard"]=3
        nation.data["tourism"]=3


def Simulation_test():
    for i in m.nationdict.values():
        print_nation(i)
    t= time.time()

    a= Simulate(m, Pqueue(m.event_enabled_list)).simulate(30)
    print("time",time.time()-t)
    for i in m.nationdict.values():
        print_nation(i)

def print_nation(nation):
    print(nation.name,nation.get_nation_all_data())

Simulation_test()