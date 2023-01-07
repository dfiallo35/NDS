from elements.elements import *
from elements.map import *
from simulation.simulation import *
from ia.planning_decisions import *
# from ia.test_planning import*

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


# def population_decline(expon, socialism, true, , [])<>{
#         for(prov, map->provinces){
#             a=prov
#             show('before', prov->population)
#             prov.population: expon.irvs(loc: prov->population)
#             show('after', prov->population)            
#     }

# def population_growth(map, **kwargs):
#     for province in map.provincedict.values():
#         province.population= province.population * 1.03
#     return {'enable': ['mortality']}
# m.add_event(name='population_growth' ,distribution= "uniform", cat= 'Economic', enabled= False, execution= population_growth, type= 'unique', decisions=[])

# m.add_event(name='population_growth' ,distribution= "uniform", category= 'Social', enabled= True, execution= population_growth, type= 'unique', decisions=[])

def mortality(map, **kwargs):
    for province in map.provincedict.values():
        province.population= province.population * 0.99
    return {'disable:': ['population_growth']}
m.add_event(name="mortality",dist=Distribution("uniform","uniform"),cat= 'Social',enabled=False,tp="",dec=[],execution=mortality)

def decrease_industrialization(map, **kwargs):
    for province in map.provincedict.values():
        if(province.data.get("industrialization")):
            province.data["industrialization"]-= 1
    return {'disable:': ['decrease_industrialization']}
m.add_event(name="decrease_industrialization",dist=Distribution("uniform","uniform"),cat= 'Economic',enabled=False,tp="",dec=[],execution=decrease_industrialization)


def industrialization_increases( state,**kargs):
    new_state=deepcopy(state)
    new_state.change_data("economic_resources",-1000) 
    new_state.change_data("industrialization",1)
    return new_state
m.add_event(name="industrialization_increases",dist=Distribution("uniform","uniform"),cat= 'Economic',enabled=False,tp="",dec=[],execution=industrialization_increases)
precond_industrialization =lambda state, **kwargs: state.get_nation_data("economic_resources")>1000
m.add_decision(name="industrialization_increases",event=m.events["industrialization_increases"],cond=precond_industrialization)


def average_living_standard_increases( state,**kargs):
    new_state=deepcopy(state)
    new_state.change_data("economic_resources",-20000)
    new_state.change_data("average_living_standard",1)
    return new_state
m.add_event(name="average_living_standard_increases",dist=Distribution("uniform","uniform"),cat= 'Social',enabled=False,tp="",dec=[],execution=average_living_standard_increases)
precond_average_living_standard=lambda state, **kwargs: state.get_nation_data("economic_resources")>20000
m.add_decision(name="average_living_standard_increases",event=m.events["average_living_standard_increases"],cond=precond_average_living_standard)


def tourism_increases( state,**kargs):
    new_state=deepcopy(state)
    new_state.change_data("economic_resources",-5000)
    new_state.change_data("tourism",1)
    return new_state
m.add_event(name="tourism_increases",dist=Distribution("uniform","uniform"),cat= 'Economic',enabled=False, tp="",dec=[],execution=tourism_increases)
precond_tourism=lambda state, **kwargs: state.get_nation_data("economic_resources")>5000
m.add_decision(name="tourism_increases",event=m.events["tourism_increases"],cond=precond_tourism)


for province in m.nationdict["Cuba"].provinces.values():
    province.data["economic_resources"]=100000
    province.data["industrialization"] =3
    province.data["average_living_standard"]=3
    province.data["tourism"]=3



def Simulation_test():
    print('init',[i.population for i in list(m.provincedict.values())])
    a= Simulate(m, Pqueue(m.event_list)).simulate(10)

    print('end', [i.population for i in list(m.provincedict.values())])


Simulation_test()