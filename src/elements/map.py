
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from elements.map_elements import *
from elements.elements import *
from elements.simulation_elements import *

import networkx as nx
from networkx import Graph
from inspect import getmembers as gm


#todo: borrar elementos del mapa
class Map:
    def __init__(self) -> None:
        self.nationdict = dict()
        self.provincedict = dict()
        self.neutraldict = dict()
        self.seadict = dict()
        self.traitdict = dict()

        self.categorydict= dict()
        self.eventdict= dict()
        self.decisionsdict= dict()

        
        self.distdict= {k:Distribution(name=k, dist=v) for k,v in Distribution.distributions.items()}
        self.distributiondict= dict()

        self.resources= set()

        # Graph of the provinces, sea and neutral neighbours
        self.province_neighbours= Graph()
    

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
    def nations(self) -> dict:
        return self.nationdict
    
    @property
    def provinces(self) -> dict:
        return self.provincedict
    
    @property
    def neutrals(self) -> dict:
        return self.neutraldict
    
    @property
    def seas(self) -> dict:
        return self.seadict
    
    @property
    def traits(self) -> dict:
        return self.traitdict
    
    @property
    def categories(self) -> dict:
        return self.categorydict
    
    @property
    def events(self) -> dict:
        return self.eventdict
    
    @property
    def distributions(self) -> dict:
        return self.distributiondict
    
    #todo: change names
    @property
    def decisions(self) -> dict:
        return self.decisionsdict
    
    # @property
    # def resources(self) -> set:
    #     return self.resources


    @property
    def all(self) -> dict:
        return {**self.nationdict, **self.provincedict, **self.neutraldict,
                **self.seadict, **self.traitdict, **self.categorydict,
                **self.eventdict, **self.decisionsdict, **self.distdict,
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
        name= self.element_name(name)
        provinces= self.element_name(provinces)
        traits= self.element_name(traits)

        self.alredy_exist(name)
        self.not_exist_list(provinces)

        for nat in self.nationdict.values():
            for prov in nat.provinces:
                if prov in provinces:
                    raise Exception(f'Province {prov} already in nation {nat.name}')

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
        name= self.element_name(name)
        neighbours= self.element_name(neighbours)

        self.alredy_exist(name)
        self.not_exist_list(neighbours)

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
        name= self.element_name(name)
        neighbours= self.element_name(neighbours)

        self.alredy_exist(name)
        self.not_exist_list(neighbours)

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
        name= self.element_name(name)
        neighbours= self.element_name(neighbours)

        self.alredy_exist(name)
        self.not_exist_list(neighbours)

        neutral= Neutral(name, extension, neighbours)
        self.provincedict[name]= neutral
        self.province_neighbours.add_node(name)
        self.__add_edges(name, neighbours)
    
    def add_trait(self, name: str):
        '''
        Add a trait to the map
        :param name: the trait name
        '''
        name= self.element_name(name)
        
        self.alredy_exist(name)

        trait= Trait(name= name)
        self.traitdict[name]= trait
    
    def add_category(self, name: str):
        '''
        Add a category to the map
        :param name: the category name
        '''
        name= self.element_name(name)
        
        self.alredy_exist(name)

        cat= Category(name)
        self.categorydict[name]= cat
    
    def add_decision_to_category(self, category: str, decision: Event):
        '''
        Add a decision to a Category. If the Category doesn't exist, it will be created
        :param category: the category
        :param decision: the decision
        '''
        # name= self.element_name(name)
        # self.alredy_exist(name)
        cat= self.categorydict.get(category)
        if cat:
            cat.add_decision(decision)
        else:
            self.categorydict[category]= Category(category)
            self.categorydict[category].add_decision(decision)
    
    #todo: controle types
    def add_event(self, name: str, dist: Distribution, cat: str, enabled: bool, tp: str, dec: list, execution, code= None, params: list=[]):
        '''
        Add an event to the map. If the event already exists, it will be updated
        :param event: the event
        '''
        name= self.element_name(name)
        cat= self.element_name(cat)
        dec= self.element_name(dec)
        dist= self.element_name(dist)

        self.alredy_exist(name)
        self.not_exist_list(dec)
        self.not_exist(dist)
        self.not_exist(cat)

        if not self.categorydict.get(cat):
            raise Exception(f'The category {cat} doesn\'t exist')
        
        event= Event(name=name, dist=self.all[dist], category=self.all[cat], enabled=enabled, type=tp, execution=execution, code=code, decisions=dec, params= params)
        self.eventdict[name]= event
        
    def add_distribution(self, name: str, dist: Distribution, **kwargs):
        '''
        Add a distribution to the map
        :param name: the distribution name
        :param distribution: the distribution
        '''
        name= self.element_name(name)
        dist= self.element_name(dist)

        self.alredy_exist(name)
        self.not_exist(dist)

        dist= Distribution(name, dist, **kwargs)
        self.distributiondict[name]= dist

    def add_decision(self, name: str, event: Event, cond, execution, params: list= []):
        '''
        Add a decision to the map
        :param name: the decision name
        :param distribution: the distribution
        '''
        name= self.element_name(name)
        event= self.element_name(event)

        self.alredy_exist(name)
        self.not_exist(event)

        dec= Decision(name, cond, self.all[event], execution, params)
        self.decisionsdict[name]= dec

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

    
    def data_add(self, element: str, data: dict, *args, **kwargs):
        """
        Add data to an element
        :param element: the element
        :param data: the data
        """
        element= self.element_name(element)
        self.not_exist(element)
        
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
        element= self.element_name(element)
        self.not_exist(element)

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
        element= self.element_name(element)
        self.not_exist(element)

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
        
    def get_map_data(self, data: str):
        properties= {name:val for (name, val) in gm(Map, lambda x: isinstance(x, property))}
        if data in properties:
            return properties[data].fget(self)
        else:
            raise Exception(f'The map doesn\'t have the attribute {data}')
    
    def get_data(self, element: str, data: str, *args, **kwargs):
        element= self.element_name(element)
        self.not_exist(element)

        properties= {name:val for (name, val) in gm(type(self.all[element]), lambda x: isinstance(x, property))}
        if data in properties:
            return properties[data].fget(self.all[element], *args, **kwargs)
        else:
            raise Exception(f'The element {element} doesn\'t have the attribute {data}')
                


    def nation_neighbours(self, nation: str):
        """
        Get the nation neighbours
        :param nation: the nation name
        :return: the nation neighbours
        """
        nation= self.element_name(nation)
        self.not_exist(nation)

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

    def get_element_name(self, element: str):
        """
        Get the name of an element
        :param element: the element
        :return: the name
        """
        if isinstance(element, str):
            return element
        elif isinstance(element, Element):
            return element.name
        else:
            raise Exception("Error: The element must be a string or an element")
    
    def element_name(self, element: list):
        """
        Get the name of an element
        :param element: the element
        :return: the name
        """
        if isinstance(element, list):
            return [self.get_element_name(i) for i in element]
        else:
            return self.get_element_name(element)

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


    def alredy_exist(self, element: str):
        element= self.get_element_name(element)
        if element in self.all:
            raise Exception(f'The element {element} already exist')
    
    def alredy_exist_list(self, element: list):
        for i in element:
            self.alredy_exist(i)

    def not_exist(self, element: str):
        element= self.get_element_name(element)
        if element not in self.all:
            raise Exception(f'The element {element} doesn\'t exist')
    
    def not_exist_list(self, element: list):
        for i in element:
            self.not_exist(i)