# import libararies
from webdriver_manager.chrome import ChromeDriverManager as cd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

executable_path={'executable_path':cd().install()}

#******MARS NEWS
def mars_news(browser):
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')

    try:
        soup.select('ul.item_list li.slide')
        news=soup.select_one('ul.item_list li.slide')
        news_title=news.find('div', class_='content_title').get_text()
        news_p=soup.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

#*****FEATURED IMAGE
def featured_image(browser):
    url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    browser.find_by_tag('button')[1]
    html=browser.html
    soup_img=bs(html, 'html.parser')
    try:
        url_src=soup_img.find('img', class_='headerimage fade-in').get('src')
    except AttributeError:
        return None
    img_ulr=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{url_src}'
    return img_ulr

#*****MARS FACTS
def mars_facts():
    # use try to handle any errors
    try:
        url='https://galaxyfacts-mars.com/'
        df=pd.read_html(url)[0]

    except BaseException:
        return None
    # rename the columns 
    df.columns=['measurement','Mars profile','Earth profile']

    return df.to_html(classes='table table-striped')

#*****MARS HEMISPHERES
def mars_hemispheres(browser):
    url='https://marshemispheres.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')

    hemisphere_image_urls=[]

    images=soup.find_all('div', class_='description')
    for image in images:
        
        title=image.find('h3').get_text()
        
        image_urls=soup.find('div', class_='item')
        url_0=image_urls.find('img')['src']
        url_1=f'https://marshemispheres.com/{url_0}'

        image_dict={}
        image_dict['title']=title
        image_dict['img_url']=url_1

        hemisphere_image_urls.append(image_dict)
    return hemisphere_image_urls

#*****SCRAPE FUNCTION TO CALL ALL FUNCTIONS DEFINED ABOVE
def scrape():
    browser=Browser('chrome', **executable_path, headless=False)
    news_title, news_p=mars_news(browser)

    # run all scrape and return a dict
    final_dict={
        'news_title':news_title,
        'news_p':news_p,
        'featured_image':featured_image(browser),
        'mars_facts':mars_facts(),
        'hemisphere_image_urls':mars_hemispheres(browser)
    }
    browser.quit()
    return final_dict

#***************
if __name__ == '__main__':
    print(scrape())

