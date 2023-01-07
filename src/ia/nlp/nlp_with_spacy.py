import re

import get_nations
import locationtagger
import spacy
import wikipedia
from spacy import displacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokenizer import Tokenizer
import math

nlp = spacy.load("en_core_web_sm")


# Initialize
def main():
    # len(countries) = 191
    # the list 'countries' has the countries ordered by the hdi index rank
    # in 'country_hdi' is a dictionary with keys as countries and value as its hdi index
    
    countries, countries_hdi = get_nations.get_all_countries()

    # countries = ["Czechia"]

    countries_regions = dict()
    countries_area = dict()
    countries_population = dict()
    
    country_content = get_pages(countries[4:10])

    for country in countries[4:10]:
        regions_to_process, area_to_process, population_to_process = text_processing(country, country_content[country])

        area, population = match_sentence_processing(country,  regions_to_process, area_to_process, population_to_process)
        
        # countries_regions[country] = regions
        countries_area[country] = area
        countries_population[country] = population


    print("areas: ", countries_area)
    print("population: ", countries_population)


def for_tests():
    countries_regions = dict()
    countries_area = dict()
    countries_population = dict()
        
    # country_content = get_pages(["United States"])
    
    # countries = ["Cuba"]
    # countries_hdi = [{"Cuba": 0.87}]

    country_content = dict()
    # country_content["Cuba"] = "According to the official census of 2010, Cuba's population was 11.2 million, comprising 5,628,996 men and 5,612,165 women. The official area of the Republic of Cuba is 109,884 km2 (42,426 sq mi) (without the territorial waters) but a total of 350,730 km2 (135,418 sq mi) including the exclusive economic zone. Cuba is the second-most populous country in the Caribbean after Haiti, with over 11 million inhabitants.[13]"
    
    # countries = ["United States"]    
    # country_content["United States"] = "The U.S. Census Bureau reported 331,449,281 residents as of April 1, 2020,[o][389] making the United States the third most populous nation in the world, after China and India. The 48 contiguous states and the District of Columbia occupy a combined area of 3,119,885 square miles (8,080,470 km2). Of this area, 2,959,064 square miles (7,663,940 km2) is contiguous land, composing 83.65% of total U.S. land area. About 15% is occupied by Alaska, a state in northwestern North America, with the remainder in Hawaii, a state and archipelago in the central Pacific, and the five populated but unincorporated insular territories of Puerto Rico, American Samoa, Guam, the Northern Mariana Islands, and the U.S. Virgin Islands. Measured by only land area, the United States is third in size behind Russia and China, and just ahead of Canada."
    
    countries = ["Norway"]
    country_content["Norway"] = "Norway has a total area of 385,207 square kilometres (148,729 sq mi) and had a population of 5,425,270 in January 2022"

    for country in countries:
        regions_to_process, area_to_process, population_to_process = text_processing(country, country_content[country])

        # region, area, population = match_sentence_processing(country,  regions_to_process, area_to_process, population_to_process)        area, population = match_sentence_processing(country,  regions_to_process, area_to_process, population_to_process)
        
        area, population = match_sentence_processing(country,  regions_to_process, area_to_process, population_to_process)
        
        # countries_regions[country] = regions
        countries_area[country] = area
        countries_population[country] = population

        print("area: ", area, "population: ", population)


# OK
def get_pages(countries: list):
    country_content = dict()

    # for country in countries[0:4]:
    for country in countries:
        title = country + " country"

        if country == "Czechia":
            title = "Czech Republic"

        content = wikipedia.page(title=title).content # auto_suggest=False fix problems with Cuba's and Canada's pages upload

        country_content[country] = content
            
    return country_content


def clean(doc):
    tokens = []

    # remove stopwords
    tokens = [token for token in doc if not token.is_stop]

    # remove empty tokens
    tokens = [token for token in tokens if token.text.strip() != ""] 
    
    # lemmatize
    text = " ".join([token.lemma_ for token in tokens])

    return text


# OK
def sent_tokenize(text: str):
    raw_doc = nlp(text)

    clean_text = clean(raw_doc)

    doc = nlp(clean_text)

    sentences = list(doc.sents)
    
    return sentences


def text_processing(country: str, content: str):  
    sentences = sent_tokenize(content)

    list_regions = []
    area_sents = []
    population_sents = []

    for sent in sentences:
        # detecting countries, cities, regions       
        list_regions = regions_extract(sent)
        
        # print("regions in text: ", list_regions)

        # Population matcher
        match_pop(sent, population_sents)
        
        # Area matcher
        match_area(sent, area_sents)
        
    return list_regions, area_sents, population_sents


def match_pop(sent, population_sents):
    pop_matcher = population_matcher(sent)

    for match_id, start, end in pop_matcher:
        span = sent[start:end]
            
        population_sents.append(span)
        # print("pop_matcher: ", span.text)


def match_area(sent, area_sents):
    _area_matcher = area_matcher(sent)

    for match_id, start, end in _area_matcher:
        span = sent[start:end]            
        area_sents.append(span)
        # print("area_matcher: ", span.text) 


def regions_extract(sent):
    list_regions = []

    for entity in sent.ents:
        if (entity.label_ == "GPE" or entity.label_ == "LOC") and entity.text not in list_regions:
            list_regions.append(entity.text)
    
    return list_regions


