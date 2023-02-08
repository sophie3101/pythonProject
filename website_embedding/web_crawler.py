from bs4 import BeautifulSoup
import requests
import urllib.parse 
import re
import time
import logging

class Crawler:
  def __init__(self, url, log_file = 'logging.log'):
    self.url = url 
    self.domain = self.get_domain(self.url)
    print('domain ', self.domain)
    self.seen = []
    logging.basicConfig(filename = log_file, encoding='utf-8', level = logging.DEBUG)
  
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

  def parse_recursive(self, all_links, seen = []):
    if all_links == []:
      return

    if len(all_links) == 1:
      seen = []
    for web_link in all_links:
      if web_link in seen: continue
      seen.append(web_link)

      hyper_links = self.parse(web_link)
      all_links.extend(hyper_links)
    print('all links', len(all_links))
    self.parse_recursive(all_links)

  def parse(self, web_link):
    print("\n******************************\n")
    logging.info(web_link)
    print('parsing {}'.format(web_link))
    # use BeautifulSoup to parse content of page
    page =  requests.get(web_link)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify()) #print page content

    # get all link on the page
    links = set(link.get('href') for link in soup.find_all('a') if link not in self.seen)
    print(links)
    logging.info(links)
    print('# of links found in this page',len(links))
    logging.info(len(links))

    # filter links, only retrive link that is valid
    hyper_links = [self.get_valid_link(link) for link in links]
    hyper_links = set(filter (lambda x: x != None, hyper_links))
    print('after filter', len(hyper_links))
    self.seen.extend(hyper_links)
    print(hyper_links)
    logging.info(hyper_links)
    print("# of parsed website ", len(self.seen))
    logging.info( len(self.seen))
    # sleep to prevent request timeout limit
    time.sleep(10)
    return hyper_links

url =  "https://openai.com/" #
crawler = Crawler(url, log_file = "imamtics_log.txt")
crawler.parse_recursive([url])
