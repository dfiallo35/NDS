try:
    from elements.elements import *
    from events.event import *
except:
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))

    from elements.elements import *
    from events.event import *

import networkx as nx
from networkx import Graph

#todo: traits and traits of nations
#todo: delete from map
#todo: delete updates


class Map:
    def __init__(self) -> None:
        self.nationdict = dict()
        self.provincedict = dict()
        self.neutraldict = dict()
        self.seadict = dict()
        self.traitdict = dict()

        self.categories= dict()
        self.events= dict()
        self.decisions= dict()

        # Graph of the provinces, sea and neutral neighbours
        self.province_neighbours= Graph()

    @property
    def mapelementsdict(self) -> dict:
        """
        Get the map elements
        :return: the map elements
        """
        return {**self.nationdict, **self.provincedict, **self.neutraldict, **self.seadict}
    
    @property
    def nation_province(self) -> dict[list]:
        """
        Get the nation provinces
        :return: the nation provinces
        """
        return {name: [province for province in nation.provinces] for name, nation in self.nationdict.items()}

    @property
    def event_list(self):
        '''
        Get the events list
        :return: the events list
        '''
        return self.events.values()
    
    @property
    def event_enabled_list(self):
        '''
        Get the enabled events list
        :return: the enabled events list
        '''
        return [event for event in self.event_list if event.enabled]

    def add_nation(self, name: str, provinces: list, traits: list= []):
        '''
        Add a nation to the map
        :param name: the nation name
        :param provinces: contains the provinces of the nation
        :param traits: the nation traits
        '''
        self.__exist_element(name)
        self.__not_exist_elements(provinces)
        for nat in self.nationdict.values():
            self.__one_of_list_exist_in_list(provinces, nat.contains)


        province_instances= dict()
        for prov in provinces:
            province_instances[prov]= self.provincedict[prov]
        
        nat= Nation(name, province_instances, traits)
        self.nationdict[name]= nat
        return nat


    def add_province(self, name: str, extension: float, development: int, population: int, neighbours: list= []):
        '''
        Add a province to the map
        :param name: the province name
        :param extension: the province extension
        :param developmen: the province development
        :param population: the province population
        :param neighbours: the province neighbours
        '''
        self.__exist_element(name)
        self.__not_exist_elements(neighbours)

        prov= Province(name, extension, development, population)
        self.provincedict[name]= prov
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)
        return prov


    def add_sea(self, name: str, extension: float, neighbours: list= []):
        '''
        Add a sea to the map
        :param name: the sea name
        :param extension: the sea extension
        :param neighbours: the sea neighbours
        '''
        self.__exist_element(name)
        self.__not_exist_elements(neighbours)

        sea= Sea(name, extension, neighbours)
        self.seadict[name]= sea
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)
        return sea


    def add_neutral(self, name: str, extension: float, neighbours: list= []):
        '''
        Add a neutral to the map
        :param name: the neutral name
        :param extension: the neutral extension
        :param neighbours: the neutral neighbours
        '''
        self.__exist_element(name)
        self.__not_exist_elements(neighbours)

        neutral= Neutral(name, extension, neighbours)
        self.provincedict[name]= neutral
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)
        return neutral
    
    def add_category(self, name: str):
        '''
        Add a category to the map
        :param name: the category name
        '''
        cat= Category(name)
        self.categories[name]= cat
        return cat
    
    def add_decision_to_category(self, category: str, decision: Event):
        '''
        Add a decision to a Category. If the Category doesn't exist, it will be created
        :param category: the category
        :param decision: the decision
        '''
        cat= self.categories.get(category)
        if cat:
            cat.add_decision(decision)
        else:
            self.categories[category]= Category(category)
            self.categories[category].add_decision(decision)
    
    def add_event(self, name: str, distribution: Distribution, category: str, enabled: bool, execution, type: str= None, decisions: list= []):
        '''
        Add an event to the map. If the event already exists, it will be updated
        :param event: the event
        '''
        if not self.categories.get(category):
            raise Exception(f'The category {category} doesn\'t exist')
        
        event= Event(name=name, distribution=distribution, category=category, execution=execution, enabled=enabled, type=type)
        self.events[event.name]= event
        self.decisions[event.name]= decisions
        return event
    

   
    def __add_update(self, element: str, updates):
        '''
        Add the updates to the element
        :param element: the element
        :param updates: the updates
        '''
        if updates.get('provinces'):
            for prov in updates['provinces']:
                self.mapelementsdict[element].provinces[prov]= self.provincedict[prov]
            updates.pop('provinces')

        if updates.get('neighbours'):
            self.__add_edges(element, updates['neighbours'])
            updates.pop('neighbours')
        
        if updates.get('traits'):
            for trait in updates['traits']:
                self.mapelementsdict[element].traits[trait]= self.traitdict[trait]
            updates.pop('traits')
        return updates
        

    def update(self, element: str, **kwargs):
        """
        Update an element
        :param element: the element
        :param kwargs: the new values
        """
        self.__not_exist_element(element)

        updates= kwargs.copy()
        updates= self.__add_update(element, updates)
        self.mapelementsdict[element].__dict__.update(updates)


    def nation_neighbours(self, nation: str):
        """
        Get the nation neighbours
        :param nation: the nation name
        :return: the nation neighbours
        """
        neighbours = []
        for province in self.nationdict[nation].provinces:
            neighbours.extend(self.province_neighbours[province])
        neighbours = list(set(neighbours))

        nation_neighbours = []
        for nat in self.nationdict:
            for province in self.nationdict[nat].provinces:
                if province in neighbours:
                    nation_neighbours.append(nat)
        nation_neighbours = list(set(nation_neighbours))
        return nation_neighbours


    def __add_edges(self, province: str, neighbours: list):
        """
        Add edges to the element
        :param element: the element
        :param neighbour: the neighbour list
        """
        for neighbour in neighbours:
            if neighbour in self.provincedict or neighbour in self.neutraldict or neighbour in self.seadict:
                self.province_neighbours.add_edge(province, neighbour)
            else:
                raise Exception("Map element not found")


    def __exist_element(self, element: str):
        """
        Detect if the element exists in the map
        :param name: the element name
        :param elements_dict: the dictionary of the elements
        """
        if self.mapelementsdict.get(element):
            raise Exception(f"The Element {element} already exists")


    def __exist_elements(self, elements: list):
        """
        Detect if elements exist on the map
        :param elements: the elements list
        :param elements_dict: the dictionary of the elements
        """
        for element in elements:
            if not self.mapelementsdict.get(element):
                raise Exception(f"The Element {element} already exists")

    def __not_exist_element(self, element: str):
        """
        Detect if the element not exists in the map
        :param name: the element name
        :param elements_dict: the dictionary of the elements
        """
        if not self.mapelementsdict.get(element):
            raise Exception(f"The Element {element} not exists")
    
    def __not_exist_elements(self, elements: list):
        """
        Detect if elements not exist on the map
        :param elements: the elements list
        :param elements_dict: the dictionary of the elements
        """
        for element in elements:
            if not self.mapelementsdict.get(element):
                raise Exception(f"The Element {element} not exists")
    
    def __exist_in_list(self, element: str, elements: list[str]):
        '''
        Detect if the element exists in the list and raise an exception if it does
        :param element: the element
        :param elements: the elements list
        '''
        if element in elements:
            raise Exception(f"The Element {element} already exists")
    
    def __one_of_list_exist_in_list(self, elements1: list[str], elements2: list[str]):
        '''
        Detect if one element exists in the list and raise an exception if it does
        :param elements1: the elements list
        :param elements2: the elements list
        '''
        for el in elements1:
            self.__exist_in_list(el, elements2)
    
    def __exist_in_dict(self, element: str, elements: dict):
        '''
        Detect if the element exists in the dict and raise an exception if it does
        :param element: the element
        :param elements: the elements dict
        '''
        if elements.get(element):
            raise Exception(f"The Element {element} already exists")