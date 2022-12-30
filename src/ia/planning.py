#from search_algorithm import *

# class Problem:
#     def __init__(self,initial_state, actions,goal_state) -> None:
#         self.actions=actions
#         self.initial_state=initial_state
#         self.goal_state=goal_state


from copy import deepcopy


class PlanningProblem:#(Problem):
    """General Planning Problem"""
    def __init__(self, initial_state:dict, actions:list, goal_state:dict()) -> None:
        #super().__init__(actions)
        self.initial_state = initial_state
        self.actions = actions
        self.goal_state = goal_state
        self.states = StateNode(initial_state)
        self.actual_state = self.states
    
    def is_goal_state(self,state):
        """Check if this state superate the objetive"""
        for key in self.goal_state:
            if state[key] < self.goal_state[key]:
                return False
        return True

    def make_planning(self):
        state=search(self)
        return state


    def heuristic_function(self,state,actions):
        """An heuristic function definited for the concret problem"""
        raise NotImplementedError
    # def apply_action_to_state(self,action,state):
    #     """return the new state after apply it an action"""
    #     raise NotImplementedError
    # def next_states(self,state):
    #     """return the next states from the state"""
    #     raise NotImplementedError
    # def select_state(self,state):
    #     """Check if this state is valid or is a good state"""
    #     raise NotImplementedError
    # def select_action(self,action):
    #     """Check if this action is valid or is a good action"""
    #     raise NotImplementedError

class Action:
    """General Action, express the action, preconditions and effects to make the planning problem"""
    def __init__(self, action, preconds, effects ):
       self.action=action
       self.preconds=preconds
       self.effects=effects

    def check_preconds(self,state):  
        """Check if the preconditions are true"""      
        raise NotImplementedError
    
    def apply_action(self, state):     
        """return the new state after apply it an action"""   
        raise NotImplementedError

class StateNode:
    """node of the tree to define the states space"""
    def __init__(self, value, parent=None) -> None:
        self.value = value
        self.parent = parent
        self.sons=[]

    def add_son(self,son):
        self.sons.append(son)
        son.parent=self
    
    def get_sons(self):
        return self.sons
    


class Queue:
    """Queue data structure."""
    def __init__(self):
        self.queue = []
        
    def push(self, element):        
        self.queue.append(element)
    
    def peek(self):
        return self.queue[0]
    
    def pop(self):
        return self.queue.pop(0)
    
    def empty(self):
        return len(self.queue) == 0

def search(problem):
    return bfsearch(problem)       

def bfsearch(problem:PlanningProblem):
    """Breadth-first search algorithm for a Planning Problem"""
    queue = Queue()
    visited = set()    
    # states:StateNode=None
    # actions:StateNode=None
    # possible_actions:list=problem.actions    
    queue.push(StateNode(value={"state":problem.initial_state,"action":None}))
    while not queue.empty():
        state = queue.pop()
        if(problem.is_goal_state(state.value["state"])):
                return state      
        if state.value["state"] not in visited:
            visited.add(state.value["state"])          
            h_values = problem.heuristic_function(state.value["state"],problem.actions)#dict with every action and the valued calculated by the heuristic function
            actions_to_do_ordered=ordered_actions_priority(state.value["state"],h_values)
            for action in actions_to_do_ordered:
                next_state=action.apply_action(deepcopy(state.value["state"]))
                next_state=StateNode(value={"action":action,"state":next_state})
                state.add_son(next_state)
                # stat=next_state
                queue.push(next_state)
    return state


def ordered_actions_priority(state,h_values):
    """receive a dict of actions and it's values and return a list of actions ordered by priority
     and comprobate that the state accomplish the precondition for each one"""
    ordered_actions=[]
    ordered_actions_priority_rec(state,h_values,ordered_actions)
    return ordered_actions

def ordered_actions_priority_rec(state,h_values,ordered_actions:list):
    """receive a dict of actions and it's values and return a list of actions ordered by priority
     and comprobate that the state accomplish the precondition for each one"""
    if not h_values:
        return
    action = max(h_values, key=h_values.get)    
    h_values.pop(action)
    if action.check_preconds(state):
        ordered_actions.append(action)
    ordered_actions_priority_rec(state,h_values,ordered_actions)




# def bfsearch(problem:PlanningProblem):
#     """Breadth-first search algorithm for a Planning Problem"""
#     queue = Queue()
#     visited = set()    
#     states:StateNode=None
#     actions:StateNode=None
#     # path=[]
#     possible_actions:list=problem.actions
#     queue.push( problem.initial_state)
#     while not queue.empty():
#         state = queue.pop()
#         if(problem.is_goal_state(state)):
#                 return states, actions        
#         if state not in visited:
#             visited.add(state)          
#             # for action in problem.actions:
#             h_values = problem.heuristic_function(state,possible_actions)#dict with every action and the valued calculated by the heuristic function
#             action=StateNode(better_action(state,h_values))  
#             possible_actions.remove(action.value)
#             if not action:
#                 continue
#             next_state=StateNode(action.value.apply_action(state))
#             if states:
#                 states.add_son(next_state)
#             states=next_state
#             if actions: 
#                 actions.add_son(action)
#             actions=action
#             queue.push(next_state.value)
#     return states, actions

# def better_action(state,h_values):
#     """receive a dict of actions and it's values and select the better action, and comprobate that the state accomplish the precondition"""
#     if not h_values:
#         return None
#     action = max(h_values, key=h_values.get)
#     if action.check_preconds(state):
#         return action
#     else:
#         h_values.pop(action)
#         return better_action(state,h_values)


def get_path(state):
    """Get the path from the initial state to the state"""
    path=[]
    while state.parent:
        path.append(state.value)
        state=state.parent
    path.append(state.value)
    return path[::-1]
    #return path.reverse()

# def apply_heuristic(problem,state):
#     """aplicate the heuristic h for the search problem."""
#     return problem.heuristic(state)

# def next(domain, state, h_values):
#     """Get the next states in order of priority"""
#     ...

# def is_goal_state(is_goal_state,state):
#     """Check if the state is a goal state."""
#     return is_goal_state(state)



