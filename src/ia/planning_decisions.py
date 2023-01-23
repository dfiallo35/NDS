from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ia.planning import *

class PlanningDecisions(PlanningProblem):
    """Planning problem for decisions."""

    def __init__(self, initial, actions,goal_state,event,goal_state_dict:dict):
        super().__init__(initial,actions,goal_state)
        self.event=event
        self.goal_state_dict=goal_state_dict

    def heuristic_function(self,state, actions_states):
        """Heuristic for the decisions problem."""
        h_values={}
        for action in actions_states.keys():
            h_values[action]=5
            if(action.category==self.event.category.name):
                h_values[action]-=2
            if(action.category=="Economic" or action.category=="Economic"):
                h_values[action]-=1

            for goal in self.goal_state_dict.keys():
                ratio_old= state.data[goal]/self.goal_state_dict[goal]*5
                ratio_new=actions_states[action].data[goal]/self.goal_state_dict[goal]*5
                # ratio_new=self.get_property_with_name(actions_states,action,goal)/self.goal_state_dict[goal]*5
                h_values[action]-= (ratio_new-ratio_old)
        return h_values

    # def get_property_with_name(self,actions_states, action_, name):
    #     """Get the property via its name"""
    #     for action in actions_states.keys():
    #         if(action.action==action_):
    #             return actions_states[action].data[name]

    def state_value(self,state,actions_states):
        """Function that return the value of an state obtaining the sum between nodes values and heuristic function"""
        hn=self.heuristic_function(state,actions_states)
        nv=self.node_values(actions_states)
        return {action: hn[action]+nv[action] for action in actions_states.keys() if (hn[action]+nv[action]<5)}


    def is_goal_state(self,state):
        """Check if the state is a goal state."""
        return self.goal_state(state)


class ActionDecision(Action):
    def __init__(self, action, preconds, event,category):
        super().__init__(action, preconds, event.execute)
        self.event=event
        self.category=category

    def check_preconds(self,state):
        """Check if the preconditions are true"""      
        return self.preconds(state)

    def apply_action(self, state):     
        """return the new state after apply it an action""" 
        # self.event.add_nation(state)
        # self.event.execute()
        new_event=self.event.get_event(state)
        new_event.execute()
        return state


