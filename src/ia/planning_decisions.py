from planning import *

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
        for goal in self.goal_state:
            if not apply_operator(self.goal_state[goal][0],state.traits[goal],self.goal_state[goal][1]):
                return False
        return True 


class Decision(Action):
    def __init__(self, action, preconds, effects):
       super().__init__(action, preconds, effects)

    def check_preconds(self,state):
        for precond in self.preconds:
            if not apply_operator(self.preconds[precond][0],state.traits[precond],self.preconds[precond][1]):
                return False
        return True
    
    def apply_action(self, state):     
        """return the new state after apply it an action"""   
        new_state=deepcopy(state)
        self.make_action(new_state)
        return new_state
    
    def make_action(self,state):
        for effect in self.effects:
            state.traits[effect]=apply_operator(self.effects[effect][0], state.traits[effect],self.effects[effect][1])

def apply_operator(operator, val1,val2):
    if operator=="<":
        return val1 < val2
    if operator==">":
        return val1 > val2
    if operator=="<=":
        return val1 <= val2
    if operator==">=":
        return val1 >= val2
    if operator=="+":
        return val1 + val2
    if operator=="-":
        return val1 - val2
    return False

