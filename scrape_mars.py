# import libararies
from webdriver_manager.chrome import ChromeDriverManager as cd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def scrape():
    # setup splinter
    executable_path={'executable_path':cd().install() }
    browser=Browser('chrome', **executable_path, headless=False)
    
    # visit the mars nasa news url
    url='https://mars.nasa.gov/news/'
    img_ulr='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    url_facts='https://galaxyfacts-mars.com/'
    image_url='https://marshemispheres.com/'
    browser.visit(url)
    
    # use bs4 to parse the html
    html=browser.html
    soup=bs(html, 'html.parser')
    
    # perfome css selection on elements 'item-list & slide'
    # we use .select sourced from https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors
    soup.select('ul.item_list li.slide')
    # use .select_one to only return the first tag matching the selector
    # use a variable to enable use later
    css_selector=soup.select_one('ul.item_list li.slide')
    # access the div class content_title to extract the heading
    css_selector.find('div', class_='content_title')
    news_title=css_selector.find('div', class_='content_title')
    # access the class article teaser body to get the paragraoh text
    news_p=css_selector.find('div', class_='article_teaser_body')
    
    # use .find_by function to locate the  image
    image=browser.find_by_text('FULL IMAGE')
    # confirm that the .find function has founf the picture
    # to confirm use splinte .is_element_present function
    confirm=browser.is_element_present_by_text('FULL IMAGE')
    # inspect the html code to locate the image link and its div class
    url_img=soup.find(class_='showimg fancybox-thumbs')['href']
    featured=img_ulr.replace('index.html', url_img)
    
    fact=pd.read_html(url_facts)
    type(fact)
    df=fact[1]
    mars_facts=df.columns=['measurement','Mars profile']
    
    # identify the full resolution link 
    images=soup.find_all('div', class_='description')
    title=image.find('h3')
        
    image_urls=soup.find('div', class_='item')
    link=image_urls.find('img')['src']
    
    # store data in a dictionary
    final_dict={
        'news_title': news_title,
        'news_p':news_p,
        'featured':featured,
        'nmars_facts':mars_facts,
        'title':title,
        'image_urls':link
    }

    browser.quit()
    
    # return results
    return final_dict