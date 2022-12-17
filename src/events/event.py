from distribution import *


class Event:
    distribution: Distribution
    enabled: bool

    def __init__(self):
        ...
    
    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the event is enabled
        '''
        return self.enabled

    def execute(self):
        '''
        Execute the event
        '''
        ...

    def next(self) -> float:
        '''
        Returns the time of the next execution of the event
        '''
        return self.distribution.randvar()
    





