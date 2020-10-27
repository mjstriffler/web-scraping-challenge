
# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
import requests as req
from flask import Flask, render_template, redirect

def init_browser():

        executable_path = {'executable_path': '/Users/SikCommunications/Downloads/chromedriver'}
        return Browser('chrome', **executable_path, headless=False)

def scrape():   

        browser = init_browser()
        mars_dict={}

# Visit url for NASA Mars News -- Latest News
        news_url = "https://mars.nasa.gov/news/"
        browser.visit(news_url)
        html = browser.html

# Parse HTML with Beautiful Soup
        soup = bs(html, "html.parser")

        news_title= soup.find_all('div', class_= 'content_title')[1].text
        news_p =soup.find_all('div', class_='article_teaser_body')[0].text

#Scape NASA site to find Featured Mars Image

        jpl_nasa_url = 'https://www.jpl.nasa.gov'
        images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(images_url)
        html = browser.html
        images_soup = bs(html, 'html.parser')

        relative_image_path = images_soup.find_all('img')[3]["src"]
        featured_image_url = jpl_nasa_url + relative_image_path

        facts_url ='https://space-facts.com/mars/'
        tables = pd.read_html(facts_url)
        mars_facts_df = tables[2]
        mars_facts_df.columns = ["Description" , "Value"]
        mars_html_table = mars_facts_df.to.html()
        mars_html_table.replace('\n','')


#Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
        usgs_url = 'https://astrogeology.usgs.gov'
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        hemispheres_html = browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')

        all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible_results')
        mars_hemispheres = all_mars_hemispheres.find_all('div, class_=item')
        hemisphere_image_urls = []

   # Iterate through each hemisphere data
        for i in mars_hemispheres:
                # Collect Title
                hemisphere = i.find('div', class_="description")
                title = hemisphere.h3.text        
                # Collect image link by browsing to hemisphere page
                hemisphere_link = hemisphere.a["href"]    
                browser.visit(usgs_url + hemisphere_link)        
                image_html = browser.html
                image_soup = bs(image_html, 'html.parser')        
                image_link = image_soup.find('div', class_='downloads')
                image_url = image_link.find('li').a['href']
                # Create Dictionary to store title and url info
                image_dict = {}
                image_dict['title'] = title
                image_dict['img_url'] = image_url        
                hemisphere_image_urls.append(image_dict)

# Mars 
        mars_dict = {
                "news_title": news_title,
                "news_p": news_p,
                "featured_image_url": featured_image_url,
                "mars_weather": mars_weather,
                "fact_table": str(mars_html_table),
                "hemisphere_images": hemisphere_image_urls
                }

        return mars_dict