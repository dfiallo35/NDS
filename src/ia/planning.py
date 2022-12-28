from search_algorithm import *

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
    def next_states(self,state):
        """return the next states from the state"""
        ...
    def select_state(self,state):
        """Check if this state is valid or is a good state"""
        ...

class PlanningProblem(Problem):
    """General Planning Problem"""
    def __init__(self, initial, actions:list):
        super().__init__(actions)
        self.initial = initial
        self.actions = actions
        states=StateNode(initial)

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
    """node of the tree to define the states space"""
    def __init__(self, state, parent=None) -> None:
        self.state = state
        self.parent = parent
        self.sons=[]

    def add_son(self,son):
        self.sons.append(son)
    

        

      
