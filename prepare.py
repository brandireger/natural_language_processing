import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

def basic_clean(string):
    string = string.lower()
    string = unicodedata.normalize('NFKD', string)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9'\s]", '', string)
    return string

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(string, return_str=True)

def stem(string):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string_stemmed = ' '.join(stems)
    return string_stemmed

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string_lemmatized = ' '.join(lemmas)
    return string_lemmatized

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    stopword_list = stopwords.words('english')
    for i in extra_words:
        stopword_list.append(i)
    if len(exclude_words) > 0:
        stopword_list = [word for word in stopword_list if word not in exclude_words]
    filtered_words = [word for word in string.split() if word not in stopword_list]
    string_without_stopwords = ' '.join(str(w) for w in filtered_words)
    return string_without_stopwords

def prep_article(df):
    df['cleaned'] = df.content.apply(lambda row: basic_clean(row))
    df['tokenized'] = df.cleaned.apply(lambda row: tokenize(row))
    df['stemmed'] = df.tokenized.apply(lambda row: stem(row))
    df['lemmatized'] = df.tokenized.apply(lambda row: lemmatize(row))
    df['clean'] = df.lemmatized.apply(lambda row: remove_stopwords(row, extra_words=['ha', 'said']))
    df = df.drop(columns=['cleaned', 'tokenized'])
    return df


