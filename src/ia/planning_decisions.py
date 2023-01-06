from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ia.planning import *

class PlanningDecisions(PlanningProblem):
    """Planning problem for decisions."""

    def __init__(self, initial, actions,goal_state):
        super().__init__(initial,actions,goal_state)

    def heuristic_function(self,state, actions):
        """Heuristic for the decisions problem."""
        h_values={}
        for action in actions:
            h_values[action]=1
        return h_values


    def is_goal_state(self,state):
        """Check if the state is a goal state."""
        return self.goal_state(state)

class Decision(Action):
    def __init__(self, action, preconds, effects):
       super().__init__(action, preconds, effects)


    def check_preconds(self,state):
        """Check if the preconditions are true"""      
        return self.preconds(state)

    def apply_action(self, state):     
        """return the new state after apply it an action"""   
        return self.effects(state)


