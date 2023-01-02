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



class MapElement(Element):
    """
    Base class for all the map elements.
    :param name: the element name
    :param extension: the element extension
    """
    def __init__(self, name: str):
        super().__init__(name)
    
    @property
    def data(self):
        return self.__dict__


class Nation(MapElement):
    def __init__(self, name: str, provinces: dict, traits: list=[]):
        super().__init__(name)
        self.provinces = provinces
        self.traits = traits

    @property
    def extension(self) -> float:
        extension = 0
        for prov in self.provinces.values():
            extension += prov.extension
        return extension
    
    @property
    def development(self) -> int:
        development = 0
        for prov in self.provinces.values():
            development += prov.development
        return development

    @property
    def population(self) -> int:
        population = 0
        for prov in self.provinces.values():
            population += prov.population
        return population

    @property
    def contains(self):
        return list(self.provinces.keys())
    
    def get_nation_data(self, data_name: str):
        data= 0
        for prov in self.provinces.values():
            if prov.data.get(data_name):
                data+= prov.data[data_name]
        return data

    def __str__(self):
        return f'{self.name} with extension: {self.extension}, development: {self.development}, population: {self.population}'

    def compare(self, new):
        if self.name == new.name:
            if type(self) == type(new):

                changes= {
                    'new': [],
                    'lost': [],
                    'changed': {}
                }
                new_prov= copy(new.provinces)
                for province in self.provinces:
                    if new.provinces.get(province):
                        new_prov.pop(province)
                        comp= self.provinces[province].compare(new.provinces[province])
                        if comp:
                            changes['changed'][province]= comp
                    else:
                        changes['lost'].append(copy(province))
                changes['new']= [copy(i) for i in new_prov]

                if changes['changed'] or changes['new'] or changes['lost']:
                    return changes
                return None

            else:
                raise Exception(f'Error: "{self.name}" and "{new.name}" are not of the same type')
        else:
            raise Exception(f'Error: "{self.name}" and "{new.name}" are not the same nation')
        

class Province(MapElement):
    def __init__(self, name: str, extension:float, development: int, population: int, **kwargs):
        super().__init__(name)
        self.extension = extension
        self.development = development
        self.population = population
        self.__dict__.update(kwargs)

    def __str__(self):
        return f'{self.name} with extension: {self.extension}, development: {self.development}, population: {self.population}'
    
    def compare(self, new):
        if self.name == new.name:
            if type(self) == type(new):
                changes= {
                    'changed': {},
                    'new': [],
                    'lost': []
                }
                new_data= copy(new.data)
                for key in self.data.keys():
                    if new.data.get(key):
                        new_data.pop(key)
                        if self.data[key] != new.data[key]:
                            changes['changed'][key]= (self.data[key], new.data[key])
                    else:
                        changes['lost'].append(copy(key))
                changes['new']= [copy(i) for i in new_data]

                if changes['changed'] or changes['new'] or changes['lost']:
                    return changes
                return None
            else:
                raise Exception(f'Error: "{self.name}" and "{new.name}" are not of the same type')
        else:
            raise Exception(f'Error: "{self.name}" and "{new.name}" are not the same province')

class Sea(MapElement):
    def __init__(self, name: str, extension:float):
        super().__init__(name)
        self.extension = extension


class Neutral(MapElement):
    def __init__(self, name: str, extension:float):
        super().__init__(name)
        self.extension = extension


#todo: add affinity values limits
class Trait(Element):
    def __init__(self, name: str):
        super().__init__(name)





class object:
    def __init__(self, val):
        self.val= val
    
    @property
    def value(self):
        return self.val
    
    @property
    def type(self):
        return self.__class__.__name__
    
    def __str__(self):
        return str(self.val)


    #Comparison
    def __eq__(self, other):
        return boolean(self.val == other.val)
    
    def __ne__(self, other):
        return boolean(self.val != other.val)
    
    def __lt__(self, other):
        return boolean(self.val < other.val)
    
    def __le__(self, other):
        return boolean(self.val <= other.val)
    
    def __gt__(self, other):
        return boolean(self.val > other.val)
    
    def __ge__(self, other):
        return boolean(self.val >= other.val)
    
    def __and__(self, other):
        return boolean(self.val and other.val)
    
    def __or__(self, other):
        return boolean(self.val or other.val)
    
    def __xor__(self, other):
        return boolean(self.val ^ other.val)
    
    def __invert__(self):
        return boolean(not self.val)
    


class number(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    
    #Arithmetic
    def __add__(self, other):
        return number(self.val + other.val)
    
    def __sub__(self, other):
        return number(self.val - other.val)
    
    def __mul__(self, other):
        return number(self.val * other.val)
    
    def __truediv__(self, other):
        return number(self.val / other.val)
    
    def __floordiv__(self, other):
        return number(self.val // other.val)
    
    def __mod__(self, other):
        return number(self.val % other.val)
    
    def __pow__(self, other):
        return number(self.val ** other.val)
    
    #Unary
    def __neg__(self):
        return number(-self.val)
    
    def __pos__(self):
        return number(self.val)
    
    def __abs__(self):
        return number(abs(self.val))



class string(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    def __add__(self, other):
        return string(self.val + other.val)
    

class boolean(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    def __str__(self):
        return str(self.val).lower()

class array(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    def __add__(self, other):
        return array(self.val + other.val)
    
    def __getitem__(self, key):
        return self.val[key]
    
    def __setitem__(self, key, value):
        self.val[key] = value
    
    def __delitem__(self, key):
        del self.val[key]
    
    def __len__(self):
        return len(self.val)
    
    def __str__(self):
        l= []
        for i in self.val:
            if type(i) == number:
                l.append(i.value)
            else:
                l.append(str(i))
        return str(l)


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


# TIME
class time(object):
    '''
    Time class to handle time. It can be converted to days, months and years.
    Only handle integer values.
    Always return the floor value.
    :param name: the time name
    :param time: the time value
    :param type: the time type. Can be 'd' for days, 'm' for months or 'y' for years
    '''
    def __init__(self, val: int, time: str='d'):
        if time not in ['d', 'm', 'y']:
            raise ValueError('Invalid time type')
        if val < 0:
            raise ValueError('Time cannot be negative')
        self.time= time

        if time == 'd':
            super().__init__(val)
        elif time == 'm':
            super().__init__(val * 30)
        elif time == 'y':
            super().__init__(val * 365)
    

    @property
    def days(self):
        return self.val
    
    @property
    def months(self):
        return self.val // 30

    @property
    def years(self):
        return self.val // 365
    
    def __str__(self):
        if self.time == 'd':
            return str(self.days) + ' days'
        elif self.time == 'm':
            return str(self.months) + ' months'
        elif self.time == 'y':
            return str(self.years) + ' years'
    
    def to_days(self):
        '''
        Convert the time to days
        :param time: the time to be converted
        :return: the time converted to days
        '''
        self.time= 'd'
    
    def to_months(self):
        '''
        Convert the time to months
        :param time: the time to be converted
        :return: the time converted to months
        '''
        self.time= 'm'
    
    def to_years(self):
        '''
        Convert the time to years
        :param time: the time to be converted
        :return: the time converted to years
        '''
        self.time= 'y'


