from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ia.planning.planning_decisions import *


def reaction_for_an_event(new_map,changes,event,possible_decisions):
    """Get a list of actions to react this event"""
    # t=time.time()    
    nations = get_affected_nations(new_map,changes)
    t2=time.time()
    # print("time to get affected nations: ",t2-t)
    decisions={}
    for nation in nations:        
        goal_func,goal_dict=get_target(nation,changes)
        # t1=time.time()
        # print("time to get goal: ",t1-t2)
        planning_tree=PlanningDecisions(nation,possible_decisions,goal_func,event,goal_dict).make_planning()
        # t3=time.time()
        # print("time to make planning: ",t3-t1)
        decisions[nation]= get_only_actions(planning_tree)
        # t4=time.time()
        # print("time to get only actions: ",t4-t3)
    return decisions
    

def get_only_actions(tree):
    """Get a list of actions from the states tree of the planning"""
    if (not tree):
        return []
    return [i["action"]  for i in get_path(tree) if i["action"]]
    # return [i for i in dec if i]

#fix
def transform_decisions( map_decisions):
    """Transform the decisions of the map into a list of actions""" 
    decisions=[]
    for decision in map_decisions.values():
        name=decision.name
        prec=decision.condition
        event_= decision.event.copy()
        cat=decision.event.category
        decisions.append(ActionDecision(action=name ,preconds=prec,event=event_,category=cat))
    return decisions

def get_affected_nations(map,changes):
    """From map changes, returns a list of nations that were affected"""
    nations=[]
    if not changes:
        return []
    for nation in map.nationdict.values():
        if nation.name in changes["changed"]:
            nations.append(nation)
    return nations

def get_target(nation,changes):
    """the goal state that you want to reach with the planning is obtained """
    goals={}
    for elem in changes["changed"][nation.name]:
        if(gets_worse(elem,changes["changed"][nation.name][elem][0],changes["changed"][nation.name][elem][1])):#todo aqui comprobar si el cambio es positivo o negativo
            if goals.__contains__(elem):
                goals[elem]=goals[elem]+changes["changed"][nation.name][elem][0]
            else: 
                goals[elem]=changes["changed"][nation.name][elem][0]
    #convert the goals into a function than comprobate this goala
    goals_function = lambda nation: all([nation.get_nation_data(goal)>=goals[goal] for goal in goals])
    return goals_function,goals



def gets_worse(field,initial_state,final_state):
    """Check if the change is a bad change for the nation"""
    return final_state < initial_state