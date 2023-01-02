try:
    from events.distribution import *
except:    
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))

    from events.distribution import *





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





