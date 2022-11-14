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



class Nation(MapElement):
    def __init__(self, name: str, contain: list, traits: list):
        super().__init__(name)
        self.contain = contain
        self.traits = traits
        


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