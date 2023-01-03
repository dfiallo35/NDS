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


# OK
def sent_tokenize(text: str):
    raw_doc = nlp(text)

    sentences = list(raw_doc.sents)

    return sentences


def text_processing(country: str, content: str):  
    sentences = sent_tokenize(content)
    list_places = set()
    area_sents = set()
    population_sents = set()

    for sent in sentences:
        # clean_doc = [token for token in my_doc if not token.is_stop and not token.is_punct]

        # detecting countries, cities, regions
       
        for entity in sent.ents:
            if entity.label_ == "GPE":
                list_places.add(entity.text)

        areas = []
        pop = []
        for token in sent:
            
            if token.lemma_ == "area":
                areas.append([ent for ent in sent.ents])
                if sent not in area_sents:
                    area_sents.add(sent)
                    print(area_sents)

            if token.like_num:
                j = token.i + 1 # next token index
                if j < len(sent):
                    next_token = sent[j]
                    if next_token.text == 'km2':
                        print(token.text)
                        area_sents.add(sent)


            if token.lemma_ == "population":
                pop.append([ent for ent in sent. ents])
                if sent not in population_sents:
                    population_sents.add(sent)
                    print(population_sents)

        # if "area" in sent.string.lower():

        # Initializing the matcher with vocab
        matcher = Matcher(nlp.vocab)

        my_pattern = []
        # my_pattern.append({"LEMMA": "area"})
        my_pattern.append({"POS": {"IN": ["NOUN", "PROPN"]}})
        my_pattern.append({"LIKE_NUM": True})
    
        matcher.add(key='AreaSearch', patterns=[my_pattern])

        areas_matches = matcher(sent)

        for match_id, start, end in areas_matches:
            string_id = nlp.vocab.strings[match_id] 
            span = sent[start:end] 
            # print(span.text)

        # matcher = PhraseMatcher(nlp.vocab)

        # ruler = nlp.add_pipe("entity_ruler")

        # patterns = [{"label": "area", "pattern": [{"TEXT": "(area)"}]}]

        # ruler.add_patterns(patterns)

        # for ent in sent.ents:
        #     if "km2" in ent.text:
        #         ent.label_ = "AREA"

        #     print(ent.text, ent.label_)

        # print("lllll")
        # print([(ent.text, ent.label_) for ent in sent.ents])


def extract_area_relation(doc):
    ...

main()