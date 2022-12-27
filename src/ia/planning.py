

class Problem:
    def __init__(self) -> None:
        self.actions:dict()#dict that contains actions with their expected result


    def goal_state(self,state):
        """Check if this state superate the objetive"""
        ...
    def heuristic_function(self):
        """An heuristic function definited for the concret problem"""
        ...
    def apply_action_to_state(self,action,state):
        """return the new state after apply it an action"""
        ...