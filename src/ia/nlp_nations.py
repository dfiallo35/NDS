import os
import re
import string

import get_nations
import locationtagger
import nltk
import pandas as pd
import requests
import wikipedia
from bs4 import *
from nltk import extract_rels, ne_chunk
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer  = WordNetLemmatizer()
stopwords   = set(nltk.corpus.stopwords.words('english'))
punctuation = string.punctuation

wikipedia.wikipedia.set_lang('en') # set the wiipedia language in english




def main():
    # countries, countries_hdi = get_nations.get_all_countries()
    countries = ["Cuba"]
    countries_hdi = [{"Cuba": 0.87}]

    # country_content = get_pages(countries)
    country_content = dict()
    country_content["Cuba"] = "According to the official census of 2010, Cuba's population was 11,241,161, comprising 5,628,996 men and 5,612,165 women. The official area of the Republic of Cuba is 109,884 km2 (42,426 sq mi) (without the territorial waters) but a total of 350,730 km² (135,418 sq mi) including the exclusive economic zone. Cuba is the second-most populous country in the Caribbean after Haiti, with over 11 million inhabitants.[13]"

    for country in countries:
        text_processing(country, country_content[country])

# OK
def get_pages(countries: list):
    country_content = dict()

    for country in countries:
        content = wikipedia.page(title=country, auto_suggest=False).content # auto_suggest=False fix problems with Cuba's and Canada's pages upload 
        
        country_content[country] = content
        
    return country_content


def tokenize(content: str):
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

    return tagged


def text_processing(country: str, content: str):
    tagged = tokenize(content)

    # chunked = []
    relations = []

    region_entities = set()
    population_subtrees = []
    areas_subtrees = []

    for item in tagged:
        region_entities, population_subtrees, areas_subtrees = search_regions(item, region_entities, population_subtrees, areas_subtrees)
        # for region in search_regions(item):
        #     region_entities.add(region)

        # for pop in search_population(item):
        #     population.append(pop)

        # search_area(item, relations)
        
        # identify named entities
        # chunked.append(nltk.chunk.ne_chunk(item))

    print(region_entities)
    print(population_subtrees)
    print(areas_subtrees)
        

def search_regions(tagged: list, region_entities, population_subtrees, areas_subtrees):
    # region_entities = set()
    # population_subtrees = []
    # area_subtrees = []

    tree = nltk.chunk.ne_chunk(tagged)
    tree.draw()
    
    for subtree in tree.subtrees():
        if subtree.label() == "GPE":
            entity_name = ' '.join(c[0] for c in subtree.leaves())
            region_entities.add(entity_name.strip())

        if subtree.label() == "Chunk":
            for leave in subtree.leaves():
                if lemmatizer.lemmatize(leave[0]) == lemmatizer.lemmatize("population"):
                    entity_name = ' '.join(c[0] for c in subtree.leaves())
                    population_subtrees.append(entity_name)
                
                if lemmatizer.lemmatize((leave[[0]] == lemmatizer.lemmatize("area"))):
                    entity_name = ' '.join(c[0] for c in subtree.leaves())
                    areas_subtrees.append(entity_name)

    return region_entities, population_subtrees, areas_subtrees


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


def search_population(tagged):
    cp = nltk.chunk.RegexpParser( " Chunk: {<NN>*<IN>*<DT>*<NNP>*<IN>*<NNP>*<VBZ>*<CD>} " )

    result = cp.parse(tagged)

    # print(result)
    result.draw()
    relations = []
    for tagged_tree in result.subtrees():
        if tagged_tree.label() == "Chunk":
            for leave in tagged_tree.leaves():
                if lemmatizer.lemmatize(leave[0]) == lemmatizer.lemmatize("population"):
                    entity_name = ' '.join(leave[0] for c in tagged_tree.leaves())
                    relations.append(entity_name)
    
    print(relations)
    return relations


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


# content = "Cuba is the second-most populous country in the Caribbean after Haiti, with over 11 million inhabitants. With an area of 505,990 km2 (195,360 sq mi), Spain is the second-largest country in the European Union (EU). The official area of the Republic of Cuba is 109,884 km2"
 
main()