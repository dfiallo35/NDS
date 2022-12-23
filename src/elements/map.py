try:
    from elements.elements import *
except:
    from elements import *

import networkx as nx
from networkx import Graph

#todo: traits and traits of nations
#todo: delete from map
#todo: delete updates

#fix: repeated provinces in nations
class Map:
    def __init__(self) -> None:
        self.nationdict = dict()
        self.provincedict = dict()
        self.neutraldict = dict()
        self.seadict = dict()
        self.traitdict = dict()

        # Graph of the provinces, sea and neutral neighbours
        self.province_neighbours= Graph()

    @property
    def mapelementsdict(self):
        """
        Get the map elements
        :return: the map elements
        """
        return {**self.nationdict, **self.provincedict, **self.neutraldict, **self.seadict}
    @property
    def nation_province(self):
        """
        Get the nation provinces
        :return: the nation provinces
        """
        return {name: [province for province in nation.provinces] for name, nation in self.nationdict.items()}

    def add_nation(self, name: str, provinces: list, traits: list= []):
        '''
        Add a nation to the map
        :param name: the nation name
        :param provinces: contains the provinces of the nation
        :param traits: the nation traits
        '''
        self.__exist_element(name)
        self.__not_exist_elements(provinces)

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

   
    def __add_update(self, element: str, updates):
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