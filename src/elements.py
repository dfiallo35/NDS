class element:
    """
    Base class for all the simulation elements.
    """
    def __init__(self, name: str):
        self.name = name


class mapelement(element):
    """
    Base class for all the map elements.
    """
    def __init__(self, name, forain):
        super().__init__(name)
        self.forain = forain




class nation(mapelement):
    def __init__(self, name: str, contain: list, traits: list):
        super().__init__(name, get_forain())
        self.contain = contain
        self.traits = traits

        def get_forain(self):
            forain=[]
            for province in self.contain:
                if not (province in self.contain):
                    forain.append(province.forain)
            return set(forain)


class province(mapelement):
    def __init__(self, name: str, developmen: int, population: int, forain: list):
        super().__init__(name, forain)
        self.developmen = developmen
        self.population = population


class sea(mapelement):
    def __init__(self, name: str, forain: list):
        super().__init__(name, forain)


class neutral(mapelement):
    def __init__(self, name: str, forain: list):
        super().__init__(name, forain)


class trait(element):
    def __init__(self, name: str):
        super().__init__(name)