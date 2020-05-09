from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # #Visit NASA webpage
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    

    #Extract lastest news title
    divs_title = soup.find_all('div', class_='content_title')
    lastest_cont=divs_title[1].find('a')
    lastest_news_title=lastest_cont.getText()
    
    #Extract Pragraph text
    divs_paragraph=soup.find_all('div', class_='article_teaser_body')
    lastest_news_paragraph=divs_paragraph[0].getText()
    
    # Store data in a dictionary
    Mars_data={}
    Mars_data["lastest_news_title"]= lastest_news_title
    Mars_data["lastest_new_paragraph"]=lastest_news_paragraph

    #Visit JPL Featured Space Image page
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    

    #Extract feature image url
    art_image = soup.find_all('article', class_='carousel_item')
    article_img=art_image[0].find('a',class_="button fancybox")
    featured_image_url=article_img['data-fancybox-href']
    featured_image_url='https://www.jpl.nasa.gov'+featured_image_url
    
    # Store data in a dictionary
    Mars_data['featured_image_url']=featured_image_url

    #Visit the Mars Weather Twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
   
    
    #Scrape Mars Weather twitter account
    html = browser.html
    soup = bs(html, "html.parser")
    
    
    #Scrape tweet
    try:
        weather_tweet = soup.select("div[data-testid=tweet]")
        weather_tweet1=weather_tweet[0]
    except IndexError:
        import re
        pattern=re.compile(r"InSight sol \d*\s\(.*?\)\slow\s.*?ºC\s\(.*?\)\shigh\s.*?ºC\s\(.*?\)\nwinds\s\D*\d*.\d*\s.{3}\s\(.*?mph\)\s.*\(.*?mph\)\npressure.*hPa")
        matches=pattern.search(str(soup))
    import re
    try:
        pattern=re.compile(r"InSight sol \d*\s\(.*?\)\slow\s.*?ºC\s\(.*?\)\shigh\s.*?ºC\s\(.*?\)\nwinds\s\D*\d*.\d*\s.{3}\s\(.*?mph\)\s.*\(.*?mph\)\npressure.*hPa")
        matches=pattern.search(str(weather_tweet1))
    except:
        pass
    matches
    try:
        weather=matches.group(0)
    except:
        import requests
        html=requests.get(url).text
        pattern=re.compile(r"InSight sol \d*\s\(.*?\)\slow\s.*?ºC\s\(.*?\)\shigh\s.*?ºC\s\(.*?\)\nwinds\s\D*\d*.\d*\s.{3}\s\(.*?mph\)\s.*\(.*?mph\)\npressure.*hPa")
        matches=pattern.search(str(html))
    weather=matches.group(0)
    weather1=weather.split('\n')
    tweet=weather1[0]+weather1[1]+weather1[2]
    tweet

    #Extract information within paratises and recompile phrases
    import re
    brakets=re.findall(r'\(.*?\)',tweet)
    print(brakets)
    tweet_list2=tweet.split(" ")
    print(tweet_list2)

    #sol informaiton extraction
    #Transform date
    Date=brakets[0]
    print(Date)
    Date1=Date[Date.find('(')+1:Date.find(')')]
    import pandas as pd
    from datetime import datetime
    import calendar
    date=pd.to_datetime(Date1)
    date

    date_element=date.date
    month=date.month
    year=date.year
    month1=calendar.month_abbr[month]
    part_date=date.strftime('%d,%Y')
    full_date="("+month1+" "+part_date+")"
    sol_info=tweet_list2[1]+" "+tweet_list2[2]+full_date
    print(sol_info)

    #Transform temperature
    #lowest temperature
    L_temperature=brakets[1]
    L_temperature_f=L_temperature[L_temperature.find('(')+1:L_temperature.find('º')]
    L_Temperature=L_temperature_f+"F"
    print(L_Temperature)
    L_Temperature_C=tweet_list2[5][0:tweet_list2[5].find('º')]
    L_Temperature_C=L_Temperature_C+"C"
    print(L_Temperature_C)
    L_Temperature_phrase="low "+L_Temperature_C+"/"+L_Temperature
    print(L_Temperature_phrase)
    
    #highest temperature
    H_temperature=brakets[2]
    H_temperature_f=H_temperature[H_temperature.find('(')+1:H_temperature.find('º')]
    H_temperature=H_temperature_f+"F"
    print(H_temperature)
    H_Temperature_C=tweet_list2[8][0:tweet_list2[8].find('º')]
    H_Temperature_C=H_Temperature_C+"C"
    print(H_Temperature_C)
    H_Temperature_phrase="high "+H_Temperature_C+"/"+H_temperature
    print(H_Temperature_phrase)

    #Extract Pressure
    tweet_list=tweet.split(")")
    pressure=tweet_list[len(tweet_list)-1]
    pressure=pressure.replace('\n','')
    pressure

    #Extract Weather
    weather=tweet_list[3]
    weather=weather.replace('\n','')
    weather=weather[0:weather.find(' ')]

    #Compile extracted information into sentence to be inserted in to the website
    Mars_weather=sol_info+","+weather+","+H_Temperature_phrase+","+L_Temperature_phrase+","+pressure
    
    # Store data in a dictionary
    Mars_data["Mars_weather"]= Mars_weather


    #Visit the Mars Facts webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    time.sleep(1)

    #Extract table from website
    import pandas as pd
    tables = pd.read_html(url)
    tables[0]
    html_table = tables[0].to_html()
    Mars_data["html_table"]=html_table
    
    

    #Visit the site for the first picture
    url='https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    
    
    time.sleep(1)

    # Scrape the site for the first picture
    html = browser.html
    soup = bs(html, "html.parser")
    

    #Extract first image url and its title
    Mars1 = soup.find_all('img', class_='wide-image')
    Mars_img_url1=Mars1[0]['src']
    Mars_img_url1='https://astrogeology.usgs.gov'+Mars_img_url1
    Mars_title_1=soup.find_all('h2', class_='title')
    Mars_title1=Mars_title_1[0].getText()
    
    #Load extracted title and picture url
    Mars_data["Mars_title1"]=Mars_title1
    Mars_data["Mars_img_url1"]=Mars_img_url1

    #Visit the site for the second picture
    url='https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    

    #Scrape the site for the second picture
    html = browser.html
    soup = bs(html, "html.parser")

    #Extract second image and its title
    Mars2 = soup.find_all('img', class_='wide-image')
    Mars_img_url2=Mars2[0]['src']
    Mars_img_url2='https://astrogeology.usgs.gov'+Mars_img_url2
    Mars_title_2=soup.find_all('h2', class_='title')
    Mars_title2=Mars_title_2[0].getText()

    #Load extracted title and picture url
    Mars_data["Mars_title2"]=Mars_title2
    Mars_data["Mars_img_url2"]=Mars_img_url2

    #Visit the site for the third picture
    url='https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
   
    
    #Scrape the site for the third picture
    html = browser.html
    soup = bs(html, "html.parser")
    
    
    #Extract third image and its title
    Mars3 = soup.find_all('img', class_='wide-image')
    Mars_img_url3=Mars3[0]['src']
    Mars_img_url3='https://astrogeology.usgs.gov'+Mars_img_url3
    Mars_title_3=soup.find_all('h2', class_='title')
    Mars_title3=Mars_title_3[0].getText()
    
    #Load extracted title and picture url
    Mars_data["Mars_title3"]=Mars_title3
    Mars_data["Mars_img_url3"]=Mars_img_url3
    
    #Visit the site for the last picture
    url='https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    
    
    #Scrape the site for the last picture
    html = browser.html
    soup = bs(html, "html.parser")
    

    #Extract last image and its title
    Mars4 = soup.find_all('img', class_='wide-image')
    Mars_img_url4=Mars4[0]['src']
    Mars_img_url4='https://astrogeology.usgs.gov'+Mars_img_url4
    Mars_title_4=soup.find_all('h2', class_='title')
    Mars_title4=Mars_title_4[0].getText()
    
    #Load extracted title and picture url
    Mars_data["Mars_title4"]=Mars_title4
    Mars_data["Mars_img_url4"]=Mars_img_url4

    # Close the browser after scraping
    browser.quit()
    
    

    # Return results
    return Mars_data
