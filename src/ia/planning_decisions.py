from planning import *

class PlanningDecisions(PlanningProblem):

    def __init__(self, initial, actions):
        super().__init__(initial,actions)

    def decisions_heuristic(domain, state):
        """Heuristic for the decisions problem."""
        ...

    def decisions_next(domain, state, goal_state, h_values):
        """Get the next states in order of priority"""
        ...

    def decisions_goal_state(state):
        """Check if the state is a goal state."""
        ...

    def select_state(state):
        """Check if this state is valid oris a good state"""
        ...

class Decision(Action):
    def __init__(self, action, precond, effect ):
       super().__init__(action, precond, effect)

    def check_preconds(self,action):
        ...
    
    def make_action(self):
        ...
