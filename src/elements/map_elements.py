from elements.elements import *

class MapElement(Element):
    """
    Base class for all the map elements.
    :param name: the element name
    :param extension: the element extension
    """
    def __init__(self, name: str):
        super().__init__(name)
    
    @property
    def data(self):
        return self.__dict__


class Nation(MapElement):
    def __init__(self, name: str, provinces: dict, traits: list=[]):
        super().__init__(name)
        self.contains = provinces
        self.traitsvar = traits

    #todo: set for all provinces
    def extension_get(self) -> float:
        extension = 0
        for prov in self.contains.values():
            extension += prov.extension
        return extension
    
    def development_set(self, value: int):
        ...
    
    extension= property(extension_get, development_set)
    
    
    def development_get(self) -> int:
        development = 0
        for prov in self.contains.values():
            development += prov.development
        return development
    
    def development_set(self, value: int):
        ...
    
    development= property(development_get, development_set)
    

    def population_get(self) -> int:
        population = 0
        for prov in self.contains.values():
            population += prov.population
        return population
    
    def population_set(self, value: int):
        ...

    population= property(population_get, population_set)

    
    def provinces_get(self):
        return self.contains
    
    def provinces_set(self, value):
        self.contains.update({value.name: value})
    
    def provinces_del(self, prov):
        self.contains.pop(prov.name)
    
    provinces= property(provinces_get, provinces_set, provinces_del)

    #todo: traits dict
    def traits_get(self):
        return self.traitsvar
    
    def traits_set(self, value):
        self.traitsvar.append(value)
    
    def traits_del(self, value):
        self.traitsvar.remove(value)
    
    traits= property(traits_get, traits_set, traits_del)

    
    def get_nation_data(self, data_name: str):
        data= 0
        for prov in self.contains.values():
            if prov.data.get(data_name):
                data+= prov.data[data_name]
        return data

    def get_nation_all_data(self):
        """returns a dictionary with all the data(resources) of the nation"""
        all_data = {}
        for prov in self.contains.values():
            for data_name in prov.data.keys():
                if all_data.get(data_name):
                    all_data[data_name]+= prov.data[data_name]
                else:
                    all_data[data_name]= prov.data[data_name]
        return all_data

    def change_data(self, data_name: str, value: int):
        """distributes a change in the country's data(resources) equally among all its provinces"""
        total_data=self.get_nation_data(data_name)
        for prov in self.contains.values():
            if prov.data.get(data_name):
                prov.data[data_name]+= prov.data[data_name]*value/total_data
        
    def __str__(self):
        return f'{self.name}'

    def compare(self, new):
        if self.name == new.name:
            if type(self) == type(new):

                changes= {
                    'new': [],
                    'lost': [],
                    'changed': {}
                }
                new_prov= copy(new.contains)
                for province in self.contains:
                    if new.contains.get(province):
                        new_prov.pop(province)
                        comp= self.contains[province].compare(new.contains[province])
                        if comp:
                            changes['changed'][province]= comp
                    else:
                        changes['lost'].append(copy(province))
                changes['new']= [copy(i) for i in new_prov]

                if changes['changed'] or changes['new'] or changes['lost']:
                    return changes
                return None

            else:
                raise Exception(f'Error: "{self.name}" and "{new.name}" are not of the same type')
        else:
            raise Exception(f'Error: "{self.name}" and "{new.name}" are not the same nation')
        

class Province(MapElement):
    def __init__(self, name: str, extension:float, development: int, population: int, **kwargs):
        super().__init__(name)
        self.extensionvar = extension
        self.developmentvar = development
        self.populationvar = population

        for i in kwargs:
            def gett(self):
                return self.__dict__[i+'var']
            def sett(self, x):
                self.__dict__[i+'var']= x

            self.__dict__[i+'var']= kwargs[i]
            setattr(self.__class__, i, property(fget= gett, fset= sett))
    
    
    def population_get(self):
        return self.populationvar
    
    def population_set(self, value: int):
        self.populationvar= value
    
    population= property(population_get, population_set)

    def development_get(self):
        return self.developmentvar
    
    def development_set(self, value: int):
        self.developmentvar= value
    
    development= property(development_get, development_set)

    def extension_get(self):
        return self.extensionvar
    
    def extension_set(self, value: int):
        self.extensionvar= value
    
    extension= property(extension_get, extension_set)




    def __str__(self):
        return f'{self.name}'
    
    def compare(self, new):
        if self.name == new.name:
            if type(self) == type(new):
                changes= {
                    'changed': {},
                    'new': [],
                    'lost': []
                }
                new_data= copy(new.data)
                for key in self.data.keys():
                    if new.data.get(key):
                        new_data.pop(key)
                        if self.data[key] != new.data[key]:
                            changes['changed'][key]= (self.data[key], new.data[key])
                    else:
                        changes['lost'].append(copy(key))
                changes['new']= [copy(i) for i in new_data]

                if changes['changed'] or changes['new'] or changes['lost']:
                    return changes
                return None
            else:
                raise Exception(f'Error: "{self.name}" and "{new.name}" are not of the same type')
        else:
            raise Exception(f'Error: "{self.name}" and "{new.name}" are not the same province')

class Sea(MapElement):
    def __init__(self, name: str, extension:float):
        super().__init__(name)
        self.extension = extension


class Neutral(MapElement):
    def __init__(self, name: str, extension:float):
        super().__init__(name)
        self.extension = extension



class Trait(Element):
    def __init__(self, name: str):
        super().__init__(name)