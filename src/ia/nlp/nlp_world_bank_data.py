import nltk
import pandas as pandas
import spacy as sp
import wbdata as wbd
import world_bank_data as wb
from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer

nlp = sp.load("en_core_web_sm")


def main(text: str):
    text_processing(text)


def clean(doc):
    tokens = []

    # remove stopwords
    tokens = [token for token in doc if not token.is_stop]

    # remove empty tokens
    tokens = [token for token in tokens if token.text.strip() != ""]

    # lemmatize
    text = " ".join([token.lemma_ for token in tokens])

    return text


def sent_tokenize(text: str):
    """
    Dado un string guarda su contenido en un documento spacy 

    Retorna una lista de las oraciones de este documento
    """

    raw_doc = nlp(text)

    clean_text = clean(raw_doc)

    doc = nlp(clean_text)

    sentences = list(doc.sents)

    return sentences


def text_processing(content: str):
    sentences = sent_tokenize(content)

    pop_sents = []
    hci_sents = []
    migration_sents = []
    life_exp_sents = []

    for sent in sentences:
        list_country = country_ent_extract(sent)
        print(list_country)

        match_hci(sent, hci_sents)

        match_pop(sent, pop_sents)

        match_migration(sent, migration_sents)

        match_life_exp(sent, life_exp_sents)

        sents_proc(pop_sents, "population")
        sents_proc(hci_sents, "hci")
        sents_proc(migration_sents, "migration")
        sents_proc(life_exp_sents, "life_exp")


def sents_proc(sents, id: str):
    for span in sents:
        date = ''
        country = ''

        for token in span:
            if token.ent_type_ == 'DATE':
                date = token.text

            if token.ent_type_ == 'GPE':
                # country = token.text
                country = wbd.search_countries(token.text)[0]['iso2Code']

                # print(wbd.search_countries(country)[0]['iso2Code'])

        if id == "population":
            try:
                print(wb.get_series('SP.POP.TOTL', country=country,
                      date=date, id_or_value='id', simplify_index=True))
            except:
                print("The requested data was not found")

        if id == "hci":
            try:
                print(wb.get_series('HD.HCI.OVRL', country=country,
                      date=date, id_or_value='id', simplify_index=True))
            except:
                print("The requested data was not found")

        if id == "migration":
            try:
                print(wb.get_series('SM.POP.NETM', country=country,
                      date=date, id_or_value='id', simplify_index=True))
            except:
                print("The requested data was not found")

        if id == "life_exp":
            try:
                print(wb.get_series('SP.DYN.LE00.IN', country=country,
                      date=date, id_or_value='id', simplify_index=True))
            except:
                print("The requested data was not found")


def country_ent_extract(sent):
    list_regions = []

    for entity in sent.ents:
        if (entity.label_ == "GPE" or entity.label_ == "LOC") and entity.text not in list_regions:
            list_regions.append(entity.text)

    return list_regions


def match_pop(sent, pop_sents):
    pop_matcher = population_matcher(sent)

    for match_id, start, end in pop_matcher:
        span = sent[start:end]

        population_sents.append(span)


def population_matcher(sent):
    matcher = Matcher(nlp.vocab)

    pattern = [
        [
            {'TEXT': {'REGEX': 'population'}},
            {'POS': {'IN': ['PROPN', 'NOUN', 'ADJ',
                            'VERB', 'PUNCT']}, 'OP': '*'},
            {"LIKE_NUM": True, 'SHAPE': 'dddd', 'OP': "*"}
        ]
    ]

    matcher.add('population', pattern)

    matches = (matcher(sent))

    return matches


def match_hci(sent, hci_sents):
    _hci_matcher = hci_matcher(sent)

    for match_id, start, end in _hci_matcher:
        span = sent[start:end]

        hci_sents.append(span)


def hci_matcher(sent):
    matcher = Matcher(nlp.vocab)

    pattern = [
        [
            {'TEXT': {'REGEX': 'hci'}},
            {'POS': {'IN': ['PROPN', 'NOUN', 'ADJ',
                            'VERB', 'PUNCT']}, 'OP': '*'},
            {"LIKE_NUM": True, 'SHAPE': 'dddd', 'OP': "*"}
        ],
        [
            {'TEXT': {'REGEX': 'human'}},
            {'TEXT': {'REGEX': 'capital'}},
            {'TEXT': {'REGEX': 'index'}},
            {'POS': {'IN': ['PROPN', 'NOUN', 'ADJ',
                            'VERB', 'PUNCT']}, 'OP': '*'},
            {"LIKE_NUM": True, 'SHAPE': 'dddd', 'OP': "*"}
        ]
    ]

    matcher.add('hci', pattern)

    matches = (matcher(sent))

    return matches


def match_migration(sent, migration_sents):
    mig_matcher = migration_matcher(sent)

    for match_id, start, end in mig_matcher:
        span = sent[start:end]

        migration_sents.append(span)


def migration_matcher(sent):
    matcher = Matcher(nlp.vocab)

    pattern = [
        [
            {'TEXT': {'REGEX': 'migration'}},
            {'POS': {'IN': ['PROPN', 'NOUN', 'ADJ',
                            'VERB', 'PUNCT']}, 'OP': '*'},
            {"LIKE_NUM": True, 'SHAPE': 'dddd', 'OP': "*"}
        ]
    ]

    matcher.add('migration', pattern)

    matches = (matcher(sent))

    return matches


def match_life_exp(sent, life_exp_sents):
    l_e_matcher = life_exp_matcher(sent)

    for match_id, start, end in l_e_matcher:
        span = sent[start:end]

        life_exp_sents.append(span)


def life_exp_matcher(sent):
    matcher = Matcher(nlp.vocab)

    pattern = [
        [
            {'TEXT': {'REGEX': 'life'}},
            {'TEXT': {'REGEX': 'expectancy'}},
            {'POS': {'IN': ['PROPN', 'NOUN', 'ADJ',
                            'VERB', 'PUNCT']}, 'OP': '*'},
            {"LIKE_NUM": True, 'SHAPE': 'dddd', 'OP': "*"}
        ]
    ]

    matcher.add('migration', pattern)

    matches = (matcher(sent))

    return matches


text_processing("What was the life expectancy of Cuba in 2020")