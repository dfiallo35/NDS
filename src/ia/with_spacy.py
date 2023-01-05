import re

import get_nations
import locationtagger
import spacy
import wikipedia
from spacy import displacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokenizer import Tokenizer

nlp = spacy.load("en_core_web_sm")

# spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

# # removes stopwords and punctuation signs
# clean_doc = [token for token in my_doc if not token.is_stop and not token.is_punct]

# # Lemmatization 
# clean_doc_lemma = [token.lemma_ for token in clean_doc]


# Initialize
def main():
    # len(countries) = 191
    # the list 'countries' has the countries ordered by the hdi index rank
    # in 'country_hdi' is a dictionary with keys as countries and value as its hdi index
    
    countries, countries_hdi = get_nations.get_all_countries()

    countries_regions = dict()
    countries_area = dict()
    countries_population = dict()
        
    country_content = get_pages(countries)

    for country in countries:
        regions_to_process, area_to_process, population_to_process = text_processing(country, country_content[country])

        # region, area, population = match_sentence_processing(country,  regions_to_process, area_to_process, population_to_process)

        # countries_regions[country] = regions
        # countries_area[country] = area
        # countries_population[country] = population


def for_tests():
    countries = ["United States"]    

    countries_regions = dict()
    countries_area = dict()
    countries_population = dict()
        
    # country_content = get_pages(["United States"])
    
    # countries = ["Cuba"]
    # countries_hdi = [{"Cuba": 0.87}]

    country_content = dict()
    # country_content["Cuba"] = "According to the official census of 2010, Cuba's population was 11,241,161, comprising 5,628,996 men and 5,612,165 women. The official area of the Republic of Cuba is 109,884 km2 (42,426 sq mi) (without the territorial waters) but a total of 350,730 km2 (135,418 sq mi) including the exclusive economic zone. Cuba is the second-most populous country in the Caribbean after Haiti, with over 11 million inhabitants.[13]"
    country_content["United States"] = "The U.S. Census Bureau reported 331,449,281 residents as of April 1, 2020,[o][389] making the United States the third most populous nation in the world, after China and India."
    
    for country in countries:
        regions_to_process, area_to_process, population_to_process = text_processing(country, country_content[country])

        # region, are, population = match_sentence_processing(country,  regions_to_process, area_to_process, population_to_process)

        # countries_regions[country] = regions
        # countries_area[country] = area
        # countries_population[country] = population


# OK
def get_pages(countries: list):
    country_content = dict()

    # for country in countries[0:4]:
    for country in countries:
        content = wikipedia.page(title=country, auto_suggest=False).content # auto_suggest=False fix problems with Cuba's and Canada's pages upload 
  
        country_content[country] = content
            
    return country_content


def clean(doc):
    tokens = []

    # remove stopwords
    tokens = [token for token in doc if not token.is_stop]

    # remove empty tokens
    tokens = [token for token in tokens if token.text.strip() != ""] 
    
    # # remove punctuation marks
    # token = [token for token in tokens if not token.is_punct]

    # lemmatize
    text = " ".join([token.lemma_ for token in tokens])

    return text


# OK
def sent_tokenize(text: str):
    raw_doc = nlp(text)

    # sentences = list(raw_doc.sents)

    clean_text = clean(raw_doc)

    doc = nlp(clean_text)

    sentences = list(doc.sents)
    
    # print(sentences)
    return sentences


def text_processing(country: str, content: str):  
    sentences = sent_tokenize(content)

    list_regions = []
    area_sents = []
    population_sents = []

    for sent in sentences:
        # detecting countries, cities, regions
       
        list_regions = regions_extract(sent)
        
        print("regions in text: ", list_regions)

        areas = []
        pop = []

        # Population matcher
        pop_matcher = population_matcher(sent)

        for match_id, start, end in pop_matcher:
            # for match_id_1, start_1, end_1 in pop_matcher:
            span = sent[start:end]
            
            population_sents.append(span)
            print("pop_matcher: ", span.text)


        # Population phrase matcher

        # pop_phrase_matcher = population_phrase_matcher(sent)

        # for match_id, start, end in pop_phrase_matcher:
        #     span = sent[start:end]
        #     print("pop_phrase_matcher: ", span.text)

       
        # Area matcher

        _area_matcher = area_matcher(sent)

        for match_id, start, end in _area_matcher:
            span = sent[start:end]            
            area_sents.append(span)
            print("area_matcher: ", span.text) 


        # Area phrase matcher
        # _area_phrase_matcher = area_phrase_matcher(sent)       

        # for match_id, start, end in _area_phrase_matcher:
        #     span = sent[start:end]
        #     print("area_phrase_matcher: ", span.text)

    return list_regions, area_sents, population_sents


def regions_extract(sent):
    list_regions = []

    for entity in sent.ents:
        if (entity.label_ == "GPE" or entity.label_ == "LOC") and entity.text not in list_regions:
            list_regions.append(entity.text)
    
    return list_regions


def population_matcher(sent):
    # print(sent)
    # for token in sent:
    #     print(token.text, " ", token.pos_)

    matcher = Matcher(nlp.vocab)
    
    pattern = [
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
            {"TEXT": {"REGEX": "mi"}}, 
            {"TEXT": {"REGEX": "mi"}}
        ],
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "mile"}}
        ]
    ]
    
    matcher.add("area", pattern) 

    matches = (matcher(sent))

    return matches


# def match_sentence_processing(country: str,  regions_to_process: list, sents_area_to_process, sents_population_to_process):
#     temp_area_text = []
#     temp_area_matche_id = []

#     for item in sents_area_to_process:
#         if len(temp_area) == 0:
#             temp_area.append(item.text)
#             # temp_area_matche_id(item)

#         else:
#             item.text



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