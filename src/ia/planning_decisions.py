from planning import *

class PlanningDecisions(PlanningProblem):
    """Planning problem for decisions."""

    def __init__(self, initial, actions,goal_state):
        super().__init__(initial,actions,goal_state)

    def heuristic(domain, state):
        """Heuristic for the decisions problem."""
        return 1

    def next(domain, state, h_values):
        """Get the next action to do in order of priority"""
        ...

    def is_goal_state(state):
        """Check if the state is a goal state."""
        ...

    def select_state(state):
        """Check if this state is valid oris a good state"""
        ...

class Decision(Action):
    def __init__(self, action, preconds, effects ):
       super().__init__(action, preconds, effects)

    def check_preconds(self,state):
        for precond in self.preconds:
            #preconds={"economical_resources":(">",1000)}  example
            if not self.apply_operator(precond.value()[0],state.traits[precond.key()],precond.value()[1]):
                return False
            return True

    
    def make_action(self,state):
        #effects={"economical_resources":("-",1000),"industrialization":("+",1)}    example
        for effect in self.effects:
            state.traits[effect.key()]=self.apply_operator(effect.value()[0], state.traits[effect.key()],effect.value()[1])

    def apply_operator(operator, val1,val2):
        if operator==">":
            return val1 < val2
        if operator==">":
            return val1 > val2
        if operator=="+":
            return val1 + val2
        if operator=="-":
            return val1 - val2

