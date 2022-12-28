

class Problem:
    def __init__(self,actions) -> None:
        self.actions=actions


    def goal_state(self,state):
        """Check if this state superate the objetive"""
        ...
    def heuristic_function(self):
        """An heuristic function definited for the concret problem"""
        ...
    def apply_action_to_state(self,action,state):
        """return the new state after apply it an action"""
        ...


class PlanningProblem(Problem): 

    def __init__(self, initial, actions):
        super().__init__(actions)
        self.initial = initial
        self.actions = actions

class Action:
    
    def __init__(self, action, precond, effect ):
       self.action=action
       self.precond=precond
       self.effect=effect

    def check_preconds(self,action):
        ...
    
    def make_action(self):
        ...

class StateNode:
    def __init__(self,state,father):
        self.state=state
        self.father=father
        self.sons=[]
    
    def get_father(self):
        return self.father
    
    
        

      
