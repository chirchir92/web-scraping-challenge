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
    
    #---------------------- MARS NEWS-----------------------------
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
    

    #-----------------------FEATURED IMAGE-------------------------------------
    # # use .find_by_tag function to locate the  image
    image=browser.find_by_tag('button')[1]
    image.click()
    # inspect the html code to locate the image link and its div class
    url_src=soup.find('img', class_='headerimage fade-in').get('src')
    img_ulr=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{url_src}'
    

    #----------------------NARS FACTS------------------------------------
    fact=pd.read_html(url_facts)
    type(fact)
    df=fact[0]
    mars_facts=df.columns=['measurement','Mars profile','Earth profile']
    

    #--------------------HEMISPHERES-------------------------------------
    hemisphere_image_urls=[]

    # identify the full resolution link 
    images=soup.find_all('div', class_='description')


    for image in images:
        image_dict={}

        title=image.find('h3')
        image_dict['title']=title.text
        
        image_url=soup.find('div', class_='item')
        url_0=image_url.find('img')['src']
        image_dict['img_url']=f'https://marshemispheres.com/{url_0}'
        
        hemisphere_image_urls.append(image_dict)
        # print(f'hemisphere_image_urls={hemisphere_image_urls}')
    

    #---------------------FINAL DICT---------------------------------
    # store data in a dictionary
    final_dict={
        'news_title': news_title,
        'news_p':news_p,
        'img_ulr':img_ulr,
        'mars_facts':mars_facts,
        'title':title,
        'hemisphere_image_urls':hemisphere_image_urls
    }
    browser.quit()
    
    # return results
    return final_dict