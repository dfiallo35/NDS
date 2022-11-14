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

