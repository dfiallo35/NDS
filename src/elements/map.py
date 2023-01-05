
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from elements.map_elements import *
from elements.elements import *
from elements.simulation_elements import *

import networkx as nx
from networkx import Graph
from inspect import getmembers as gm

#todo: definir correctamente los traits
#todo: borrar elementos del mapa

#todo: __exist_element for every element
#todo: revisar los casos en que se sobreescriben los elementos o se da exepcion de que ya existen


class Map:
    def __init__(self) -> None:
        self.nationdict = dict()
        self.provincedict = dict()
        self.neutraldict = dict()
        self.seadict = dict()
        self.traitdict = dict()

        self.categorydict= dict()
        self.eventdict= dict()
        self.decisions= dict()

        self.distdict= {k:v for k,v in Distribution.distributions.items()}
        self.distributiondict= dict()

        self.resources= set()

        # Graph of the provinces, sea and neutral neighbours
        self.province_neighbours= Graph()
    
    #check: test for map, nations are ok
    def compare(self, new):
        '''
        Compare the map with another map
        :param other: the other map
        :return: True if the maps are the same
        '''
        new_nations= copy(new.nationdict)
        changes= {
                    'changed': {},
                    'new': [],
                    'lost': []
                }
        for nation in self.nationdict.values():
            if new.nationdict.get(nation.name):
                new_nations.pop(nation.name)
                comp= nation.compare(new.nationdict[nation.name])
                if comp:
                    changes['changed'][nation.name]= comp
            else:
                changes['lost'].append(nation.name)
        changes['new'] = [copy(i) for i in new_nations.values()]

        if changes['changed'] or changes['new'] or changes['lost']:
            return changes
        return None

    @property
    def mapelementsdict(self) -> dict:
        """
        Get the map elements
        :return: the map elements
        """
        return {**self.nationdict, **self.provincedict, **self.neutraldict, **self.seadict}
    
    @property
    def all(self) -> dict:
        return {**self.nationdict, **self.provincedict, **self.neutraldict,
                **self.seadict, **self.traitdict, **self.categorydict,
                **self.eventdict, **self.decisions, **self.distdict,
                **self.distributiondict}
    
    @property
    def nation_province(self) -> dict[list]:
        """
        Get the nation provinces
        :return: the nation provinces
        """
        return {name: [province for province in nation.contains] for name, nation in self.nationdict.items()}

    @property
    def event_list(self):
        '''
        Get the events list
        :return: the events list
        '''
        return self.eventdict.values()
    
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


    def add_province(self, name: str, extension: float, development: int, population: int, neighbours: list= [], **kwargs):
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

        for i in kwargs:
            self.resources.add(i)
        prov= Province(name, extension, development, population, **kwargs)
        self.provincedict[name]= prov
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)


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
    
    def add_trait(self, name: str):
        '''
        Add a trait to the map
        :param name: the trait name
        '''
        self.__exist_element(name)
        trait= Trait(name= name)
        self.traitdict[name]= trait
    
    def add_category(self, name: str):
        '''
        Add a category to the map
        :param name: the category name
        '''
        cat= Category(name)
        self.categorydict[name]= cat
    
    def add_decision_to_category(self, category: str, decision: Event):
        '''
        Add a decision to a Category. If the Category doesn't exist, it will be created
        :param category: the category
        :param decision: the decision
        '''
        cat= self.categorydict.get(category)
        if cat:
            cat.add_decision(decision)
        else:
            self.categorydict[category]= Category(category)
            self.categorydict[category].add_decision(decision)
    
    def add_event(self, name: str, distribution: Distribution, category: str, enabled: bool, type: str, decisions: list, execution, code= None, args: list=[]):
        '''
        Add an event to the map. If the event already exists, it will be updated
        :param event: the event
        '''
        if not self.categorydict.get(category):
            raise Exception(f'The category {category} doesn\'t exist')
        
        event= Event(name=name, distribution=distribution, category=category, enabled=enabled, type=type, execution=execution, code=code, decisions=decisions, args= args)
        self.eventdict[name]= event
        
    def add_distribution(self, name: str, distribution: Distribution, **kwargs):
        '''
        Add a distribution to the map
        :param name: the distribution name
        :param distribution: the distribution
        '''
        dist= Distribution(name, distribution, **kwargs)
        self.distributiondict[name]= dist


    def update(self, element: str, data: dict):
        """
        Update an element
        :param element: the element
        :param kwargs: the new values
        """
        if data.get('add'):
            self.data_add(element, data['add'])
        if data.get('delete'):
            self.data_delete(element, data['delete'])
        if data.get('update'):
            self.data_update(element, data['update'])

    
    def data_add(self, element: str, data: dict):
        """
        Add data to an element
        :param element: the element
        :param data: the data
        """
        self.__not_exist_element(element)
        
        properties= {name:val for (name, val) in gm(type(self.all[element]), lambda x: isinstance(x, property))}
        for key in data:
            if key in properties:
                if type(properties[key].fget(self.all[element])) == list:
                    if type(data[key]) == list:
                        for i in data[key]:
                            properties[key].fset(self.all[element], self.all[i])
                    else:
                        properties[key].fset(self.all[element], self.all[data[key]])
                else:
                    raise Exception(f'Error: the property {key} is not a list')
            else:
                raise Exception(f'The property {key} doesn\'t exist')

    
    def data_update(self, element: str, data: dict):
        """
        Change the data of an element
        :param element: the element
        :param data: the new data
        """
        self.__not_exist_element(element)

        properties= {name:val for (name, val) in gm(type(self.all[element]), lambda x: isinstance(x, property))}
        for key in data:
            if key in properties:
                if type(data[key]) == type(properties[key].fget(self.all[element])):
                    if type(data[key]) == list:
                        for i in data[key]:
                            if i in self.all:
                                properties[key].fset(self.all[element], self.all[i])
                            else:
                                properties[key].fset(self.all[element], i)
                    else:
                        if data[key] in self.all:
                            properties[key].fset(self.all[element], self.all[data[key]])
                        else:
                            properties[key].fset(self.all[element], data[key])
                else:
                    raise Exception(f'Error: the type of the property {key} is not {type(data[key])}')
            else:
                raise Exception(f'The element {element} doesn\'t have the attribute {key}')

    def data_delete(self, element: str, data: dict):
        """
        Delete data from an element
        :param element: the element
        :param data: the data
        """
        self.__not_exist_element(element)

        properties= {name:val for (name, val) in gm(type(self.all[element]), lambda x: isinstance(x, property))}
        for key in data:
            if key in properties:
                if type(properties[key].fget(self.all[element])) == list:
                    if type(data[key]) == list:
                        for i in data[key]:
                            properties[key].fdel(self.all[element], self.all[i])
                    else:
                        properties[key].fdel(self.all[element], self.all[data[key]])
                else:
                    raise Exception(f'Error: the property {key} is not a list')
            else:
                raise Exception(f'The property {key} doesn\'t exist')
        

    
    def get_data(self, element: str, data: str):
        self.__not_exist_element(element)

        properties= {name:val for (name, val) in gm(type(self.all[element]), lambda x: isinstance(x, property))}
        if data in properties:
            return properties[data].fget(self.all[element])
        else:
            raise Exception(f'The element {element} doesn\'t have the attribute {data}')
                


    def nation_neighbours(self, nation: str):
        """
        Get the nation neighbours
        :param nation: the nation name
        :return: the nation neighbours
        """
        neighbours = []
        for province in self.nationdict[nation].contains:
            neighbours.extend(self.province_neighbours[province])
        neighbours = list(set(neighbours))

        nation_neighbours = []
        for nat in self.nationdict:
            for province in self.nationdict[nat].contains:
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