from distribution import *


class Event:
    distribution: Distribution

    def __init__(self):
        ...

    def run(self):
        '''
        Execute the event
        '''
        ...

    def next(self):
        '''
        Returns the time of the next execution of the event
        '''
        return self.distribution.randvar()
    







