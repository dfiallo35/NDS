from planning_decisions import *


def reaction_for_an_event(event,map):
    """Get a list of actions to react this event"""
    new_map=apply_event_to_map(event,deepcopy(map))
    changes=get_changes_to_map(map,new_map)
    nations = get_affected_nations(changes,new_map)
    for nation in nations:
        PlanningDecisions(nation,map.actions,get_target(nation,changes))

    

def apply_event_to_map(event,map):
    """Apply the event to the map"""
    ...

def get_changes_to_map(old_map,new_map):
    """Compare the map with the map obtained after the event and return the diferences both maps"""
    ...

def get_affected_nations(changes,new_map):
    """From map changes, returns a list of nations that were affected"""
    ...

def get_target(nation,changes):
    """the goal state that you want to reach with the planning is obtained """
    ...
