import world_bank_data as wb

from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer
from spacy.language import Language
from spacy import load

from json import load as json_load
from os.path import realpath, join, dirname
data_dir= realpath(join(dirname(__file__), 'data'))

import pandas as pd

nlp = load("en_core_web_sm")
years= [str(year) for year in range(1960, 2023)]


class NLPMatcher:
    def __init__(self):
        self.matcher = Matcher(nlp.vocab)
        self.patterns = []

    def match(self, sentence: str):
        elements= []
        for match_id, start, end in (self.matcher(sentence)):
            span = sentence[start:end]
            elements.append((nlp.vocab.strings[match_id], span.text))
        return elements
    
    def add(self, id: str, patterns: list):
        self.patterns.append(patterns)
        self.matcher.add(id, patterns)



class NLP:
    def __init__(self):
        self.nations:dict = NLP.get_nations()
        self.indicators:dict = NLP.get_indicators()
        self.nation_matcher = self.generate_nation_matcher()
        self.indicators_matcher = self.generate_indicators_matcher()
        self.year_matcher = self.generate_year_matcher()
    

    def get_nations():
        with open(realpath(join(data_dir,'countries.json'))) as json_file:
            data = json_load(json_file)
            return data['name']
    
    def get_indicators():
        with open(realpath(join(data_dir,'data.json'))) as json_file:
            data = json_load(json_file)
            return data['name']
    


    def generate_nation_matcher(self):
        matcher= NLPMatcher()
        for nat in self.nations:
            pnat= []
            for word in self.tokenize_pattern(nat):
                word= str(word)
                pnat.append({'TEXT': word.lower()})
            if pnat:
                matcher.add(nat, [pnat])

        for key, nat in zip(self.nations, self.nations.values()):
            pnat= []
            for word in self.tokenize_pattern(nat):
                word= str(word)
                pnat.append({'TEXT': word.lower()})
            if pnat:
                matcher.add(key, [pnat])

        return matcher
    
    def generate_indicators_matcher(self):
        matcher= NLPMatcher()
        for key, ind in zip(self.indicators.keys(), self.indicators.values()):
            pind= []
            for word in self.tokenize_pattern(ind.split('(')[0]):
                word= str(word)
                if len(pind) < 2:
                    pind.append({'TEXT': word.lower()})
                else:
                    pind.append({'TEXT': word.lower(), 'OP': '?'})
            if pind:
                matcher.add(key, [pind])

        return matcher
    
    def generate_year_matcher(self):
        matcher= NLPMatcher()
        matcher.add('year', [[{'SHAPE': 'dddd'}]])
        return matcher



    def tokenize_pattern(self, text: str):
        tokens= self.tokenize(text)
        return [i for i in tokens if not i.is_punct]

    def tokenize(self, text: str):
        nlp_text= nlp(text.lower())
        tokens = [token for token in nlp_text if not token.is_stop and token.text.strip() != ""]
        return tokens
        
    def normalize(self, text: str):
        tokens= self.tokenize(text)
        new_text:Language = nlp(" ".join([token.lemma_ for token in tokens]))
        return list(new_text.sents)



    def text_processing(self, content: str):
        results= []
        for sentence in self.normalize(content):
            nations= self.match_nation(sentence)
            years= self.match_year(sentence)
            data= self.match_data(sentence)

            r={}
            if nations:
                r['nations']= nations
            if years:
                r['years']= years
            if data:
                r['data']= data
            if r:
                results.append(r)
            
        return results
    
    def get_results(self, results: list):
        rsl= []
        for result in results:
            if not result.get('nations'):
                print('Error: No nations')

            elif result.get('nations') and result.get('data') and result.get('years'):
                if len(result['years']) > 1:
                    print('Error: More than one year')
                
                else:
                    r= {data[1]: [] for data in result['data']}
                    index= [i[1] for i in result['nations']]
                    for nation in result['nations']:
                        for data in result['data']:
                            try:
                                series= wb.get_series(data[0], nation[0], date=str(result['years'][0][1]))
                                r[data[1]].append(series.tolist()[0])
                            except:
                                r[data[1]].append(None)
                    
                    rsl.append(
                        pd.DataFrame(r, index=index)
                    )
                
            
            elif result.get('nations') and result.get('data') and not result.get('years'):
                if len(result['nations']) > 1 and len(result['data']) > 1:
                    print('Error: More than one nation and data')
                
                elif len(result['nations']) > 1 or len(result['nations']) ==1  and len(result['data']) == 1:
                    r= {year : [] for year in years}
                    index= [i[1] for i in result['nations']]
                    for nation in result['nations']:
                        series= wb.get_series(result['data'][0][0], nation[0])
                        data= {key: val for key, val in zip(list(series.axes[0].levels[2]), series.tolist())}
                        for year in years:
                            r[year].append(data.get(year))
                        
                    rsl.append(
                        pd.DataFrame(r, index= index)
                    )
                
                elif len(result['nations']) == 1 and len(result['data']) > 1:
                    r= {year : [] for year in years}
                    index= [i[1] for i in result['data']]
                    for data in result['data']:
                        series= wb.get_series(data[0], result['nations'][0][0])
                        data= {key: val for key, val in zip(list(series.axes[0].levels[2]), series.tolist())}
                        for year in years:
                            r[year].append(data.get(year))
                    
                    rsl.append(
                        pd.DataFrame(r, index= index)
                    )

            
            elif result.get('nations') and not result.get('data') and not result.get('years'):
                print('Error: Select data')
        return rsl
        
    def get_data(self, query: str):
        '''
        Create DataFrames based on the query
        '''
        data= self.text_processing(query)
        results= self.get_results(data)
        return results

    def get_nation(self, query: str, map):
        '''
        Generate the nations based on the query and add them to the map
        '''
        ...
    

    def match_nation(self, sentence):
        return self.nation_matcher.match(sentence)

    def match_data(self, sentence):
        return self.indicators_matcher.match(sentence)
    
    def match_year(self, sentence):
        return self.year_matcher.match(sentence)
        

# a= NLP()
# print(a.text_processing('from Cuba take the Population also the life expectancy the hci and the net migration in 2030. From Brazil take the migration. Then from Cuba the population'))

