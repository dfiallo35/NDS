try:
    from events.distribution import *
    from elements.map import *
except:    
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))

    from elements.map import *
    from events.distribution import *



#note: un evento siempre define un cambio en el estado del mapa


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
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}'

    def execute(self, map: Map, **kwargs):
        '''
        Execute the event
        '''
        ...

    def next(self) -> float:
        '''
        Returns the time of the next execution of the event
        '''
        return self.distribution.randvar()
    





