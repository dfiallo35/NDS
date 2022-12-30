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


#todo: instant events (works when the event is created)
class Event:
    def __init__(self, name: str, distribution: Distribution, category: Category, execution, enabled: bool= True, type: str= None):
        self.name= name
        self.category= category
        self.distribution= distribution
        self.enabled= enabled
        self.type= type
        self.execution= execution
    
    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the event is enabled
        '''
        return self.enabled
    
    def __str__(self) -> str:
        return f'{self.name}'

    def execute(self, map, **kwargs):
        '''
        Execute the event
        '''
        if self.type == 'unique':
            self.enabled= False
        return self.execution(map, **kwargs)

    def next(self) -> float:
        '''
        Returns the time of the next execution of the event
        '''
        return self.distribution.randvar()
    
    def __str__(self) -> str:
        return f'{self.name}'
    




