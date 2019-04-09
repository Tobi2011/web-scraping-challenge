from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import json


def init_browser():

  executable_path = {"executable_path": "C:\Program Files\Common Files\chromedriver"}
  return Browser("chrome", **executable_path, headless=False)

def scrape():
  # def scrape_info():
  browser = init_browser()
  # ------------------------------------------------------------------------------

  # Visit website
  url = "https://mars.nasa.gov/news/"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into Soup
  html = browser.html
  soup = bs(html, "html.parser")

  # Get desired fields
  news_title = soup.find('div', {"class":"content_title"}).text
  news_p = soup.find('div', {"class":"rollover_description_inner"}).text
  # ------------------------------------------------------------------------------
  # Visit website
  url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into Soup
  html = browser.html
  soup = bs(html, "html.parser")

  featured_image_url = soup.find('a', {"id":"full_image"})['data-fancybox-href']
  featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
  # ------------------------------------------------------------------------------
  # Visit website
  url = "https://twitter.com/marswxreport?lang=en"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into Soup
  html = browser.html
  soup = bs(html, "html.parser")

  mars_weather = soup.find('p',\
                          {"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})\
                          .getText()
  mars_weather = mars_weather.split('hPa',1)[0] + 'hPa'
  mars_weather = 'sol' + mars_weather.split('sol', 1)[1]
  # ------------------------------------------------------------------------------
  # Visit website
  url = "https://space-facts.com/mars/"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into Soup
  html = browser.html
  soup = bs(html, "html.parser")

  table = soup.find("table",{"id":"tablepress-mars"})
  ptable = pd.read_html(str(table))[0]
  ptable = ptable.set_index(0)
  ptable.index.names = [""]
  ptable.columns = ["Value"]
  html_table = ptable.to_html()

  # ------------------------------------------------------------------------------
  # Visit website
  url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into Soup
  html = browser.html
  soup = bs(html, "html.parser")

  sources = soup.find_all("a",{"class":"itemLink product-item"})
  links = set(["https://astrogeology.usgs.gov" + link["href"] for link in sources])

  hemisphere_image_urls = []
  for link in links:
      browser.visit(link)
      time.sleep(1)
      
      html = browser.html
      soup = bs(html, "html.parser")
      
      link_dict = {}
      img_link = soup.find('img',{"class":"wide-image"})["src"]
      title = soup.find('h2', {"class":"title"}).text
      link_dict["title"] = title.split(" Enhanced",1)[0]
      link_dict["img_link"] = "https://astrogeology.usgs.gov" + img_link
      
      hemisphere_image_urls.append(link_dict)
  # ------------------------------------------------------------------------------

  # Store data in a dictionary
  mars_data = {
      "news_title": news_title,
      "news_p": news_p,
      "featured_image_url": featured_image_url,
      "mars_weather": mars_weather,
      "html_table": html_table,
      "hemisphere_image_urls": hemisphere_image_urls
  }

  # Close the browser after scraping
  browser.quit()
  print(json.dumps(mars_data))
    # Return results
  return mars_data