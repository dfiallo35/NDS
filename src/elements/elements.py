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