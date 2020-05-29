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

def Faiths_blogs_function(urls, cache=False):
    '''
    This function takes in a list of Codeup Blog urls and a parameter
    with default cache == False which returns a df from a csv file.
    If cache == True, the function scrapes the title and text for each url, 
    creates a list of dictionaries with the title and text for each blog, 
    converts list to df, and returns df.
    '''
    if cache == False:
        df = pd.read_csv('big_blogs.csv', index_col=0)
    else:
        headers = {'User-Agent': 'Codeup Bayes Data Science'} 

        # Create an empty list to hold dictionaries
        articles = []

        # Loop through each url in our list of urls
        for url in urls:

            # get request to each url saved in response
            response = get(url, headers=headers)

            # Create soup object from response text and parse
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save the title of each blog in variable title
            title = soup.find('h1', itemprop='headline').text

            # Save the text in each blog to variable text
            text = soup.find('div', itemprop='text').text

            # Create a dictionary holding the title and text for each blog
            article = {'title': title, 'content': text}

            # Add each dictionary to the articles list of dictionaries
            articles.append(article)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(articles)

        # Write df to csv file for faster access
        df.to_csv('codeup_blogs.csv')
    
    return df

def get_all_urls():
    '''
    This function scrapes all of the Codeup blog urls from
    the main Codeup blog page and returns a list of urls.
    '''
    # The main Codeup blog page with all the urls
    url = 'https://codeup.com/resources/#blog'
    
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # Send request to main page and get response
    response = get(url, headers=headers)
    
    # Create soup object using response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Create empty list to hold the urls for all blogs
    urls = []
    
    # Create a list of the element tags that hold the href/links
    link_list = soup.find_all('a', class_='jet-listing-dynamic-link__link')
    
    # get the href/link from each element tag in my list
    for link in link_list:
        
        # Add the link to my urls list
        urls.append(link['href'])
        
    return urls


def get_inshort_articles(url):
    regexp = r'https://inshorts.com/en/read/(?P<category>.+)'
    category = re.match(regexp, url).groups()[0]
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
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
