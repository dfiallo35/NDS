
class Queue:
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

def bfsearch(problem):
    """Breadth-first search algorithm."""
    queue = Queue()
    visited = set()
    path=[]
    queue.push((0, problem.initial_state))
    while not queue.empty():
        state = queue.pop()
        if goal_state(state):
            return state
        if state not in visited:
            visited.add(state)            
            if(goal_state(goal_state,state)):
                return state
            h_values= apply_heuristic(problem,state) 
            for next_state in problem.next(state, h_values):      
                if problem.select_state(next_state):        
                    queue.push(next_state)
                    path.append(next_state)
    return state,path


def apply_heuristic(problem,state):
    """aplicate the heuristic h for the search problem."""
    return problem.heuristic(state)

def next(domain, state, h_values):
    """Get the next states in order of priority"""
    ...

def goal_state(case_goal_state,state):
    """Check if the state is a goal state."""
    return case_goal_state(state)