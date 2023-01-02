from planning_decisions import *

class Nation():
    def __init__(self, name: str, provinces: dict, traits: list):
        #super().__init__(name)
        self.provinces = provinces
        self.data = traits
        self.name = name

# traits = {"weather":2,"economical_resources":123434,"mineral_resources":{"water":2,"iron":2,"petroleum":2},"economic_spheres":{"industrialization":3,"tourism":4},
#                 "inhabitants_number":15443,"IDH":3,"average_living_standard ":2,"population_immigration-migration":(1,4),"territory_km2":2312,
#                 "PIB":1074000000000,"international_relations":{"Spain":3,"EEUU":-5,"Russia":4,"China":3}}

traits = {"weather":2,"economical_resources":123434,"water":2,"iron":2,"petroleum":2,"industrialization":3,"tourism":4,
                "inhabitants_number":15443,"IDH":3,"average_living_standard":2,"population_immigration-migration":(1,4),"territory_km2":2312,
                "PIB":1074000000000,"international_relations":{"Spain":3,"EEUU":-5,"Russia":4,"China":3}}




precond_industrialization =lambda state, **kwargs: state.data["economical_resources"]>1000
precond_average_living_standard=lambda state, **kwargs: state.data["economical_resources"]>20000
precond_tourism=lambda state, **kwargs: state.data["economical_resources"]>5000

def effects_industrialization( state,**kargs):
    new_state=deepcopy(state)
    new_state.data["economical_resources"] -= 1000
    new_state.data["industrialization"]+=1
    return new_state

def effects_average_living_standard( state,**kargs):
    new_state=deepcopy(state)
    new_state.data["economical_resources"] -= 20000
    new_state.data["average_living_standard"]+=1
    return new_state

def effects_tourism( state,**kargs):
    new_state=deepcopy(state)
    new_state.data["economical_resources"] -= 5000
    new_state.data["tourism"]+=1
    return new_state

def goal_statep1(state,**kargs):
    return state.data["industrialization"]>=5 and state.data["average_living_standard"]>=4 and state.data["tourism"]>=5




actions=[Decision(action="increase_industrialization",preconds=precond_industrialization ,effects=effects_industrialization),
         Decision(action="increase_average_living_standard",preconds=precond_average_living_standard ,effects=effects_average_living_standard),
         Decision(action="increase_tourism",preconds=precond_tourism ,effects=effects_tourism)]


# actions=[Decision(action="increase_industrialization",preconds={"economical_resources":(">",1000)},effects={"economical_resources":("-",1000),"industrialization":("+",1)}),
#          Decision(action="increase_average_living_standard",preconds={"economical_resources":(">",20000)},effects={"economical_resources":("-",20000),"average_living_standard":("+",1)}),
#          Decision(action="increase_tourism",preconds={"economical_resources":(">",5000)},effects={"economical_resources":("-",5000),"tourism":("+",1)})]
        #  Decision(action="",preconds={"economical_resources":(">",1000)},effects={"economical_resources":("-",1000),"industrialization":("+",1)}),]

initial_state=Nation(name="Brazil",provinces={},traits=traits)


decisions=PlanningDecisions(initial_state,actions, goal_state=goal_statep1)
#decisions=PlanningDecisions(initial_state,actions, goal_state={"water":(">=",5),"average_living_standard":(">=",3)})

states=decisions.make_planning()

# print(states)
# print([[i["state"].data, "-------------------->",i["action"].action if i["action"] else None,"!!!!!!!!!!!!!!!!!!!!!!!!!!!"] for i in get_path(states)])
print( [i["action"].action if i["action"] else None for i in get_path(states)])



