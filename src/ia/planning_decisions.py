from planning import *

class PlanningDecisions(PlanningProblem):
    """Planning problem for decisions."""

    def __init__(self, initial, actions,goal_state):
        super().__init__(initial,actions,goal_state)

    def heuristic(state, actions):
        """Heuristic for the decisions problem."""
        h_values={}
        for action in actions:
            h_values[action]=1


    # def next(self,domain, state, h_values):
    #     """Get the next action to do in order of priority"""
    #     ...

    def is_goal_state(self,state):
        """Check if the state is a goal state."""
        for goal in self.goal_state:
            #preconds={"economical_resources":(">",1000)}  example
            if not apply_operator(self.goal_state[goal][0],state.traits[goal],self.goal_state[goal][1]):
                return False
            return True 

    # def select_state(self,state):
    #     """Check if this state is valid oris a good state"""
    #     ...


class Decision(Action):
    def __init__(self, action, preconds, effects):
       super().__init__(action, preconds, effects)

    def check_preconds(self,state):
        for precond in self.preconds:
            #preconds={"economical_resources":(">",1000)}  example
            if not apply_operator(precond.value()[0],state.traits[precond.key()],precond.value()[1]):
                return False
            return True

    
    def make_action(self,state):
        #effects={"economical_resources":("-",1000),"industrialization":("+",1)}    example
        for effect in self.effects:
            state.traits[effect]=apply_operator(self.effects[effect][0], state.traits[effect],self.effects[effect][1])

def apply_operator(operator, val1,val2):
    if operator==">":
        return val1 < val2
    if operator==">":
        return val1 > val2
    if operator=="+":
        return val1 + val2
    if operator=="-":
        return val1 - val2

