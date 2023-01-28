#note: En las comparaciones no se tienen en cuenta lso cambios en los nombres de las provincias o naciones
#note: Se asume que estos son invariables
from copy import deepcopy as copy
from inspect import getmembers as gm

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


class Log(Element):
    '''
    The log of the simulation. It is used to store the data of the simulation.
    '''
    def __init__(self, name: str, initial_map):
        super().__init__(name)
        self.log= {}
        self.initial_map= initial_map
    
    
    def add(self, time: int, event, data: dict):
        '''
        Add a new event to the log
        :param time: the time of the event
        :param event: the event
        :param old_map: the map before the event
        :param new_map: the map after the event
        '''
        if self.log.get(time):
            self.log[time].append((event, data))
        else:
            self.log[time]= [(event, data)]
    
    def get_day_data(self, day: int):
        '''
        Return the data of the day
        :param day: the day
        '''
        return self.log.get(day)
    
    def get_nation_data(self, nation: str, data: str):
        l= []
        for time in range(0, list(self.log.keys())[-1]+1):
            if l:
                #fix
                datavar=l[-1]
            else:
                datavar=self.initial_map.get_data(self.initial_map.all[nation], data)

            if self.log.get(time):
                for d in self.log[time]:
                    if d[1] and nation in d[1]['changed'] and data + 'var' in d[1]['changed'][nation]:
                        datavar= d[1]['changed'][nation][data + 'var'][1]
            l.append(datavar)
        return l


    def get_log_data(self, data: str):
        properties= {name:val for (name, val) in gm(Log, lambda x: isinstance(x, property))}
        if data in properties:
            return properties[data].fget(self)
        else:
            raise Exception(f'The map doesn\'t have the attribute {data}')


class Logs:
    def __init__(self):
        self.logs= {}
        self.log_counter= 0
        self.current_log= None
    
    @property
    def all(self):
        return [log for log in self.logs.values()]
    
    def add(self, map):
        self.log_counter+=1
        self.logs['log'+str(self.log_counter)] = Log('log'+str(self.log_counter), map)
        self.current_log= self.logs['log'+str(self.log_counter)]
    
    def get_map_data(self, data: str):
        properties= {name:val for (name, val) in gm(Log, lambda x: isinstance(x, property))}
        if data in properties:
            return properties[data].fget(self)
        else:
            raise Exception(f'The map doesn\'t have the attribute {data}')