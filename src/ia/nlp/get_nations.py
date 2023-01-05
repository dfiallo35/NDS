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
        country_hdi[item[0]] = item[1]

    return list_of_countries, country_hdi 