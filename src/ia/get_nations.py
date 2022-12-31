import pandas as pd
import requests
from bs4 import *


def get_all_countries():
    """
    Get from a wikipedia page table the list of countries
    """

    url = "https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index"

    response = requests.get(url)

    table_class = "wikitable sortable jquery-tablesorter"

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    # indiatable = soup.find('table',{'class':"wikitable"})
    
    dfs = pd.read_html(response.text)

    # print(dfs)

    # len(dfs)

    # print(dfs[4].head())

    df = dfs[1] # table with nations idh
    # print(df)

    
    list_of_countries = df[df.columns[2]].values.tolist() 
    # print(list_of_countries)

    list_countries_hdi = df[df.columns[3]].values.tolist()
    # print(list_countries_hdi)

    # return list_of_countries, list_countries_hdi
    
    return list_of_countries    

    # convert list to dataframe
    # df = pd.DataFrame(df[0])
    # print(df.head())

    # drop the unwanted columns
    # data = df.drop(["Rank", "Land in km2 (mi2)", "Water in km2 (mi2)", "% water", "Notes"], axis=1)
    # rename columns for ease
    # data = data.rename(columns={"State or union territory": "State","Population(2011)[3]": "Population"})
    # print(data.head())

