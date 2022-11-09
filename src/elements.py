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
    def __init__(self, name, extension:float, forain):
        super().__init__(name)
        self.forain = forain
        self.extension = extension



class Nation(MapElement):
    def __init__(self, name: str, extension:float, contain: list, traits: list, forain: list):
        super().__init__(name, extension, forain)
        self.contain = contain
        self.traits = traits
        self.forain = forain
        


class Province(MapElement):
    def __init__(self, name: str, extension:float, developmen: int, population: int, forain: list):
        super().__init__(name, extension, forain)
        self.developmen = developmen
        self.population = population


class Sea(MapElement):
    def __init__(self, name: str, extension:float, forain: list):
        super().__init__(name, extension, forain)


class Neutral(MapElement):
    def __init__(self, name: str, extension:float, forain: list):
        super().__init__(name, extension, forain)


class Trait(Element):
    def __init__(self, name: str):
        super().__init__(name)