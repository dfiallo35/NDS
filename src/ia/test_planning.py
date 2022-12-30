from planning_decisions import *

class Nation():
    def __init__(self, name: str, provinces: dict, traits: list):
        #super().__init__(name)
        self.provinces = provinces
        self.traits = traits
        self.name = name

# traits = {"weather":2,"economical_resources":123434,"mineral_resources":{"water":2,"iron":2,"petroleum":2},"economic_spheres":{"industrialization":3,"tourism":4},
#                 "inhabitants_number":15443,"IDH":3,"average_living_standard ":2,"population_immigration-migration":(1,4),"territory_km2":2312,
#                 "PIB":1074000000000,"international_relations":{"Spain":3,"EEUU":-5,"Russia":4,"China":3}}

traits = {"weather":2,"economical_resources":123434,"water":2,"iron":2,"petroleum":2,"industrialization":3,"tourism":4,
                "inhabitants_number":15443,"IDH":3,"average_living_standard ":2,"population_immigration-migration":(1,4),"territory_km2":2312,
                "PIB":1074000000000,"international_relations":{"Spain":3,"EEUU":-5,"Russia":4,"China":3}}

actions=[Decision(action="increase_industrialization",preconds={"economical_resources":(">",1000)},effects={"economical_resources":("-",1000),"industrialization":("+",1)}),
         Decision(action="increase_average_living_standard",preconds={"economical_resources":(">",20000)},effects={"economical_resources":("-",20000),"average_living_standard":("+",1)})]
        #  Decision(action="",preconds={"economical_resources":(">",1000)},effects={"economical_resources":("-",1000),"industrialization":("+",1)}),
        #  Decision(action="",preconds={"economical_resources":(">",1000)},effects={"economical_resources":("-",1000),"industrialization":("+",1)}),]

initial_state=Nation(name="Brazil",provinces={},traits=traits)

decisions=PlanningDecisions(initial_state,actions, goal_state={"industrialization":(">=",4)})
states,actions=decisions.make_planning()

for i in(get_path(states)):
    print(i.traits)
for i in (get_path(actions)):
    print(i.action)


