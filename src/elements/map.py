from elements.map_elements import *
from elements.elements import *
from elements.simulation_elements import *

import networkx as nx
from networkx import Graph
from inspect import getmembers as gm



class Map:
    def __init__(self) -> None:
        self.nationdict = dict()
        self.seadict = dict()
        self.traitdict = dict()
        
        self.categorydict= dict()
        self.simulation_eventdict= dict()
        self.decision_eventdict= dict()
        self.functiondict= dict()
        self.decisionsdict= dict()
        
        self.distdict= {k:Distribution(name=k, dist=v) for k,v in Distribution.distributions.items()}
        self.distributiondict= dict()

        self.dataset= set()

        self.neighbours_graph= Graph()

        self.en_dis_events= {
            'enable': [],
            'disable': []
        }
        self.log= Log(self)
    

    def compare(self, new):
        '''
        Compare the map with another map
        :param other: the other map
        :return: True if the maps are the same
        '''
        if type(self) != type(new):
            raise Exception(f'Error: "{self.name}" and "{new.name}" are not of the same type')
        
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
        return {**self.nationdict, **self.seadict}
    
    @property
    def nations(self) -> dict:
        return self.nationdict
    
    @property
    def seas(self) -> dict:
        return self.seadict
    
    @property
    def traits(self) -> dict:
        return self.traitdict
    
    @property
    def categories(self) -> dict:
        return self.categorydict
    
    #fix
    @property
    def events(self) -> dict:
        return {**self.decision_eventdict, **self.simulation_eventdict, **self.functiondict}
    
    @property
    def distributions(self) -> dict:
        return self.distributiondict
    

    @property
    def decisions(self) -> dict:
        return self.decisionsdict
    
    @property
    def data(self) -> set:
        return self.dataset


    @property
    def all(self) -> dict:
        return {**self.nationdict, **self.distributiondict, **self.functiondict,
                **self.seadict, **self.traitdict, **self.categorydict,
                **self.simulation_eventdict, **self.decision_eventdict,
                **self.decisionsdict, **self.distdict}
    
    @property
    def event_enabled_list(self):
        '''
        Get the enabled events list
        :return: the enabled events list
        '''
        return [event for event in self.simulation_eventdict.values() if event.enabled]

    def enable(self, event: Event):
        '''
        Enable an event
        :param event: the event
        '''
        self.not_exist(event.name)
        if event.name not in self.en_dis_events['enable']:
            self.en_dis_events['enable'].append(event.name)
            if event.name in self.en_dis_events['disable']:
                self.en_dis_events['disable'].remove(event.name)

    
    def disable(self, event: Event):
        '''
        Disable an event
        :param event: the event
        '''
        self.not_exist(event.name)
        if event.name not in self.en_dis_events['disable']:
            self.en_dis_events['disable'].append(event.name)
            if event.name in self.en_dis_events['enable']:
                self.en_dis_events['enable'].remove(event.name)

    def add_nation(self, name: str, population: int, extension: int, traits: list= [], neighbours: list= [], *args, **kwargs):
        '''
        Add a nation to the map
        :param name: the nation name
        '''
        name= self.element_name(name)
        traits= self.element_name(traits)
        self.alredy_exist(name)

        for data in kwargs:
            if data not in self.dataset:
                self.add_data_to_nations(data)
                
        
        nat= Nation(name, population, extension, traits, *args, **kwargs)
        self.nationdict[name]= nat
        self.neighbours_graph.add_node(name)
        self.add_edges(name, neighbours)

    def add_data_to_nations(self, data: str):
        '''
        Add data to a nation
        :param nation: the nation
        :param data: the data
        :param value: the value
        '''
        for nat in self.nationdict.values():
            nat: Nation= nat
            if not nat.__dict__.get(data+'var'):
                nat.add_data(data, None)

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
        self.neighbours_graph.add_node(name)
        self.add_edges(name, neighbours)

    
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
    
    
    def add_function(self, name: str, execution, code= None, params: list=[]):
        name= self.element_name(name)
        self.alredy_exist(name)

        f= Function(name=name, execution=execution, code=code, params= params)
        self.functiondict[name]= f

    def add_decision_event(self, name: str, cat: str, execution, code= None, params: list=[]):
        '''
        Add an event to the map. If the event already exists, it will be updated
        :param event: the event
        '''
        name= self.element_name(name)
        self.alredy_exist(name)
        
        event= DecisionEvent(name=name, category=cat, execution=execution, code=code, params= params)
        self.decision_eventdict[name]= event

    
    def add_simulation_event(self, name: str, dist: Distribution, cat: str, enabled: bool, dec: list, execution, code= None):
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
        
        event= SimulationEvent(name=name, dist=self.all[dist], category=self.all[cat], enabled=enabled, execution=execution, code=code, decisions=dec)
        self.simulation_eventdict[name]= event
        
    def add_distribution(self, name: str, dist: Distribution, *args, **kwargs):
        '''
        Add a distribution to the map
        :param name: the distribution name
        :param distribution: the distribution
        '''
        name= self.element_name(name)
        dist= self.element_name(dist)

        self.alredy_exist(name)
        self.not_exist(dist)

        dist= Distribution(name, dist, *args, **kwargs)
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
                
    def map_data(self, data: str):
        properties= {name:val for (name, val) in gm(Map, lambda x: isinstance(x, property))}
        if data in properties:
            return properties[data].fget(self)
        else:
            raise Exception(f'The map doesn\'t have the attribute {data}')

    #fix
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
            neighbours.extend(self.neighbours_graph[province])
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


    def add_edges(self, province: str, neighbours: list):
        """
        Add edges to the element
        :param element: the element
        :param neighbour: the neighbour list
        """
        for neighbour in neighbours:
            if neighbour in self.seas or neighbour in self.nations:
                self.neighbours_graph.add_edge(province, neighbour)
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