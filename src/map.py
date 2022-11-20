from elements import *
import networkx as nx
from networkx import Graph

class Map:
    def __init__(self) -> None:
        self.nationdict = dict()
        self.provincedict = dict()
        self.neutraldict = dict()
        self.seadict = dict()

        # Graph of the provinces, sea and neutral neighbours
        self.province_neighbours= Graph()

    @property
    def mapelementsdict(self):
        """
        Get the map elements
        :return: the map elements
        """
        return {**self.nationdict, **self.provincedict, **self.neutraldict, **self.seadict}

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


    def nation_neighbours(self, nation: str):
        """
        Get the nation neighbours
        :param nation: the nation name
        :return: the nation neighbours
        """
        neighbours = []
        for province in self.nationdict[nation].contain:
            neighbours.extend(self.province_neighbours[province])
        neighbours = list(set(neighbours))

        nation_neighbours = []
        for nat in self.nationdict:
            for province in self.nationdict[nat].contain:
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



    def __detect_element(self, name: str, elements_dict: dict):
        """
        Detect if an element is already in the map
        :param name: the element name
        :param elements_dict: the dictionary of the elements
        """
        if elements_dict.get(name) != None:
            raise Exception("Element already exists")