def population_matcher(sent):
    matcher = Matcher(nlp.vocab)
    
    pattern = [
        [
            # {"TEXT" : {"REGEX": {"IN": ["population", "census"]}}},   
            {"TEXT" : {"REGEX": "population"}},             
            {"LIKE_NUM": True, "OP": "+"},
        ],
        [
            # {"TEXT" : {"REGEX": {"IN": ["population", "census"]}}},   
            {"TEXT" : {"REGEX": "population"}},             
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"},
            {"TEXT": {"REGEX": "reside"}, "OP": "*"}

        ],
        [
            {"TEXT" : {"REGEX": "total"}},   
            {"TEXT" : {"REGEX": "population"}},             
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"},
            {"TEXT": {"REGEX": "reside"}, "OP": "*"}

        ],
        # [
        #     {"POS": "PROPN"},   
        #     {"TEXT" : {"REGEX": "population"}},             
        #     {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
        #     {"LIKE_NUM": True, "OP": "+"},
        #     {"TEXT": {"REGEX": "reside"}, "OP": "*"}

        # ],
        [  
            {"LOWER" : "census"},             
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "+"}, 
            {"LIKE_NUM": True, "OP": "+"},
            # {"TEXT": {"REGEX": "reside"}, "OP": "*"}
        ],
        [    
            {"LOWER" : {"REGEX": "census"}},   
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"TEXT" : {"REGEX": "population"}},          
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"},
            # {"TEXT": {"REGEX": "reside"}, "OP": "*"}

        ]
    ]
    
    matcher.add("population", pattern) 

    matches = (matcher(sent))

    return matches


def area_matcher(sent):
    matcher = Matcher(nlp.vocab)

    pattern = [
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX":"km2"}}
        ], 
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX":"square"}}, 
            {"TEXT": {"REGEX":"kilometer"}}
        ], 
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX":"square"}}, 
            {"TEXT": {"REGEX":"kilometre"}}
        ],
        [
            {"TEXT" : {"REGEX": "span"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX":"km2"}}
        ], 
        [
            {"TEXT" : {"REGEX": "encompass"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX":"km2"}}
        ], 
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "mi"}}, 
            {"TEXT": {"REGEX": "mi"}}
        ],
        [
            {"TEXT" : {"REGEX": "span"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "mi"}}, 
            {"TEXT": {"REGEX": "mi"}}
        ],
        [
            {"TEXT" : {"REGEX": "encompass"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "mi"}}, 
            {"TEXT": {"REGEX": "mi"}}
        ],
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "mile"}}
        ],
        [
            {"TEXT" : {"REGEX": "span"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "mile"}}
        ],
        [
            {"TEXT" : {"REGEX": "encompass"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "mile"}}
        ],
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "kilometer"}}
        ],
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "kilometre"}}
        ],
        [
            {"TEXT" : {"REGEX": "span"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "kilometer"}}
        ],
        [
            {"TEXT" : {"REGEX": "span"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "kilometre"}}
        ],
        [
            {"TEXT" : {"REGEX": "encompass"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "kilometer"}}
        ],
        [
            {"TEXT" : {"REGEX": "encompass"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "kilometre"}}
        ],
    ]
    
    matcher.add("area", pattern) 

    matches = (matcher(sent))

    return matches


def match_sentence_processing(country: str,  regions_to_process: list, sents_area_to_process, sents_population_to_process):
    country_area = 0
    country_population = 0

    for sent in sents_area_to_process:
        for token in sent:
            if token.like_num:
                digits = ""

                for i in range(0, len(token.text)):
                    if token.text[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        digits = digits + token.text[i] 
                
                if token.head.text == "mi2" or (token.head.text == "mile"): # and sent[token.head.text] == "mile"):
                    temp = float(digits) * 2.589988
                
                    if country_area < temp:
                        country_area = float(temp)
                
                if digits != "" and (token.head.text == "km2" or token.head.text == "kilometre"  or token.head.text == "kilometer") and country_area < float(digits):
                    country_area = float(digits)      
                    

    for sent in sents_population_to_process:
        for token in sent:
            
            if token.text != "million" and token.text != "thousand":                         
                # print(token.text)
                if token.like_num and token.ent_type_ != "PERECENT":                    
                    
                    # print(token.text)
                    digits = ""  
                    # dot = False
                    # n = 0

                    for i in range(0, len(token.text)):
                        
                        # if token.text[i] == ".":
                        #     dot = True
                        #     continue
                        
                        if token.text[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                        # if token.text[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                            digits = digits + token.text[i] 

                            # if dot:
                            #     n = n + 1

                    if digits != "":
                        int_digits = float(digits)
                        # int_digits = int(digits)
                    
                    if token.head.text == "million":
                        # int_digits = int_digits * (10 ** (6 - n))
                        int_digits = int_digits * (10 ** 6)

                    if country_population < int_digits:
                        country_population = int_digits 
                        # print(country_population)   


    return country_area, country_population


def getting_regions(country: str, region_list: list):
    """
    """
    
    # text = ' '.join(r for r in region_list)

    place_entity = locationtagger.find_locations(text)
    
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



# Phrase matchers

def area_phrase_matcher(sent):
    matcher = PhraseMatcher(nlp.vocab)

    area_term = ["area"]
        
    pattern_area = [nlp.make_doc(text) for text in area_term]

    matcher.add("area_phrase_matcher", None, *pattern_area)

    area_phrase_matcher = matcher(sent)
    
    return area_phrase_matcher


def population_phrase_matcher(sent):
    matcher = PhraseMatcher(nlp.vocab)

    pop_terms = ["population", "be"]
        
    pattern_pop = [nlp.make_doc(text) for text in pop_terms]

    matcher.add("pop_phrase_matcher", None, *pattern_pop)

    pop_phrase_matcher = matcher(sent)

    return pop_phrase_matcher


main()

# for_tests()