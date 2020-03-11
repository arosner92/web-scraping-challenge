import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from pprint import pprint
from splinter import Browser
import time 


def scrape():
    news = 'https://mars.nasa.gov/news/'
    img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    tweets = 'https://twitter.com/marswxreport?lang=en'
    facts = 'https://space-facts.com/mars/'
    hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    results = {}
    
    # News
    response = requests.get(news)
    time.sleep(3)
    news_soup = BeautifulSoup(response.text, 'lxml')
    title = news_soup.find('div', class_= 'content_title')
    news_title = title.a.text.strip()
    p = news_soup.find('div', class_= 'rollover_description_inner')
    news_p = p.text.strip()
    results['news_title'] = news_title
    results['news_text'] = news_p
    
    # Image
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(img)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    featured_img_url = browser.find_by_css('.main_image').first['src']
    results['image_url'] = featured_img_url

    # Tweet
    response = requests.get(tweets)
    tweet_soup = BeautifulSoup(response.text, 'lxml')
    t = tweet_soup.find_all('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    for i in t:
        if 'InSight' in i.text:
            i.a.decompose()
            results['tweet'] = i.text
            break
    
    # Facts
    facts_html = pd.read_html(facts)
    facts_df = facts_html[0]
    facts_df.columns = ['Description', 'Data']
    facts_df.set_index('Description', inplace=True)
    html_table = facts_df.to_html()
    html_table = html_table.replace('\n', '')
    results['table_html'] = html_table

    # Hemispheres
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(hemis)

    for i in range(4):
        link = browser.links.find_by_partial_text('Hemisphere')[i]
        link.click()
        title = browser.find_by_css('.title').first.text
        url = browser.find_by_text('Sample').first['href']
        results[title] = url
        browser.back()
        
    return results
