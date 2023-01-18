import nltk
import sqlite3
import pandas as pd
from nltk import load_parser

from nltk import extract_rels, ne_chunk
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import string

lemmatizer  = WordNetLemmatizer()
stopwords   = set(nltk.corpus.stopwords.words('english'))
punctuation = string.punctuation

questions = ['what', 'which', 'how', 'who']





def normalize(text):
    """
    Normalize the text from the sentences
    Uses lemmatization to convert a word to ita cannonical form
    eliminates stopwords and punctuation signs 
    """

    for token in nltk.word_tokenize(text):
        # token = token.lower()
        token = lemmatizer.lemmatize(token)
        if token in questions or (token not in stopwords and token not in punctuation):
            yield token


def main():
    # tagged = []

    # tree =  nltk.chunk.ne_chunk(tagged)
    # tree.draw()


    # NEW !!!!!!!

    # connecting to data base
    conn = sqlite3.connect('db.db')

    c = conn.cursor()

    # nltk.data.show_cfg('grammars/book_grammars/sql0.fcfg')
    # nltk.data.show_cfg('grammars/book_grammars/sql1.fcfg')

    cp = load_parser('src/ia/nlp/grammars.fcfg')
    query = 'What cities are located in Greece'
    # nlp_query = 'What is the population of Greece'

    # tokenize nlp query
    # words = normalize(nlp_query)

    # query = ""
    # for item in words:
    #     print(item)
    #     query += item + " " 
    # # print(words)

    # print(query)

    # words = word_tokenize(nlp_query)
    # query = ' '.join([w for w in words if not w in stopwords or w in questions])

    # print(query)

    trees = list(cp.parse(query.split()))
    print(trees)
    # # answer = trees[0].label()['SEM']
    # # answer = [s for s in answer if s]
    # # q = ' '.join(answer)
    # # print(q)

    # c.execute(q)

    # # printing result
    # df = pd.DataFrame(c.fetchall(), columns=['cities'])
    # print (df)  
    

def tokenize(query: str):
    # sentence tokenize
    sentences = nltk.sent_tokenize(query)

    remove_urls(query)

    remove_html(query)

    normalized_text = []

    # for each sentence normalized the text (this includes word_tokenize)
    for sent in nltk.sent_tokenize(content):
        normalized_text.append(list(normalize(sent)))
    
    tagged = []

    for word in normalized_text:
        tagged.append(nltk.pos_tag(word))

    return tagged



main()


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

