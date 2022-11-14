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


    def add_nation(self, name: str, extension: float, contain: list, traits: list):
        self.__detect_element(name, self.nationdict)
        nat= Nation(name, extension, contain, traits)
        self.nationdict[name]= nat
        return nat

    def add_province(self, name: str, extension: float, developmen: int, population: int, neighbours: list):
        self.__detect_element(name, self.provincedict)
        prov= Province(name, extension, developmen, population)
        self.provincedict[name]= prov
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)
        return prov

    def add_sea(self, name: str, extension: float, neighbours: list):
        self.__detect_element(name, self.neutraldict)
        sea= Sea(name, extension, neighbours)
        self.seadict[name]= sea
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)
        return sea

    def add_neutral(self, name: str, extension: float, neighbours: list):
        self.__detect_element(name, self.provincedict)
        neutral= Neutral(name, extension, neighbours)
        self.provincedict[name]= neutral
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)
        return neutral

