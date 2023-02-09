from bs4 import BeautifulSoup
import requests
import urllib.parse 
import time
import sys
import os
from collections import deque
from url_dict import Url_Dict
from miscelleneous import fileToList, listToFile
class Crawler:
  def __init__(self, url, level = 2, log_file = 'logging.log'):
    self.url = url 
    self.domain = urllib.parse.urlparse(self.url).netloc
    self.queue = deque([self.url])
    self.seen = []
  
    # for logging
    if os.path.isfile(os.path.join(os.path.dirname(__file__),log_file)):
      os.remove(os.path.join(os.path.dirname(__file__),log_file))
    # sys.stdout = open(log_file, 'w')

  def parse_recursive(self, seen = []):
    while self.queue:
      web_link = self.queue.pop() # remove from right side of queue
      print("\nParsing website {} \n".format(web_link))
      if web_link in seen: continue
      seen.append(web_link)

      self.parse_one_page(web_link)


  def parse_one_page(self, web_link):
    # use BeautifulSoup to parse content of page
    page =  requests.get(web_link)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify()) #print page content

    # get all link on the page
    links = set(link.get('href') for link in soup.find_all('a') if link not in self.seen)
    print('Number of links found in this page', len(links))
    # print(links)
    url_collections = Url_Dict(self.domain)

    # add the main website if the list links does not contain
    if web_link not in links: links.add(web_link)
    url_collections.parse_list(links)
    print(url_collections.url_dict)
    listToFile(links)
  # def parse_from_file(self):
  #   links = fileToList()
  #   # print(links)
  #   url_collections = Url_Dict(self.domain)
  #   url_collections.parse_list(links)
  #   print(url_collections.url_dict)
   
url = "https://github.com/" #"https://immatics.com/"#
crawler = Crawler(url)
crawler.parse_recursive()
# crawler.parse_from_file()

