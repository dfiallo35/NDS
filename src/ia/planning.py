from copy import deepcopy
from scipy.special import factorial

class PlanningProblem:
    """General Planning Problem"""
    def __init__(self, initial_state, actions, goal_state) -> None:
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
        return {action:1 for action in actions.keys()}

    def state_value(self,state,actions_new_states):
        """Function that return the value of an state obtaining the sum between nodes values and heuristic function"""
        hn=self.heuristic_function(state,actions_new_states)
        nv=self.node_values(actions_new_states)
        return {action: hn[action]+nv[action] for action in actions_new_states.keys()}

    def node_values(self,actions):
        """Return the default value for an action"""
        # nv={}
        # for action in actions:
        #     nv[action]=1
        return {action:0 for action in actions.keys()}
        # return nv



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
    iterations=0
    queue.push(StateNode(value={"state":problem.initial_state,"action":None}))
    while not queue.empty():
        iterations+=1
        max_iterations=factorial(len(problem.actions))*5
        print("iterations and max_iterations",iterations,max_iterations)
        if iterations > max_iterations:
            return None
        state = queue.pop()
        if(problem.is_goal_state(state.value["state"])):
                return state
        if state.value["state"] not in visited:
            visited.add(state.value["state"])        
            # h_values = problem.heuristic_function(state.value["state"],problem.actions)#dict with every action and the valued calculated by the heuristic function
            new_states=get_new_states(problem.actions,state.value["state"])
            h_values = problem.state_value(state.value["state"],new_states)#dict with every action and the valued calculated by the heuristic function
            actions_to_do_ordered=ordered_actions_priority(h_values)
            for action in actions_to_do_ordered:
                # next_state=actions_to_do_ordered[action]#action.apply_action(deepcopy(state.value["state"]))
                next_state=StateNode(value={"action":action,"state":new_states[action]})
                state.add_son(next_state)
                queue.push(next_state)
    return None # No solution found

def get_new_states(actions,state):
    """returns a dict with every actions that can be done and the new state obtained"""
    return {action:action.apply_action(deepcopy(state)) for action in actions if action.check_preconds(state)}

def ordered_actions_priority(h_values):
    """receive a dict of actions and it's values and return a list of actions ordered by priority
     and comprobate that the state accomplish the precondition for each one"""
    ordered_actions=[]
    ordered_actions_priority_rec(h_values,ordered_actions)
    return ordered_actions

def ordered_actions_priority_rec(h_values,ordered_actions:list):
    """receive a dict of actions and it's values and return a list of actions ordered by priority
     and comprobate that the state accomplish the precondition for each one"""
    if not h_values:
        return
    action = min(h_values, key=h_values.get)    
    h_values.pop(action)
    # if action.check_preconds(state):
    ordered_actions.append(action)
    ordered_actions_priority_rec(h_values,ordered_actions)



# def bfsearch(problem:PlanningProblem):
#     """Breadth-first search algorithm for a Planning Problem"""    
#     queue = Queue()
#     visited = set()   
#     iterations=0
#     queue.push(StateNode(value={"state":problem.initial_state,"action":None}))
#     while not queue.empty():
#         iterations+=1
#         if iterations > factorial(len(problem.actions)):
#             return None
#         state = queue.pop()
#         if(problem.is_goal_state(state.value["state"])):
#                 return state
#         if state.value["state"] not in visited:
#             visited.add(state.value["state"])        
#             # h_values = problem.heuristic_function(state.value["state"],problem.actions)#dict with every action and the valued calculated by the heuristic function
#             h_values = problem.state_value(state.value["state"],problem.actions)#dict with every action and the valued calculated by the heuristic function
#             actions_to_do_ordered=ordered_actions_priority(state.value["state"],h_values)
#             for action in actions_to_do_ordered:
#                 next_state=action.apply_action(deepcopy(state.value["state"]))
#                 next_state=StateNode(value={"action":action,"state":next_state})
#                 state.add_son(next_state)
#                 queue.push(next_state)


# def ordered_actions_priority(state,h_values):
#     """receive a dict of actions and it's values and return a list of actions ordered by priority
#      and comprobate that the state accomplish the precondition for each one"""
#     ordered_actions=[]
#     ordered_actions_priority_rec(state,h_values,ordered_actions)
#     return ordered_actions

# def ordered_actions_priority_rec(state,h_values,ordered_actions:list):
#     """receive a dict of actions and it's values and return a list of actions ordered by priority
#      and comprobate that the state accomplish the precondition for each one"""
#     if not h_values:
#         return
#     action = min(h_values, key=h_values.get)    
#     h_values.pop(action)
#     if action.check_preconds(state):
#         ordered_actions.append(action)
#     ordered_actions_priority_rec(state,h_values,ordered_actions)


def get_path(state):
    """Get the path from the initial state to the state"""
    path=[]
    if(not state):
        return None
    while state.parent:
        path.append(state.value)
        state=state.parent
    path.append(state.value)
    return path[::-1]




