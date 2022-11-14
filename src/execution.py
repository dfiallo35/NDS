from functions import *
from queue import PriorityQueue

class Execution:
    def __init__(self) -> None:
        self.elements= dict()
        self.execution_queue = PriorityQueue()
        
    def run(self):
        raise NotImplementedError

