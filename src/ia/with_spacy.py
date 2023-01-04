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


# 
def main():
    # countries, countries_hdi = get_nations.get_all_countries()
    
    # country_content = get_pages(countries)


    # countries = ["United States"]    
    
    # country_content = get_pages(["United States"])
    
    countries = ["Cuba"]
    countries_hdi = [{"Cuba": 0.87}]

    country_content = dict()
    country_content["Cuba"] = "According to the official census of 2010, Cuba's population was 11,241,161, comprising 5,628,996 men and 5,612,165 women. The official area of the Republic of Cuba is 109,884 km2 (42,426 sq mi) (without the territorial waters) but a total of 350,730 km2 (135,418 sq mi) including the exclusive economic zone. Cuba is the second-most populous country in the Caribbean after Haiti, with over 11 million inhabitants.[13]"


    # for country in countries[0:4]:
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

    # with content.retokenize() as retokenizer:
    #     attrs = {"NOUN": "PROPN"}
    #     retokenizer.merge(cpntent[0:2], attrs=attrs)

    for sent in sentences:
        # detecting countries, cities, regions
       
        list_regions.add(region for region in regions_extract(sent))

        areas = []
        pop = []
        # for token in sent:
            
            # if token.lemma_ == "area":
            #     areas.append([ent for ent in sent.ents])
            #     if sent not in area_sents:
            #         area_sents.add(sent)
            #         print(area_sents)

            # if token.lemma_ == "population":
            #     pop.append([ent for ent in sent. ents])
            #     if sent not in population_sents:
            #         population_sents.add(sent)
            #         print(population_sents)


        # Population phrase matcher
        # pop_phrase_matcher = population_phrase_matcher(sent)

        # for match_id, start, end in pop_phrase_matcher:
        #     span = sent[start:end]
        #     print("pop_phrase_matcher: ", span.text)

        # Population matcher
        pop_matcher = population_matcher(sent)

        for match_id, start, end in pop_matcher:
            span = sent[start:end]
            print("pop_matcher: ", span.text)


        # Area phrase matcher
        # _area_phrase_matcher = area_phrase_matcher(sent)       

        # for match_id, start, end in _area_phrase_matcher:
        #     span = sent[start:end]
        #     print("area_phrase_matcher: ", span.text)

        _area_matcher = area_matcher(sent)
        for match_id, start, end in _area_matcher:
            span = sent[start:end]
            print("area_matcher: ", span.text)



# def remove_entities(sent):
#     entities = [entity.text for entity in sent.ents]

#     for token in sent:
#         tokens = [token for token in sent if not (token.text in entities)]

#     text = " ".join([token.text for token in tokens])
    
#     doc = nlp(text)

#     return doc



def regions_extract(sent):
    list_regions = set()

    for entity in sent.ents:
        if entity.label_ == "GPE":
            list_regions.add(entity.text)
    
    return list_regions


def population_matcher(sent):
    # print(sent)
    # for token in sent:
    #     print(token.text, " ", token.pos_)

    matcher = Matcher(nlp.vocab)
    
    pattern = [
        [
            {"TEXT" : {"REGEX": "population"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}
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
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX":"km2"}}
        ], 
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "mi"}}, 
            {"TEXT": {"REGEX": "mi"}}
        ],
        [
            {"TEXT" : {"REGEX": "area"}}, 
            {"POS": {"IN": ["PROPN", "NOUN", "ADJ"]}, "OP": "*"}, 
            {"LIKE_NUM": True, "OP": "+"}, 
            {"TEXT": {"REGEX": "square"}}, 
            {"TEXT": {"REGEX": "mile"}}
        ]
    ]
    
    matcher.add("area", pattern) 

    matches = (matcher(sent))

    return matches


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