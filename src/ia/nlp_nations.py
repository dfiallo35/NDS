import nltk
import wikipedia 
from nltk.corpus import wordnet, stopwords
from nltk import ne_chunk, extract_rels
import locationtagger
import requests
from bs4 import *
import string
import re
import os 
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd


import get_nations

lemmatizer  = WordNetLemmatizer()
stopwords   = set(nltk.corpus.stopwords.words('english'))
punctuation = string.punctuation

wikipedia.wikipedia.set_lang('en') # set the wiipedia language in english

# list of countries to consider
countries = set()
# countries = ["Cuba", "Canada", "Spain", "France", "United Kingdom", "Portugal", "Denmark", "United States"] 

# dictionary with keys as countries and values as their proccesed wikipedia page content
tagged_info = dict()

regions = dict()

# from a wikipedia page gets all countries names
# countries = get_nations.get_all_countries()


def get_pages(countries: list):
    """
    For every country listed in countries search its wikipedia page
    then tokenize the sentences and tagged them
    get countries: list of the countries to consider   
    """
    # for country in countries:
    for country in countries[0: 1]:
        content = wikipedia.page(title=country, auto_suggest=False).content # auto_suggest=False fix problems with Cuba's and Canada's pages upload 
        # content = "Granma, Havana, Pinar del Rio"

        regions[country] = set()
        getting_regions(country, content)

        # text_proccesing(content)


def text_proccesing(content: str):
    # sentence tokenize
    sentences = nltk.sent_tokenize(content)

    remove_urls(content)

    remove_html(content)

    normalized_text = []

    # for each sentence normalized the text (this includes word_tokenize)
    # for sent in nltk.sent_tokenize(content):
    #     normalized_text.append(list(normalize(sent)))
    
    for sent in nltk.sent_tokenize(content):
        normalized_text.append(list(nltk.word_tokenize(sent)))

    tagged = []

    for word in normalized_text:
        tagged.append(nltk.pos_tag(word))

    # chunked = []
    relations = []
    for item in tagged:
        search_entities(item, relations)    

        search_area(item, relations)
        
        # identify named entities
        # chunked.append(nltk.chunk.ne_chunk(item))
        

def search_entities(tagged, relations):
    chunked = []
    result = nltk.chunk.ne_chunk(tagged)
    result.draw()
    
    for tagged_tree in result.subtrees():
        if tagged_tree.label() == "GPE":
            entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
            relations.append(entity_name)


def search_area(tagged, relations):
    
    # grammar = "NP: {<DT>?<JJ>*<NN>}"
    # grammar = "NN: {<IN>?CD}"
    # cp = nltk.RegexpParser(grammar)

    cp = nltk.chunk.RegexpParser( " Chunk: {<NN>*<IN>*<DT>*<NNP>*<IN>*<NNP>*<VBZ>*<CD>} " )

    result = cp.parse(tagged)

    # print(result)
    result.draw()

    for tagged_tree in result.subtrees():
        if tagged_tree.label() == "Chunk":
            entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
            relations.append(entity_name)
    
    print(relations)


def remove_html(text):
    """
    Removes the htmls found in the text
    """
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)


def remove_urls(text):
    """
    Removes the urls found in the text
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)
    

def normalize(text):
    """
    Normalize the text from the sentences
    Uses lemmatization to convert a word to ita cannonical form
    eliminates stopwords and punctuation signs 
    """

    for token in nltk.word_tokenize(text):
        # token = token.lower()
        token = lemmatizer.lemmatize(token)
        if token not in stopwords and token not in punctuation:
            yield token


# this doesn't recognize Cuban provinces
def getting_regions(country: str, text: str):
    """
    Gets regions using locationtagger
    get country: string with the country's regions to search
    get text: text to search
    saves the regions in the dictionary regions
    """

    place_entity = locationtagger.find_locations(text=text)
    
    if country in place_entity.country_regions:
        for reg in  place_entity.country_regions[country]:
            regions[country].add(reg)

        # regions[country]. = set(place_entity.country_regions[country])

    # if country in place_entity.country_cities:
    #     for reg in  place_entity.country_cities[country]:
    #         regions[country].add(reg)

    if city in place_entity.region_cities:
        for reg in place_entity.region_cities[city]:
            regions[country].add(reg)

    # regions[country] = reg

    # for rgn in place_entity.country_regions[country]:
    #     regions[country].append(rgn) 
    # regions[country] = place_entity.country_regions


content = "Cuba is the second-most populous country in the Caribbean after Haiti, with over 11 million inhabitants. With an area of 505,990 km2 (195,360 sq mi), Spain is the second-largest country in the European Union (EU). The official area of the Republic of Cuba is 109,884 km2"
 
text_proccesing(content)