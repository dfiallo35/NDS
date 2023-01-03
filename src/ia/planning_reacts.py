from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ia.planning_decisions import *


def reaction_for_an_event(event,map,new_map,changes,time):
    """Get a list of actions to react this event"""
    nations = get_affected_nations(new_map,changes)
    decisions={}
    for nation in nations:
        decisions[nation]= PlanningDecisions(nation,map.decisions,get_target(nation,changes)).make_planning()
    return decisions
    
    
# def apply_event_to_map(event,map):
#     """Apply the event to the map"""
#     ...

# def get_changes_to_map(old_map,new_map):
#     """Compare the map with the map obtained after the event and return the diferences both maps"""
#     ...

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
    goals_function = lambda nation: all([nation.get_nation_data(goal)>=goals[goal] for goal in goals])
    return goals_function
