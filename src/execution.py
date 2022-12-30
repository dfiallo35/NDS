from elements.map import Map
from elements.elements import *


#todo: get the execution list
#todo: generar codigo de funciones
#todo: terminar value method
class Code:
    def __init__(self) -> None:
        self.elements= dict()
        self.vars= dict()

        self.execution_list = list()
        self.map= Map()

    def run(self):
        '''
        Run the code
        '''
        next= self.next()
        while next:
            next.execute()
            next= self.next()
    
    def next(self):
        '''
        Run the next line of code
        '''
        ...
    
    def add_element(self, element: str, **kwargs):
        '''
        Add an element to the map
        :param element: the element to add
        '''
        elements={
            'nation': self.map.add_nation,
            'province': self.map.add_province,
            'sea': self.map.add_sea,
            'neutral': self.map.add_neutral
        }
        if element in elements:
            elements[element](**kwargs)
        else:
            raise Exception('The element is not recognized')
