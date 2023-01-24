from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ia.planning_decisions import *
# import gc


def reaction_for_an_event(map,new_map,changes,event,possible_decisions):
    """Get a list of actions to react this event"""
    t=time.time()    
    nations = get_affected_nations(new_map,changes)
    # print("time to get affected nations",time.time()-t)
    t2=time.time()
    decisions={}
    # possible_decisions=transform_decisions(map.decisions)
    # print("len decisions in planning",len(possible_decisions))
    # print("time to transform decisions",time.time()-t2)
    # print(possible_decisions)
    for nation in nations:
        goal_func,goal_dict=get_target(nation,changes)
        t1=time.time()
        planning_tree=PlanningDecisions(nation,possible_decisions,goal_func,event,goal_dict).make_planning()
        decisions[nation]= get_only_actions(planning_tree)
        # print("time to do the planning",time.time()-t1)
        # delete_tree(get_root(planning_tree))
    return decisions
    

def get_only_actions(tree):
    """Get a list of actions from the states tree of the planning"""
    if (not tree):
        return []
    dec=[i["action"] if i["action"] else None for i in get_path(tree)]
    return [i for i in dec if i]

# def get_root(tree):    
#     if (not tree):
#         return    
#     while tree.parent:
#         tree=tree.parent
#     return tree

# def delete_tree(tree):
#     """Delete the tree of the planning"""
#     if (not tree):
#         return    
#     for child in tree.sons:
#         delete_tree(child)
#     del tree
#     gc.collect()



def transform_decisions( map_decisions):
    """Transform the decisions of the map into a list of actions""" 
    decisions=[]
    for decision in map_decisions.values():
        name=decision.name
        prec=decision.condition
        event_=deepcopy(decision.event)
        cat=decision.event.category
        decisions.append(ActionDecision(action=name ,preconds=prec,event=event_,category=cat))

        # decisions.append(ActionDecision(action=decision.name ,preconds=decision.condition,event=deepcopy(decision.event),category=decision.event.category))
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
    # for province in changes["changed"][nation.name]["changed"].keys():
    for elem in changes["changed"][nation.name]:
        if(gets_worse(elem,changes["changed"][nation.name][elem][0],changes["changed"][nation.name][elem][1])):#todo aqui comprobar si el cambio es positivo o negativo
            if goals.__contains__(elem):
                goals[elem]=goals[elem]+changes["changed"][nation.name][elem][0]
            else:
                goals[elem]=changes["changed"][nation.name][elem][0]
    #convert the goals into a function than comprobate this goal
    goals_function = lambda nation: all([nation.get_nation_data(goal)>=goals[goal] for goal in goals])
    return goals_function,goals



def gets_worse(field,initial_state,final_state):
    """Check if the change is a bad change for the nation"""
    # return final_state.get_nation_data(field)<initial_state.get_nation_data(field)
    return final_state < initial_state