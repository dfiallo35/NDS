#from search_algorithm import *

# class Problem:
#     def __init__(self,initial_state, actions,goal_state) -> None:
#         self.actions=actions
#         self.initial_state=initial_state
#         self.goal_state=goal_state


class PlanningProblem:#(Problem):
    """General Planning Problem"""
    def __init__(self, initial_state:dict, actions:dict(),goal_state:dict()) -> None:
        super().__init__(actions)
        self.initial_state = initial_state
        self.actions = actions
        self.goal_state = goal_state
        self.states=StateNode(initial_state)
        self.actual_state=self.states
    
    def is_goal_state(self,state):
        """Check if this state superate the objetive"""
        for key in self.goal_state:
            if state[key] < self.goal_state[key]:
                return False
        return True

    def heuristic_function(self):
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
    def __init__(self, state, parent=None) -> None:
        self.state = state
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
    """Breadth-first search algorithm."""
    queue = Queue()
    visited = set()    
    state:StateNode
    actions:StateNode
    # path=[]
    queue.push( problem.initial_state)
    while not queue.empty():
        state = queue.pop()
        if(problem.is_goal_state(state)):
                return state,actions        
        if state not in visited:
            visited.add(state)          
            # for action in problem.actions:
            h_values = problem.heuristic(state,problem.actions)#dict with every action and the valued calculated by the heuristic function
            action=better_action(state,h_values)
            if not action:
                continue
            next_state=action.apply_action(state)
            state.add_son(next_state)
            state=next_state
            actions.add_son(action)
            actions=action
            queue.push(next_state)
            # if action.check_preconds(state): #and problem.select_action(action):
            #     next_state=action.apply_action(state)
            #     state.add_son(next_state)
            #     state=next_state
            #     actions.add_son(action)
            #     actions=action
            #     queue.push(next_state)

            # else: h_values.pop(action)
                    # if problem.select_state(next_state):
                    #     queue.push(next_state)
                        # path.append(next_state)
            # for next_state in problem.next(state, h_values):      
            #     if problem.select_state(next_state):        
            #         queue.push(next_state)
                    # path.append(next_state)
    return state, actions#,path

def better_action(state,h_values):
    """receive a dict of actions and it's values and select the better action, and comprobate that the state accomplish the precondition"""
    if not h_values:
        return None
    action = max(h_values, key=h_values.get)
    if action.check_preconds(state):
        return action
    else:
        h_values.pop(action)
        return better_action(state,h_values)


def get_path(state):
    """Get the path from the initial state to the state"""
    path=[]
    while state.parent:
        path.append(state)
        state=state.parent
    path.append(state)
    return path.reverse()

# def apply_heuristic(problem,state):
#     """aplicate the heuristic h for the search problem."""
#     return problem.heuristic(state)

# def next(domain, state, h_values):
#     """Get the next states in order of priority"""
#     ...

# def is_goal_state(is_goal_state,state):
#     """Check if the state is a goal state."""
#     return is_goal_state(state)



