class Element:
    """
    Base class for all the simulation elements.
    :param name: the element name
    """
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class MapElement(Element):
    """
    Base class for all the map elements.
    :param name: the element name
    :param extension: the element extension
    """
    def __init__(self, name: str):
        super().__init__(name)


class Nation(MapElement):
    def __init__(self, name: str, provinces: dict, traits: list):
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


class Province(MapElement):
    def __init__(self, name: str, extension:float, development: int, population: int):
        super().__init__(name)
        self.extension = extension
        self.development = development
        self.population = population


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
    def __init__(self, name: str, affinity: dict[str: int]):
        super().__init__(name)
        self.affinity = affinity
    
    def __str__(self):
        return self.name + ' ' + str(self.afinity)



# TIME
class Time(Element):
    def __init__(self, name: str, time: int):
        super().__init__(name)
        self.time= time
    
    @property
    def get_time(self):
        return self.time
    
    @property
    def days(self):
        return self.to_days().time
    
    @property
    def months(self):
        return self.to_months().time
    
    @property
    def years(self):
        return self.to_years().time
    
    def to_days(self):
        '''
        Convert the time to days
        :param time: the time to be converted
        :return: the time converted to days
        '''
        ...
    
    def to_months(self):
        '''
        Convert the time to months
        :param time: the time to be converted
        :return: the time converted to months
        '''
        ...
    
    def to_years(self):
        '''
        Convert the time to years
        :param time: the time to be converted
        :return: the time converted to years
        '''
        ...

class Day(Time):
    def __init__(self, name: str, time: int):
        super().__init__(name, time)
    
    def __str__(self):
        return str(self.time) + ' days'
    
    def to_days(self):
        '''
        Convert the time to days
        :param time: the time to be converted
        :return: the time converted to days
        '''
        return Day(self.name, self.time)
    
    def to_months(self):
        '''
        Convert the time to months
        :param time: the time to be converted
        :return: the time converted to months
        '''
        return Month(self.name, self.time / 30)
    
    def to_years(self):
        '''
        Convert the time to years
        :param time: the time to be converted
        :return: the time converted to years
        '''
        return Year(self.name, self.time / 365)

class Month(Time):
    def __init__(self, name: str, time: int):
        super().__init__(name, time)
    
    def __str__(self):
        return str(self.time) + ' months'
    
    def to_days(self):
        '''
        Convert the time to days
        :param time: the time to be converted
        :return: the time converted to days
        '''
        return Day(self.name, self.time * 30)
    
    def to_months(self):
        '''
        Convert the time to months
        :param time: the time to be converted
        :return: the time converted to months
        '''
        return Month(self.name, self.time)
    
    def to_years(self):
        '''
        Convert the time to years
        :param time: the time to be converted
        :return: the time converted to years
        '''
        return Year(self.name, self.time / 12)

class Year(Time):
    def __init__(self, name: str, time: int):
        super().__init__(name, time)
    
    def __str__(self):
        return str(self.time) + ' years'
    
    def to_days(self):
        '''
        Convert the time to days
        :param time: the time to be converted
        :return: the time converted to days
        '''
        return Day(self.name, self.time * 365)
    
    def to_months(self, time: int):
        '''
        Convert the time to months
        :param time: the time to be converted
        :return: the time converted to months
        '''
        return Month(self.name, time * 12)
    
    def to_years(self):
        '''
        Convert the time to years
        :param time: the time to be converted
        :return: the time converted to years
        '''
        return Year(self.name, self.time)


class object:
    def __init__(self, val) -> None:
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