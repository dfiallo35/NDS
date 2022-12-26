
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

def search(domain, initial_state, goal_state, heuristic):
    return bfsearch(domain, initial_state, goal_state, heuristic)

def bfsearch(domain, initial_state, goal_state, heuristic,case_goal_state):
    """Breadth-first search algorithm."""
    queue = Queue()
    visited = set()
    queue.push((0, initial_state))
    while not queue.empty():
        state = queue.pop()
        if goal_state(state):
            return state
        if state not in visited:
            visited.add(state)            
            if(goal_state(case_goal_state,state)):
                return state
            h_values= apply_heuristic(domain,state,heuristic) 
            for next_state in next(domain, state, h_values):                
                queue.push()

    return state


def apply_heuristic(domain,state,h):
    """aplicate the heuristic h for the search problem."""
    return h(domain,state)

def next(domain, state, h_values):
    """Get the next states in order of priority"""
    ...

def goal_state(case_goal_state,state):
    """Check if the state is a goal state."""
    return case_goal_state(state)