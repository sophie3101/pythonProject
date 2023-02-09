from bs4 import BeautifulSoup
import requests
import urllib.parse 
import re
import time
import sys
import os
from collections import deque
import pickle
from url import Link
class Crawler:
  def __init__(self, url, level = 2, log_file = 'logging.log'):
    self.url = url 
    self.domain = self.get_domain(self.url)
    print('domain ', self.domain)
    self.queue = deque([self.url])
    # determine level of crawling. E.g 2 means the script will extracts all website up to http:aaa/bbb 
    # and level 3 will extract up to https://aaa/bbb/ccc
    self.level = level
    self.seen = []
    # self.linkDict = dict(self.url:{})
    # for logging
    if os.path.isfile(os.path.join(os.path.dirname(__file__),log_file)):
      os.remove(os.path.join(os.path.dirname(__file__),log_file))
    # sys.stdout = open(log_file, 'w')

    
  def crawl(self):
    domain = urllib.parse.urlparse(self.url).netloc
    self.parse_webpage(self.url)

  def get_domain(self, link):
    return urllib.parse.urlparse(link).netloc

  def get_valid_link(self, link):
    # return empty link if link is not valid
    # get rid of link containing # e.g  https://openai.com/#faq-token
    if link == None or 'javascript' in link or re.search('^\/$', link.strip()) or re.search(r'mailto', link) or re.search(r'#', link): return None
    # print(link)
    if re.search(r'https?', link):
      return link if (self.get_domain(link) == self.domain and link not in self.seen) else None
    else:
      hyper_link = urllib.parse.urljoin(self.url, link)
      # print(link, '          ', hyper_link)
      return hyper_link if (self.is_link(hyper_link) and self.get_domain(hyper_link) == self.domain and link not in self.seen) else None

  def is_link(self, link):
    # check if link is valid
    status = requests.get(link).status_code
    return status >= 200 and status < 300

  def parse_recursive(self, seen = []):
    while self.queue:
      web_link = self.queue.pop() # remove from right side of queue
      print("\nParsing website {} \n".format(web_link))
    #   if web_link in seen: continue
    #   seen.append(web_link)
      # identify the level of website
      hyper_links = self.parse(web_link)
      # self.queue.extendleft(hyper_links)
    # print('all links', len(self.deque))
    # self.parse_recursive(self.deque)

  def parse(self, web_link):
    # use BeautifulSoup to parse content of page
    page =  requests.get(web_link)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify()) #print page content

    # get all link on the page
    links = set(link.get('href') for link in soup.find_all('a') if link not in self.seen)
    # print(links)
    print('Number of links found in this page',len(links))

    # filter links, only retrive link that is valid
    hyper_links = [self.get_valid_link(link) for link in links]
    hyper_links = set(filter (lambda x: x != None, hyper_links))
    print('after filter', len(hyper_links))
    self.seen.extend(hyper_links)
    print(hyper_links)
  
    print("# of parsed website ", len(self.seen))
    self.listToFile(list(hyper_links))
    return list(hyper_links)

  def listToFile(self, links) :
    with open('links.txt', 'wb') as fh:
      pickle.dump(links, fh)

  def fileToList(self):
    with open("links.txt", "rb") as f: # "rb" because we want to read in binary mode
      links = pickle.load(f)
    
    for link in links:
      print(link)
      L = Link(link)
      
url = "https://immatics.com/" #"https://openai.com/" #
crawler = Crawler(url)
crawler.fileToList()
# crawler.parse_recursive()
# close and reset output to console
# sys.stdout.close()
# sys.stdout = sys.__stdout__
