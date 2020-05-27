import numpy as np
import pandas as pd
import re

from requests import get
from bs4 import BeautifulSoup
import os

def get_codeup_articles(url):
    regexp = r'https://codeup.com/(?P<article_name>.+?)/'
    article_name = re.match(regexp, url).groups()[0]
    
    # if we already have the data, read it locally
    if os.path.exists(f'{article_name}.txt'):
        with open(f'{article_name}.txt') as f:
            article = f.read()
        title = article_name
        return title, article
    
    # otherwise make the data
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    title = soup.title.text
    article = soup.find('div', itemprop='text').text

    # save it for next time
    with open(f'{article_name}.txt', 'w') as f:
        f.write(article)

    return title, article

def make_codeup_articles_df():
    urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
            'https://codeup.com/data-science-myths/',
            'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
            'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
            'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']
    
    article_df = pd.DataFrame(columns=['title', 'content'])
    
    for url in urls:
        title, article = get_codeup_articles(url)
        article_df = article_df.append(
            {'title': title,
             'content': article
            }, ignore_index=True)
    return article_df

def get_inshort_articles(url):
    regexp = r'https://inshorts.com/en/read/(?P<category>.+)'
    category = re.match(regexp, url).groups()[0]
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Empty containers
    titles = []
    contents = []
    df = pd.DataFrame(columns=['title', 'content', 'category'])
    
    # List of titles
    for card in soup.find_all('span', itemprop="headline"):
        titles.append(card.text)
    
    # List of contents
    for card in soup.find_all('div', itemprop="articleBody"):
        contents.append(card.text)
    
    # Zip the two lists together and add to df
    zipped = zip(titles, contents)
    for card in zipped:
        df = df.append({'title': card[0],
                        'content': card[1],
                        'category': category},
                      ignore_index=True)
    
    return df

def make_inshort_articles_df():
    # if we already have the data, read it locally
    if os.path.exists('inshort_articles.csv'):
        return pd.read_csv('inshort_articles.csv', index_col='Unnamed: 0')
    
    # otherwise make the data
    categories = ['https://inshorts.com/en/read/business',
              'https://inshorts.com/en/read/sports',
              'https://inshorts.com/en/read/technology',
              'https://inshorts.com/en/read/entertainment']
    
    big_df = pd.DataFrame()

    for category in categories:
        df = get_inshort_articles(category)
        big_df = big_df.append(df, ignore_index=True)
    
    big_df = big_df.drop_duplicates()
    
    # save it for next time
    big_df.to_csv('inshort_articles.csv')
    
    return big_df
