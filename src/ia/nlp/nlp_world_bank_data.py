import nltk
import pandas as pandas
import spacy as sp
import wbdata as wbd
import world_bank_data as wb
from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer

nlp = sp.load("en_core_web_sm")


# def main(text: str):
#     text_processing(text)


indicator = {'population': 'SP.POP.TOTL', 'hci': 'HD.HCI.OVRL', 'human capital index': 'HD.HCI.OVRL', 'life expectancy': 'SP.DYN.LE00.IN',
             'poverty headcount ratio': 'SI.POV.DDAY', 'population growth': 'SP.POP.GROW', 'migration': 'SM.POP.NETM', 'GDP': 'NY.GDP.MKTP.CD',
             'GDP per capita': 'NY.GDP.PCAP.CD', 'GDP growth': 'NY.GDP.MKTP.KD.ZG', 'unemployment': 'SL.UEM.TOTL.ZS', 'inflation': 'FP.CPI.TOTL.ZG',
             'personal remittances': 'BX.TRF.PWKR.DT.GD.ZS', 'CO2 emissions': 'EN.ATM.CO2E.PC', 'forest area': 'AG.LND.FRST.ZS',
             'access to electricty': 'EG.ELC.ACCS.ZS', 'annual freshwater withdrawals': 'ER.H2O.FWTL.ZS',
             'people using safely managed sanitation services': 'SH.STA.SMSS.ZS', 'intentional homicides': 'VC.IHR.PSRC.P5',
             'central government debt': 'GC.DOD.TOTL.GD.ZS', 'statistical perfomance indicators': 'IQ.SPI.OVRL',
             'individuals using the internet': 'IT.NET.USER.ZS', 'proportion of seats held by women in national parliaments': 'SG.GEN.PARL.ZS',
             'foreign direct investment': 'BX.KLT.DINV.WD.GD.ZS', 'foreign direct investment': 'BX.KLT.DINV.WD.GD.ZS'}


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

    match_sent = []
    # pop_sents = []
    # hci_sents = []
    # migration_sents = []
    # life_exp_sents = []
    # unemployment_sents = []
    # inflation_sents = []

    result_list = []

    for sent in sentences:

        # Human capital index

        # hci_matcher(sent, hci_sents)
        # sents_proc(hci_sents, "hci", result_list)        
        hci_matcher(sent, match_sent)
        sents_proc(match_sent, "hci", result_list)

        # Total population

        # population_matcher(sent, pop_sents)
        # sents_proc(pop_sents, "population", result_list)
        population_matcher(sent, match_sent)
        sents_proc(match_sent, "population", result_list)

        # Net migration

        # migration_matcher(sent, migration_sents)
        # sents_proc(migration_sents, "migration", result_list)
        migration_matcher(sent, match_sent)
        sents_proc(match_sent, "migration", result_list)

        # Life expectancy

        # life_exp_matcher(sent, life_exp_sents)
        # sents_proc(life_exp_sents, "life expectancy", result_list)
        life_exp_matcher(sent, match_sent)
        sents_proc(match_sent, "life expectancy", result_list)

        # Unemployment

        # unemployment_matcher(sent, unemployment_sents)
        # sents_proc(unemployment_sents, "unemployment", result_list)
        unemployment_matcher(sent, match_sent)
        sents_proc(match_sent, "unemployment", result_list)

        # Inflation

        # inflation_matcher(sent, inflation_sents)
        # sents_proc(inflation_sents, "inflation", result_list)
        inflation_matcher(sent, match_sent)
        sents_proc(match_sent, "inflation", result_list)

    return result_list

    # print(result_list)


ind = {'population': 'SP.POP.TOTL', 'inflation': 'FP.CPI.TOTL.ZG', 'migration': 'SM.POP.NETM',
       'hci': 'HD.HCI.OVRL', 'life expectancy': 'SP.DYN.LE00.IN', 'unemployment': 'SL.UEM.TOTL.ZS'}


def sents_proc(sents, id: str, result_list: list):
    # result_list = []

    if len(sents) > 0:
        span = sents[len(sents) - 1]
        date = ''
        country = []

        for token in span:
            if token.ent_type_ == 'DATE':
                date = token.text

            if token.ent_type_ == 'GPE':
                country.append(wbd.search_countries(token.text)[0]['iso2Code'])

        try:
            result_list.append(wb.get_series(ind[id], country=country,
                                             date=date, id_or_value='id', simplify_index=False))

        except:
            result_list.append(
                "The requested data about " + id + " was not found")


# def country_ent_extract(sent):
#     list_regions = []

#     for entity in sent.ents:
#         if (entity.label_ == "GPE" or entity.label_ == "LOC") and entity.text not in list_regions:
#             list_regions.append(entity.text)

#     return list_regions


def population_matcher(sent, pop_sents):
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

    for match_id, start, end in matches:
        span = sent[start:end]

        pop_sents.append(span)


def hci_matcher(sent, hci_sents):
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

    for match_id, start, end in matches:
        span = sent[start:end]

        hci_sents.append(span)


def migration_matcher(sent, migration_sents):
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

    for match_id, start, end in matches:
        span = sent[start:end]

        migration_sents.append(span)


def life_exp_matcher(sent, life_exp_sents):
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

    matcher.add('life_expec', pattern)

    matches = (matcher(sent))

    for match_id, start, end in matches:
        span = sent[start:end]

        life_exp_sents.append(span)


def unemployment_matcher(sent, unemployment_sents):
    matcher = Matcher(nlp.vocab)

    pattern = [
        [
            {'TEXT': {'REGEX': 'unemployment'}},
            {'POS': {'IN': ['PROPN', 'NOUN', 'ADJ',
                            'VERB', 'PUNCT']}, 'OP': '*'},
            {"LIKE_NUM": True, 'SHAPE': 'dddd', 'OP': "*"}
        ]
    ]

    matcher.add('unemployment', pattern)

    matches = (matcher(sent))

    for match_id, start, end in matches:
        span = sent[start:end]

        unemployment_sents.append(span)


def inflation_matcher(sent, inflation_sents):
    matcher = Matcher(nlp.vocab)

    pattern = [
        [
            {'TEXT': {'REGEX': 'inflation'}},
            {'POS': {'IN': ['PROPN', 'NOUN', 'ADJ',
                            'VERB', 'PUNCT']}, 'OP': '*'},
            {"LIKE_NUM": True, 'SHAPE': 'dddd', 'OP': "*"}
        ]
    ]

    matcher.add('inflation', pattern)

    matches = (matcher(sent))

    for match_id, start, end in matches:
        span = sent[start:end]

        inflation_sents.append(span)


# for item in text_processing("What was the life expectancy, population, migration, hci, unemployment, inflation of Spain in 2020"):
#     print("   ")
#     print(item)

# print(text_processing("What was the population and the life expectancy of Cuba in 2020"))
