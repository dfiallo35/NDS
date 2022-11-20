class Element:
    """
    Base class for all the simulation elements.
    """
    def __init__(self, name: str):
        self.name = name


class MapElement(Element):
    """
    Base class for all the map elements.
    """
    def __init__(self, name):
        super().__init__(name)


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
    def __init__(self, name: str, extension:float, developmen: int, population: int):
        super().__init__(name, extension)
        self.developmen = developmen
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