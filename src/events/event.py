try:
    from events.distribution import *
except:    
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))

    from events.distribution import *



class Category:
    def __init__(self, name: str):
        self.name= name
        self.decisions= list()
    
    def add_decision(self, decision):
        self.decisions.append(decision)
    
    def __str__(self) -> str:
        return f'{self.name}'

class Politic(Category):
    def __init__(self):
        super().__init__('Politic')

class Economic(Category):
    def __init__(self):
        super().__init__('Economic')

class Social(Category):
    def __init__(self):
        super().__init__('Social')

#note: un evento siempre define un cambio en el estado del mapa


#todo: unique events(works only one time)

class Event:
    def __init__(self, name: str, distribution: Distribution, category: Category, enabled: bool= True):
        self.name= name
        self.category= category
        self.distribution= distribution
        self.enabled= enabled
    
    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the event is enabled
        '''
        return self.enabled
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}'

    def execute(self, map, **kwargs):
        '''
        Execute the event
        '''
        ...

    def next(self) -> float:
        '''
        Returns the time of the next execution of the event
        '''
        return self.distribution.randvar()
    
    def __str__(self) -> str:
        return f'{self.name}'
    




