from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ia.planning_decisions import *


def reaction_for_an_event(map,new_map,changes):
    """Get a list of actions to react this event"""
    nations = get_affected_nations(new_map,changes)
    decisions={}
    possible_decisions=transform_decisions(map.decisions)
    for nation in nations:
        decisions[nation]= get_only_actions(PlanningDecisions(nation,possible_decisions,get_target(nation,changes)).make_planning())
    return decisions
    

def get_only_actions(tree):
    """Get a list of actions from the states tree of the planning"""
    return [i["action"] if i["action"] else None for i in get_path(tree)]

def transform_decisions(map_decisions):
    """Transform the decisions of the map into a list of actions""" 
    decisions=[]
    for decision in map_decisions:
        decisions.append(Decision(decision.name ,decision.preconds,decision.event))
    return decisions

def get_affected_nations(map,changes):
    """From map changes, returns a list of nations that were affected"""
    nations=[]
    for nation in map.nationdict.values():
        if nation.name in changes["changed"]:
            nations.append(nation)
    return nations

def get_target(nation,changes):
    """the goal state that you want to reach with the planning is obtained """
    goals={}
    for province in changes["changed"][nation.name]["changed"].keys():
        for elem in changes["changed"][nation.name]["changed"][province]["changed"]:
            if goals.__contains__(elem):
                goals[elem]=goals[elem]+changes["changed"][nation.name]["changed"][province]["changed"][elem][0]
            else:
                goals[elem]=changes["changed"][nation.name]["changed"][province]["changed"][elem][0]
    #convert the goals into a function than comprobate this goal
    #todo aqui comprobar si el cambio es positivo o negativo
    goals_function = lambda nation: all([nation.get_nation_data(goal)>=goals[goal] for goal in goals])
    return goals_function
