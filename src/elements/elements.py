#note: En las comparaciones no se tienen en cuenta lso cambios en los nombres de las provincias o naciones
#note: Se asume que estos son invariables
from copy import deepcopy as copy

class Element:
    """
    Base class for all the simulation elements.
    :param name: the element name
    """
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name
    
    
    def compare(self, other):
        if type(self) == type(other):
            changes= {}
            for key in self.__dict__.keys():
                if self.__dict__[key] != other.__dict__[key]:
                    changes[key]= (self.__dict__[key], other.__dict__[key])
            return changes
        else:
            raise Exception(f'Error: "{self.name}" and "{other.name}" are not of the same type')


class Log:
    '''
    The log of the simulation. It is used to store the data of the simulation.
    '''
    def __init__(self) -> None:
        self.log= {}
    
    def add(self, time: int, event, old_map, new_map):
        '''
        Add a new event to the log
        :param time: the time of the event
        :param event: the event
        :param old_map: the map before the event
        :param new_map: the map after the event
        '''
        ...
