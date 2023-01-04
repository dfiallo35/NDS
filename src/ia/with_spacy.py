import re

import get_nations
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
    
    country_content = get_pages(countries)

    for country in countries:
        text_processing(country, country_content[country])


def for_tests():
    # countries = ["United States"]    
    
    # country_content = get_pages(["United States"])
    
    countries = ["Cuba"]
    # countries_hdi = [{"Cuba": 0.87}]

    country_content = dict()
    country_content["Cuba"] = "According to the official census of 2010, Cuba's population was 11,241,161, comprising 5,628,996 men and 5,612,165 women. The official area of the Republic of Cuba is 109,884 km2 (42,426 sq mi) (without the territorial waters) but a total of 350,730 km2 (135,418 sq mi) including the exclusive economic zone. Cuba is the second-most populous country in the Caribbean after Haiti, with over 11 million inhabitants.[13]"
    # country_content["United States"] = "The U.S. Census Bureau reported 331,449,281 residents as of April 1, 2020,[o][389] making the United States the third most populous nation in the world, after China and India."
    
    for country in countries:
        text_processing(country, country_content[country])



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

    list_regions = set()
    area_sents = set()
    population_sents = set()

    for sent in sentences:
        # detecting countries, cities, regions
       
        list_regions = regions_extract(sent)

        print("regions in text: ", list_regions)

        areas = []
        pop = []

        # Population matcher
        pop_matcher = population_matcher(sent)

        for match_id, start, end in pop_matcher:
            span = sent[start:end]
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
            print("area_matcher: ", span.text) 


        # Area phrase matcher
        # _area_phrase_matcher = area_phrase_matcher(sent)       

        # for match_id, start, end in _area_phrase_matcher:
        #     span = sent[start:end]
        #     print("area_phrase_matcher: ", span.text)


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
            {"LOWER" : "census"},             
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "+"}, 
            {"LIKE_NUM": True, "OP": "+"},
            {"TEXT": {"REGEX": "reside"}, "OP": "*"}
        ],
        [    
            {"LOWER" : {"REGEX": "census"}},   
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"TEXT" : {"REGEX": "population"}},          
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ", "VERB", "PUNCT"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"},
            {"TEXT": {"REGEX": "reside"}, "OP": "*"}

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