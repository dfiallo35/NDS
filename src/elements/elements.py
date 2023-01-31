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
    
    def day(self, day: int):
        '''
        Return the data of the day
        :param day: the day
        '''
        return self.log.get(day)
    
    
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
        for time in range(0, max(list(self.log.keys()))+1):
            if l:
                datavar=l[-1]
            else:
                datavar=self.initial_map.get_data(self.initial_map.all[nation], data)

            if self.log.get(time):
                for d in self.log[time]:
                    if nation in d[1]['changed'] and data + 'var' in d[1]['changed'][nation]:
                        if isinstance(d[1]['changed'][nation][data + 'var'], tuple):
                            datavar= d[1]['changed'][nation][data + 'var'][1]
                        else:
                            datavar= d[1]['changed'][nation][data + 'var']
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
    
    # @property
    # def all(self):
    #     return [log for log in self.logs.values()]
    
    @property
    def all(self):
        if self.logs.get('log1'):
            return {**self.logs, 'log_avg': self.avg()}
        else:
            return self.logs
    
    #fix end time
    def avg(self):
        new_log = Log('log_avg', self.logs['log1'].initial_map)
        data= set()
        nations= set()
        max_time= max([max(list(i.log.keys())) for i in list(self.logs.values())])
        for time in range(0, max_time+1):
            for log in self.logs.values():
                if log.log.get(time):
                    for data_in_time in log.log[time]:
                        for nation in data_in_time[1]['changed']:
                            nations.add(nation)
                            for d in data_in_time[1]['changed'][nation]:
                                data.add(d[:-3])

        new_data= {log: {} for log in self.logs}
        for log in self.logs.values():
            for nation in nations:
                for d in data:
                    data_get= log.get_nation_data(nation, d)
                    if len(data_get) < max_time+1:
                        data_get.extend([data_get[-1]]*(max_time+1-len(data_get)))
                    
                    if not new_data[log.name].get(nation):
                        new_data[log.name][nation]= {d: data_get}
                    else:
                        new_data[log.name][nation].update({d: data_get})
        
        for time in range(0, max_time+1):
            current_data= {'changed': {n:{} for n in nations}}
            for nation in nations:
                for d in data:
                    if not current_data['changed'].get(nation):
                        current_data['changed'][nation]={d+'var': sum([i[nation][d][time] for i in new_data.values()]) / len(self.logs)}
                    else:
                        current_data['changed'][nation].update({d+'var': sum([i[nation][d][time] for i in new_data.values()]) / len(self.logs)})
            new_log.add(time, None, current_data)
        return new_log

    def fill_list(self, list, length):
        if len(list) < length:
            list.extend([list[-1]]*(length-len(list)))
        return list



    
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