# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
# BeautifulSoup, Pandas, and Requests/Splinter
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import pymongo



conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

def scrape():

    mars_data = {}

    # Chrome Driver
    # Allows you to interact with chrome from python, just like a printer driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', headless=False)


    # ===================================================
    # Nasa Mars News
    # ===================================================

    # Go to url and visit browser
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

    # Beautiful Soup Parsing
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Grab and print Title and Paragraph
    news_title = soup.find('div', class_ ='content_title').text
    #print(news_title)

    news_p = soup.find('div', class_ = 'article_teaser_body').text
    #print(news_p)

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p


    # ===================================================
    # JPL Mars Images - Featured Image 
    # ===================================================

    # Go to url and visit browser
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Beautiful Soup Parsing
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
        
    # Find image store as result
    result = soup.find('article', class_='carousel_item')

    # Split apostrohe's from link
    link = result['style'].split("'")


    # class, data-descripotion are attributes of the anchor element a tag
    # when we want elements, treat it like object properties
    # attritribute are treated like dicts. 

    # print(link)

    featured_image_url = 'https://www.jpl.nasa.gov/' + link[1]

    mars_data['featured_image_url'] = featured_image_url


    # ===================================================
    # Mars Weather Twitter Scrape
    # ===================================================

    # Go to url and visit browser
    url = 'https://twitter.com/MarsWxReport?lang=en'
    browser.visit(url)

    # Beautiful Soup Parsing
    html_tweet = browser.html
    soup = BeautifulSoup(html_tweet, 'html.parser')
    
    # Grab and Print Tweet
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_data['mars_weather'] = mars_weather


    # ===================================================
    # Mars Facts
    # ===================================================

    # Go to url and visit browser
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Use pandas function read_html to find any tables and extract data in table
    tables = pd.read_html(url)
    tables

    # put into data frame
    # this says what type of element we extracted --> type(tables)
    mars_facts = tables[0]

    # Name the data frame and add column headers, convert to html
    mars_facts.columns = ['Measurement', 'Value']
    mars_facts = mars_facts.to_html()
    mars_data['mars_facts'] = mars_facts

    


    # ===================================================
    # Mars Hemisphere
    # ===================================================

    # Go to url and visit browser
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Beautiful Soup Parsing
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the list of data in the html
    collapsible_results = soup.find_all('div', class_ = 'item')

    # Create an empty list to store your results found
    hemisphere_image_urls = []

    # Create loop to find title and image for each hemisphere
    for item in collapsible_results:
    
        # Go to description class within collapsible results
        result = item.find('div', class_='description')

        # Find Title
        title = result.a.h3.text
        
        # Find Link for Download
        img_url = result.a['href']
        img_url = 'https://astrogeology.usgs.gov' + img_url

        browser.visit(img_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        img_download = soup.find('div', class_ ='downloads')
        img_url_download = img_download.ul.li.a['href']
        
        
        #print(title)
        #print(img_url)
        #print(img_url_download)

        hemisphere_image_url = {'title' : title, 'img_url' : img_url_download}

        hemisphere_image_urls.append(hemisphere_image_url)


    mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    return mars_data


#if __name__ == "__main__":
#    app.run(debug=True)
