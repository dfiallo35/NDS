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
    def __init__(self, name: str, extension: float):
        super().__init__(name)
        self.extension = extension


class Nation(Element):
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
        return self.provinces.keys()


class Province(MapElement):
    def __init__(self, name: str, extension:float, development: int, population: int):
        super().__init__(name, extension)
        self.development = development
        self.population = population


class Sea(MapElement):
    def __init__(self, name: str, extension:float):
        super().__init__(name, extension)


class Neutral(MapElement):
    def __init__(self, name: str, extension:float):
        super().__init__(name, extension)


class Trait(Element):
    def __init__(self, name: str):
        super().__init__(name)