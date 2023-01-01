from planning_decisions import *


def reaction_for_an_event(event,map,new_map,changes,time):
    """Get a list of actions to react this event"""
    nations = get_affected_nations(changes)
    decisions={}
    for nation in nations:
        decisions[nation]= PlanningDecisions(nation,map.actions,get_target(nation,changes))
    return decisions
    
    

# def apply_event_to_map(event,map):
#     """Apply the event to the map"""
#     ...

# def get_changes_to_map(old_map,new_map):
#     """Compare the map with the map obtained after the event and return the diferences both maps"""
#     ...

def get_affected_nations(map,changes):
    """From map changes, returns a list of nations that were affected"""
    nations={}
    for nation in map.nations:
        if nation.name in changes["change"]:
            nations.append(nation)
    return nations

def get_target(nation,changes):
    """the goal state that you want to reach with the planning is obtained """
    ...
