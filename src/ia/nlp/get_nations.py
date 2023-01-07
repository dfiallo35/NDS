import pandas as pd
import requests
from bs4 import *


def get_all_countries():
    """
    Get from a wikipedia page table the list of countries
    """

    url = "https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index"

    response = requests.get(url)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    
    dfs = pd.read_html(response.text)

    df = dfs[1] # table with nations idh

    # keep only country and hdi columns
    df = df.drop(df.columns[[0, 1, 4]], axis=1) 
    df = df.droplevel(1, axis=1)
  
    list_of_countries = df[df.columns[0]].values.tolist() 

    # list_countries_hdi = df[df.columns[1]].values.tolist()

    rc = df.to_records(index=False)
    rc_list = list(rc)
    # print(result)

    country_hdi = dict()

    for item in rc_list:
        country_hdi[item[0]] = float(item[1])

    # countries_list = list_of_countries
    # hdi = country_hdi

    return list_of_countries, country_hdi 


def get_population(countries_list: list):
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"

    response = requests.get(url)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    
    dfs = pd.read_html(response.text)

    df = dfs[0]

    # keep only country and population in 2019 columns
    df = df.drop(df.columns[[1, 2, 3, 5]], axis=1)

    # rename Country / Area 
    df = df.rename(columns={"Country / Area": "Country"})

    for index, row in df.iterrows():
        if "[" in row["Country"]:
            new_value = ""
            for i in range(0, len(row["Country"])):
                if row["Country"][i] == "[":
                    break
                new_value = new_value + row["Country"][i]
            
            df.Country = df.Country.replace({row["Country"]: new_value})

        # if row["Country"] not in countries_list:
        #     df = df.drop(index)
   
    rc = df.to_records(index=False)
    rc_list = list(rc)
    print(rc_list)

    country_population = dict()

    for item in rc_list:
        country_population[item[0]] = item[1]

    population = country_population 
    
    return country_population


def get_area_extension(countries_list: list):
    url = "https://simple.wikipedia.org/wiki/List_of_countries_by_area"

    response = requests.get(url)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    
    dfs = pd.read_html(response.text)

    df = dfs[0] # table with nations idh

    # keep only country and area
    df = df.drop(df.columns[[0]], axis=1)

    # rename Total in km2 (mi2)
    df = df.rename(columns={"Total in km2 (mi2)": "Area"})

    for index, row in df.iterrows():
        value = ""
        
        for i in range(0, len(row["Area"])):
            if row["Area"][i] == " ":
                break
            if row["Area"][i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                value = value + row["Area"][i]
            
        _int_val = float(value)
        df.Area = df.Area.replace({row["Area"]: _int_val})

    # print(df)
      
    rc = df.to_records(index=False)
    rc_list = list(rc)

    country_area = dict()

    for item in rc_list:
        country_area[item[0]] = item[1]

    return country_area


# countries_list, hdi = get_all_countries()
# # print(countries_list)
# # print(countries_list["China"])
# # print()
# # population = get_population(countries_list)
# area = get_area_extension(countries_list)

# print(countries_list)
# print()
# print(hdi)
# print()
# print(population)
# print()
# print(area)

